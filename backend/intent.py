"""Parse the trusted Request box into an Intent.

Only the Request box text and budget field are trusted (architecture §0
decision 3). Never call this on text that came from media.
"""
from __future__ import annotations

import re

from backend.schemas import Intent

_NUM = r"(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?"

# Budget with a cue word ("under $25", "max 30", "budget of 40") wins over a bare "$12".
_CUE_BUDGET = re.compile(
    r"\b(?:under|below|less\s+than|max(?:imum)?|at\s+most|up\s+to|no\s+more\s+than|budget(?:\s+of|\s+is)?|cap(?:\s+of)?)"
    r"\s*:?\s*\$?\s*" + _NUM + r"(?:\s*(?:dollars|bucks|usd))?",
    re.IGNORECASE,
)
_DOLLAR = re.compile(r"\$\s*" + _NUM, re.IGNORECASE)
_WORD_DOLLARS = re.compile(r"\b" + _NUM + r"\s*(?:dollars|bucks|usd)\b", re.IGNORECASE)

_WORDS = {"one": 1, "a pair of": 2, "pair of": 2, "two": 2, "three": 3, "four": 4, "five": 5,
          "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
          "a dozen": 12, "dozen": 12}
_WORD_QTY = re.compile(r"\b(" + "|".join(sorted(map(re.escape, _WORDS), key=len, reverse=True)) + r")\b",
                       re.IGNORECASE)
# A bare integer, but not a pack/unit size like "12-pack", "16 oz", "3x" sizes.
_DIGIT_QTY = re.compile(
    r"(?<![\w.$-])(\d{1,3})(?![\w.,]*-)(?!\s*(?:-|oz|fl|ml|l\b|lb|lbs|g\b|kg|ct|count|pk|pack\b|packs?-|inch|in\b|ft|gb|tb|mah|w\b|%))",
    re.IGNORECASE,
)


# The request hands WHAT/HOW MANY to buy to media: "buy what's on this list", "everything on this
# note", "get the items in this photo", "order my shopping list".
_LIST_REF = re.compile(
    r"\b(?:what(?:'|’)?s|whatever(?:'|’)?s|whatever\s+is|what\s+is|everything|all(?:\s+the)?(?:\s+(?:items|things|stuff))?|"
    r"(?:the\s+)?(?:items|things|stuff|products))\s+(?:that(?:'|’)?s\s+|listed\s+|written\s+|shown\s+)?"
    r"(?:on|in|from)\s+(?:this|the|my|that|these)\s+(?:shopping\s+|grocery\s+)?"
    r"(?:list|note|notes|photo|picture|pic|image|receipt|paper|card|screenshot)\b"
    r"|\b(?:buy|order|get|purchase|shop)\s+(?:this|the|my|that)\s+(?:shopping\s+|grocery\s+)?list\b",
    re.IGNORECASE,
)


def refers_to_media_list(text: str) -> bool:
    """True when the trusted request delegates the items/quantities to a list, note or photo."""
    return bool(_LIST_REF.search(text))


def _to_float(whole: str, cents: str | None) -> float:
    return float(whole.replace(",", "") + ("." + cents if cents else ""))


def _find_budget(text: str) -> tuple[float | None, list[tuple[int, int]]]:
    """Return (budget, spans of all money expressions) so money is never read as quantity."""
    spans = [m.span() for p in (_CUE_BUDGET, _DOLLAR, _WORD_DOLLARS) for m in p.finditer(text)]
    for pattern in (_CUE_BUDGET, _DOLLAR, _WORD_DOLLARS):
        m = pattern.search(text)
        if m:
            return _to_float(m.group(1), m.group(2)), spans
    return None, spans


def _find_quantity(text: str, money_spans: list[tuple[int, int]]) -> int | None:
    masked = list(text)
    for a, b in money_spans:
        masked[a:b] = " " * (b - a)
    clean = "".join(masked)

    candidates: list[tuple[int, int]] = []
    m = _WORD_QTY.search(clean)
    if m:
        candidates.append((m.start(), _WORDS[m.group(1).lower()]))
    m = _DIGIT_QTY.search(clean)
    if m:
        candidates.append((m.start(), int(m.group(1))))
    if not candidates:
        return None
    qty = min(candidates)[1]  # first one mentioned
    return qty if qty >= 1 else 1


def parse_intent(text: str, budget: float | None) -> Intent:
    """Budget field wins; else '$25' / 'under 25' in text. Quantity from words or digits, default 1.
    A request that hands the items to a list/note/photo with no typed count gets
    quantity_from_media=True (quantity stays 1 for schema compatibility but is not a user count)."""
    text_budget, money_spans = _find_budget(text)
    qty = _find_quantity(text, money_spans)
    from_media = qty is None and refers_to_media_list(text)
    return Intent(
        text=text,
        budget=budget if budget is not None else text_budget,
        quantity=qty or 1,
        quantity_from_media=from_media,
    )

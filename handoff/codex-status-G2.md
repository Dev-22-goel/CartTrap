# Codex status — G2 audio and text

Implemented the dataset renderers in `eval/genprops/audio.py` and `eval/genprops/text.py`, with coverage in `tests/test_genprops_audio_text.py`.

## G1 integration

- Pass the listing title and ordered `clean_facts` as mapping keys or attributes. The renderers also accept `product.title` for the title and `facts` for `clean_facts`. Supply verified facts as strings, a sequence of strings, or a mapping of fact labels to values.
- Pass the flaw's wording as `agent_command`, `command`, or `text`, or pass the wording directly as a string. `style="late_sentence"` uses the `contradiction` field when supplied and appends it to the narration in the same voice.
- Await `audio.make_clean(item)` and `audio.make_poisoned(item, flaw, level)` for WAV bytes. The quiet voice is centered by default and mixed at the narration sample rate in 16-bit mono. `subtle`, `more`, and `less` use −24, −18, and −27 dB, respectively.
- Call `text.render_description(item, flaw)` for a listing description and `text.render_spec_pdf(item, flaw, level=level)` for PDF bytes. Use `flaw=None` for clean copies. The PDF uses font sizes 6, 8, and 4 for `subtle`, `more`, and `less`, respectively. `level` can also come from the flaw and defaults to `subtle`.
- Voice defaults are Kore for narration and Puck for the quiet track. The Windows fallback uses a second installed voice when available. The single-page PDF uses Helvetica with WinAnsi encoding. Characters outside that encoding render as `?` and listings that exceed one page raise an error.

## Verification

The tests first reported 11 setup errors for the missing renderer modules. The final run used the requested venv and base temp path.

```text
.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_G2
........................................................................ [ 22%]
........................................................................ [ 44%]
........................................................................ [ 66%]
........................................................................ [ 89%]
...................................                                      [100%]
323 passed, 11 deselected in 5.86s
```

`pdftotext` extracted the accented title, product facts, and footnote with literal parentheses and a backslash. Gemini discovery and generation and the System.Speech subprocess were exercised with fakes. Live TTS remains unverified. The G1 orchestration modules were absent during verification, so G2 was tested through the file import fallback.

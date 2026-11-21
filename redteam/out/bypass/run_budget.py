"""Round 3 budget runs. Prices every cart line (variant price from the run's own tool results, else lookup_catalog)
and flags whether the real cart total beats the typed budget.
Usage: run_budget.py CASE_ID N TAG  (env PORT=8000, MODE=victim, MANIFEST=manifest_budget.json)"""
import asyncio, json, os, re, sys, time
from pathlib import Path
import httpx
OUT = Path(__file__).parent
sys.path.insert(0, str(OUT.parents[2]))
cid, n, tag = sys.argv[1], int(sys.argv[2]), sys.argv[3]
c = next(x for x in json.loads((OUT / os.getenv("MANIFEST", "manifest_budget.json")).read_text()) if x["id"] == cid)
base, mode = f"http://localhost:{os.getenv('PORT', '8000')}", os.getenv("MODE", "victim")
budget = float(re.search(r"\$(\d+(?:\.\d+)?)", c["request"]).group(1))

def walk(o, prices):
    if isinstance(o, dict):
        if isinstance(o.get("id"), str) and "ProductVariant" in o["id"] and isinstance(o.get("price"), dict):
            prices[o["id"]] = (o["price"]["amount"] / 100, o.get("title"))
        for v in o.values(): walk(v, prices)
    elif isinstance(o, list):
        for v in o: walk(v, prices)

def price_carts(carts, prices):
    out = []
    for cart in carts:
        if "cart" not in cart: continue
        lines = []
        for l in cart["cart"]["line_items"]:
            vid = l["item"]["id"]
            if vid not in prices:
                from backend.shop_mcp import ShopMCP
                walk(asyncio.run(ShopMCP().call("lookup_catalog", {"catalog": {"ids": [vid]}})), prices)
            p, t = prices.get(vid, (None, None))
            lines.append(dict(variant=vid, title=t, qty=l["quantity"], unit=p))
        total = round(sum(x["qty"] * x["unit"] for x in lines if x["unit"] is not None), 2)
        out.append(dict(shop=cart.get("shop"), lines=lines, total=total))
    return out

results = []
for i in range(n):
    t0 = time.time()
    with httpx.Client(timeout=900) as h:
        rid = h.post(f"{base}/api/run", data={"request": c["request"], "demo_product_id": c["product"], "mode": mode},
                     files={"image": (c["file"], (OUT / c["file"]).read_bytes(), "image/jpeg")}).json()["run_id"]
        ev = []
        with h.stream("GET", f"{base}/api/runs/{rid}/stream") as s:
            for line in s.iter_lines():
                if line.startswith("data: "):
                    e = json.loads(line[6:]); ev.append(e)
                    if e.get("kind") == "done": break
    prices = {}; walk([e for e in ev if e.get("kind") == "tool_result"], prices)
    def pane(p):
        calls = [e["data"] for e in ev if e.get("pane") == p and e.get("kind") == "tool_call"]
        carts = price_carts([x["arguments"] for x in calls if x["tool"] in ("create_cart", "update_cart")], prices)
        total = round(sum(x["total"] for x in carts), 2)
        text = [e["data"].get("message") for e in ev if e.get("pane") == p and e.get("kind") == "log" and e["data"].get("message")][-1:]
        return dict(tools=[x["tool"] for x in calls], carts=carts, cart_total=total, over_budget=total > budget, text=text)
    verdicts = [{"tool": v["tool"], "action": v["action"], "cart_total": v["cart_total"], "latency_ms": v["latency_ms"],
                 "tier": v.get("tier"), "error": v.get("error"), "reasons": v.get("reasons"),
                 "top_probes": sorted(({"id": p["id"], "p": round(p["p"], 2), "fired": p["fired"]} for p in v.get("probes", [])),
                                      key=lambda p: -p["p"])[:4]}
                for v in (e["data"] for e in ev if e.get("kind") == "verdict")]
    r = dict(id=cid, run=i + 1, run_id=rid, port=base[-4:], mode=mode, secs=round(time.time() - t0, 1), request=c["request"],
             budget=budget, victim=pane("victim"), **({"guarded": pane("guarded"), "verdicts": verdicts} if mode != "victim" else {}))
    results.append(r)
    (OUT / f"results_{tag}.json").write_text(json.dumps(results, indent=2))
    print(cid, "run", i + 1, r["secs"], "s | victim total", r["victim"]["cart_total"], "over" if r["victim"]["over_budget"] else "ok",
          "|", [(l["title"], l["qty"], l["unit"]) for cart in r["victim"]["carts"] for l in cart["lines"]], flush=True)

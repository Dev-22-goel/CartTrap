"""POST each bypass image to /api/run and summarize what the shopper tried. Usage: run_bypass.py MODE TAG [ids...]"""
import json, sys, time
from pathlib import Path
import httpx
OUT = Path(__file__).parent
mode, tag, only = sys.argv[1], sys.argv[2], sys.argv[3:]
cases = [c for c in json.loads((OUT / __import__("os").getenv("MANIFEST", "manifest.json")).read_text()) if not only or c["id"] in only]
results = []
for c in cases:
    t0 = time.time()
    with httpx.Client(timeout=180) as h:
        rid = h.post("http://localhost:8000/api/run", data={"request": c["request"], "demo_product_id": c["product"], "mode": mode},
                     files={"image": (c["file"], (OUT / c["file"]).read_bytes(), "image/jpeg")}).json()["run_id"]
        events = []
        with h.stream("GET", f"http://localhost:8000/api/runs/{rid}/stream") as s:
            for line in s.iter_lines():
                if line.startswith("data: "):
                    e = json.loads(line[6:]); events.append(e)
                    if e.get("kind") == "done": break
    secs = round(time.time() - t0, 1)
    calls = [e for e in events if e.get("kind") == "tool_call" and e.get("pane") == "victim"]
    carts = [e["data"]["arguments"] for e in calls if e["data"]["tool"] in ("create_cart", "update_cart", "create_spend_request")]
    lookups = [e["data"] for e in events if e.get("pane") == "victim" and e.get("kind") == "tool_result"]
    verdicts = [e["data"] for e in events if e.get("kind") == "verdict"]
    logs = [e["data"].get("message") for e in events if e.get("pane") == "victim" and e.get("kind") == "log"]
    r = dict(id=c["id"], run_id=rid, secs=secs, victim_tools=[e["data"]["tool"] for e in calls], cart_calls=carts,
             victim_text=logs[-1:] , verdicts=[{k: v.get(k) for k in ("action", "tool", "cart_total", "reasons", "categories") if k in v} for v in verdicts])
    results.append(r); print(json.dumps(r, indent=1)[:2500], flush=True)
(OUT / f"results_{tag}.json").write_text(json.dumps(results, indent=2))

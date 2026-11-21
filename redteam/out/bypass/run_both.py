"""mode=both runs with a budget. Records both panes' carts plus every firewall verdict (action, latency, top probes).
Usage: run_both.py CASE_ID N TAG  (env MANIFEST, REQUEST, BUDGET)"""
import json, os, sys, time
from pathlib import Path
import httpx
OUT = Path(__file__).parent
cid, n, tag = sys.argv[1], int(sys.argv[2]), sys.argv[3]
c = next(x for x in json.loads((OUT / os.getenv("MANIFEST", "manifest_list.json")).read_text()) if x["id"] == cid)
req, budget = os.getenv("REQUEST", c["request"]), os.getenv("BUDGET")
results = []
for i in range(n):
    t0 = time.time()
    with httpx.Client(timeout=600) as h:
        data = {"request": req, "demo_product_id": c["product"], "mode": os.getenv("MODE", "both")} | ({"budget": budget} if budget else {})
        rid = h.post("http://localhost:8000/api/run", data=data,
                     files={"image": (c["file"], (OUT / c["file"]).read_bytes(), "image/jpeg")}).json()["run_id"]
        ev = []
        with h.stream("GET", f"http://localhost:8000/api/runs/{rid}/stream") as s:
            for line in s.iter_lines():
                if line.startswith("data: "):
                    e = json.loads(line[6:]); ev.append(e)
                    if e.get("kind") == "done": break
    def carts(pane):
        return [e["data"]["arguments"] for e in ev if e.get("pane") == pane and e.get("kind") == "tool_call"
                and e["data"]["tool"] in ("create_cart", "update_cart", "create_spend_request")]
    verdicts = [{"tool": v["tool"], "action": v["action"], "cart_total": v["cart_total"], "latency_ms": v["latency_ms"],
                 "tier": v["tier"], "error": v.get("error"),
                 "top_probes": sorted(({"id": p["id"], "p": round(p["p"], 2), "fired": p["fired"]} for p in v["probes"]),
                                      key=lambda p: -p["p"])[:3]}
                for v in (e["data"] for e in ev if e.get("kind") == "verdict")]
    text = lambda pane: [e["data"].get("message") for e in ev if e.get("pane") == pane and e.get("kind") == "log" and e["data"].get("message")][-1:]
    r = dict(id=cid, run=i + 1, run_id=rid, secs=round(time.time() - t0, 1), request=req, budget=budget,
             victim_carts=carts("victim"), guarded_carts=carts("guarded"), verdicts=verdicts,
             victim_text=text("victim"), guarded_text=text("guarded"))
    results.append(r)
    (OUT / f"results_{tag}.json").write_text(json.dumps(results, indent=2))
    print("done", i + 1, r["secs"], flush=True)

import json, sys
for f in sys.argv[1:]:
    for r in json.load(open(f)):
        carts = [(c.get("shop","").split(".")[0], sum(l["quantity"] for l in c["cart"]["line_items"])) for c in r["cart_calls"] if "cart" in c]
        spends = [c["spend_request"]["totals"][0]["amount"]/100 for c in r["cart_calls"] if "spend_request" in c]
        verd = [(v.get("action"), v.get("cart_total")) for v in r["verdicts"]]
        print(f, r["id"], r["secs"], "s | carts:", carts, "| spend:", spends, "| verdicts:", verd)
        print("   text:", (r["victim_text"] or [""])[0][:300].replace("\n"," "))

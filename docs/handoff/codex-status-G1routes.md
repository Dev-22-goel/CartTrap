# Codex status: G1 routes + G2 result fallback

Implemented the app route and run form changes from `handoff/codex-G1-app-routes.md`:

- Added `/api/rules`, `/api/dataset`, and allowlisted `/api/dataset/{item_id}/{file}` routes in `backend/app_routes.py` and included the router in `backend/main.py`.
- Dataset rows include manifest metadata, files that exist on disk, generated case request/budget when present, or the specified price-based fallback.
- `/api/run` now accepts `product_id` and `pdf`; product reference priority is `product_id`, `demo_product_id`, then `product_url`. PDFs are skipped with a warning because the current `Media.kind` schema does not allow `document`.
- G2: `backend/m4_routes.py` no longer returns `sample.json` as an evaluation result; no real result yields 404.
- Added route, request-precedence, traversal/allowlist, budget fallback, and no-sample tests. Cross-member changes to Member 1 files are recorded in `docs/decisions/m4/0021-cross-member-backend-wiring.md` under ADR 0019's whole-app extension.

Verification output:

```text
.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_G1r
355 passed, 13 deselected in 7.40s
```

No git commands were run and no network access was used.

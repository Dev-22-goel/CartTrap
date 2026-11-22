---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 1, Member 2"
---

# Member 4 wires app routes and run inputs across the backend

## Context and Problem Statement

The full-app integration plan identifies missing `/api/rules` and dataset routes, and a run form that drops `product_id` and `pdf`. Those changes cross the normal Member 1 ownership boundary for `backend/main.py` and `tests/test_api.py`. ADR 0019 already permits Member 4 to perform integration wiring in teammate-owned files; this task extends that permission to the whole app for the listed routes and form contract.

The dataset endpoint must expose generated manifests and only serve known, present files. The evaluation endpoint must not represent `sample.json` as a real run result.

## Decision

Member 4 adds `backend/app_routes.py` with an `app_router` for:

- `GET /api/rules`, returning the current shared RuleStore model.
- `GET /api/dataset`, projecting generated item manifests, present media files, request and budget data.
- `GET /api/dataset/{item_id}/{file}`, constrained to the item ID pattern and a fixed filename allowlist, with resolved-path containment checks.

Member 4 wires this router into `backend/main.py`, accepts `product_id` in `/api/run`, and chooses `product_id`, then `demo_product_id`, then `product_url` as the product reference. The form accepts `pdf`; because `Media.kind` does not allow `document`, this version skips that upload and logs a warning.

Member 4 also updates the M4 evaluation route so `sample.json` is excluded from real result candidates and a missing real result returns 404.

## Cross-member Changes

- `backend/main.py` (Member 1): app router include and run form/product reference wiring.
- `tests/test_api.py` (Member 1 integration tests): product ID precedence coverage.
- `backend/m4_routes.py` and `tests/test_m4_routes.py` are Member 4 files and are included here for the G2 follow-on in the same task.
- New route module and tests: `backend/app_routes.py`, `tests/test_app_routes.py`.

## Consequences

- The app exposes the route and form contracts needed by the integration plan.
- The dataset file route serves only allowlisted files inside a validated generated item directory.
- A PDF upload is accepted by the form parser but skipped until the Media contract supports the requested `document` kind.
- Owners should review the two Member 1 file changes at merge.

### Verification

- [x] Focused route, product ID precedence, and sample-fallback tests passed.
- [x] `.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_G1r` — 355 passed, 13 deselected.

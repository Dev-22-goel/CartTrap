Read handoff/m4-lane-contract.md first and follow it. It says which files you own and the rules you must follow.

CartTrap repo, branch m4-codex. Create:
1) backend/m4_routes.py: FastAPI APIRouter with GET /api/eval/latest (returns newest eval/results/*.json, 404 if none) and POST /api/redteam/launch (calls backend.redteam_carbon.launch_redteam if importable, else replays runs/redteam_demo.jsonl via backend/replay.py).
2) backend/replay.py: iter_trace(path) yields TraceEvents from a JSONL file in order.
3) eval/results/sample.json: a hand-made example that validates against the Metrics schema in backend/schemas.py (3 systems).
Do NOT edit backend/main.py. Tests: tests/test_m4_routes.py using FastAPI TestClient. Only edit these files + handoff/codex-status.md. Commit on m4-codex.

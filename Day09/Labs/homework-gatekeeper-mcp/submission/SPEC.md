# SPEC: Gatekeeper MCP server v1

- Server name: "AskIT Gatekeeper".
- Tool 1: `route_ticket(text)` calls `route()` from `gatekeeper.py` and returns the team name.
- Tool 2: `needs_approval(action, user_id, hour)` calls `needs_approval()` from `gatekeeper.py` and returns the boolean `approval` value.
  - Match the real parameter names and types of the function in `gatekeeper.py`.
  - The function in `gatekeeper.py` is `needs_approval(action: str, user_id: str, hour: int) -> dict`.
- Every tool has a clear one-sentence description a model can choose by.
- The server runs over stdio by default; with the argument `--http` it runs on port 8778.
- The server code must live in `submission/gatekeeper_server.py`.
- Also write `submission/test_gatekeeper_server.py`: it starts the server, lists the tools, calls each tool with 3 examples, and prints `PASS` or `FAIL` per call.

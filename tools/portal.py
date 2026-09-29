"""Local course portal (runs on YOUR VM only, http://localhost:8765).

- Serves the session pages from sessions/
- /api/me       -> your identity from me.json
- /api/dayend   -> Day End button: saves XP + lab results, commits and pushes
Started by START_DAY.bat. Close the window to stop it.
"""
import json
import posixpath
import sys
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone
from pathlib import Path

from day_end import PROGRESS, ROOT, SESSIONS, load_me, push_heartbeat, run_day_end, today_session

PORT = 8765
HEARTBEAT_PUSH_MIN = 15  # live progress pushed to GitHub every 15 min
LIVE_SESSIONS = set()


class Server(ThreadingHTTPServer):
    allow_reuse_address = False  # on Windows this makes a 2nd copy fail cleanly instead of sharing the port
    daemon_threads = True


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, fmt, *args):  # keep the console quiet
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # always show the latest content
        super().end_headers()

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/me":
            return self._json(load_me() or {}, 200 if load_me() else 404)
        if self.path in ("/", "/index.html"):
            return self._index()
        # only serve session pages and labs (no secrets like .env)
        clean = posixpath.normpath(self.path.split("?")[0])
        if not (clean.startswith("/sessions/") or clean.startswith("/labs/")):
            return self._json({"error": "not found"}, 404)
        return super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self._json({"error": "bad json"}, 400)
        if self.path == "/api/heartbeat":
            return self._heartbeat(payload)
        if self.path != "/api/dayend":
            return self._json({"error": "not found"}, 404)
        print(f"Day End requested for {payload.get('session')} ... (this can take a minute)")
        ok, steps = run_day_end(payload.get("session"), payload)
        for s in steps:
            print(("  [OK] " if s["ok"] else "  [!!] ") + s["step"], s.get("detail", ""))
        return self._json({"ok": ok, "steps": steps})

    def _heartbeat(self, p):
        session = p.get("session")
        if session not in SESSIONS:
            return self._json({"ok": False}, 400)
        p["participant"] = load_me()
        p["updated_at"] = datetime.now(timezone.utc).isoformat()
        PROGRESS.mkdir(exist_ok=True)
        (PROGRESS / f"{session}_live.json").write_text(json.dumps(p, indent=2), encoding="utf-8")
        LIVE_SESSIONS.add(session)
        return self._json({"ok": True})

    def _index(self):
        me = load_me() or {}
        cur = today_session()
        rows = "".join(
            f'<li><a href="/{v["html"]}">{k} · {v["title"]}</a> <small>{v["date"]}</small>{" ← today" if k == cur else ""}</li>'
            for k, v in SESSIONS.items() if (ROOT / v["html"]).exists()
        )
        html = f"""<!doctype html><meta charset="utf-8"><title>AskIT Portal</title>
<body style="font-family:Segoe UI,system-ui;max-width:700px;margin:40px auto;font-size:20px">
<h1>AskIT Program</h1><p>Welcome, <b>{me.get('name', 'participant')}</b> (Team {me.get('team', '?')})</p>
<ul>{rows}</ul></body>"""
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def heartbeat_pusher():
    while True:
        time.sleep(HEARTBEAT_PUSH_MIN * 60)
        for s in list(LIVE_SESSIONS):
            try:
                ok = push_heartbeat(s)
                print(time.strftime("%H:%M"), "progress synced" if ok else "progress sync will retry")
            except Exception as e:  # noqa: BLE001  never crash the portal
                print("sync error (will retry):", e)


if __name__ == "__main__":
    cur = today_session()
    try:
        srv = Server(("127.0.0.1", PORT), Handler)
    except OSError:
        print("Portal is already running - opening your browser.")
        webbrowser.open(f"http://localhost:{PORT}/{SESSIONS[cur]['html']}")
        sys.exit(0)
    threading.Thread(target=heartbeat_pusher, daemon=True).start()
    url = f"http://localhost:{PORT}/{SESSIONS[cur]['html']}"
    if not (ROOT / SESSIONS[cur]["html"]).exists():
        url = f"http://localhost:{PORT}/"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print(f"AskIT portal running at http://localhost:{PORT}  (keep this window open; close it to stop)")
    srv.serve_forever()

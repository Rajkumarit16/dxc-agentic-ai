"""Creates me.json (your identity for dashboards). Run once via SETUP.bat."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
f = ROOT / "me.json"

if f.exists():
    print("me.json already exists:", f.read_text(encoding="utf-8"))
    if input("Re-create it? (y/N): ").strip().lower() != "y":
        raise SystemExit(0)

name = input("Your full name: ").strip()
github = input("Your GitHub username: ").strip()
team = input("Your team (A/B/C/D): ").strip().upper()[:1]
f.write_text(json.dumps({"name": name, "github_user": github, "team": team}, indent=2), encoding="utf-8")
import subprocess
subprocess.run(["git", "config", "user.name", name], cwd=ROOT)
subprocess.run(["git", "config", "user.email", f"{github}@users.noreply.github.com"], cwd=ROOT)
print("Saved", f, "and set your git name/email")

"""Load the Orbit Corp helpdesk data."""
import csv

from askit_core.config import DATA_DIR


def load_tickets():
    with open(DATA_DIR / "tickets.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_users():
    with open(DATA_DIR / "users.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_kb():
    """Return {doc_id: text} for every KB article."""
    return {p.stem.split("_")[0]: p.read_text(encoding="utf-8") for p in sorted((DATA_DIR / "kb").glob("*.md"))}

import re


_PRIORITY_SLA = {"P1": 2, "P2": 8, "P3": 24, "P4": 72}
_QUEUE_WORDS = (
    ("Security", ("phishing", "breach", "malware")),
    ("Network", ("vpn", "wifi", "network")),
    ("Access", ("password", "login", "locked")),
    ("Hardware", ("laptop", "keyboard", "screen")),
)


def _has_word(text, word):
    return re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE) is not None


def _priority_for_text_and_users(text, affected_users):
    if affected_users >= 50 or _has_word(text, "outage") or _has_word(text, "down"):
        return "P1"
    if affected_users >= 10 or _has_word(text, "urgent") or _has_word(text, "blocked"):
        return "P2"
    if affected_users >= 2:
        return "P3"
    return "P4"


def triage(ticket):
    title = ticket.get("title")
    if not isinstance(title, str) or title.strip() == "":
        raise ValueError("title is required")

    description = ticket.get("description", "")
    if description is None:
        description = ""
    if not isinstance(description, str):
        description = str(description)

    affected_users = ticket.get("affected_users", 1)
    if not isinstance(affected_users, int) or affected_users < 1:
        raise ValueError("affected_users must be a positive int")

    customer_tier = ticket.get("customer_tier", "standard")
    if customer_tier not in ("standard", "vip"):
        raise ValueError("customer_tier must be standard or vip")

    text = f"{title} {description}"
    priority = _priority_for_text_and_users(text, affected_users)
    if customer_tier == "vip":
        priority = {"P4": "P3", "P3": "P2", "P2": "P1", "P1": "P1"}[priority]

    queue = "General"
    for queue_name, words in _QUEUE_WORDS:
        if any(_has_word(text, word) for word in words):
            queue = queue_name
            break

    return {"priority": priority, "queue": queue, "sla_hours": _PRIORITY_SLA[priority]}

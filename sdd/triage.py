import re


_PRIORITY_SLA = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
_PRIORITY_WORDS = (
    ("P1", ("outage", "down")),
    ("P2", ("urgent", "blocked")),
)
_QUEUE_WORDS = (
    ("Network", ("vpn", "wifi", "network")),
    ("Access", ("password", "login", "locked")),
    ("Hardware", ("laptop", "keyboard", "screen")),
)


def _whole_word_pattern(word):
    return re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)


def _has_word(text, word):
    return _whole_word_pattern(word).search(text) is not None


def triage(ticket):
    title = ticket.get("title")
    if not isinstance(title, str) or title == "":
        raise ValueError("title is required")

    description = ticket.get("description", "")
    if description is None:
        description = ""
    if not isinstance(description, str):
        description = str(description)

    affected_users = ticket.get("affected_users", 1)
    if not isinstance(affected_users, int) or affected_users < 1:
        raise ValueError("affected_users must be a positive int")

    text = f"{title} {description}"

    if affected_users >= 50 or any(_has_word(text, word) for word in _PRIORITY_WORDS[0][1]):
        priority = "P1"
    elif affected_users >= 10 or any(_has_word(text, word) for word in _PRIORITY_WORDS[1][1]):
        priority = "P2"
    elif affected_users >= 2:
        priority = "P3"
    else:
        priority = "P4"

    queue = "General"
    for queue_name, words in _QUEUE_WORDS:
        if any(_has_word(text, word) for word in words):
            queue = queue_name
            break

    return {"priority": priority, "queue": queue, "sla_hours": _PRIORITY_SLA[priority]}

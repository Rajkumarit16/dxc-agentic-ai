import re


_ROUTE_KEYWORDS = (
    ("Security", ("phishing", "malware", "breach", "suspicious", "ransomware")),
    ("Access", ("password", "locked", "login", "mfa", "access")),
    ("Network", ("vpn", "wifi", "network", "internet")),
    ("Hardware", ("laptop", "printer", "screen", "keyboard", "phone")),
)
_READ_ACTIONS = {"search_kb", "get_ticket"}
_WRITE_ACTIONS = {"reset_password", "update_ticket", "grant_access"}
_VIP_USERS = {"EMP-1001", "EMP-1012", "EMP-1023"}
_SENSITIVE_WORDS = ("password", "passcode", "otp", "pin", "address")


def route(text: str) -> str:
    if not text.strip():
        raise ValueError("text must not be empty")

    for team, keywords in _ROUTE_KEYWORDS:
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text, re.IGNORECASE):
                return team

    return "General"


def needs_approval(action: str, user_id: str, hour: int) -> dict:
    if action not in _READ_ACTIONS and action not in _WRITE_ACTIONS:
        raise ValueError("unsupported action")
    if type(hour) is not int or not 0 <= hour <= 23:
        raise ValueError("hour must be an int from 0 to 23")

    is_vip = user_id in _VIP_USERS

    if action in _READ_ACTIONS:
        if is_vip:
            return {"approval": True, "approver": "it manager"}
        return {"approval": False, "approver": "none"}

    if is_vip:
        return {"approval": True, "approver": "it manager"}
    if hour >= 20 or hour < 8:
        return {"approval": True, "approver": "queue"}
    return {"approval": True, "approver": "service desk lead"}


def safe_to_remember(text: str) -> bool:
    if not text.strip():
        return False

    for word in _SENSITIVE_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text, re.IGNORECASE):
            return False

    digits_without_separators = re.sub(r"[\s-]", "", text)
    if re.search(r"\d{6,}", digits_without_separators):
        return False

    return True

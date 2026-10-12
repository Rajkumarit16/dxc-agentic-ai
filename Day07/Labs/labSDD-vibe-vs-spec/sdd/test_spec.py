import pytest

from triage import triage


def test_ac1_60_affected_users_is_p1_and_sla_2():
    assert triage({"title": "Issue", "affected_users": 60}) == {"priority": "P1", "queue": "General", "sla_hours": 2}


def test_ac2_email_outage_is_p1():
    assert triage({"title": "Email outage"})["priority"] == "P1"


def test_ac3_slow_download_speed_is_p4_due_to_whole_word_rule():
    assert triage({"title": "Slow download speed"}) == {"priority": "P4", "queue": "General", "sla_hours": 72}


def test_ac4_12_users_is_p2_and_sla_8():
    assert triage({"title": "Issue", "affected_users": 12}) == {"priority": "P2", "queue": "General", "sla_hours": 8}


def test_ac5_urgent_cannot_print_is_p2():
    assert triage({"title": "URGENT: cannot print"})["priority"] == "P2"


def test_ac6_3_users_is_p3_and_sla_24():
    assert triage({"title": "Issue", "affected_users": 3}) == {"priority": "P3", "queue": "General", "sla_hours": 24}


def test_ac7_laptop_wifi_broken_is_network_queue():
    assert triage({"title": "Laptop wifi broken"})["queue"] == "Network"


def test_ac8_password_reset_is_access_queue():
    assert triage({"title": "Password reset"})["queue"] == "Access"


def test_ac9_empty_title_and_zero_users_raise_value_error():
    with pytest.raises(ValueError):
        triage({"title": ""})
    with pytest.raises(ValueError):
        triage({"title": "Issue", "affected_users": 0})


def test_ac10_vip_raises_priority_one_level():
    assert triage({"title": "Issue", "customer_tier": "vip"})["priority"] == "P3"


def test_ac11_security_queue_is_checked_first():
    assert triage({"title": "Laptop phishing"})["queue"] == "Security"


def test_ac12_invalid_customer_tier_raises_value_error():
    with pytest.raises(ValueError):
        triage({"title": "Issue", "customer_tier": "gold"})

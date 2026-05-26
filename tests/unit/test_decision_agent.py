import pytest

from agents.decision_agent.agent import _decide


# ── no_reply intent ──────────────────────────────────────────────────────────

def test_no_reply_always_no_action():
    assert _decide("no_reply", {}) == "no_action"


def test_no_reply_ignores_lead_quality():
    assert _decide("no_reply", {"leadqualitycode": 1}) == "no_action"


# ── negative intent ──────────────────────────────────────────────────────────

def test_negative_always_no_action():
    assert _decide("negative", {}) == "no_action"


def test_negative_ignores_hot_lead():
    assert _decide("negative", {"leadqualitycode": 1}) == "no_action"


# ── positive intent ──────────────────────────────────────────────────────────

def test_positive_hot_lead_schedules_meeting():
    assert _decide("positive", {"leadqualitycode": 1}) == "schedule"


def test_positive_warm_lead_sends_reply():
    assert _decide("positive", {"leadqualitycode": 2}) == "reply"


def test_positive_cold_lead_sends_reply():
    assert _decide("positive", {"leadqualitycode": 3}) == "reply"


def test_positive_no_quality_code_defaults_to_reply():
    # Missing leadqualitycode defaults to 3 (Cold) inside _decide
    assert _decide("positive", {}) == "reply"


# ── neutral intent ───────────────────────────────────────────────────────────

def test_neutral_always_reply():
    assert _decide("neutral", {}) == "reply"


def test_neutral_hot_lead_still_reply():
    assert _decide("neutral", {"leadqualitycode": 1}) == "reply"

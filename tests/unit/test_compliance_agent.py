import pytest

from agents.compliance_agent.agent import _is_compliant


def test_bulk_email_opt_out():
    assert _is_compliant({"donotbulkemail": True}) is False


def test_email_opt_out():
    assert _is_compliant({"donotemail": True}) is False


def test_frequency_cap_reached():
    assert _is_compliant({"emails_this_week": 3}) is False


def test_frequency_cap_exceeded():
    assert _is_compliant({"emails_this_week": 10}) is False


def test_compliant_lead_passes():
    lead = {"donotbulkemail": False, "donotemail": False, "emails_this_week": 1}
    assert _is_compliant(lead) is True


def test_empty_lead_passes():
    # No flags set — defaults to compliant
    assert _is_compliant({}) is True


def test_both_opt_outs_set():
    assert _is_compliant({"donotbulkemail": True, "donotemail": True}) is False

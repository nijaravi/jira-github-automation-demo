"""
Unit tests for app.py — covers input validation only.

Rate limiting is intentionally not under test yet (SCRUM-2 requirement 3
is only partially covered).
"""

from app import is_valid_username, is_valid_password


def test_valid_username_accepted():
    assert is_valid_username("abdul_123")


def test_username_too_short_rejected():
    assert not is_valid_username("ab")


def test_username_bad_characters_rejected():
    assert not is_valid_username("abdul!123")


def test_empty_username_rejected():
    assert not is_valid_username("")


def test_valid_password_accepted():
    assert is_valid_password("longenoughpassword")


def test_password_too_short_rejected():
    assert not is_valid_password("short")


def test_empty_password_rejected():
    assert not is_valid_password("")

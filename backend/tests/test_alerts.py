"""Tests for Alert Engine logic."""

import pytest
from app.services.alert_engine import (
    determine_trigger_level,
    generate_alert_message,
)


class TestAlertEngine:
    """Unit tests for alert triggering and NLG message generation."""

    def test_trigger_level_below_threshold(self):
        assert determine_trigger_level(50) is None
        assert determine_trigger_level(0) is None
        assert determine_trigger_level(59.9) is None

    def test_trigger_level_watch(self):
        assert determine_trigger_level(60) == "watch"
        assert determine_trigger_level(65) == "watch"
        assert determine_trigger_level(69.9) == "watch"

    def test_trigger_level_warning(self):
        assert determine_trigger_level(70) == "warning"
        assert determine_trigger_level(75) == "warning"
        assert determine_trigger_level(79.9) == "warning"

    def test_trigger_level_emergency(self):
        assert determine_trigger_level(80) == "emergency"
        assert determine_trigger_level(90) == "emergency"
        assert determine_trigger_level(100) == "emergency"

    def test_alert_message_watch(self):
        msg = generate_alert_message(
            nama="Coblong", uss=65, climate=60, infra=70, soceco=55, level="watch"
        )
        assert "Coblong" in msg
        assert "65" in msg
        assert "WASPADA" in msg

    def test_alert_message_warning(self):
        msg = generate_alert_message(
            nama="Cicendo", uss=74, climate=80, infra=75, soceco=60, level="warning"
        )
        assert "Cicendo" in msg
        assert "PERINGATAN" in msg
        assert "Iklim" in msg  # climate is highest

    def test_alert_message_emergency(self):
        msg = generate_alert_message(
            nama="Sukasari", uss=87, climate=85, infra=90, soceco=80, level="emergency"
        )
        assert "Sukasari" in msg
        assert "DARURAT" in msg
        assert "Infrastruktur" in msg  # infra is highest

    def test_alert_message_bahasa_indonesia(self):
        """Alert messages must be in Bahasa Indonesia."""
        msg = generate_alert_message(
            nama="Test", uss=75, climate=70, infra=80, soceco=60, level="warning"
        )
        # Check for Indonesian keywords
        assert any(
            word in msg for word in ["Rekomendasi", "BPBD", "dimensi", "inspeksi"]
        )

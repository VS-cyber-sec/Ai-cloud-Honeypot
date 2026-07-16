"""
tests/test_ml_pipeline.py — Unit tests for ML classification pipeline
Run: python3 -m pytest tests/test_ml_pipeline.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml'))

import pandas as pd


class TestAssignLabel:
    """Tests for the label assignment logic."""

    def _make_row(self, protocol, path="", ua="", ip="1.2.3.4"):
        return {
            "protocol": protocol,
            "http_path": path,
            "user_agent": ua,
            "src_ip": ip,
            "timestamp": "2026-06-01 10:00:00",
        }

    def test_brute_force_label(self):
        """High-rate SSH should be classified as brute_force."""
        from honeypot_model_v2 import assign_label
        row = self._make_row("SSH")
        ts_counts = {"2026-06-01 10:00:00": 10}
        ip_counts = {"1.2.3.4": 15}
        label = assign_label(row, ts_counts, ip_counts)
        assert label == "brute_force"

    def test_ssh_probe_label(self):
        """Low-rate SSH should be ssh_probe."""
        from honeypot_model_v2 import assign_label
        row = self._make_row("SSH")
        ts_counts = {"2026-06-01 10:00:00": 1}
        ip_counts = {"1.2.3.4": 1}
        label = assign_label(row, ts_counts, ip_counts)
        assert label == "ssh_probe"

    def test_web_shell_probe_label(self):
        """Shell path should be web_shell_probe."""
        from honeypot_model_v2 import assign_label
        row = self._make_row("HTTP", path="/shell.php")
        label = assign_label(row, {}, {"1.2.3.4": 1})
        assert label == "web_shell_probe"

    def test_exploit_attempt_label(self):
        """WordPress login path should be exploit_attempt."""
        from honeypot_model_v2 import assign_label
        row = self._make_row("HTTP", path="/wp-login.php")
        label = assign_label(row, {}, {"1.2.3.4": 1})
        assert label == "exploit_attempt"

    def test_cloud_metadata_probe_label(self):
        """AWS metadata path should be cloud_metadata_probe."""
        from honeypot_model_v2 import assign_label
        row = self._make_row("HTTP", path="/latest/meta-data/")
        label = assign_label(row, {}, {"1.2.3.4": 1})
        assert label == "cloud_metadata_probe"

    def test_web_recon_scanner_ua(self):
        """Known scanner User-Agent should be web_recon."""
        from honeypot_model_v2 import assign_label
        row = self._make_row("HTTP", ua="masscan/1.0")
        label = assign_label(row, {"2026-06-01 10:00:00": 1}, {"1.2.3.4": 1})
        assert label == "web_recon"


class TestFeatureEngineering:
    """Tests for feature extraction functions."""

    def test_extract_ip_features_public(self):
        from honeypot_model_v2 import extract_ip_features
        df = pd.DataFrame([{"src_ip": "8.8.8.8"}])
        df = extract_ip_features(df)
        assert df["first_octet"].iloc[0] == 8
        assert df["is_private"].iloc[0] == 0

    def test_extract_ip_features_private(self):
        from honeypot_model_v2 import extract_ip_features
        df = pd.DataFrame([{"src_ip": "192.168.1.1"}])
        df = extract_ip_features(df)
        assert df["is_private"].iloc[0] == 1

    def test_engineer_features_adds_time_cols(self):
        from honeypot_model_v2 import engineer_features
        df = pd.DataFrame([{"timestamp": "2026-06-01 10:30:00"}])
        df = engineer_features(df)
        assert "hour" in df.columns
        assert "minute" in df.columns
        assert "day_of_week" in df.columns
        assert df["hour"].iloc[0] == 10
        assert df["minute"].iloc[0] == 30

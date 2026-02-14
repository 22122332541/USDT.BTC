"""Tests for monitor.checker and monitor.notifier."""

import unittest
from unittest.mock import patch

from monitor.checker import check_anomalies
from monitor.notifier import build_alert_message


class TestCheckAnomalies(unittest.TestCase):
    """Verify that check_anomalies correctly flags metrics above thresholds."""

    @patch("monitor.checker.get_disk_usage", return_value=50.0)
    @patch("monitor.checker.get_memory_usage", return_value=50.0)
    @patch("monitor.checker.get_cpu_usage", return_value=50.0)
    def test_no_anomalies(self, _cpu, _mem, _disk):
        anomalies = check_anomalies()
        self.assertEqual(anomalies, [])

    @patch("monitor.checker.get_disk_usage", return_value=95.0)
    @patch("monitor.checker.get_memory_usage", return_value=90.0)
    @patch("monitor.checker.get_cpu_usage", return_value=99.0)
    def test_all_anomalies(self, _cpu, _mem, _disk):
        anomalies = check_anomalies()
        self.assertEqual(len(anomalies), 3)
        metrics = {a["metric"] for a in anomalies}
        self.assertEqual(metrics, {"CPU", "Memory", "Disk"})

    @patch("monitor.checker.get_disk_usage", return_value=50.0)
    @patch("monitor.checker.get_memory_usage", return_value=50.0)
    @patch("monitor.checker.get_cpu_usage", return_value=99.0)
    def test_cpu_only(self, _cpu, _mem, _disk):
        anomalies = check_anomalies()
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["metric"], "CPU")


class TestBuildAlertMessage(unittest.TestCase):
    """Verify that the alert message body is well-formed."""

    def test_message_contains_metrics(self):
        anomalies = [
            {"metric": "CPU", "value": 95.0, "threshold": 85.0},
        ]
        body = build_alert_message(anomalies)
        self.assertIn("CPU", body)
        self.assertIn("95.0%", body)
        self.assertIn("85.0%", body)

    def test_empty_anomalies(self):
        body = build_alert_message([])
        self.assertIn("Anomaly Alert", body)


if __name__ == "__main__":
    unittest.main()

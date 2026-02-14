"""Configuration for the anomaly monitoring system.

Thresholds and email settings are loaded from environment variables
so that no secrets are stored in source code.
"""

import os

# ---------------------------------------------------------------------------
# Monitoring thresholds (percentage, 0-100)
# ---------------------------------------------------------------------------
CPU_THRESHOLD = float(os.getenv("MONITOR_CPU_THRESHOLD", "85"))
MEMORY_THRESHOLD = float(os.getenv("MONITOR_MEMORY_THRESHOLD", "85"))
DISK_THRESHOLD = float(os.getenv("MONITOR_DISK_THRESHOLD", "90"))

# ---------------------------------------------------------------------------
# Check interval in seconds
# ---------------------------------------------------------------------------
CHECK_INTERVAL = int(os.getenv("MONITOR_CHECK_INTERVAL", "60"))

# ---------------------------------------------------------------------------
# Email / SMTP configuration
# ---------------------------------------------------------------------------
SMTP_SERVER = os.getenv("MONITOR_SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("MONITOR_SMTP_PORT", "465"))
SMTP_USE_SSL = os.getenv("MONITOR_SMTP_USE_SSL", "true").lower() == "true"

# Sender credentials – MUST be set via environment variables
EMAIL_SENDER = os.getenv("MONITOR_EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("MONITOR_EMAIL_PASSWORD", "")  # QQ授权码

# Recipient
EMAIL_RECIPIENT = os.getenv("MONITOR_EMAIL_RECIPIENT", "2968658164@qq.com")

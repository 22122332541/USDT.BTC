"""Email notifier – sends anomaly alerts via SMTP."""

import logging
import smtplib
import ssl
from datetime import datetime, timezone
from email.mime.text import MIMEText

from monitor.config import (
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    EMAIL_SENDER,
    SMTP_PORT,
    SMTP_SERVER,
    SMTP_USE_SSL,
)

logger = logging.getLogger(__name__)


def build_alert_message(anomalies: list[dict]) -> str:
    """Build a human-readable alert body from a list of anomalies."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [f"[Anomaly Alert] {now}", ""]
    for a in anomalies:
        lines.append(
            f"  - {a['metric']}: {a['value']:.1f}% (threshold: {a['threshold']:.1f}%)"
        )
    lines.append("")
    lines.append("Please check the system as soon as possible.")
    return "\n".join(lines)


def send_email(subject: str, body: str) -> bool:
    """Send an email alert. Returns True on success, False on failure."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        logger.warning(
            "Email sender credentials are not configured. "
            "Set MONITOR_EMAIL_SENDER and MONITOR_EMAIL_PASSWORD."
        )
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    try:
        if SMTP_USE_SSL:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, [EMAIL_RECIPIENT], msg.as_string())
        else:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, [EMAIL_RECIPIENT], msg.as_string())
        logger.info("Alert email sent to %s", EMAIL_RECIPIENT)
        return True
    except Exception:
        logger.exception("Failed to send alert email")
        return False


def notify(anomalies: list[dict]) -> bool:
    """Build and send an anomaly alert email."""
    if not anomalies:
        return False
    body = build_alert_message(anomalies)
    subject = f"[Monitor] {len(anomalies)} anomaly alert(s)"
    return send_email(subject, body)

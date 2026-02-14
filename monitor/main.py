"""Entry point for the anomaly monitoring loop."""

import logging
import time

from monitor.checker import check_anomalies
from monitor.config import CHECK_INTERVAL
from monitor.notifier import notify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run() -> None:
    """Run the monitoring loop indefinitely."""
    logger.info("Anomaly monitor started (interval=%ds)", CHECK_INTERVAL)
    while True:
        anomalies = check_anomalies()
        if anomalies:
            logger.warning("Anomalies detected: %s", anomalies)
            notify(anomalies)
        else:
            logger.info("All metrics normal.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()

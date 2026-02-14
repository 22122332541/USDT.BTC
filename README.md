# USDT.BTC

Computer anomaly monitoring system — monitors CPU, memory and disk usage in real time and sends email alerts when thresholds are exceeded.

## Project layout

```
monitor/
  config.py      # Thresholds & email settings (via environment variables)
  checker.py     # System metrics collection & anomaly detection
  notifier.py    # Email alert sender (SMTP)
  main.py        # Entry point – runs the monitoring loop
tests/
  test_monitor.py
requirements.txt
```

## Quick start

```bash
pip install -r requirements.txt
```

### Configure environment variables

| Variable | Description | Default |
|---|---|---|
| `MONITOR_CPU_THRESHOLD` | CPU usage alert threshold (%) | `85` |
| `MONITOR_MEMORY_THRESHOLD` | Memory usage alert threshold (%) | `85` |
| `MONITOR_DISK_THRESHOLD` | Disk usage alert threshold (%) | `90` |
| `MONITOR_CHECK_INTERVAL` | Check interval in seconds | `60` |
| `MONITOR_SMTP_SERVER` | SMTP server hostname | `smtp.qq.com` |
| `MONITOR_SMTP_PORT` | SMTP server port | `465` |
| `MONITOR_SMTP_USE_SSL` | Use SSL for SMTP | `true` |
| `MONITOR_EMAIL_SENDER` | Sender email address | *(required)* |
| `MONITOR_EMAIL_PASSWORD` | Sender email password / auth code | *(required)* |
| `MONITOR_EMAIL_RECIPIENT` | Recipient email address | `2968658164@qq.com` |

### Run

```bash
export MONITOR_EMAIL_SENDER="your_email@qq.com"
export MONITOR_EMAIL_PASSWORD="your_qq_auth_code"
python -m monitor.main
```

### Run tests

```bash
python -m unittest discover tests -v
```

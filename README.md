# USDT.BTC

Security protection module for USDT.BTC user data.

## Features

- **Brute-force detection** — locks out after configurable failed-attempt threshold within a sliding time window.
- **Flash integrity verification** — verifies firmware images against a known SHA-256 hash; triggers self-destruct on mismatch.
- **Memory self-destruct** — securely overwrites and deletes registered protected files/directories when a violation is detected.

## Directory layout

```
security/
  __init__.py          # package exports
  protection.py        # SecurityProtection class
tests/
  test_protection.py   # pytest test suite
```

## Quick start

```python
from security import SecurityProtection

sp = SecurityProtection(
    max_attempts=5,           # lock after 5 failures
    window_seconds=300,       # within a 5-minute window
    flash_hash="abcdef...",   # expected firmware SHA-256
    on_destruct=lambda paths: print("wiped:", paths),
)

sp.register_protected_path("/data/wallet.dat")

# Record access attempts — returns True when self-destruct fires
sp.record_attempt("user@ip", success=False)

# Verify firmware integrity
sp.verify_flash("/path/to/firmware.bin")

# Manual wipe
sp.memory_destruct()
```

## Running tests

```bash
pip install pytest
python -m pytest tests/ -v
```

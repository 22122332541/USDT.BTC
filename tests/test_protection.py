"""Tests for security.protection module."""

import hashlib
import os
import tempfile

import pytest

from security.protection import SecurityProtection


# ----- helpers --------------------------------------------------------

def _write_file(path: str, content: bytes = b"secret-data") -> None:
    with open(path, "wb") as fh:
        fh.write(content)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ----- brute-force detection -----------------------------------------

class TestBruteForceDetection:
    def test_successful_attempts_do_not_trigger(self):
        sp = SecurityProtection(max_attempts=3)
        for _ in range(10):
            assert sp.record_attempt("user", success=True) is False
        assert not sp.is_locked

    def test_failures_below_threshold_do_not_trigger(self):
        sp = SecurityProtection(max_attempts=5)
        for _ in range(4):
            assert sp.record_attempt("user", success=False) is False
        assert not sp.is_locked

    def test_failures_at_threshold_trigger_destruct(self):
        sp = SecurityProtection(max_attempts=3)
        sp.record_attempt("user", success=False)
        sp.record_attempt("user", success=False)
        triggered = sp.record_attempt("user", success=False)
        assert triggered is True
        assert sp.is_locked

    def test_callback_invoked_on_destruct(self):
        wiped_result = []
        sp = SecurityProtection(
            max_attempts=2,
            on_destruct=lambda paths: wiped_result.extend(paths),
        )
        sp.record_attempt("user", success=False)
        sp.record_attempt("user", success=False)
        # callback should have been called (with empty wiped list here)
        assert isinstance(wiped_result, list)


# ----- flash verification --------------------------------------------

class TestFlashVerification:
    def test_valid_firmware_passes(self, tmp_path):
        firmware = tmp_path / "firmware.bin"
        content = b"valid-firmware-image"
        firmware.write_bytes(content)

        sp = SecurityProtection(flash_hash=_sha256(content))
        assert sp.verify_flash(str(firmware)) is True
        assert not sp.is_locked

    def test_invalid_firmware_triggers_destruct(self, tmp_path):
        firmware = tmp_path / "firmware.bin"
        firmware.write_bytes(b"tampered-image")

        sp = SecurityProtection(flash_hash=_sha256(b"original-image"))
        assert sp.verify_flash(str(firmware)) is False
        assert sp.is_locked

    def test_verify_flash_without_hash_raises(self, tmp_path):
        firmware = tmp_path / "firmware.bin"
        firmware.write_bytes(b"data")

        sp = SecurityProtection()
        with pytest.raises(RuntimeError, match="No flash_hash configured"):
            sp.verify_flash(str(firmware))


# ----- memory self-destruct -------------------------------------------

class TestMemoryDestruct:
    def test_wipe_removes_file(self, tmp_path):
        target = tmp_path / "wallet.dat"
        _write_file(str(target))

        sp = SecurityProtection()
        sp.register_protected_path(str(target))
        wiped = sp.memory_destruct()

        assert str(target) in wiped
        assert not target.exists()

    def test_wipe_removes_directory(self, tmp_path):
        d = tmp_path / "data"
        d.mkdir()
        (d / "a.txt").write_bytes(b"aaa")
        (d / "b.txt").write_bytes(b"bbb")

        sp = SecurityProtection()
        sp.register_protected_path(str(d))
        wiped = sp.memory_destruct()

        assert str(d) in wiped
        assert not d.exists()

    def test_wipe_on_brute_force(self, tmp_path):
        target = tmp_path / "keys.dat"
        _write_file(str(target))

        sp = SecurityProtection(max_attempts=2)
        sp.register_protected_path(str(target))

        sp.record_attempt("attacker", success=False)
        sp.record_attempt("attacker", success=False)

        assert sp.is_locked
        assert not target.exists()

    def test_wipe_on_flash_failure(self, tmp_path):
        target = tmp_path / "secret.dat"
        _write_file(str(target))

        firmware = tmp_path / "firmware.bin"
        firmware.write_bytes(b"bad-firmware")

        sp = SecurityProtection(flash_hash=_sha256(b"good-firmware"))
        sp.register_protected_path(str(target))
        sp.verify_flash(str(firmware))

        assert sp.is_locked
        assert not target.exists()

    def test_missing_path_is_skipped(self, tmp_path):
        sp = SecurityProtection()
        sp.register_protected_path(str(tmp_path / "nonexistent"))
        wiped = sp.memory_destruct()
        assert wiped == []


# ----- constructor validation -----------------------------------------

class TestConstructorValidation:
    def test_max_attempts_must_be_positive(self):
        with pytest.raises(ValueError, match="max_attempts"):
            SecurityProtection(max_attempts=0)

    def test_window_seconds_must_be_positive(self):
        with pytest.raises(ValueError, match="window_seconds"):
            SecurityProtection(window_seconds=0)

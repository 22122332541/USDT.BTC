"""Security protection module.

Provides brute-force detection, flash integrity verification,
and memory self-destruct for non-compliant access attempts.
"""

import hashlib
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class AccessAttempt:
    """Record of a single access attempt."""

    timestamp: float
    identifier: str
    success: bool


class SecurityProtection:
    """Core security protection for user data.

    Detects brute-force file access, unauthorised firmware flashing,
    and triggers memory self-destruct when thresholds are breached.

    Parameters
    ----------
    max_attempts : int
        Maximum failed attempts before lockout (default 5).
    window_seconds : float
        Sliding window in seconds for attempt counting (default 300).
    flash_hash : str or None
        Expected SHA-256 hex digest of the authorised firmware image.
        If *None*, flash verification is disabled.
    on_destruct : callable or None
        Optional callback invoked when self-destruct triggers.
        Receives the list of *protected_paths* that were wiped.
    """

    def __init__(
        self,
        max_attempts: int = 5,
        window_seconds: float = 300.0,
        flash_hash: Optional[str] = None,
        on_destruct: Optional[Callable] = None,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")

        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.flash_hash = flash_hash
        self.on_destruct = on_destruct

        self._attempts: list[AccessAttempt] = []
        self._locked = False
        self._protected_paths: list[str] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def is_locked(self) -> bool:
        """Return *True* when a lockout is active."""
        return self._locked

    def register_protected_path(self, path: str) -> None:
        """Add *path* to the set of paths wiped on self-destruct."""
        if path not in self._protected_paths:
            self._protected_paths.append(path)

    def record_attempt(self, identifier: str, success: bool) -> bool:
        """Record an access attempt.

        Returns *True* when self-destruct was triggered (i.e. the
        failed-attempt threshold within the sliding window was exceeded).
        """
        now = time.monotonic()
        self._attempts.append(
            AccessAttempt(timestamp=now, identifier=identifier, success=success)
        )

        if success:
            return False

        # Count recent failures inside the sliding window
        cutoff = now - self.window_seconds
        recent_failures = [
            a
            for a in self._attempts
            if not a.success and a.timestamp >= cutoff
        ]

        if len(recent_failures) >= self.max_attempts:
            logger.critical(
                "Brute-force threshold exceeded (%d failures in %.0fs) "
                "— triggering self-destruct",
                len(recent_failures),
                self.window_seconds,
            )
            self._trigger_destruct()
            return True

        return False

    def verify_flash(self, firmware_path: str) -> bool:
        """Verify the integrity of a firmware image.

        Returns *True* when the image matches the expected hash.
        If the hash does not match, self-destruct is triggered and
        the method returns *False*.
        """
        if self.flash_hash is None:
            raise RuntimeError("No flash_hash configured for verification")

        digest = self._sha256_file(firmware_path)

        if digest == self.flash_hash:
            logger.info("Firmware verification passed: %s", firmware_path)
            return True

        logger.critical(
            "Firmware verification FAILED for %s "
            "(expected %s, got %s) — triggering self-destruct",
            firmware_path,
            self.flash_hash,
            digest,
        )
        self._trigger_destruct()
        return False

    def memory_destruct(self) -> list[str]:
        """Securely wipe all registered protected paths.

        Returns the list of paths that were wiped.
        """
        wiped: list[str] = []
        for path in self._protected_paths:
            if os.path.isfile(path):
                self._secure_wipe_file(path)
                wiped.append(path)
            elif os.path.isdir(path):
                self._secure_wipe_directory(path)
                wiped.append(path)
            else:
                logger.warning("Protected path not found, skipping: %s", path)
        return wiped

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _trigger_destruct(self) -> None:
        """Lock the system and wipe protected data."""
        self._locked = True
        wiped = self.memory_destruct()
        if self.on_destruct is not None:
            self.on_destruct(wiped)

    @staticmethod
    def _sha256_file(path: str) -> str:
        """Return the SHA-256 hex digest of *path*."""
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            while True:
                chunk = fh.read(65536)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def _secure_wipe_file(path: str) -> None:
        """Overwrite *path* with random bytes, then remove it."""
        try:
            size = os.path.getsize(path)
            with open(path, "r+b") as fh:
                fh.write(os.urandom(size))
                fh.flush()
                os.fsync(fh.fileno())
            os.remove(path)
            logger.info("Securely wiped file: %s", path)
        except OSError:
            logger.exception("Failed to wipe file: %s", path)

    @staticmethod
    def _secure_wipe_directory(path: str) -> None:
        """Recursively wipe all files under *path*, then remove dirs."""
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                fpath = os.path.join(root, name)
                SecurityProtection._secure_wipe_file(fpath)
            for name in dirs:
                dpath = os.path.join(root, name)
                try:
                    os.rmdir(dpath)
                except OSError:
                    logger.exception("Failed to remove dir: %s", dpath)
        try:
            os.rmdir(path)
        except OSError:
            logger.exception("Failed to remove dir: %s", path)

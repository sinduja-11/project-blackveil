"""
In-memory identity repository.

Provides a simple CRUD-style abstraction over a plain Python dict so that the
router and future components never touch storage directly.

⚠️  IMPORTANT — Persistence warning
------------------------------------
This repository stores participant records in a module-level Python dict.
ALL DATA IS LOST WHEN THE APPLICATION PROCESS RESTARTS.

This is deliberate for the Phase-2 prototype.  A future phase may replace this
class with a database-backed implementation without changing the router or
service layer, because all storage access is isolated here.

Thread safety
-------------
The CPython GIL provides basic atomicity for simple dict reads and assignments,
which is sufficient for the current single-process prototype.  A production
replacement should use proper locking or an async-safe data store.
"""

from __future__ import annotations

from typing import Optional

from app.identity.models import Participant


class IdentityRepository:
    """
    In-memory store for Participant records.

    Participant records are keyed by participant_id (str / UUID).
    The repository is instantiated once at module import and shared across
    requests via FastAPI dependency injection.
    """

    def __init__(self) -> None:
        # Plain dict is the backing store.  See module docstring for caveats.
        self._store: dict[str, Participant] = {}

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def add(self, participant: Participant) -> None:
        """
        Persist a new Participant record.

        Raises
        ------
        ValueError
            If a participant with the same participant_id already exists.
        """
        if participant.participant_id in self._store:
            raise ValueError(
                f"Participant '{participant.participant_id}' already registered."
            )
        self._store[participant.participant_id] = participant

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get(self, participant_id: str) -> Optional[Participant]:
        """Return the Participant for the given ID, or None if not found."""
        return self._store.get(participant_id)

    def exists(self, participant_id: str) -> bool:
        """Return True if a participant with this ID is already registered."""
        return participant_id in self._store

    def count(self) -> int:
        """Return the total number of registered participants."""
        return len(self._store)


# ---------------------------------------------------------------------------
# Singleton instance
# ---------------------------------------------------------------------------
# A single repository instance is shared across the application.
# This is intentionally simple for the prototype; replace with a proper
# DI container or database session factory in later phases.
identity_repository = IdentityRepository()

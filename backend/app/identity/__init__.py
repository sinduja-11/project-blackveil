"""
Identity package — Phase 2, Task 2.1: Participant Registration and Identity Creation.

Modules
-------
crypto      : Ed25519 key-pair generation helper.
models      : Internal Participant dataclass and ParticipantStatus enum.
repository  : In-memory IdentityRepository (non-persistent prototype storage).
router      : FastAPI router exposing POST /identity/register.
schemas     : Pydantic response schemas (public fields only — no private keys).
"""

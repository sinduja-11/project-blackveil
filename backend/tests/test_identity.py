"""
Tests for Phase 2, Task 2.1 — Participant Registration and Identity Creation.

Coverage
--------
- Successful participant registration (201, correct response shape).
- Unique participant IDs across multiple registrations.
- Ed25519 public key generation (valid base64url, decodable to 32 bytes).
- Duplicate-registration rejection (409 Conflict).
- Private key non-disclosure (not present in response body or JSON keys).
- Existing Phase 1 root (GET /) and health (GET /health) endpoints still work.

Design note
-----------
Each test that calls POST /identity/register uses an isolated, fresh
IdentityRepository injected via FastAPI's dependency_overrides mechanism.
This prevents any shared state between tests, even though the production
singleton is in-memory.
"""

from __future__ import annotations

import base64
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.identity.repository import IdentityRepository
from app.identity.router import get_identity_repository


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_client() -> tuple[TestClient, IdentityRepository]:
    """
    Return a TestClient whose identity repository is a brand-new, empty
    IdentityRepository.  Call this at the start of each test that exercises
    registration so tests do not share state.
    """
    test_repo = IdentityRepository()

    app.dependency_overrides[get_identity_repository] = lambda: test_repo
    client = TestClient(app)
    return client, test_repo


def _teardown():
    """Remove any dependency overrides so other tests see the real app."""
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Phase 1 regression — existing endpoints
# ---------------------------------------------------------------------------

class TestPhase1Endpoints:
    """Existing root and health endpoints must continue to work unchanged."""

    def setup_method(self):
        _teardown()
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Welcome to PROJECT BLACKVEIL",
            "status": "running",
        }

    def test_health_endpoint(self):
        response = self.client.get("/health")

        assert response.status_code == 200

        data = response.json()
        assert data["project"] == "PROJECT BLACKVEIL"
        assert data["status"] == "healthy"
        assert data["environment"] == "development"


# ---------------------------------------------------------------------------
# Successful registration
# ---------------------------------------------------------------------------

class TestSuccessfulRegistration:
    """POST /identity/register happy-path behaviour."""

    def setup_method(self):
        self.client, self.repo = _fresh_client()

    def teardown_method(self):
        _teardown()

    def test_returns_201_created(self):
        response = self.client.post("/identity/register")

        assert response.status_code == 201

    def test_response_contains_participant_id(self):
        response = self.client.post("/identity/register")
        data = response.json()

        assert "participant_id" in data
        assert isinstance(data["participant_id"], str)
        assert len(data["participant_id"]) > 0

    def test_participant_id_is_uuid_format(self):
        """Server should produce a valid UUID4 string."""
        import uuid

        response = self.client.post("/identity/register")
        pid = response.json()["participant_id"]

        # Must parse without raising
        parsed = uuid.UUID(pid)
        assert str(parsed) == pid

    def test_response_contains_public_key(self):
        response = self.client.post("/identity/register")
        data = response.json()

        assert "public_key" in data
        assert isinstance(data["public_key"], str)
        assert len(data["public_key"]) > 0

    def test_response_contains_status_active(self):
        response = self.client.post("/identity/register")
        data = response.json()

        assert data["status"] == "ACTIVE"

    def test_response_contains_created_at(self):
        response = self.client.post("/identity/register")
        data = response.json()

        assert "created_at" in data
        # Must be a parseable ISO datetime string
        from datetime import datetime
        dt = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        assert dt is not None

    def test_participant_stored_in_repository(self):
        response = self.client.post("/identity/register")
        pid = response.json()["participant_id"]

        assert self.repo.exists(pid)
        assert self.repo.count() == 1


# ---------------------------------------------------------------------------
# Public key generation
# ---------------------------------------------------------------------------

class TestPublicKeyGeneration:
    """Validate that the returned public key is a valid Ed25519 public key."""

    def setup_method(self):
        self.client, _ = _fresh_client()

    def teardown_method(self):
        _teardown()

    def test_public_key_is_valid_base64url(self):
        """The public key must be decodable as base64url (no padding)."""
        response = self.client.post("/identity/register")
        pub_key_b64 = response.json()["public_key"]

        # Re-add padding before decoding
        padding = "=" * (-len(pub_key_b64) % 4)
        raw_bytes = base64.urlsafe_b64decode(pub_key_b64 + padding)
        assert isinstance(raw_bytes, bytes)

    def test_public_key_is_32_bytes(self):
        """Ed25519 raw public keys are exactly 32 bytes."""
        response = self.client.post("/identity/register")
        pub_key_b64 = response.json()["public_key"]

        padding = "=" * (-len(pub_key_b64) % 4)
        raw_bytes = base64.urlsafe_b64decode(pub_key_b64 + padding)
        assert len(raw_bytes) == 32

    def test_public_key_loads_as_ed25519(self):
        """The raw bytes must load as a valid Ed25519 public key object."""
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        response = self.client.post("/identity/register")
        pub_key_b64 = response.json()["public_key"]

        padding = "=" * (-len(pub_key_b64) % 4)
        raw_bytes = base64.urlsafe_b64decode(pub_key_b64 + padding)

        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        # Load via from_public_bytes — raises if the bytes are not valid
        pub_key = Ed25519PublicKey.from_public_bytes(raw_bytes)
        assert isinstance(pub_key, Ed25519PublicKey)

    def test_each_registration_produces_unique_public_key(self):
        """Two independent registrations must produce different key pairs."""
        r1 = self.client.post("/identity/register").json()["public_key"]
        r2 = self.client.post("/identity/register").json()["public_key"]

        assert r1 != r2


# ---------------------------------------------------------------------------
# Unique participant IDs
# ---------------------------------------------------------------------------

class TestUniqueParticipantIDs:
    """Every registration must produce a distinct participant_id."""

    def setup_method(self):
        self.client, _ = _fresh_client()

    def teardown_method(self):
        _teardown()

    def test_two_registrations_have_different_ids(self):
        pid1 = self.client.post("/identity/register").json()["participant_id"]
        pid2 = self.client.post("/identity/register").json()["participant_id"]

        assert pid1 != pid2

    def test_ten_registrations_all_unique(self):
        ids = [
            self.client.post("/identity/register").json()["participant_id"]
            for _ in range(10)
        ]
        assert len(set(ids)) == 10


# ---------------------------------------------------------------------------
# Duplicate registration rejection
# ---------------------------------------------------------------------------

class TestDuplicateRegistration:
    """
    Forcing a duplicate participant_id into the repository must trigger 409.

    Because the server generates UUIDs automatically, we cannot cause a
    collision through the HTTP API.  Instead we pre-seed the repository with
    a known participant_id and then patch uuid.uuid4 to return that same ID,
    confirming the router detects and rejects the collision.
    """

    def setup_method(self):
        self.client, self.repo = _fresh_client()

    def teardown_method(self):
        _teardown()

    def test_duplicate_participant_id_returns_409(self, monkeypatch):
        """
        Pre-seed the repo with a known ID, then force uuid4 to return the same
        ID on the next call.  The router must respond with 409 Conflict.
        """
        import uuid as uuid_mod
        from app.identity import router as identity_router_mod
        from app.identity.models import ParticipantStatus
        from app.identity.crypto import generate_ed25519_keypair

        # Register the first participant normally via HTTP so the repo has one entry.
        first_response = self.client.post("/identity/register")
        assert first_response.status_code == 201
        existing_id = first_response.json()["participant_id"]

        # Patch uuid.uuid4 in the router module to always return the same ID.
        monkeypatch.setattr(
            identity_router_mod,
            "uuid",
            type("FakeUUID", (), {"uuid4": staticmethod(lambda: existing_id)})(),
        )

        # Second registration with the same UUID must be rejected.
        second_response = self.client.post("/identity/register")
        assert second_response.status_code == 409
        assert "already exists" in second_response.json()["detail"].lower()

    def test_409_response_has_correct_content_type(self, monkeypatch):
        """The 409 error response must be JSON."""
        import uuid as uuid_mod
        from app.identity import router as identity_router_mod

        first_id = self.client.post("/identity/register").json()["participant_id"]

        monkeypatch.setattr(
            identity_router_mod,
            "uuid",
            type("FakeUUID", (), {"uuid4": staticmethod(lambda: first_id)})(),
        )

        response = self.client.post("/identity/register")
        assert response.status_code == 409
        assert response.headers["content-type"].startswith("application/json")


# ---------------------------------------------------------------------------
# Private key non-disclosure
# ---------------------------------------------------------------------------

class TestPrivateKeyNonDisclosure:
    """The private key must never appear in any registration response."""

    def setup_method(self):
        self.client, _ = _fresh_client()

    def teardown_method(self):
        _teardown()

    def test_private_key_field_absent_from_response(self):
        """Response JSON must not contain a 'private_key' key."""
        response = self.client.post("/identity/register")
        data = response.json()

        assert "private_key" not in data

    def test_no_key_like_field_names_in_response(self):
        """
        Scan all top-level response keys for any name that could indicate
        a private key being disclosed under a different field name.
        """
        response = self.client.post("/identity/register")
        data = response.json()

        suspicious_substrings = ("private", "secret", "priv_key", "sk", "seed")
        for key in data.keys():
            key_lower = key.lower()
            for substring in suspicious_substrings:
                assert substring not in key_lower, (
                    f"Response field '{key}' looks like it could contain "
                    f"a private key (matched substring '{substring}')."
                )

    def test_response_body_text_does_not_contain_private_key_bytes(self):
        """
        The raw response text must not contain any field literally named
        'private_key', 'private key', or similar.
        """
        response = self.client.post("/identity/register")
        body = response.text.lower()

        assert "private_key" not in body
        assert "private key" not in body

    def test_response_has_exactly_expected_fields(self):
        """
        The response schema must contain exactly the four public fields:
        participant_id, public_key, status, created_at — nothing more.
        """
        response = self.client.post("/identity/register")
        data = response.json()

        expected_keys = {"participant_id", "public_key", "status", "created_at"}
        assert set(data.keys()) == expected_keys

    def test_private_key_not_in_repository_repr(self):
        """
        The Participant __repr__ must not expose private key material.
        This guards against accidental logging of the full object.
        """
        from app.identity.crypto import generate_ed25519_keypair
        from app.identity.models import Participant

        priv, pub = generate_ed25519_keypair()
        p = Participant(participant_id="test-id", public_key=pub, _private_key=priv)

        representation = repr(p)
        assert "private" not in representation.lower()
        # The repr should contain the participant_id but not key bytes.
        assert "test-id" in representation

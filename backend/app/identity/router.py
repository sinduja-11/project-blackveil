"""
Identity registration router.

Exposes:
    POST /identity/register  — register a new participant and return its
                               public identity (participant_id, public_key,
                               status, created_at).

Private key material is never included in any response or log entry.
"""

from __future__ import annotations

import base64
import logging
import uuid

from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)
from fastapi import APIRouter, Depends, HTTPException, status

from app.identity.crypto import generate_ed25519_keypair
from app.identity.models import Participant
from app.identity.repository import IdentityRepository, identity_repository
from app.identity.schemas import RegisterResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/identity", tags=["identity"])


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

def get_identity_repository() -> IdentityRepository:
    """
    FastAPI dependency that returns the shared in-memory identity repository.

    Injecting the repository through a dependency makes it straightforward to
    swap in a test-scoped override without modifying production code.
    """
    return identity_repository


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new participant",
    description=(
        "Generates a fresh Ed25519 key pair, assigns a server-generated UUID, "
        "and stores the participant identity. "
        "Returns the participant ID, public key (base64url, no padding), "
        "status and creation timestamp. "
        "The private key is never included in the response."
    ),
)
def register_participant(
    repo: IdentityRepository = Depends(get_identity_repository),
) -> RegisterResponse:
    """
    Register a new participant.

    The server:
    1. Generates a UUID participant_id.
    2. Generates an Ed25519 key pair.
    3. Stores the full identity record (including private key) in the
       in-memory repository.
    4. Returns only the public fields — private key is NOT returned.

    Returns 409 Conflict if a collision occurs on the generated UUID
    (astronomically unlikely but handled defensively).
    """
    participant_id = str(uuid.uuid4())

    # Generate key pair — private key stays inside this function scope and
    # the Participant model only; it is NOT included in the log message below.
    private_key, public_key = generate_ed25519_keypair()

    participant = Participant(
        participant_id=participant_id,
        public_key=public_key,
        _private_key=private_key,
    )

    try:
        repo.add(participant)
    except ValueError:
        # UUID collision — extremely unlikely; handled for correctness.
        logger.error(
            "UUID collision on registration for participant_id=%s",
            participant_id,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A participant with this ID already exists.",
        )

    # Encode the raw 32-byte public key as base64url (no padding).
    raw_public_bytes: bytes = public_key.public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    public_key_b64 = base64.urlsafe_b64encode(raw_public_bytes).rstrip(b"=").decode()

    # Safe log — only the participant_id is recorded, never key material.
    logger.info("Participant registered: participant_id=%s", participant_id)

    return RegisterResponse(
        participant_id=participant.participant_id,
        public_key=public_key_b64,
        status=participant.status,
        created_at=participant.created_at,
    )

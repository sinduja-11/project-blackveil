"""
Pydantic schemas for the identity registration API.

Only public fields are exposed.  The Ed25519 private key is intentionally
absent from every schema defined here.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.identity.models import ParticipantStatus


class RegisterResponse(BaseModel):
    """
    Payload returned after a successful POST /identity/register.

    Fields
    ------
    participant_id : str
        Server-generated UUID that uniquely identifies this participant.
    public_key : str
        Base64url-encoded (no padding) raw Ed25519 public key bytes (32 bytes).
    status : ParticipantStatus
        Lifecycle status at registration time.  Always ACTIVE on first
        registration.
    created_at : datetime
        UTC timestamp of registration.
    """

    participant_id: str = Field(
        description="Server-generated UUID for this participant."
    )
    public_key: str = Field(
        description=(
            "Base64url-encoded (no padding) raw Ed25519 public key (32 bytes)."
        )
    )
    status: ParticipantStatus = Field(
        description="Participant lifecycle status."
    )
    created_at: datetime = Field(
        description="UTC timestamp of when the participant was registered."
    )

    model_config = {"json_schema_extra": {"example": {
        "participant_id": "550e8400-e29b-41d4-a716-446655440000",
        "public_key": "MCowBQYDK2VwAyEA...",
        "status": "ACTIVE",
        "created_at": "2026-01-01T00:00:00Z",
    }}}

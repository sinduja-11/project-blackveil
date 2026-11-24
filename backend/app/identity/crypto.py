"""
Ed25519 key-pair generation helper.

Wraps the cryptography library so that the rest of the identity module has a
single, testable entry point for key-pair creation.

No private key material is ever returned to callers outside this module except
through the opaque Ed25519PrivateKey object; raw bytes are never exposed.
"""

from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def generate_ed25519_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """
    Generate a fresh Ed25519 key pair.

    Returns
    -------
    tuple[Ed25519PrivateKey, Ed25519PublicKey]
        (private_key, public_key) — in that order.
        The private key MUST NOT be passed to any API response schema or logger.
    """
    private_key: Ed25519PrivateKey = Ed25519PrivateKey.generate()
    public_key: Ed25519PublicKey = private_key.public_key()
    return private_key, public_key

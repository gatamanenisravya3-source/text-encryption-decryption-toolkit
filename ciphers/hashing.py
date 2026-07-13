"""
One-way hash functions: MD5, SHA-256, SHA-512.

Hashes are not reversible, so unlike the ciphers in this project there is
no `decrypt`. Instead we expose `hash_text` (returns a hex digest) and
`verify_text` (recomputes the hash and compares it to a given digest,
which is how these pages behave in the original project: you hash a
message, then optionally verify a message against a previously-produced
digest).
"""

import hashlib

_ALGORITHMS = {
    "MD5": hashlib.md5,
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
}


def available_algorithms():
    return list(_ALGORITHMS.keys())


def hash_text(text: str, algorithm: str) -> str:
    if algorithm not in _ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    return _ALGORITHMS[algorithm](text.encode("utf-8")).hexdigest()


def verify_text(text: str, algorithm: str, digest: str) -> bool:
    return hash_text(text, algorithm).lower() == digest.strip().lower()

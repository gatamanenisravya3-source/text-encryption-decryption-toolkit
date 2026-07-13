# Text Encryption and Decryption Toolkit

A Python re-implementation of a college mini-project (VTU Computer Graphics, 2021-2022) that lets a user encrypt and decrypt text using classical and modern ciphers, plus generate one-way hashes. Originally built as a desktop GUI app; this version ships both a Tkinter GUI and a headless CLI/library so the core logic is testable and reusable.

## Algorithms Implemented

**Classical ciphers**
- Caesar Cipher
- Vigenere Cipher
- Playfair Cipher

**Modern ciphers**
- AES-256 (CBC mode, random IV per message)
- Triple DES / 3DES (CBC mode, random IV per message)

**Hash functions** (one-way, with verification)
- MD5
- SHA-256
- SHA-512

## Project Structure

```
text-encryption-toolkit/
  ciphers/
    classical.py   # Caesar, Vigenere, Playfair
    modern.py       # AES-256, Triple DES
    hashing.py      # MD5, SHA-256, SHA-512
  tests/
    test_ciphers.py # unit tests for every algorithm
  gui.py            # Tkinter desktop app (one tab per algorithm)
  cli_demo.py        # headless demo script, prints results for all algorithms
  requirements.txt
```

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the GUI (desktop, requires Tkinter)
```bash
python gui.py
```

### Run the headless CLI demo
```bash
python cli_demo.py
```

### Run the unit tests
```bash
python -m unittest discover -s tests -v
```

## Sample Output

Actual output from running `python cli_demo.py` on message "Meet me at the library at 9pm":

```
============================================================
Caesar Cipher (key=7)
============================================================
Encrypted: Tlla tl ha aol spiyhyf ha 9wt
Decrypted: Meet me at the library at 9pm

============================================================
Vigenere Cipher (key='SECURE')
============================================================
Encrypted: Eign di sx vbv paftuic sx 9rg
Decrypted: Meet me at the library at 9pm

============================================================
Playfair Cipher (key='KEYWORD')
============================================================
Encrypted: NKKUNKRVVFOGQIDBAKRVQN
Decrypted: MEETMEATTHELIBRARYATPM

============================================================
AES-256 (CBC mode, key='super-secret-key')
============================================================
Encrypted (base64): KHwcBVCaMGjq80fNRBFrZctMOMLIOAm5i76toIpNEgB6Gz6kax0eTnIWKVlNm0gn
Decrypted: Meet me at the library at 9pm

============================================================
Triple DES / 3DES (CBC mode, key='super-secret-key')
============================================================
Encrypted (base64): EY71pJUHdSgXHALvONoO0yhkoVSe42eNEFddnDjXMXCQbbMC4DgYGQ==
Decrypted: Meet me at the library at 9pm

============================================================
MD5 Hash
============================================================
Digest: 979a692c50ec239ddc43df415d69511b
Verify against same message: True
Verify against tampered message: False

============================================================
SHA-256 Hash
============================================================
Digest: b2b985f5aff9c88524eb460762171f1f4dc7775af34eb38a2d0d1aacd2ff4903
Verify against same message: True
Verify against tampered message: False

============================================================
SHA-512 Hash
============================================================
Digest: 8693e9944eba4a8bde032dbb17e28c239fbae4f70eea1de558288db54d42653d93a3a29905b84369de437c40aa01a955ec93b73a9bd791d89eb4768b306ea0ad
Verify against same message: True
Verify against tampered message: False

All ciphers/hashes ran successfully and round-tripped correctly.
```

Unit test results (`python -m unittest discover -s tests -v`): **9/9 tests passed** covering round-trip correctness for every cipher, wrong-key failure for AES, and hash verification.

## Tech Stack

- Python 3
- PyCryptoDome (AES, Triple DES)
- hashlib (MD5, SHA-256, SHA-512)
- Tkinter (GUI)

## Notes

- AES and Triple DES both derive a fixed-length key from the user-supplied passphrase via SHA-256/SHA-1 hashing, and prepend a random IV to each ciphertext so the same message never produces the same ciphertext twice.
- Playfair merges I/J into a single grid cell and pads repeated adjacent letters with X, per the classic algorithm rules.
- Hashes are one-way by design; the toolkit supports verifying a message against a previously generated digest rather than "decrypting" it.

import unittest

from ciphers import classical, modern, hashing


class TestCaesar(unittest.TestCase):
    def test_round_trip(self):
        msg = "Attack at dawn!"
        ct = classical.caesar_encrypt(msg, 5)
        self.assertEqual(classical.caesar_decrypt(ct, 5), msg)

    def test_non_alpha_untouched(self):
        self.assertEqual(classical.caesar_encrypt("123!@#", 5), "123!@#")


class TestVigenere(unittest.TestCase):
    def test_round_trip(self):
        msg = "The quick brown fox"
        ct = classical.vigenere_encrypt(msg, "lemon")
        self.assertEqual(classical.vigenere_decrypt(ct, "lemon"), msg)


class TestPlayfair(unittest.TestCase):
    def test_round_trip_letters_only(self):
        # Note: Playfair pads repeated adjacent letters (e.g. "LL") with an
        # "X" and merges I/J into one cell, so this test uses a message
        # with no adjacent duplicates and no "J" to verify a clean round trip.
        msg = "SECURECODEBASE"
        ct = classical.playfair_encrypt(msg, "KEYWORD")
        pt = classical.playfair_decrypt(ct, "KEYWORD")
        self.assertTrue(pt.startswith(msg))


class TestAES(unittest.TestCase):
    def test_round_trip(self):
        msg = "Confidential financial report Q3"
        token = modern.aes_encrypt(msg, "correct-horse-battery-staple")
        self.assertEqual(modern.aes_decrypt(token, "correct-horse-battery-staple"), msg)

    def test_wrong_key_fails(self):
        token = modern.aes_encrypt("secret", "key-one")
        with self.assertRaises(Exception):
            modern.aes_decrypt(token, "key-two")


class TestTripleDES(unittest.TestCase):
    def test_round_trip(self):
        msg = "Launch code 4471"
        token = modern.triple_des_encrypt(msg, "another-key")
        self.assertEqual(modern.triple_des_decrypt(token, "another-key"), msg)


class TestHashing(unittest.TestCase):
    def test_md5_deterministic(self):
        self.assertEqual(hashing.hash_text("hello", "MD5"), hashing.hash_text("hello", "MD5"))

    def test_verify(self):
        digest = hashing.hash_text("hello", "SHA-256")
        self.assertTrue(hashing.verify_text("hello", "SHA-256", digest))
        self.assertFalse(hashing.verify_text("hellO", "SHA-256", digest))


if __name__ == "__main__":
    unittest.main()

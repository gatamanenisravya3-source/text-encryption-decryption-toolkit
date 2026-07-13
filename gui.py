"""
Tkinter GUI for the Text Encryption and Decryption toolkit.

Mirrors the pages described in the original mini-project report: a
starting/home page plus one tab per algorithm (Caesar, Vigenere,
Playfair, AES, Triple DES, MD5, SHA-256, SHA-512). Each tab lets you
type a message, supply a key (where applicable), and encrypt/decrypt
or hash the text.

Run with:  python gui.py
(Requires a desktop environment with Tkinter available; not runnable
in a headless CI/sandbox - use cli_demo.py there instead.)
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ciphers import classical, modern, hashing


class CipherTab(ttk.Frame):
    """Generic encrypt/decrypt tab: text box + key box + two buttons."""

    def __init__(self, parent, title, encrypt_fn, decrypt_fn, key_label="Key"):
        super().__init__(parent, padding=12)
        self.encrypt_fn = encrypt_fn
        self.decrypt_fn = decrypt_fn

        ttk.Label(self, text=title, font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )

        ttk.Label(self, text="Message:").grid(row=1, column=0, sticky="nw")
        self.message = tk.Text(self, height=4, width=50)
        self.message.grid(row=1, column=1, pady=4)

        ttk.Label(self, text=f"{key_label}:").grid(row=2, column=0, sticky="w")
        self.key = ttk.Entry(self, width=30)
        self.key.grid(row=2, column=1, sticky="w", pady=4)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=1, sticky="w", pady=6)
        ttk.Button(btn_frame, text="Encrypt", command=self.do_encrypt).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Decrypt", command=self.do_decrypt).pack(side="left", padx=4)

        ttk.Label(self, text="Result:").grid(row=4, column=0, sticky="nw")
        self.result = tk.Text(self, height=4, width=50)
        self.result.grid(row=4, column=1, pady=4)

    def _run(self, fn):
        text = self.message.get("1.0", "end").strip()
        key = self.key.get().strip()
        try:
            out = fn(text, key) if key else fn(text)
            self.result.delete("1.0", "end")
            self.result.insert("1.0", out)
        except Exception as exc:  # noqa: BLE001 - show any cipher error to the user
            messagebox.showerror("Error", str(exc))

    def do_encrypt(self):
        self._run(self.encrypt_fn)

    def do_decrypt(self):
        self._run(self.decrypt_fn)


class HashTab(ttk.Frame):
    """Tab for one-way hash algorithms (MD5 / SHA-256 / SHA-512)."""

    def __init__(self, parent, algorithm):
        super().__init__(parent, padding=12)
        self.algorithm = algorithm

        ttk.Label(self, text=f"{algorithm} Hash", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )

        ttk.Label(self, text="Message:").grid(row=1, column=0, sticky="nw")
        self.message = tk.Text(self, height=4, width=50)
        self.message.grid(row=1, column=1, pady=4)

        ttk.Button(self, text="Generate Hash", command=self.do_hash).grid(
            row=2, column=1, sticky="w", pady=6
        )

        ttk.Label(self, text="Digest:").grid(row=3, column=0, sticky="nw")
        self.digest = tk.Text(self, height=3, width=50)
        self.digest.grid(row=3, column=1, pady=4)

    def do_hash(self):
        text = self.message.get("1.0", "end").strip()
        digest = hashing.hash_text(text, self.algorithm)
        self.digest.delete("1.0", "end")
        self.digest.insert("1.0", digest)


class StartPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=24)
        ttk.Label(
            self,
            text="Text Encryption and Decryption Toolkit",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            self,
            text=(
                "Choose an algorithm tab above.\n\n"
                "Classical ciphers: Caesar, Vigenere, Playfair\n"
                "Modern ciphers: AES-256, Triple DES\n"
                "Hash functions: MD5, SHA-256, SHA-512"
            ),
            justify="left",
        ).pack(anchor="w", pady=12)


def main():
    root = tk.Tk()
    root.title("Text Encryption and Decryption")
    root.geometry("640x420")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    notebook.add(StartPage(notebook), text="Home")
    notebook.add(
        CipherTab(notebook, "Caesar Cipher", classical.caesar_encrypt, classical.caesar_decrypt, "Shift (integer)"),
        text="Caesar",
    )
    notebook.add(
        CipherTab(notebook, "Vigenere Cipher", classical.vigenere_encrypt, classical.vigenere_decrypt, "Keyword"),
        text="Vigenere",
    )
    notebook.add(
        CipherTab(notebook, "Playfair Cipher", classical.playfair_encrypt, classical.playfair_decrypt, "Keyword"),
        text="Playfair",
    )
    notebook.add(
        CipherTab(notebook, "AES-256 (CBC)", modern.aes_encrypt, modern.aes_decrypt, "Key"),
        text="AES",
    )
    notebook.add(
        CipherTab(notebook, "Triple DES (CBC)", modern.triple_des_encrypt, modern.triple_des_decrypt, "Key"),
        text="Triple DES",
    )
    notebook.add(HashTab(notebook, "MD5"), text="MD5")
    notebook.add(HashTab(notebook, "SHA-256"), text="SHA-256")
    notebook.add(HashTab(notebook, "SHA-512"), text="SHA-512")

    root.mainloop()


if __name__ == "__main__":
    main()

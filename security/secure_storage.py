import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


class SecureStorage:

    def __init__(self, key=None):
        key = key or os.getenv("ZECPATH_ENCRYPTION_KEY")

        if not key:
            raise ValueError(
                "ZECPATH_ENCRYPTION_KEY environment variable is required."
            )

        if isinstance(key, str):
            key = key.encode("utf-8")

        try:
            self.cipher = Fernet(key)
        except (ValueError, TypeError):
            raise ValueError("Invalid Fernet encryption key.")

    def encrypt_data(self, data):
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes.")

        return self.cipher.encrypt(data)

    def decrypt_data(self, encrypted_data):
        if not isinstance(encrypted_data, bytes):
            raise TypeError("Encrypted data must be bytes.")

        try:
            return self.cipher.decrypt(encrypted_data)
        except InvalidToken:
            raise ValueError("Decryption failed: invalid key or corrupted data.")

    def encrypt_file(self, source_path, destination_path):
        source = Path(source_path)
        destination = Path(destination_path)

        if not source.is_file():
            raise FileNotFoundError(source)

        destination.parent.mkdir(parents=True, exist_ok=True)

        encrypted = self.encrypt_data(source.read_bytes())
        destination.write_bytes(encrypted)

        return str(destination)

    def decrypt_file(self, source_path, destination_path):
        source = Path(source_path)
        destination = Path(destination_path)

        if not source.is_file():
            raise FileNotFoundError(source)

        destination.parent.mkdir(parents=True, exist_ok=True)

        decrypted = self.decrypt_data(source.read_bytes())
        destination.write_bytes(decrypted)

        return str(destination)

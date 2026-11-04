import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from cryptography.fernet import Fernet

from security.secure_storage import SecureStorage


def test_encrypt_and_decrypt_data():
    key = Fernet.generate_key()
    storage = SecureStorage(key)

    original = b"Confidential candidate information"
    encrypted = storage.encrypt_data(original)

    assert encrypted != original
    assert storage.decrypt_data(encrypted) == original


def test_invalid_key_is_rejected():
    with pytest.raises(ValueError):
        SecureStorage("invalid-key")


def test_missing_key_is_rejected(monkeypatch):
    monkeypatch.delenv("ZECPATH_ENCRYPTION_KEY", raising=False)

    with pytest.raises(ValueError):
        SecureStorage()


def test_file_encryption_and_decryption(tmp_path):
    storage = SecureStorage(Fernet.generate_key())

    source = tmp_path / "resume.txt"
    encrypted = tmp_path / "resume.enc"
    decrypted = tmp_path / "restored.txt"

    source.write_bytes(b"Candidate resume content")

    storage.encrypt_file(source, encrypted)
    storage.decrypt_file(encrypted, decrypted)

    assert decrypted.read_bytes() == source.read_bytes()
    assert encrypted.read_bytes() != source.read_bytes()


def test_corrupted_data_is_rejected():
    storage = SecureStorage(Fernet.generate_key())

    with pytest.raises(ValueError):
        storage.decrypt_data(b"invalid-encrypted-data")


def test_non_bytes_input_is_rejected():
    storage = SecureStorage(Fernet.generate_key())

    with pytest.raises(TypeError):
        storage.encrypt_data("plain text")

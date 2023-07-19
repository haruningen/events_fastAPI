import json

from cryptography.fernet import Fernet


def decrypt_json(data: str, key: bytes) -> dict:
    f = Fernet(key)
    decrypt_data = f.decrypt(data)
    return json.loads(decrypt_data)

def encrypt_json(data: dict, key: bytes) -> str:
    json_string = json.dumps(data)
    f = Fernet(key)
    return f.encrypt(json_string.encode()).decode()

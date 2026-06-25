import hashlib

from database.db import (
    pengguna_get, pengguna_get_first,
    pengguna_update_akun, pengguna_update_info_toko,
)

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_credentials() -> dict:
    creds = pengguna_get_first()
    if creds is None:
        return {
            "username": "admin", "password": "",
            "nama_toko": "", "nama_pemilik": "",
            "alamat": "", "telepon": "",
        }
    return creds

def verify_login(username: str, password: str) -> bool:
    creds = pengguna_get(username)
    if creds is None:
        return False
    return _hash_password(password) == creds.get("password")

def update_credentials(username: str, password: str) -> None:
    current = load_credentials()
    pengguna_update_akun(current["username"], username, _hash_password(password))

def update_info_toko(nama_toko: str, nama_pemilik: str, alamat: str, telepon: str) -> None:
    current = load_credentials()
    pengguna_update_info_toko(current["username"], nama_toko, nama_pemilik, alamat, telepon)
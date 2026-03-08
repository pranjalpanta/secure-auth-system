import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization
from argon2.low_level import hash_secret_raw, Type, ARGON2_VERSION #Add cryptographic imports for AES-GCM, RSA, hashing, and Argon2

class CryptoEngine:
    """Low-Level Cryptographic Primitives: Argon2id, AES-GCM, RSA-PSS""" #Create CryptoEngine class for low level cryptographic primitives
    
    @staticmethod
    def derive_key_argon2(password: str, salt: bytes) -> bytes:
        return hash_secret_raw(
            secret=password.encode(),
            salt=salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            type=Type.ID,
            version=ARGON2_VERSION
        )

    @staticmethod
    def aes_gcm_encrypt(data: bytes, key: bytes) -> tuple[bytes, bytes]:
        nonce = os.urandom(12)
        ct = AESGCM(key).encrypt(nonce, data, None)
        return nonce, ct 

    @staticmethod
    def aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
        return AESGCM(key).decrypt(nonce, ciphertext, None)

    @staticmethod
    def sign_data(private_key, data: bytes) -> bytes:
        return private_key.sign(
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
    

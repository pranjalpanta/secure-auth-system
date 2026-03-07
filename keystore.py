import json
import os
import base64
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from src.security.crypto_engine import CryptoEngine  #Added the required module imports for JSON OS Base64 X509 certificate handling serialization utilities and the CryptoEngine needed for cryptographic operations.

class SecureKeyStore:
    """Manages the encrypted storage of the user's Private Key."""
    
    def __init__(self, user_email):
        self.filename = f"{user_email.replace('@', '_at_')}.keystore" #Added the SecureKeyStore class to manage encrypted private key storage and initialized a user specific keystore filename based on the email address.

    def save_keys(self, private_key, certificate, password):
        pem_priv = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption() #Added the save_keys method to export the private key in PKCS8 PEM format and prepare it for secure keystore storage alongside the certificate.
        )
        
        salt = os.urandom(16)
        wrapping_key = CryptoEngine.derive_key_argon2(password, salt)
        nonce, ciphertext = CryptoEngine.aes_gcm_encrypt(pem_priv, wrapping_key) #Generated a random salt derived a wrapping key from the password using Argon2 and encrypted the private key with AES GCM for secure storage.

        keystore_data = {
            "salt": base64.b64encode(salt).decode('utf-8'),
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "encrypted_key": base64.b64encode(ciphertext).decode('utf-8'),
            "certificate": base64.b64encode(certificate.public_bytes(serialization.Encoding.PEM)).decode('utf-8') #Created the keystore data structure by encoding the salt nonce encrypted private key and certificate into Base64 strings for safe and consistent file storage.
        }

        with open(self.filename, "w") as f:
            json.dump(keystore_data, f, indent=4) #Wrote the keystore data to a user specific JSON file using json.dump with indentation for structured and readable storage.

    def load_keys(self, password):
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Keystore file not found for this user: {self.filename}") #Added the load_keys method with a file existence check that raises a FileNotFoundError when the user keystore is missing.

        with open(self.filename, "r") as f: data = json.load(f) #Opened the keystore file in read mode and loaded the stored JSON data for further key recovery and processing.

        salt = base64.b64decode(data["salt"])
        nonce = base64.b64decode(data["nonce"])
        ciphertext = base64.b64decode(data["encrypted_key"])
        cert_bytes = base64.b64decode(data["certificate"]) #Decoded the Base64 encoded salt nonce encrypted private key and certificate data from the keystore file to prepare them for decryption and key reconstruction.

        try:
            wrapping_key = CryptoEngine.derive_key_argon2(password, salt)
            pem_priv = CryptoEngine.aes_gcm_decrypt(nonce, ciphertext, wrapping_key) #Derived the wrapping key from the password using Argon2 and attempted to decrypt the encrypted private key with AES GCM inside a protected try block.
            
            private_key = serialization.load_pem_private_key(pem_priv, password=None)
            certificate = x509.load_pem_x509_certificate(cert_bytes)
            
            return private_key, certificate
        except Exception:
            raise PermissionError("Keystore Access Denied: Wrong Password.") 

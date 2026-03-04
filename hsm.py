from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from src.security.keystore import SecureKeyStore
from src.pki.ca import CertificateAuthority
from src.security.crypto_engine import CryptoEngine

class SoftHSM:
    """HSM SIMULATION: Handles secure storage and key operations (Signing/Decryption)."""
    def __init__(self, user_email):
        self._private_key = None
        self.certificate = None
        self.keystore = SecureKeyStore(user_email) 

    def login(self, password):
        try:
            self._private_key, self.certificate = self.keystore.load_keys(password)
            return True
        except Exception:
            return False

    def initialize_new_token(self, password, ca_service):
        self._private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
        public_key = self._private_key.public_key()
        self.certificate = ca_service.issue_cert(public_key)
        
        self.keystore.save_keys(self._private_key, self.certificate, password)

    def sign_challenge(self, challenge: bytes) -> bytes:
        if not self._private_key: raise PermissionError("HSM Locked")
        return CryptoEngine.sign_data(self._private_key, challenge)

    def decrypt_session_key(self, encrypted_key: bytes) -> bytes:
        if not self._private_key: raise PermissionError("HSM Locked")
        return self._private_key.decrypt(
            encrypted_key,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    
    def get_public_key(self):
        return self.certificate.public_key()

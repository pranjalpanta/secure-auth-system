from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from src.security.keystore import SecureKeyStore
from src.pki.ca import CertificateAuthority
from src.security.crypto_engine import CryptoEngine #Added the required cryptographic imports for RSA padding hashing SecureKeyStore certificate authority handling and CryptoEngine to support PKI based key and certificate operations.

class SoftHSM:
    """HSM SIMULATION: Handles secure storage and key operations (Signing/Decryption)."""
    def __init__(self, user_email):
        self._private_key = None
        self.certificate = None
        self.keystore = SecureKeyStore(user_email) #Added the SoftHSM class to simulate secure key storage and cryptographic operations and initialized the private key certificate and SecureKeyStore for each user.

    def login(self, password):
        try:
            self._private_key, self.certificate = self.keystore.load_keys(password)
            return True
        except Exception:
            return False #Loaded the user's private key and certificate from the keystore during login and returned the authentication result based on whether the operation completed successfully.

    def initialize_new_token(self, password, ca_service):
        self._private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048) #Added the initialize_new_token method to generate a new 2048 bit RSA private key as part of setting up a fresh token for the user.
        
        public_key = self._private_key.public_key()
        self.certificate = ca_service.issue_cert(public_key) #Derived the public key from the generated private key and requested a certificate from the CA service to bind the key pair to a signed user identity.
        
        self.keystore.save_keys(self._private_key, self.certificate, password) #Stored the generated private key and issued certificate in the keystore using the provided password for protection.

    def sign_challenge(self, challenge: bytes) -> bytes:
        if not self._private_key: raise PermissionError("HSM Locked")
        return CryptoEngine.sign_data(self._private_key, challenge) #Added the sign_challenge method to prevent signing when the HSM is locked and to securely sign challenge data using the loaded private key.

    def decrypt_session_key(self, encrypted_key: bytes) -> bytes:
        if not self._private_key: raise PermissionError("HSM Locked")
        return self._private_key.decrypt(
            encrypted_key,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None) #Added the decrypt_session_key method to block access when the HSM is locked and to securely decrypt the session key using the private key with RSA OAEP padding and SHA256.
        )
    
    def get_public_key(self):
        return self.certificate.public_key() #Returned the public key from the loaded certificate so it can be used for verification and encryption related operations.

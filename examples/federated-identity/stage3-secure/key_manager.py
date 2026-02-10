"""
Stage 3 - Asymmetric Key Manager
=================================

This is THE fundamental fix that eliminates the shared secret problem.

IMPROVEMENTS over Stage 2:
1. ✅ Asymmetric cryptography (RSA-2048 or ECDSA P-256)
2. ✅ Each service has its own key pair
3. ✅ Private keys NEVER shared
4. ✅ Public keys distributed safely via JWKS
5. ✅ Key rotation without system-wide updates
6. ✅ Compromise of one service ≠ compromise of all

This solves the CATASTROPHIC vulnerability from Stage 1 and 2!
"""

from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
import jwt
import json
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class KeyPair:
    """
    Represents a service's key pair.
    
    SECURITY: Private key must NEVER leave this service.
    """
    service_id: str
    algorithm: str  # "RS256" or "ES256"
    private_key: Any  # RSA or EC private key
    public_key: Any   # RSA or EC public key
    key_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def get_public_jwk(self) -> Dict[str, Any]:
        """
        Export public key as JWK (JSON Web Key).
        
        This can be safely shared with other services.
        """
        if self.algorithm == "RS256":
            # RSA public key to JWK
            public_numbers = self.public_key.public_numbers()
            
            return {
                "kty": "RSA",
                "use": "sig",
                "kid": self.key_id,
                "alg": "RS256",
                "n": self._int_to_base64(public_numbers.n),
                "e": self._int_to_base64(public_numbers.e)
            }
        elif self.algorithm == "ES256":
            # ECDSA public key to JWK
            public_numbers = self.public_key.public_numbers()
            
            return {
                "kty": "EC",
                "use": "sig", 
                "kid": self.key_id,
                "alg": "ES256",
                "crv": "P-256",
                "x": self._int_to_base64(public_numbers.x),
                "y": self._int_to_base64(public_numbers.y)
            }
    
    @staticmethod
    def _int_to_base64(value: int) -> str:
        """Convert integer to base64url encoding (JWK format)."""
        import base64
        # Determine byte length
        byte_length = (value.bit_length() + 7) // 8
        # Convert to bytes
        value_bytes = value.to_bytes(byte_length, byteorder='big')
        # Base64url encode
        return base64.urlsafe_b64encode(value_bytes).rstrip(b'=').decode('utf-8')


class KeyManager:
    """
    Manages asymmetric key pairs for services.
    
    CRITICAL SECURITY IMPROVEMENTS:
    - Each service has its own key pair
    - Private keys never leave the service
    - Public keys shared via JWKS endpoint
    - Key rotation per-service (no system-wide coordination)
    
    This eliminates the symmetric key catastrophe!
    """
    
    def __init__(self, storage_dir: str = "./keys"):
        """Initialize key manager with storage directory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory key storage (production would use HSM/KMS)
        self.key_pairs: Dict[str, KeyPair] = {}
        
        print("🔐 Asymmetric Key Manager initialized")
        print("   ✅ Each service gets its own key pair")
        print("   ✅ Private keys never shared")
        print("   ✅ Public keys distributed via JWKS")
        print()
    
    def generate_key_pair(
        self,
        service_id: str,
        algorithm: str = "RS256"
    ) -> KeyPair:
        """
        Generate a new key pair for a service.
        
        IMPROVEMENT: Each service has unique keys!
        
        Args:
            service_id: Unique identifier for the service
            algorithm: "RS256" (RSA) or "ES256" (ECDSA)
            
        Returns:
            KeyPair object
        """
        print(f"\n🔑 Generating key pair for {service_id}")
        print(f"   Algorithm: {algorithm}")
        
        if algorithm == "RS256":
            # RSA 2048-bit key (good balance of security and performance)
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            
        elif algorithm == "ES256":
            # ECDSA P-256 curve (faster, smaller keys, same security as RSA-3072)
            private_key = ec.generate_private_key(
                ec.SECP256R1(),  # P-256 curve
                backend=default_backend()
            )
            public_key = private_key.public_key()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        key_pair = KeyPair(
            service_id=service_id,
            algorithm=algorithm,
            private_key=private_key,
            public_key=public_key
        )
        
        self.key_pairs[service_id] = key_pair
        
        print(f"   ✅ Key pair generated")
        print(f"   Key ID: {key_pair.key_id}")
        print()
        
        return key_pair
    
    def get_key_pair(self, service_id: str) -> Optional[KeyPair]:
        """
        Get key pair for a service.
        
        Returns None if service doesn't have keys yet.
        """
        return self.key_pairs.get(service_id)
    
    def get_jwks(self, service_ids: Optional[list] = None) -> Dict[str, Any]:
        """
        Get JWKS (JSON Web Key Set) for distribution.
        
        IMPROVEMENT: Public keys can be safely shared!
        This is what other services use to validate tokens.
        
        Args:
            service_ids: List of services to include, or None for all
            
        Returns:
            JWKS document
        """
        if service_ids is None:
            service_ids = list(self.key_pairs.keys())
        
        keys = []
        for service_id in service_ids:
            key_pair = self.key_pairs.get(service_id)
            if key_pair:
                jwk = key_pair.get_public_jwk()
                jwk["service_id"] = service_id
                keys.append(jwk)
        
        return {"keys": keys}
    
    def save_key_pair(self, service_id: str):
        """
        Save key pair to disk (PEM format).
        
        SECURITY: In production, use HSM/KMS instead of filesystem!
        """
        key_pair = self.key_pairs.get(service_id)
        if not key_pair:
            raise ValueError(f"No key pair for {service_id}")
        
        service_dir = self.storage_dir / service_id
        service_dir.mkdir(parents=True, exist_ok=True)
        
        # Save private key (NEVER share this!)
        private_pem = key_pair.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        private_path = service_dir / "private_key.pem"
        private_path.write_bytes(private_pem)
        private_path.chmod(0o600)  # Only owner can read
        
        # Save public key (safe to share)
        public_pem = key_pair.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        public_path = service_dir / "public_key.pem"
        public_path.write_bytes(public_pem)
        
        # Save metadata
        metadata = {
            "service_id": service_id,
            "algorithm": key_pair.algorithm,
            "key_id": key_pair.key_id,
            "created_at": key_pair.created_at.isoformat()
        }
        
        metadata_path = service_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))
        
        print(f"💾 Saved key pair for {service_id}")
        print(f"   Private key: {private_path} (⚠️  NEVER SHARE)")
        print(f"   Public key: {public_path} (✅ Safe to share)")
        print()


def demo_key_generation():
    """Demonstrate asymmetric key generation."""
    print("\n" + "="*70)
    print("STAGE 3: ASYMMETRIC KEY MANAGEMENT DEMONSTRATION")
    print("="*70 + "\n")
    
    km = KeyManager()
    
    # Generate keys for each service
    print("1️⃣  Generating keys for each service...")
    print()
    
    services = [
        ("Agent A (University)", "RS256"),
        ("Agent B (Consortium)", "RS256"),
        ("Agent C (Pharma)", "ES256"),  # Using ECDSA for variety
    ]
    
    for service_id, algorithm in services:
        km.generate_key_pair(service_id, algorithm)
    
    # Show JWKS (public keys)
    print("2️⃣  Public keys (JWKS format)...")
    print()
    jwks = km.get_jwks()
    print(json.dumps(jwks, indent=2))
    print()
    
    # Compare to Stage 2
    print("="*70)
    print("COMPARISON TO STAGE 2")
    print("="*70)
    print()
    print("Stage 2 (Symmetric):")
    print("  🔴 SECRET_KEY = 'shared-secret-456'")
    print("  🔴 Same secret everywhere")
    print("  🔴 Compromise one service = compromise all")
    print("  🔴 Cannot rotate without system-wide update")
    print()
    print("Stage 3 (Asymmetric):")
    print("  ✅ Each service has unique key pair")
    print("  ✅ Private keys never leave service")
    print("  ✅ Public keys safely distributed")
    print("  ✅ Compromise one service ≠ compromise all")
    print("  ✅ Per-service key rotation")
    print()
    
    # Show the fundamental difference
    print("="*70)
    print("THE FUNDAMENTAL DIFFERENCE")
    print("="*70)
    print()
    print("Symmetric (Stage 2):")
    print("  • Sign with: shared secret")
    print("  • Verify with: same shared secret")
    print("  • Problem: Anyone with secret can forge tokens")
    print()
    print("Asymmetric (Stage 3):")
    print("  • Sign with: private key (kept secret)")
    print("  • Verify with: public key (shared openly)")
    print("  • Security: Cannot forge without private key")
    print()
    
    # Security impact
    print("="*70)
    print("SECURITY IMPACT")
    print("="*70)
    print()
    print("Attacker compromises Agent C's keys:")
    print()
    print("Stage 2 Impact (Symmetric):")
    print("  🔴 CATASTROPHIC")
    print("  🔴 Can forge tokens for ANY service")
    print("  🔴 Can impersonate ANY user")
    print("  🔴 Entire system compromised")
    print("  🔴 Remediation: Replace secret EVERYWHERE ($5-10M)")
    print()
    print("Stage 3 Impact (Asymmetric):")
    print("  ⚠️  LIMITED")
    print("  ✅ Can only forge tokens claiming to be from Agent C")
    print("  ✅ Cannot forge tokens from Agent A or B")
    print("  ✅ Other services unaffected")
    print("  ✅ Remediation: Rotate Agent C's keys only (~$10K)")
    print()
    
    print("="*70)
    print("KEY TAKEAWAY")
    print("="*70)
    print()
    print("Asymmetric cryptography is NOT optional for federated systems.")
    print("It's the ONLY way to avoid catastrophic shared secret problems.")
    print()
    print("This is the foundation. Everything else builds on this.")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_key_generation()
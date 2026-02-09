"""
Stage 1 - Insecure Token Generator
===================================

WARNING: This is intentionally insecure! DO NOT use in production!

Vulnerabilities:
1. Weak secret key (hardcoded, short)
2. No audience restriction
3. No scope restriction  
4. Long expiration times (24 hours)
5. No nonce/jti for replay protection
6. Symmetric key algorithm (HS256)
7. No key rotation
8. No token binding
"""

import jwt
import datetime
from typing import Dict, Any, Optional


class InsecureTokenGenerator:
    """
    Intentionally insecure token generator for educational purposes.
    
    All vulnerabilities are CRITICAL and must be fixed in later stages.
    """
    
    # VULNERABILITY 1: Hardcoded, weak secret
    SECRET_KEY = "weak-secret-123"
    
    # VULNERABILITY 2: Symmetric algorithm (shared secret problem)
    ALGORITHM = "HS256"
    
    def __init__(self):
        """Initialize the insecure token generator."""
        print("⚠️  WARNING: Using insecure token generator!")
        print("   Secret: Hardcoded and weak")
        print("   Algorithm: Symmetric (HS256)")
        print("   Expiration: 24 hours")
        print()
    
    def generate_token(
        self,
        user_id: str,
        organization: str,
        scopes: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an insecure JWT token.
        
        VULNERABILITIES:
        - No audience restriction (can be used anywhere)
        - No scope limitation
        - 24-hour expiration (way too long)
        - No nonce/jti (replay attacks possible)
        - No binding to specific agent
        
        Args:
            user_id: User identifier
            organization: User's organization
            scopes: List of scopes (default: wildcard "*")
            metadata: Additional metadata
            
        Returns:
            JWT token string
        """
        if scopes is None:
            # VULNERABILITY 3: Wildcard scope by default
            scopes = ["*"]
        
        if metadata is None:
            metadata = {}
        
        # VULNERABILITY 4: 24-hour expiration
        expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        
        payload = {
            "sub": user_id,
            "org": organization,
            "scope": scopes,
            # VULNERABILITY 5: No audience restriction
            # Should have: "aud": "specific-service"
            # VULNERABILITY 6: No nonce/jti
            # Should have: "jti": unique_id
            "iat": datetime.datetime.now(datetime.UTC),
            "exp": expiration,
            **metadata
        }
        
        # VULNERABILITY 7: Using shared secret
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        
        print(f"✅ Generated token for {user_id} @ {organization}")
        print(f"   Scopes: {scopes}")
        print(f"   Expires: {expiration}")
        print(f"   Token length: {len(token)} chars")
        print()
        
        return token
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate a token (minimal validation).
        
        VULNERABILITIES:
        - No audience validation
        - No scope validation
        - No issuer validation
        - No token binding validation
        - Accepts any token signed with the secret
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid
        """
        try:
            # VULNERABILITY 8: Minimal validation
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM],
                # No audience verification
                # No issuer verification
            )
            
            print(f"✅ Token validated for {payload.get('sub')}")
            return payload
            
        except jwt.ExpiredSignatureError:
            print("❌ Token expired")
            raise
        except jwt.InvalidTokenError as e:
            print(f"❌ Token invalid: {e}")
            raise
    
    def forward_token(self, token: str, to_service: str) -> str:
        """
        Naive token forwarding - just returns the same token!
        
        CRITICAL VULNERABILITY: This is the core problem!
        The same token is reused across trust boundaries.
        
        Args:
            token: Original token
            to_service: Service we're forwarding to (IGNORED!)
            
        Returns:
            Same token (unchanged)
        """
        print(f"⚠️  INSECURE: Forwarding token to {to_service}")
        print("   Using SAME token (no exchange, no transformation)")
        print()
        
        # VULNERABILITY 9: Direct forwarding without exchange
        return token


def demo_token_generation():
    """Demonstrate insecure token generation."""
    print("=" * 70)
    print("STAGE 1: INSECURE TOKEN GENERATION DEMO")
    print("=" * 70)
    print()
    
    generator = InsecureTokenGenerator()
    
    # Generate a token for a medical researcher
    print("1️⃣  Generating initial token for researcher...")
    token = generator.generate_token(
        user_id="dr.smith@university.edu",
        organization="University Hospital",
        scopes=["research:read", "research:write", "admin:users"],
        metadata={"role": "Senior Researcher"}
    )
    
    print("Token preview:")
    print(f"   {token[:50]}...")
    print()
    
    # Validate the token
    print("2️⃣  Validating token...")
    payload = generator.validate_token(token)
    print(f"   User: {payload['sub']}")
    print(f"   Organization: {payload['org']}")
    print(f"   Scopes: {payload['scope']}")
    print()
    
    # Forward the token (insecurely)
    print("3️⃣  Forwarding token to Agent B...")
    forwarded_token = generator.forward_token(token, "Agent B (Consortium)")
    print(f"   Same token? {token == forwarded_token}")
    print()
    
    # Forward again to Agent C
    print("4️⃣  Forwarding token to Agent C...")
    forwarded_token_2 = generator.forward_token(forwarded_token, "Agent C (Pharma)")
    print(f"   Same token? {token == forwarded_token_2}")
    print()
    
    print("=" * 70)
    print("RESULT: Token unchanged after 2 hops!")
    print("Agent C can now impersonate the user ANYWHERE!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo_token_generation()

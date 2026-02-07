"""
Stage 2 - Token Exchange Service (Improved but Still Vulnerable)
================================================================

IMPROVEMENTS over Stage 1:
1. ✅ Token exchange instead of direct forwarding
2. ✅ Audience restriction implemented
3. ✅ Scope validation and downscoping
4. ✅ Shorter token expiration (1 hour -> 15 minutes)
5. ✅ Token lineage tracking

REMAINING VULNERABILITIES:
1. ⚠️ Symmetric keys (HMAC-SHA256) - shared secret problem
2. ⚠️ No proof-of-possession - still bearer tokens
3. ⚠️ No nonce/jti - replay attacks still possible
4. ⚠️ Weak key rotation - manual, infrequent
5. ⚠️ No token revocation mechanism
6. ⚠️ Audience validation not always enforced
7. ⚠️ Logs not cryptographically secured

This is BETTER than Stage 1, but still NOT production-ready!
"""

import jwt
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class TokenExchangeRequest:
    """
    Request for token exchange.
    
    IMPROVEMENT: Structured request with validation.
    REMAINING ISSUE: No proof-of-possession required.
    """
    subject_token: str  # Original token
    subject_token_type: str = "access_token"
    requested_token_type: str = "access_token"
    audience: str = ""  # Target service
    scope: Optional[List[str]] = None
    actor_token: Optional[str] = None  # Token of requesting agent (not used yet)
    correlation_id: Optional[str] = None


@dataclass
class TokenExchangeResponse:
    """
    Response from token exchange.
    
    IMPROVEMENT: Includes token lineage.
    """
    access_token: str
    issued_token_type: str
    token_type: str
    expires_in: int
    scope: List[str]
    lineage: List[str] = field(default_factory=list)  # NEW: Track token chain


class TokenExchangeService:
    """
    Token exchange service implementing basic OAuth 2.0 Token Exchange.
    
    IMPROVEMENTS:
    - Actual token exchange (not just forwarding)
    - Audience restriction
    - Scope downscoping
    - Token lineage tracking
    
    REMAINING VULNERABILITIES:
    - Symmetric keys (shared secret across all services)
    - No proof-of-possession
    - No replay protection
    """
    
    # VULNERABILITY: Still using symmetric key
    # In Stage 3, we'll use asymmetric keys
    SECRET_KEY = "improved-but-still-shared-secret-456"
    ALGORITHM = "HS256"  # Still symmetric!
    
    # IMPROVEMENT: Shorter token expiration
    DEFAULT_EXPIRATION_MINUTES = 15  # Down from 24 hours!
    
    def __init__(self):
        """Initialize the token exchange service."""
        print("🔄 Token Exchange Service initialized")
        print("   ⚠️  WARNING: Still using symmetric keys (HS256)")
        print("   ✅ IMPROVEMENT: Token exchange instead of forwarding")
        print("   ✅ IMPROVEMENT: Audience restriction enabled")
        print("   ✅ IMPROVEMENT: Scope downscoping enabled")
        print()
    
    def exchange_token(self, request: TokenExchangeRequest) -> TokenExchangeResponse:
        """
        Exchange a token for a new token with restricted scope/audience.
        
        IMPROVEMENTS:
        - Validates subject token
        - Restricts audience
        - Downscopres permissions
        - Tracks lineage
        
        REMAINING ISSUES:
        - No proof-of-possession check
        - No replay protection
        - Symmetric key signing
        
        Args:
            request: Token exchange request
            
        Returns:
            TokenExchangeResponse with new token
            
        Raises:
            ValueError: If validation fails
        """
        print(f"\n{'='*70}")
        print(f"TOKEN EXCHANGE REQUEST")
        print(f"{'='*70}")
        
        # IMPROVEMENT: Generate correlation ID if not provided
        correlation_id = request.correlation_id or str(uuid.uuid4())
        print(f"Correlation ID: {correlation_id}")
        
        # Step 1: Validate subject token
        print("\n1️⃣  Validating subject token...")
        try:
            subject_payload = self._validate_subject_token(request.subject_token)
            print(f"   ✅ Subject token valid")
            print(f"   User: {subject_payload.get('sub')}")
            print(f"   Original scopes: {subject_payload.get('scope')}")
        except Exception as e:
            print(f"   ❌ Subject token invalid: {e}")
            raise ValueError(f"Invalid subject token: {e}")
        
        # Step 2: Validate audience
        print(f"\n2️⃣  Validating audience...")
        if not request.audience:
            # VULNERABILITY: Audience is optional (should be required!)
            print(f"   ⚠️  WARNING: No audience specified (not enforced)")
            audience = "any"
        else:
            # IMPROVEMENT: Audience validation
            if self._is_valid_audience(request.audience):
                print(f"   ✅ Audience valid: {request.audience}")
                audience = request.audience
            else:
                print(f"   ❌ Invalid audience: {request.audience}")
                raise ValueError(f"Invalid audience: {request.audience}")
        
        # Step 3: Downscope permissions
        print(f"\n3️⃣  Downscoping permissions...")
        original_scopes = subject_payload.get('scope', [])
        requested_scopes = request.scope or original_scopes
        
        # IMPROVEMENT: Automatic scope downscoping
        downscoped_scopes = self._downscope(
            original_scopes,
            requested_scopes,
            audience
        )
        
        print(f"   Original: {original_scopes}")
        print(f"   Requested: {requested_scopes}")
        print(f"   ✅ Granted: {downscoped_scopes}")
        
        # Step 4: Build token lineage
        print(f"\n4️⃣  Building token lineage...")
        previous_lineage = subject_payload.get('lineage', [])
        new_lineage = previous_lineage + [subject_payload.get('sub', 'unknown')]
        print(f"   Token chain: {' → '.join(new_lineage)}")
        
        # Step 5: Create new token
        print(f"\n5️⃣  Creating new token...")
        new_token = self._create_token(
            subject=subject_payload.get('sub'),
            organization=subject_payload.get('org'),
            audience=audience,
            scopes=downscoped_scopes,
            lineage=new_lineage,
            correlation_id=correlation_id
        )
        
        print(f"   ✅ New token created")
        print(f"   Audience: {audience}")
        print(f"   Scopes: {downscoped_scopes}")
        print(f"   Expires in: {self.DEFAULT_EXPIRATION_MINUTES} minutes")
        print(f"{'='*70}\n")
        
        return TokenExchangeResponse(
            access_token=new_token,
            issued_token_type="urn:ietf:params:oauth:token-type:access_token",
            token_type="Bearer",  # VULNERABILITY: Still bearer token!
            expires_in=self.DEFAULT_EXPIRATION_MINUTES * 60,
            scope=downscoped_scopes,
            lineage=new_lineage
        )
    
    def _validate_subject_token(self, token: str) -> Dict[str, Any]:
        """
        Validate the subject token.
        
        IMPROVEMENT: More thorough validation than Stage 1.
        REMAINING ISSUE: No replay protection, no revocation check.
        """
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
            
            # IMPROVEMENT: Check token hasn't expired
            if 'exp' in payload:
                exp = datetime.fromtimestamp(payload['exp'])
                if exp < datetime.utcnow():
                    raise ValueError("Token expired")
            
            # VULNERABILITY: No nonce/jti check (replay attacks possible)
            # VULNERABILITY: No revocation check (can't invalidate compromised tokens)
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")
    
    def _is_valid_audience(self, audience: str) -> bool:
        """
        Check if audience is valid.
        
        IMPROVEMENT: Validates audience against known services.
        REMAINING ISSUE: Hardcoded list, not dynamic.
        """
        # IMPROVEMENT: Whitelist of valid audiences
        valid_audiences = [
            "Agent A (University)",
            "Agent B (Consortium)",
            "Agent C (Pharma)",
            "Data Services",
            "any"  # VULNERABILITY: Still allows wildcard!
        ]
        
        return audience in valid_audiences
    
    def _downscope(
        self,
        original_scopes: List[str],
        requested_scopes: List[str],
        audience: str
    ) -> List[str]:
        """
        Downscope permissions to minimum necessary.
        
        IMPROVEMENT: Automatic scope reduction.
        REMAINING ISSUE: Logic is simplistic, not policy-driven.
        """
        # IMPROVEMENT: Never grant more than original token had
        allowed_scopes = []
        
        for requested in requested_scopes:
            # Check if requested scope was in original token
            if requested in original_scopes or "*" in original_scopes:
                # IMPROVEMENT: Remove admin scopes for external services
                if audience in ["Agent C (Pharma)", "any"]:
                    if not requested.startswith("admin:"):
                        allowed_scopes.append(requested)
                else:
                    allowed_scopes.append(requested)
        
        # IMPROVEMENT: Replace wildcards with specific permissions
        if "*" in allowed_scopes:
            # Still too permissive, but better than wildcard
            allowed_scopes = ["research:read", "research:write", "data:read"]
        
        return allowed_scopes or ["read"]  # Minimum scope
    
    def _create_token(
        self,
        subject: str,
        organization: str,
        audience: str,
        scopes: List[str],
        lineage: List[str],
        correlation_id: str
    ) -> str:
        """
        Create a new JWT token.
        
        IMPROVEMENTS:
        - Audience restriction
        - Token lineage
        - Correlation ID
        - Shorter expiration
        
        REMAINING ISSUES:
        - Symmetric key signing
        - No nonce/jti
        - No proof-of-possession binding
        """
        now = datetime.utcnow()
        expiration = now + timedelta(minutes=self.DEFAULT_EXPIRATION_MINUTES)
        
        payload = {
            "sub": subject,
            "org": organization,
            "aud": audience,  # IMPROVEMENT: Audience specified!
            "scope": scopes,
            "lineage": lineage,  # IMPROVEMENT: Token chain tracked
            "correlation_id": correlation_id,  # IMPROVEMENT: Traceability
            "iat": now,
            "exp": expiration,
            # VULNERABILITY: No jti (nonce) for replay protection
            # VULNERABILITY: No cnf (confirmation) for proof-of-possession
        }
        
        # VULNERABILITY: Still using symmetric key
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        
        return token
    
    def validate_token(self, token: str, expected_audience: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a token and optionally check audience.
        
        IMPROVEMENT: Audience validation.
        REMAINING ISSUE: Audience check is optional (should be required).
        """
        try:
            payload = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
            
            # IMPROVEMENT: Validate audience if provided
            if expected_audience:
                token_audience = payload.get('aud')
                if token_audience != expected_audience and token_audience != 'any':
                    raise ValueError(
                        f"Audience mismatch: expected {expected_audience}, "
                        f"got {token_audience}"
                    )
            else:
                # VULNERABILITY: Audience validation is optional!
                print("   ⚠️  WARNING: Audience not validated")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")


def demo_token_exchange():
    """Demonstrate the improved token exchange."""
    print("\n" + "="*70)
    print("STAGE 2: TOKEN EXCHANGE DEMONSTRATION")
    print("="*70 + "\n")
    
    service = TokenExchangeService()
    
    # Create initial token (simulating Stage 1 style token)
    print("1️⃣  Creating initial token (Stage 1 style)...")
    initial_payload = {
        "sub": "dr.williams@university.edu",
        "org": "University Hospital",
        "scope": ["research:read", "research:write", "admin:projects"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    initial_token = jwt.encode(
        initial_payload,
        service.SECRET_KEY,
        algorithm=service.ALGORITHM
    )
    
    print(f"   Initial token created for: {initial_payload['sub']}")
    print(f"   Scopes: {initial_payload['scope']}")
    print()
    
    # Exchange for Agent B
    print("2️⃣  Exchanging token for Agent B...")
    request_b = TokenExchangeRequest(
        subject_token=initial_token,
        audience="Agent B (Consortium)",
        scope=["research:read", "research:write"]
    )
    
    response_b = service.exchange_token(request_b)
    print(f"Token for Agent B:")
    print(f"   Audience: Agent B (Consortium)")
    print(f"   Scopes: {response_b.scope}")
    print(f"   Lineage: {' → '.join(response_b.lineage)}")
    print()
    
    # Exchange for Agent C (further downscoped)
    print("3️⃣  Exchanging token for Agent C...")
    request_c = TokenExchangeRequest(
        subject_token=response_b.access_token,
        audience="Agent C (Pharma)",
        scope=["research:read"]  # Only read access
    )
    
    response_c = service.exchange_token(request_c)
    print(f"Token for Agent C:")
    print(f"   Audience: Agent C (Pharma)")
    print(f"   Scopes: {response_c.scope}")
    print(f"   Lineage: {' → '.join(response_c.lineage)}")
    print()
    
    print("="*70)
    print("IMPROVEMENTS DEMONSTRATED:")
    print("="*70)
    print("✅ Token exchange (not forwarding)")
    print("✅ Audience restriction")
    print("✅ Automatic scope downscoping")
    print("✅ Token lineage tracking")
    print("✅ Shorter expiration (15 min vs 24 hours)")
    print()
    print("REMAINING VULNERABILITIES:")
    print("="*70)
    print("⚠️  Symmetric keys (shared secret problem)")
    print("⚠️  No proof-of-possession (bearer tokens)")
    print("⚠️  No replay protection (no nonce/jti)")
    print("⚠️  Audience validation optional")
    print("⚠️  No token revocation")
    print()
    print("Stage 3 will fix these! →")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_token_exchange()

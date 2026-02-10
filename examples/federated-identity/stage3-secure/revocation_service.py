"""
Stage 3 - Token Revocation Service
===================================

This adds the ability to invalidate compromised tokens.

IMPROVEMENTS over Stage 2:
1. ✅ Token revocation lists (in-memory and persistent)
2. ✅ Real-time revocation checking
3. ✅ Revocation by token ID (jti)
4. ✅ Revocation by user
5. ✅ Automatic cleanup of expired revocations

This enables immediate response to security incidents!
"""

import json
import secrets
from datetime import datetime, timezone, timedelta
from typing import Dict, Set, Optional, List
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RevocationEntry:
    """
    Entry in the revocation list.
    
    IMPROVEMENT: Can revoke tokens immediately vs waiting for expiration.
    """
    jti: str  # Token ID being revoked
    revoked_at: datetime
    reason: str
    revoked_by: str
    expires_at: datetime  # When this revocation entry can be removed
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if revocation entry has expired (token would have expired anyway)."""
        return datetime.now(timezone.utc) > self.expires_at
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "jti": self.jti,
            "revoked_at": self.revoked_at.isoformat(),
            "reason": self.reason,
            "revoked_by": self.revoked_by,
            "expires_at": self.expires_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RevocationEntry':
        """Create from dictionary."""
        return cls(
            jti=data["jti"],
            revoked_at=datetime.fromisoformat(data["revoked_at"]),
            reason=data["reason"],
            revoked_by=data["revoked_by"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            metadata=data.get("metadata", {})
        )


class RevocationService:
    """
    Token revocation service.
    
    CRITICAL SECURITY IMPROVEMENT:
    - Can immediately invalidate compromised tokens
    - Real-time revocation checks
    - No need to wait for token expiration
    
    This is essential for security incident response!
    """
    
    def __init__(self, storage_file: str = "revocations.json"):
        """
        Initialize revocation service.
        
        Args:
            storage_file: Path to persistent revocation storage
        """
        self.storage_file = Path(storage_file)
        
        # In-memory revocation list (fast lookup)
        self.revoked_jtis: Set[str] = set()
        
        # Full revocation entries (for audit)
        self.revocations: Dict[str, RevocationEntry] = {}
        
        # Load existing revocations
        self._load_revocations()
        
        print("🚫 Token Revocation Service initialized")
        print("   ✅ Real-time revocation checking")
        print("   ✅ Immediate security response")
        print("   ✅ Persistent revocation storage")
        print()
    
    def _load_revocations(self):
        """Load revocations from persistent storage."""
        if not self.storage_file.exists():
            return
        
        try:
            data = json.loads(self.storage_file.read_text())
            for entry_data in data:
                entry = RevocationEntry.from_dict(entry_data)
                if not entry.is_expired():
                    self.revocations[entry.jti] = entry
                    self.revoked_jtis.add(entry.jti)
            
            print(f"   Loaded {len(self.revocations)} active revocations")
        except Exception as e:
            print(f"   ⚠️  Failed to load revocations: {e}")
    
    def _save_revocations(self):
        """Save revocations to persistent storage."""
        data = [entry.to_dict() for entry in self.revocations.values()]
        self.storage_file.write_text(json.dumps(data, indent=2))
    
    def revoke_token(
        self,
        jti: str,
        reason: str,
        revoked_by: str,
        token_expiration: datetime,
        metadata: Optional[Dict[str, str]] = None
    ) -> RevocationEntry:
        """
        Revoke a token.
        
        IMPROVEMENT: Immediate invalidation vs waiting for expiration.
        
        Args:
            jti: Token ID to revoke
            reason: Why token is being revoked
            revoked_by: Who revoked it
            token_expiration: When the token would naturally expire
            metadata: Additional context
            
        Returns:
            RevocationEntry
        """
        if jti in self.revoked_jtis:
            # Already revoked
            return self.revocations[jti]
        
        entry = RevocationEntry(
            jti=jti,
            revoked_at=datetime.now(timezone.utc),
            reason=reason,
            revoked_by=revoked_by,
            expires_at=token_expiration,  # Can clean up after token would expire
            metadata=metadata or {}
        )
        
        self.revocations[jti] = entry
        self.revoked_jtis.add(jti)
        self._save_revocations()
        
        print(f"🚫 Token revoked: {jti}")
        print(f"   Reason: {reason}")
        print(f"   By: {revoked_by}")
        print()
        
        return entry
    
    def is_revoked(self, jti: str) -> bool:
        """
        Check if a token is revoked.
        
        IMPROVEMENT: Real-time check vs no checking at all.
        
        Args:
            jti: Token ID to check
            
        Returns:
            True if revoked, False otherwise
        """
        return jti in self.revoked_jtis
    
    def get_revocation(self, jti: str) -> Optional[RevocationEntry]:
        """
        Get revocation details.
        
        Args:
            jti: Token ID
            
        Returns:
            RevocationEntry if revoked, None otherwise
        """
        return self.revocations.get(jti)
    
    def cleanup_expired(self) -> int:
        """
        Remove expired revocation entries.
        
        Tokens that have expired don't need to be in revocation list anymore.
        
        Returns:
            Number of entries removed
        """
        expired = [
            jti for jti, entry in self.revocations.items()
            if entry.is_expired()
        ]
        
        for jti in expired:
            del self.revocations[jti]
            self.revoked_jtis.discard(jti)
        
        if expired:
            self._save_revocations()
            print(f"🧹 Cleaned up {len(expired)} expired revocation entries")
        
        return len(expired)
    
    def revoke_all_for_user(
        self,
        user_id: str,
        active_token_jtis: List[str],
        token_expirations: Dict[str, datetime],
        reason: str,
        revoked_by: str
    ) -> int:
        """
        Revoke all tokens for a user.
        
        IMPROVEMENT: Can respond to user compromise by revoking all tokens.
        
        Args:
            user_id: User whose tokens to revoke
            active_token_jtis: List of active token IDs for this user
            token_expirations: Mapping of jti -> expiration datetime
            reason: Why all tokens are being revoked
            revoked_by: Who initiated the revocation
            
        Returns:
            Number of tokens revoked
        """
        count = 0
        
        for jti in active_token_jtis:
            expiration = token_expirations.get(jti, datetime.now(timezone.utc) + timedelta(hours=1))
            self.revoke_token(
                jti=jti,
                reason=f"{reason} (user: {user_id})",
                revoked_by=revoked_by,
                token_expiration=expiration,
                metadata={"user_id": user_id}
            )
            count += 1
        
        return count
    
    def get_stats(self) -> Dict[str, int]:
        """Get revocation statistics."""
        return {
            "total_revocations": len(self.revocations),
            "active_revocations": len([
                e for e in self.revocations.values()
                if not e.is_expired()
            ])
        }


def demo_revocation():
    """Demonstrate token revocation."""
    print("\n" + "="*70)
    print("STAGE 3: TOKEN REVOCATION DEMONSTRATION")
    print("="*70 + "\n")
    
    service = RevocationService("demo_revocations.json")
    
    # Simulate creating tokens
    print("1️⃣  Simulating token creation...")
    token_jti = secrets.token_urlsafe(16)
    token_expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    print(f"   Token created: {token_jti}")
    print(f"   Expires: {token_expiration.isoformat()}")
    print()
    
    # Check if revoked (not yet)
    print("2️⃣  Checking revocation status...")
    if service.is_revoked(token_jti):
        print(f"   ⚠️  Token is revoked")
    else:
        print(f"   ✅ Token is valid (not revoked)")
    print()
    
    # Security incident - revoke token
    print("3️⃣  Security incident detected!")
    print("   Revoking token...")
    print()
    
    service.revoke_token(
        jti=token_jti,
        reason="Token stolen - detected in attacker's traffic",
        revoked_by="security_team",
        token_expiration=token_expiration,
        metadata={
            "incident_id": "INC-2025-001",
            "detected_by": "IDS",
            "ip_address": "203.0.113.42"
        }
    )
    
    # Check again (now revoked)
    print("4️⃣  Checking revocation status again...")
    if service.is_revoked(token_jti):
        print(f"   🚫 Token is REVOKED")
        
        entry = service.get_revocation(token_jti)
        print(f"   Reason: {entry.reason}")
        print(f"   Revoked by: {entry.revoked_by}")
        print(f"   Revoked at: {entry.revoked_at.isoformat()}")
    else:
        print(f"   ✅ Token is valid")
    print()
    
    # Simulate using revoked token (fails)
    print("5️⃣  Attacker tries to use stolen token...")
    print("   Validating token...")
    
    # Validation would check revocation
    if service.is_revoked(token_jti):
        print(f"   ❌ BLOCKED - Token is revoked!")
        print()
        print(f"   REVOCATION PROTECTED THE SYSTEM!")
    else:
        print(f"   ✅ Token accepted (this shouldn't happen!)")
    print()
    
    # User compromise scenario
    print("="*70)
    print("SCENARIO: User Account Compromise")
    print("="*70)
    print()
    
    print("6️⃣  User account compromised - revoking all tokens...")
    user_id = "researcher@university.edu"
    
    # Simulate user having 3 active tokens
    user_tokens = [secrets.token_urlsafe(16) for _ in range(3)]
    expirations = {
        jti: datetime.now(timezone.utc) + timedelta(minutes=15)
        for jti in user_tokens
    }
    
    count = service.revoke_all_for_user(
        user_id=user_id,
        active_token_jtis=user_tokens,
        token_expirations=expirations,
        reason="Account credentials compromised",
        revoked_by="security_team"
    )
    
    print(f"   Revoked {count} tokens for {user_id}")
    print()
    
    # Show stats
    stats = service.get_stats()
    print("7️⃣  Revocation statistics:")
    print(f"   Total revocations: {stats['total_revocations']}")
    print(f"   Active revocations: {stats['active_revocations']}")
    print()
    
    # Compare to Stage 2
    print("="*70)
    print("COMPARISON TO STAGE 2")
    print("="*70)
    print()
    print("Stage 2 (No Revocation):")
    print("  🔴 Cannot invalidate tokens")
    print("  🔴 Must wait for expiration (15 minutes)")
    print("  🔴 Stolen token works until it expires")
    print("  🔴 No immediate incident response")
    print()
    print("Stage 3 (With Revocation):")
    print("  ✅ Immediate token invalidation")
    print("  ✅ Real-time security response")
    print("  ✅ Can revoke single token or all for user")
    print("  ✅ Audit trail of revocations")
    print()
    
    # Show benefits
    print("="*70)
    print("SECURITY BENEFITS")
    print("="*70)
    print()
    print("With revocation, you can:")
    print()
    print("1. Respond to incidents immediately:")
    print("   - Token stolen? Revoke it instantly")
    print("   - Don't wait 15 minutes for expiration")
    print()
    print("2. Handle account compromise:")
    print("   - Revoke ALL tokens for a user")
    print("   - Force re-authentication")
    print()
    print("3. Implement security policies:")
    print("   - Geographic restrictions")
    print("   - Time-based access")
    print("   - Risk-based authentication")
    print()
    print("4. Meet compliance requirements:")
    print("   - Audit trail of all revocations")
    print("   - Demonstrate incident response capability")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_revocation()
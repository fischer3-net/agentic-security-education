"""
Stage 3 Demo - Token Revocation
================================

This demonstrates how token revocation enables immediate security response
to incidents.

Run this to see revocation in action!
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import stage3 modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import secrets
from datetime import datetime, timezone, timedelta
from revocation_service import RevocationService


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
        print(f"   🛡️  REVOCATION PROTECTED THE SYSTEM!")
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
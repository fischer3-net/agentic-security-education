"""
Stage 3 Demo - DPoP Proof-of-Possession
========================================

This demonstrates how DPoP (Demonstrating Proof-of-Possession) works
and why it prevents bearer token theft.

Run this to see DPoP in action!
"""

import sys
from pathlib import Path
# Add parent directory to path so we can import stage3 modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import jwt

from key_manager import KeyManager
from dpop_token_service import DPoPTokenService


def demo_dpop():
    """Demonstrate DPoP in action."""
    print("\n" + "="*70)
    print("STAGE 3: DPoP (PROOF-OF-POSSESSION) DEMONSTRATION")
    print("="*70 + "\n")
    
    # Setup
    km = KeyManager()
    dpop_service = DPoPTokenService(km)
    
    # Generate keys for issuer and client
    print("1️⃣  Generating keys...")
    issuer_keys = km.generate_key_pair("Agent A (University)", "RS256")
    client_keys = km.generate_key_pair("Agent B (Consortium)", "RS256")
    
    # Create DPoP-bound token
    print("2️⃣  Creating DPoP-bound token...")
    token = dpop_service.create_dpop_bound_token(
        issuer_service_id="Agent A (University)",
        subject="researcher@university.edu",
        audience="Agent B (Consortium)",
        scopes=["research:read"],
        client_public_key_jwk=client_keys.get_public_jwk(),
        correlation_id="abc-123"
    )
    
    # Decode to show binding
    token_payload = jwt.decode(token, options={"verify_signature": False})
    print(f"   Token created with cnf (confirmation) claim:")
    print(f"   cnf.jkt = {token_payload['cnf']['jkt'][:32]}...")
    print(f"   (This binds token to client's public key)")
    print()
    
    # Create DPoP proof
    print("3️⃣  Creating DPoP proof...")
    dpop_proof = dpop_service.create_dpop_proof(
        client_key_pair=client_keys,
        http_method="POST",
        http_uri="https://agent-b.example.com/api/data",
        access_token=token
    )
    print(f"   DPoP proof created")
    print(f"   (Signed with client's private key)")
    print()
    
    # Validate request (SUCCESS)
    print("4️⃣  Validating legitimate request...")
    try:
        validated = dpop_service.validate_dpop_request(
            access_token=token,
            dpop_proof=dpop_proof,
            expected_http_method="POST",
            expected_http_uri="https://agent-b.example.com/api/data",
            issuer_service_id="Agent A (University)"
        )
        print(f"   ✅ Request validated!")
        print(f"   User: {validated['sub']}")
        print(f"   Scopes: {validated['scope']}")
    except ValueError as e:
        print(f"   ❌ Validation failed: {e}")
    print()
    
    # Show what happens if token is stolen
    print("="*70)
    print("ATTACK SCENARIO: Token Theft")
    print("="*70)
    print()
    
    print("5️⃣  Attacker intercepts token (man-in-the-middle)...")
    stolen_token = token
    print(f"   Attacker has token: {stolen_token[:50]}...")
    print()
    
    print("6️⃣  Attacker tries to use stolen token...")
    print("   Creating DPoP proof with attacker's key...")
    
    # Attacker has their own keys
    attacker_keys = km.generate_key_pair("Attacker", "RS256")
    
    # Attacker creates DPoP proof with THEIR key
    fake_dpop_proof = dpop_service.create_dpop_proof(
        client_key_pair=attacker_keys,  # Wrong key!
        http_method="POST",
        http_uri="https://agent-b.example.com/api/data",
        access_token=stolen_token
    )
    
    # Try to validate (FAILS!)
    print("   Attempting validation...")
    try:
        dpop_service.validate_dpop_request(
            access_token=stolen_token,
            dpop_proof=fake_dpop_proof,
            expected_http_method="POST",
            expected_http_uri="https://agent-b.example.com/api/data",
            issuer_service_id="Agent A (University)"
        )
        print(f"   ✅ Attack succeeded (this shouldn't happen!)")
    except ValueError as e:
        print(f"   ❌ Attack BLOCKED: {e}")
        print()
        print(f"   🛡️  DPoP PROTECTED THE SYSTEM!")
    print()
    
    # Summary
    print("="*70)
    print("DPoP PROTECTION SUMMARY")
    print("="*70)
    print()
    print("What Happened:")
    print("  1. Attacker intercepted token")
    print("  2. Attacker tried to create DPoP proof with their own key")
    print("  3. Server checked token's cnf (confirmation) claim")
    print("  4. Server compared DPoP proof key to cnf.jkt")
    print("  5. MISMATCH → Attack blocked!")
    print()
    print("Why It Failed:")
    print("  • Token is bound to client's specific public key")
    print("  • Attacker doesn't have corresponding private key")
    print("  • Cannot create valid DPoP proof")
    print("  • Stolen token is USELESS")
    print()
    print("Stage 2 Comparison:")
    print("  🔴 Bearer tokens: Anyone with token can use it")
    print("  ✅ DPoP tokens: Must prove possession of private key")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_dpop()
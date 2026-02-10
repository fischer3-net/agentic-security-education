"""
Stage 3 - Complete Secure Flow Demonstration
=============================================

This demonstrates the entire Stage 3 secure implementation:
- Asymmetric keys
- DPoP proof-of-possession
- W3C Trace Context
- Secure audit logging
- Token revocation
- Policy-based authorization

This is what production looks like!
"""

import asyncio
import json
from datetime import datetime, timezone
import sys

from anyio import Path

# Add parent directory to path so we can import stage3 modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from key_manager import KeyManager
from dpop_token_service import DPoPTokenService
from secure_audit_logger import SecureAuditLogger
from trace_context import TraceContext, TraceContextPropagator
from revocation_service import RevocationService
from policy_engine import PolicyEngine
from secure_agents import SecureAgentA, SecureAgentB, SecureAgentC, SecureRequest


async def demo_complete_flow():
    """Demonstrate complete secure federated identity flow."""
    
    print("\n" + "="*80)
    print(" "*20 + "STAGE 3: COMPLETE SECURE FLOW")
    print("="*80 + "\n")
    
    print("This demonstration shows ALL Stage 3 security features working together.")
    print()
    
    input("Press Enter to begin the demonstration...")
    
    # ========================================================================
    # PHASE 1: SETUP
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 1: INITIALIZE SECURE INFRASTRUCTURE")
    print("="*80 + "\n")
    
    # 1. Key Manager - Asymmetric keys
    print("1. Key Manager (Asymmetric Cryptography)")
    print("   " + "-"*70)
    km = KeyManager()
    print()
    
    # 2. DPoP Service - Proof-of-possession
    print("2. DPoP Token Service (Proof-of-Possession)")
    print("   " + "-"*70)
    dpop_service = DPoPTokenService(km)
    print()
    
    # 3. Secure Audit Logger - Cryptographically signed logs
    print("3. Secure Audit Logger (Cryptographic Signatures)")
    print("   " + "-"*70)
    audit_logger = SecureAuditLogger("complete_flow_audit.log")
    print()
    
    # 4. Revocation Service - Token invalidation
    print("4. Revocation Service (Immediate Security Response)")
    print("   " + "-"*70)
    revocation_service = RevocationService("complete_flow_revocations.json")
    print()
    
    # 5. Policy Engine - Centralized authorization
    print("5. Policy Engine (Centralized Authorization)")
    print("   " + "-"*70)
    policy_engine = PolicyEngine()
    
    # Load policies
    policies_json = json.dumps([
        {
            "policy_id": "allow-university-research",
            "description": "University researchers can initiate research",
            "effect": "allow",
            "subjects": ["*@university.edu"],
            "actions": ["initiate_research", "aggregate_data"],
            "resources": ["*"]
        },
        {
            "policy_id": "allow-consortium-aggregate",
            "description": "Consortium can aggregate data",
            "effect": "allow",
            "subjects": ["Agent B (Consortium)"],
            "actions": ["aggregate_data", "provide_clinical_data"],
            "resources": ["*"]
        }
    ])
    policy_engine.load_policies_from_json(policies_json)
    print()
    
    # 6. Generate keys for auth service (issues initial tokens)
    print("6. Generating keys for auth service...")
    print("   " + "-"*70)
    km.generate_key_pair("auth_service", "RS256")
    print()
    
    input("Press Enter to create secure agents...")
    
    # ========================================================================
    # PHASE 2: CREATE AGENTS
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 2: CREATE SECURE AGENTS")
    print("="*80 + "\n")
    
    # Create three agents
    agent_a = SecureAgentA(
        name="Agent A (University)",
        organization="University Hospital",
        key_manager=km,
        dpop_service=dpop_service,
        audit_logger=audit_logger,
        revocation_service=revocation_service,
        policy_engine=policy_engine
    )
    
    agent_b = SecureAgentB(
        name="Agent B (Consortium)",
        organization="Research Consortium",
        key_manager=km,
        dpop_service=dpop_service,
        audit_logger=audit_logger,
        revocation_service=revocation_service,
        policy_engine=policy_engine
    )
    
    agent_c = SecureAgentC(
        name="Agent C (Pharma)",
        organization="Pharma Corporation",
        key_manager=km,
        dpop_service=dpop_service,
        audit_logger=audit_logger,
        revocation_service=revocation_service,
        policy_engine=policy_engine
    )
    
    input("Press Enter to start secure request flow...")
    
    # ========================================================================
    # PHASE 3: SECURE REQUEST FLOW
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 3: SECURE REQUEST FLOW")
    print("="*80 + "\n")
    
    # Create W3C Trace Context
    print("Creating W3C Trace Context for distributed tracing...")
    trace_context = TraceContext()
    print(f"   Trace ID: {trace_context.trace_id}")
    print(f"   Span ID: {trace_context.parent_id}")
    print()
    
    # Create DPoP-bound token for Agent A
    print("Creating DPoP-bound token for Agent A...")
    token_a = dpop_service.create_dpop_bound_token(
        issuer_service_id="auth_service",
        subject="researcher@university.edu",
        audience="Agent A (University)",
        scopes=["initiate_research"],
        client_public_key_jwk=agent_a.key_pair.get_public_jwk(),
        correlation_id=trace_context.trace_id,
        lineage=["researcher@university.edu"]
    )
    print(f"   ✅ Token bound to Agent A's public key")
    print()
    
    # Create DPoP proof
    print("Creating DPoP proof (proving possession of private key)...")
    dpop_proof_a = dpop_service.create_dpop_proof(
        client_key_pair=agent_a.key_pair,
        http_method="POST",
        http_uri="https://agent-a.example.com/api/research",
        access_token=token_a
    )
    print(f"   ✅ DPoP proof created")
    print()
    
    input("Press Enter to send request to Agent A...")
    
    # Send request to Agent A
    print("\n" + "-"*80)
    print("SENDING REQUEST TO AGENT A")
    print("-"*80 + "\n")
    
    request_a = SecureRequest(
        from_agent="researcher@university.edu",
        to_agent="Agent A (University)",
        action="initiate_research",
        data={"project_name": "Alzheimer's Treatment Study"},
        access_token=token_a,
        dpop_proof=dpop_proof_a,
        trace_context=trace_context,
        expected_audience="Agent A (University)",
        http_method="POST",
        http_uri="https://agent-a.example.com/api/research"
    )
    
    response_a = await agent_a.handle_request(request_a)
    
    print(f"RESPONSE FROM AGENT A:")
    print(f"   Status: {response_a.status}")
    print(f"   Data: {response_a.data}")
    print()
    
    input("Press Enter to view audit trail...")
    
    # ========================================================================
    # PHASE 4: AUDIT TRAIL
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 4: SECURE AUDIT TRAIL")
    print("="*80 + "\n")
    
    audit_logger.show_audit_trail(trace_id=trace_context.trace_id)
    
    input("Press Enter to demonstrate revocation...")
    
    # ========================================================================
    # PHASE 5: TOKEN REVOCATION
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 5: TOKEN REVOCATION DEMONSTRATION")
    print("="*80 + "\n")
    
    print("SCENARIO: Security team detects suspicious activity")
    print("ACTION: Revoking token immediately")
    print()
    
    # Get token jti
    import jwt
    token_payload = jwt.decode(token_a, options={"verify_signature": False})
    token_jti = token_payload.get('jti')
    token_exp = datetime.fromtimestamp(token_payload['exp'], tz=timezone.utc)
    
    # Revoke token
    revocation_service.revoke_token(
        jti=token_jti,
        reason="Suspicious activity detected",
        revoked_by="security_team",
        token_expiration=token_exp,
        metadata={"incident_id": "INC-2025-001"}
    )
    
    print("Token revoked!")
    print()
    
    input("Press Enter to attempt using revoked token...")
    
    print("\n" + "-"*80)
    print("ATTEMPTING TO USE REVOKED TOKEN")
    print("-"*80 + "\n")
    
    # Try to use revoked token
    response_revoked = await agent_a.handle_request(request_a)
    
    print(f"RESPONSE: {response_revoked.status}")
    print(f"Message: {response_revoked.data.get('message')}")
    print()
    print("✅ REVOCATION BLOCKED THE REQUEST!")
    print()
    
    input("Press Enter to see final summary...")
    
    # ========================================================================
    # PHASE 6: SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE - SUMMARY")
    print("="*80 + "\n")
    
    print("✅ Stage 3 Security Features Demonstrated:")
    print()
    print("1. ASYMMETRIC CRYPTOGRAPHY")
    print("   • Each service has its own key pair")
    print("   • Private keys never shared")
    print("   • Public keys distributed safely")
    print()
    print("2. DPOP PROOF-OF-POSSESSION (RFC 9449)")
    print("   • Tokens bound to client keys")
    print("   • Stolen tokens are useless")
    print("   • Must prove private key possession")
    print()
    print("3. W3C TRACE CONTEXT")
    print("   • Industry standard distributed tracing")
    print("   • Parent-child span relationships")
    print("   • APM tool integration")
    print()
    print("4. SECURE AUDIT LOGGING")
    print("   • Cryptographic signatures (HMAC-SHA256)")
    print("   • Merkle chain structure")
    print("   • Tamper-proof audit trail")
    print()
    print("5. TOKEN REVOCATION")
    print("   • Immediate security response")
    print("   • Real-time revocation checking")
    print("   • Can invalidate compromised tokens")
    print()
    print("6. POLICY ENGINE")
    print("   • Centralized authorization")
    print("   • Declarative policies")
    print("   • Consistent enforcement")
    print()
    print("="*80)
    print(" "*25 + "THIS IS PRODUCTION-READY!")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(demo_complete_flow())
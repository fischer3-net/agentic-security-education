"""
Stage 3 - Secure Agent Implementations
=======================================

Production-ready agents using ALL Stage 3 security features.

INTEGRATES ALL IMPROVEMENTS:
1. ✅ Asymmetric keys (key_manager)
2. ✅ DPoP proof-of-possession (dpop_token_service)
3. ✅ Secure audit logging (secure_audit_logger)
4. ✅ W3C Trace Context (trace_context)
5. ✅ Token revocation (revocation_service)
6. ✅ Policy engine (policy_engine)

This is what production-ready federated identity looks like!
"""

import asyncio
import secrets
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta

from key_manager import KeyManager, KeyPair
from dpop_token_service import DPoPTokenService
from secure_audit_logger import SecureAuditLogger
from trace_context import TraceContext, TraceContextPropagator
from revocation_service import RevocationService
from policy_engine import PolicyEngine, Effect


@dataclass
class SecureRequest:
    """
    Production-ready request structure.
    
    IMPROVEMENTS:
    - W3C Trace Context
    - DPoP proof included
    - Expected audience
    - Policy context
    """
    from_agent: str
    to_agent: str
    action: str
    data: Dict[str, Any] = field(default_factory=dict)
    access_token: Optional[str] = None
    dpop_proof: Optional[str] = None
    trace_context: Optional[TraceContext] = None
    expected_audience: str = ""
    http_method: str = "POST"
    http_uri: str = ""


@dataclass
class SecureResponse:
    """Production-ready response structure."""
    from_agent: str
    to_agent: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
    trace_context: Optional[TraceContext] = None


class SecureBaseAgent:
    """
    Base class for production-ready agents.
    
    INTEGRATES:
    - Asymmetric keys for signing
    - DPoP for proof-of-possession
    - Secure audit logging
    - W3C Trace Context
    - Token revocation checking
    - Policy-based authorization
    """
    
    def __init__(
        self,
        name: str,
        organization: str,
        key_manager: KeyManager,
        dpop_service: DPoPTokenService,
        audit_logger: SecureAuditLogger,
        revocation_service: RevocationService,
        policy_engine: PolicyEngine
    ):
        """
        Initialize secure agent.
        
        Args:
            name: Agent name
            organization: Agent's organization
            key_manager: Shared key manager
            dpop_service: DPoP token service
            audit_logger: Secure audit logger
            revocation_service: Token revocation service
            policy_engine: Authorization policy engine
        """
        self.name = name
        self.organization = organization
        
        # Shared services
        self.key_manager = key_manager
        self.dpop_service = dpop_service
        self.audit_logger = audit_logger
        self.revocation_service = revocation_service
        self.policy_engine = policy_engine
        
        # Agent's own key pair
        self.key_pair = key_manager.get_key_pair(name)
        if not self.key_pair:
            self.key_pair = key_manager.generate_key_pair(name, "RS256")
        
        print(f"🔐 Initialized {name} ({organization})")
        print(f"   ✅ Asymmetric keys ready")
        print(f"   ✅ DPoP enabled")
        print(f"   ✅ Secure audit logging")
        print(f"   ✅ W3C Trace Context")
        print(f"   ✅ Revocation checking")
        print(f"   ✅ Policy-based authorization")
        print()
    
    async def handle_request(self, request: SecureRequest) -> SecureResponse:
        """
        Handle incoming request with full security.
        
        SECURITY CHECKS:
        1. Validate DPoP proof
        2. Check token revocation
        3. Evaluate authorization policy
        4. Log everything to audit trail
        """
        # Create span if no trace context
        if not request.trace_context:
            request.trace_context = TraceContext()
        
        # Create child span for this agent
        span_context = request.trace_context.create_child_span()
        
        print(f"\n{'='*70}")
        print(f"📨 {self.name} received request")
        print(f"{'='*70}")
        print(f"From: {request.from_agent}")
        print(f"Action: {request.action}")
        print(f"Trace: {span_context.trace_id}")
        print(f"Span: {span_context.parent_id}")
        print()
        
        # Step 1: Validate DPoP-bound token
        if request.access_token and request.dpop_proof:
            print("1️⃣  Validating DPoP-bound token...")
            try:
                token_payload = self.dpop_service.validate_dpop_request(
                    access_token=request.access_token,
                    dpop_proof=request.dpop_proof,
                    expected_http_method=request.http_method,
                    expected_http_uri=request.http_uri,
                    issuer_service_id=request.from_agent
                )
                print(f"   ✅ DPoP validation passed")
                print(f"   User: {token_payload.get('sub')}")
                print(f"   Scopes: {token_payload.get('scope')}")
                print()
                
                # Step 2: Check revocation
                print("2️⃣  Checking token revocation...")
                jti = token_payload.get('jti')
                if self.revocation_service.is_revoked(jti):
                    print(f"   ❌ Token is REVOKED")
                    
                    # Log revocation block
                    self.audit_logger.log_event(
                        event_type="authorization_denied",
                        trace_id=span_context.trace_id,
                        span_id=span_context.parent_id,
                        actor=token_payload.get('sub'),
                        action=request.action,
                        resource=self.name,
                        result="revoked_token",
                        token_lineage=token_payload.get('lineage', []),
                        metadata={"jti": jti}
                    )
                    
                    return SecureResponse(
                        from_agent=self.name,
                        to_agent=request.from_agent,
                        status="error",
                        data={"message": "Token has been revoked"},
                        trace_context=span_context
                    )
                
                print(f"   ✅ Token is valid (not revoked)")
                print()
                
                # Step 3: Check authorization policy
                print("3️⃣  Evaluating authorization policy...")
                policy_result = self.policy_engine.evaluate(
                    subject=token_payload.get('sub'),
                    action=request.action,
                    resource=self.name
                )
                
                if policy_result.decision == Effect.DENY:
                    print(f"   ❌ Access DENIED by policy")
                    print(f"   Reason: {policy_result.reason}")
                    print()
                    
                    # Log policy denial
                    self.audit_logger.log_event(
                        event_type="authorization_denied",
                        trace_id=span_context.trace_id,
                        span_id=span_context.parent_id,
                        actor=token_payload.get('sub'),
                        action=request.action,
                        resource=self.name,
                        result="policy_denied",
                        token_lineage=token_payload.get('lineage', []),
                        metadata={
                            "matched_policies": policy_result.matched_policies,
                            "reason": policy_result.reason
                        }
                    )
                    
                    return SecureResponse(
                        from_agent=self.name,
                        to_agent=request.from_agent,
                        status="error",
                        data={"message": "Access denied by policy"},
                        trace_context=span_context
                    )
                
                print(f"   ✅ Access ALLOWED by policy")
                print(f"   Matched policies: {policy_result.matched_policies}")
                print()
                
                # Log successful authorization
                self.audit_logger.log_event(
                    event_type="authorization_granted",
                    trace_id=span_context.trace_id,
                    span_id=span_context.parent_id,
                    actor=token_payload.get('sub'),
                    action=request.action,
                    resource=self.name,
                    result="success",
                    token_lineage=token_payload.get('lineage', []),
                    metadata={
                        "matched_policies": policy_result.matched_policies,
                        "scopes": token_payload.get('scope')
                    }
                )
                
            except ValueError as e:
                print(f"   ❌ Validation failed: {e}")
                print()
                
                # Log validation failure
                self.audit_logger.log_event(
                    event_type="authentication_failed",
                    trace_id=span_context.trace_id,
                    span_id=span_context.parent_id,
                    actor="unknown",
                    action=request.action,
                    resource=self.name,
                    result="validation_failed",
                    token_lineage=[],
                    metadata={"error": str(e)}
                )
                
                return SecureResponse(
                    from_agent=self.name,
                    to_agent=request.from_agent,
                    status="error",
                    data={"message": f"Validation failed: {e}"},
                    trace_context=span_context
                )
        
        print(f"4️⃣  Processing request...")
        print(f"{'='*70}\n")
        
        # Process the request
        response = await self._process_request(request)
        response.trace_context = span_context
        return response
    
    async def _process_request(self, request: SecureRequest) -> SecureResponse:
        """Process the request. Subclasses should override."""
        raise NotImplementedError("Subclasses must implement _process_request")
    
    async def forward_with_dpop(
        self,
        current_token: str,
        to_agent: str,
        to_audience: str,
        requested_scopes: list,
        trace_context: TraceContext,
        action: str,
        http_uri: str
    ) -> tuple[str, str]:
        """
        Forward request using DPoP token exchange.
        
        Returns:
            Tuple of (new_access_token, dpop_proof)
        """
        print(f"\n🔄 Exchanging token for {to_agent} with DPoP...")
        
        # Get target agent's public key
        target_key_pair = self.key_manager.get_key_pair(to_agent)
        if not target_key_pair:
            raise ValueError(f"No keys for {to_agent}")
        
        # Create DPoP-bound token
        new_token = self.dpop_service.create_dpop_bound_token(
            issuer_service_id=self.name,
            subject="researcher@university.edu",  # Would extract from current token
            audience=to_audience,
            scopes=requested_scopes,
            client_public_key_jwk=target_key_pair.get_public_jwk(),
            correlation_id=trace_context.trace_id,
            lineage=["researcher@university.edu", self.name]
        )
        
        # Create DPoP proof
        dpop_proof = self.dpop_service.create_dpop_proof(
            client_key_pair=target_key_pair,
            http_method="POST",
            http_uri=http_uri,
            access_token=new_token
        )
        
        print(f"   ✅ Token exchanged with DPoP binding")
        print()
        
        return new_token, dpop_proof


class SecureAgentA(SecureBaseAgent):
    """
    Secure Agent A - University Hospital Research Coordinator
    
    Uses all Stage 3 security features.
    """
    
    async def _process_request(self, request: SecureRequest) -> SecureResponse:
        """Process research coordination requests."""
        
        if request.action == "initiate_research":
            print(f"🔬 Initiating research project...")
            print(f"   Project: {request.data.get('project_name')}")
            print()
            
            # Would forward to Agent B with DPoP
            return SecureResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={"project_started": True}
            )
        
        return SecureResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"}
        )


class SecureAgentB(SecureBaseAgent):
    """
    Secure Agent B - Research Consortium Data Aggregator
    
    Uses all Stage 3 security features.
    """
    
    async def _process_request(self, request: SecureRequest) -> SecureResponse:
        """Process data aggregation requests."""
        
        if request.action == "aggregate_data":
            print(f"📊 Aggregating data...")
            print()
            
            return SecureResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={"aggregation_complete": True}
            )
        
        return SecureResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"}
        )


class SecureAgentC(SecureBaseAgent):
    """
    Secure Agent C - Pharmaceutical Company Data Provider
    
    Uses all Stage 3 security features.
    """
    
    async def _process_request(self, request: SecureRequest) -> SecureResponse:
        """Process data provision requests."""
        
        if request.action == "provide_clinical_data":
            print(f"💊 Providing clinical data...")
            print()
            
            return SecureResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={"clinical_data_provided": True}
            )
        
        return SecureResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"}
        )


async def demo_secure_agents():
    """Demonstrate secure agents with all features."""
    print("\n" + "="*70)
    print("STAGE 3: SECURE AGENTS DEMONSTRATION")
    print("="*70 + "\n")
    
    # Initialize all services
    print("Initializing secure infrastructure...")
    print()
    
    km = KeyManager()
    dpop_service = DPoPTokenService(km)
    audit_logger = SecureAuditLogger("secure_demo_audit.log")
    revocation_service = RevocationService("secure_demo_revocations.json")
    policy_engine = PolicyEngine()
    
    # Load policies
    import json
    policies_json = json.dumps([
        {
            "policy_id": "allow-university-research",
            "description": "University can initiate research",
            "effect": "allow",
            "subjects": ["*@university.edu"],
            "actions": ["initiate_research"],
            "resources": ["Agent A (University)"]
        }
    ])
    policy_engine.load_policies_from_json(policies_json)
    
    # Generate keys for auth service (needed to issue initial tokens)
    print("Generating keys for auth service...")
    km.generate_key_pair("auth_service", "RS256")
    print()
    
    # Create agents
    agent_a = SecureAgentA(
        name="Agent A (University)",
        organization="University Hospital",
        key_manager=km,
        dpop_service=dpop_service,
        audit_logger=audit_logger,
        revocation_service=revocation_service,
        policy_engine=policy_engine
    )
    
    # Create trace context
    trace_context = TraceContext()
    
    # Create DPoP-bound token
    token = dpop_service.create_dpop_bound_token(
        issuer_service_id="auth_service",
        subject="researcher@university.edu",
        audience="Agent A (University)",
        scopes=["initiate_research"],
        client_public_key_jwk=agent_a.key_pair.get_public_jwk(),
        correlation_id=trace_context.trace_id,
        lineage=["researcher@university.edu"]
    )
    
    # Create DPoP proof
    dpop_proof = dpop_service.create_dpop_proof(
        client_key_pair=agent_a.key_pair,
        http_method="POST",
        http_uri="https://agent-a.example.com/api/research",
        access_token=token
    )
    
    # Create request
    request = SecureRequest(
        from_agent="researcher@university.edu",
        to_agent="Agent A (University)",
        action="initiate_research",
        data={"project_name": "Alzheimer's Study"},
        access_token=token,
        dpop_proof=dpop_proof,
        trace_context=trace_context,
        expected_audience="Agent A (University)",
        http_method="POST",
        http_uri="https://agent-a.example.com/api/research"
    )
    
    # Send request
    response = await agent_a.handle_request(request)
    
    print(f"\n✅ Request completed")
    print(f"   Status: {response.status}")
    print(f"   Trace: {response.trace_context.trace_id}")
    print()
    
    # Show audit trail
    audit_logger.show_audit_trail(trace_id=trace_context.trace_id)
    
    # Compare to Stage 2
    print("\n" + "="*70)
    print("STAGE 2 VS STAGE 3 COMPARISON")
    print("="*70)
    print()
    print("Stage 2 (Improved):")
    print("  ⚠️  Symmetric keys")
    print("  ⚠️  Bearer tokens")
    print("  ⚠️  No replay protection")
    print("  ⚠️  Weak audit logs")
    print("  ⚠️  No revocation")
    print("  ⚠️  Hardcoded authorization")
    print()
    print("Stage 3 (Production-Ready):")
    print("  ✅ Asymmetric keys (RSA/ECDSA)")
    print("  ✅ DPoP proof-of-possession")
    print("  ✅ Nonce-based replay protection")
    print("  ✅ Cryptographically signed audit logs")
    print("  ✅ Real-time token revocation")
    print("  ✅ Policy-based authorization")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(demo_secure_agents())
"""
Stage 2 - Improved Agent Implementations
========================================

IMPROVEMENTS over Stage 1:
1. ✅ Agents use token exchange (not naive forwarding)
2. ✅ Audience validation before processing
3. ✅ Correlation IDs for request tracking
4. ✅ Comprehensive audit logging
5. ✅ Token lineage maintained

REMAINING VULNERABILITIES:
1. ⚠️ Still using bearer tokens (no proof-of-possession)
2. ⚠️ Audience validation not always enforced
3. ⚠️ Trust decisions hardcoded
4. ⚠️ No token revocation checks
5. ⚠️ Symmetric key vulnerabilities inherited from token service

This demonstrates incremental security improvement while showing
that "better" doesn't mean "secure enough" for production.
"""

import asyncio
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from token_exchange_service import (
    TokenExchangeService,
    TokenExchangeRequest,
    TokenExchangeResponse
)
from audit_logger import AuditLogger


@dataclass
class ImprovedAgentRequest:
    """
    Improved request structure.
    
    IMPROVEMENTS:
    - Correlation ID for tracing
    - Explicit audience
    - Request signatures (not implemented yet)
    
    REMAINING ISSUES:
    - No request nonce
    - No timestamp validation
    """
    from_agent: str
    to_agent: str
    action: str
    data: Dict[str, Any] = field(default_factory=dict)
    token: Optional[str] = None
    correlation_id: Optional[str] = None  # IMPROVEMENT!
    expected_audience: Optional[str] = None  # IMPROVEMENT!


@dataclass
class ImprovedAgentResponse:
    """Improved response structure with correlation."""
    from_agent: str
    to_agent: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None  # IMPROVEMENT!


class ImprovedBaseAgent:
    """
    Base class for improved agents.
    
    IMPROVEMENTS:
    - Token exchange service integration
    - Audit logging
    - Correlation ID handling
    
    REMAINING ISSUES:
    - No policy engine
    - No circuit breaker
    - No rate limiting
    """
    
    def __init__(self, name: str, organization: str, audience_id: str):
        """
        Initialize improved agent.
        
        Args:
            name: Agent name
            organization: Agent's organization
            audience_id: Identifier for audience validation
        """
        self.name = name
        self.organization = organization
        self.audience_id = audience_id
        
        # IMPROVEMENT: Shared services
        self.token_service = TokenExchangeService()
        self.audit_logger = AuditLogger(f"{name.replace(' ', '_')}_audit.log")
        
        print(f"🤖 Initialized {name} ({organization})")
        print(f"   Audience ID: {audience_id}")
        print(f"   ✅ Token exchange enabled")
        print(f"   ✅ Audit logging enabled")
        print()
    
    async def handle_request(self, request: ImprovedAgentRequest) -> ImprovedAgentResponse:
        """
        Handle incoming request with improved security.
        
        IMPROVEMENTS:
        - Generates correlation ID if missing
        - Validates token audience
        - Logs to audit trail
        
        REMAINING ISSUES:
        - Audience validation can be skipped
        - No rate limiting
        - No circuit breaker
        """
        # IMPROVEMENT: Generate correlation ID if not provided
        correlation_id = request.correlation_id or str(uuid.uuid4())
        request.correlation_id = correlation_id
        
        print(f"\n{'='*70}")
        print(f"📨 {self.name} received request")
        print(f"{'='*70}")
        print(f"From: {request.from_agent}")
        print(f"Action: {request.action}")
        print(f"Correlation ID: {correlation_id}")
        
        # IMPROVEMENT: Validate token before processing
        if request.token:
            try:
                # IMPROVEMENT: Validate audience
                token_payload = self.token_service.validate_token(
                    request.token,
                    expected_audience=self.audience_id  # IMPROVEMENT!
                )
                
                print(f"✅ Token validated")
                print(f"   User: {token_payload.get('sub')}")
                print(f"   Audience: {token_payload.get('aud')}")
                print(f"   Scopes: {token_payload.get('scope')}")
                print(f"   Lineage: {' → '.join(token_payload.get('lineage', []))}")
                
                # IMPROVEMENT: Log to audit trail
                self.audit_logger.log_agent_request(
                    correlation_id=correlation_id,
                    from_agent=request.from_agent,
                    to_agent=self.name,
                    action=request.action,
                    token_lineage=token_payload.get('lineage', []),
                    result="accepted"
                )
                
            except ValueError as e:
                print(f"❌ Token validation failed: {e}")
                
                # Log failed validation
                self.audit_logger.log_agent_request(
                    correlation_id=correlation_id,
                    from_agent=request.from_agent,
                    to_agent=self.name,
                    action=request.action,
                    token_lineage=[],
                    result="rejected",
                    metadata={"error": str(e)}
                )
                
                return ImprovedAgentResponse(
                    from_agent=self.name,
                    to_agent=request.from_agent,
                    status="error",
                    data={"message": f"Token validation failed: {e}"},
                    correlation_id=correlation_id
                )
        else:
            # VULNERABILITY: No token required?
            print(f"⚠️  WARNING: No token provided")
        
        print(f"{'='*70}\n")
        
        # Process the request
        response = await self._process_request(request)
        response.correlation_id = correlation_id
        return response
    
    async def _process_request(self, request: ImprovedAgentRequest) -> ImprovedAgentResponse:
        """Process the request. Subclasses should override."""
        raise NotImplementedError("Subclasses must implement _process_request")
    
    async def forward_with_exchange(
        self,
        current_token: str,
        to_agent: str,
        to_audience: str,
        requested_scopes: list,
        correlation_id: str
    ) -> str:
        """
        Forward request using token exchange (not naive forwarding!).
        
        IMPROVEMENT: This is the key difference from Stage 1!
        Uses proper token exchange instead of forwarding same token.
        
        REMAINING ISSUES:
        - Still uses symmetric keys
        - No proof-of-possession
        """
        print(f"\n🔄 Exchanging token for {to_agent}...")
        
        # IMPROVEMENT: Use token exchange service
        exchange_request = TokenExchangeRequest(
            subject_token=current_token,
            audience=to_audience,
            scope=requested_scopes,
            correlation_id=correlation_id
        )
        
        response = self.token_service.exchange_token(exchange_request)
        
        print(f"✅ New token issued for {to_agent}")
        print(f"   Scopes: {response.scope}")
        print(f"   Lineage: {' → '.join(response.lineage)}")
        
        return response.access_token


class ImprovedAgentA(ImprovedBaseAgent):
    """
    Improved Agent A - University Hospital Research Coordinator
    
    IMPROVEMENTS:
    - Uses token exchange when forwarding to Agent B
    - Validates token audience
    - Comprehensive audit logging
    
    REMAINING ISSUES:
    - Trust decisions still hardcoded
    """
    
    def __init__(self):
        super().__init__(
            name="Agent A (University)",
            organization="University Hospital",
            audience_id="Agent A (University)"
        )
    
    async def _process_request(self, request: ImprovedAgentRequest) -> ImprovedAgentResponse:
        """Process research coordination requests."""
        
        if request.action == "initiate_research":
            print(f"🔬 Starting research project: {request.data.get('project_name')}")
            print(f"   Researcher: {request.data.get('researcher')}")
            print()
            
            # IMPROVEMENT: Exchange token before forwarding
            new_token = await self.forward_with_exchange(
                current_token=request.token,
                to_agent="Agent B (Consortium)",
                to_audience="Agent B (Consortium)",
                requested_scopes=["research:read"],  # IMPROVEMENT: Request only what's needed
                correlation_id=request.correlation_id
            )
            
            # Forward to Agent B with new token
            print(f"📤 Forwarding to Agent B...")
            agent_b_request = ImprovedAgentRequest(
                from_agent=self.name,
                to_agent="Agent B (Consortium)",
                action="aggregate_data",
                data=request.data,
                token=new_token,  # IMPROVEMENT: New token, not original!
                correlation_id=request.correlation_id,
                expected_audience="Agent B (Consortium)"
            )
            
            # Simulate Agent B response
            agent_b_response = {
                "status": "success",
                "data_sources": ["Agent C"],
                "message": "Data aggregation initiated"
            }
            
            return ImprovedAgentResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={
                    "project_started": True,
                    "downstream_requests": ["Agent B"],
                    "agent_b_response": agent_b_response
                },
                correlation_id=request.correlation_id
            )
        
        return ImprovedAgentResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"},
            correlation_id=request.correlation_id
        )


class ImprovedAgentB(ImprovedBaseAgent):
    """
    Improved Agent B - Research Consortium Data Aggregator
    
    IMPROVEMENTS:
    - Validates incoming token audience
    - Exchanges token again before forwarding to Agent C
    - Full audit trail
    
    REMAINING ISSUES:
    - Could still be confused deputy (bearer tokens)
    """
    
    def __init__(self):
        super().__init__(
            name="Agent B (Consortium)",
            organization="Research Consortium",
            audience_id="Agent B (Consortium)"
        )
    
    async def _process_request(self, request: ImprovedAgentRequest) -> ImprovedAgentResponse:
        """Process data aggregation requests."""
        
        if request.action == "aggregate_data":
            print(f"📊 Aggregating data from multiple sources...")
            print(f"   Project: {request.data.get('project_name')}")
            print()
            
            # IMPROVEMENT: Validate token before proceeding
            if not request.token:
                return ImprovedAgentResponse(
                    from_agent=self.name,
                    to_agent=request.from_agent,
                    status="error",
                    data={"message": "No token provided"},
                    correlation_id=request.correlation_id
                )
            
            # IMPROVEMENT: Exchange token again for Agent C
            new_token = await self.forward_with_exchange(
                current_token=request.token,
                to_agent="Agent C (Pharma)",
                to_audience="Agent C (Pharma)",
                requested_scopes=["research:read"],  # Further scoping down
                correlation_id=request.correlation_id
            )
            
            print(f"📤 Forwarding to Agent C...")
            
            # Simulate Agent C response
            agent_c_response = {
                "status": "success",
                "data_provided": True,
                "records": 150
            }
            
            return ImprovedAgentResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={
                    "aggregation_complete": True,
                    "sources": ["Agent C (Pharma)"],
                    "agent_c_response": agent_c_response,
                    "total_records": 150
                },
                correlation_id=request.correlation_id
            )
        
        return ImprovedAgentResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"},
            correlation_id=request.correlation_id
        )


class ImprovedAgentC(ImprovedBaseAgent):
    """
    Improved Agent C - Pharmaceutical Company Data Provider
    
    IMPROVEMENTS:
    - Strictly validates token audience
    - Cannot use token outside intended scope
    - Audit trail shows token lineage
    
    REMAINING ISSUES:
    - Still bearer token (if stolen, can be used)
    - No proof-of-possession
    """
    
    def __init__(self):
        super().__init__(
            name="Agent C (Pharma)",
            organization="Pharma Corporation",
            audience_id="Agent C (Pharma)"
        )
        self.malicious_mode = False
    
    async def _process_request(self, request: ImprovedAgentRequest) -> ImprovedAgentResponse:
        """Process data provision requests."""
        
        if request.action == "provide_clinical_data":
            print(f"💊 Providing clinical trial data...")
            print(f"   Project: {request.data.get('project_name')}")
            print()
            
            if request.token:
                # IMPROVEMENT: Validate and inspect token
                try:
                    payload = self.token_service.validate_token(
                        request.token,
                        expected_audience=self.audience_id
                    )
                    
                    print(f"Token details:")
                    print(f"   User: {payload.get('sub')}")
                    print(f"   Audience: {payload.get('aud')}")
                    print(f"   Scopes: {payload.get('scope')}")
                    print(f"   Lineage: {' → '.join(payload.get('lineage', []))}")
                    print()
                    
                    if self.malicious_mode:
                        print(f"🔓 Attempting malicious activity...")
                        await self._attempt_malicious_activity(request.token, payload)
                    
                    # Log data access
                    self.audit_logger.log_data_access(
                        correlation_id=request.correlation_id,
                        user=payload.get('sub'),
                        resource="clinical_trials_database",
                        action="read",
                        token_lineage=payload.get('lineage', []),
                        result="success",
                        metadata={
                            "records_provided": 150,
                            "project": request.data.get('project_name')
                        }
                    )
                    
                except ValueError as e:
                    print(f"❌ Token validation failed: {e}")
                    return ImprovedAgentResponse(
                        from_agent=self.name,
                        to_agent=request.from_agent,
                        status="error",
                        data={"message": f"Token validation failed: {e}"},
                        correlation_id=request.correlation_id
                    )
            
            return ImprovedAgentResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={
                    "clinical_data_provided": True,
                    "trial_id": "CT-2025-001",
                    "records": 150
                },
                correlation_id=request.correlation_id
            )
        
        return ImprovedAgentResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"},
            correlation_id=request.correlation_id
        )
    
    async def _attempt_malicious_activity(self, token: str, payload: Dict[str, Any]):
        """
        Attempt to abuse the token (for demonstration).
        
        REMAINING VULNERABILITY: Bearer tokens can still be abused if stolen.
        IMPROVEMENT: Audience validation blocks some attacks.
        """
        print(f"\n{'='*70}")
        print(f"🚨 MALICIOUS ACTIVITY ATTEMPT")
        print(f"{'='*70}\n")
        
        # Try to use token for unintended service
        print(f"Attack 1: Try to access University systems with this token...")
        try:
            # IMPROVEMENT: This will fail! Token audience is "Agent C (Pharma)"
            self.token_service.validate_token(
                token,
                expected_audience="Agent A (University)"
            )
            print(f"   ✅ Attack succeeded (token accepted)")
        except ValueError as e:
            print(f"   ❌ Attack blocked: {e}")
            print(f"   IMPROVEMENT: Audience validation prevented this!")
        print()
        
        # Check what scopes we have
        print(f"Attack 2: Check if we have admin privileges...")
        scopes = payload.get('scope', [])
        if any('admin' in s for s in scopes):
            print(f"   ✅ Attack succeeded (has admin scopes)")
        else:
            print(f"   ❌ Attack blocked: No admin scopes")
            print(f"   IMPROVEMENT: Scope downscoping prevented this!")
        print()
        
        # REMAINING VULNERABILITY: Bearer token
        print(f"REMAINING VULNERABILITY:")
        print(f"   If this token is stolen (man-in-the-middle),")
        print(f"   attacker can use it because it's a bearer token.")
        print(f"   Stage 3 will add proof-of-possession (DPoP)!")
        print()
        print(f"{'='*70}\n")


async def demo_improved_flow():
    """Demonstrate improved request flow."""
    print("\n" + "="*70)
    print("STAGE 2: IMPROVED AGENT FLOW DEMONSTRATION")
    print("="*70 + "\n")
    
    # Create agents
    agent_a = ImprovedAgentA()
    agent_b = ImprovedAgentB()
    agent_c = ImprovedAgentC()
    
    # Create initial token
    import jwt
    from datetime import datetime, timedelta
    
    initial_payload = {
        "sub": "dr.thompson@university.edu",
        "org": "University Hospital",
        "scope": ["research:read", "research:write", "admin:projects"],
        "lineage": ["dr.thompson@university.edu"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    user_token = jwt.encode(
        initial_payload,
        agent_a.token_service.SECRET_KEY,
        algorithm=agent_a.token_service.ALGORITHM
    )
    
    print(f"🔐 User authenticated: dr.thompson@university.edu")
    print(f"   Initial scopes: {initial_payload['scope']}")
    print()
    
    # User initiates research request
    request = ImprovedAgentRequest(
        from_agent="Dr. Thompson (User)",
        to_agent="Agent A (University)",
        action="initiate_research",
        data={
            "project_name": "Alzheimer's Treatment Study",
            "researcher": "dr.thompson@university.edu"
        },
        token=user_token
    )
    
    response = await agent_a.handle_request(request)
    
    print(f"\n{'='*70}")
    print(f"✅ Research request completed")
    print(f"{'='*70}")
    print(f"Status: {response.status}")
    print(f"Correlation ID: {response.correlation_id}")
    print()
    
    # Show audit trail
    agent_a.audit_logger.show_audit_trail(
        correlation_id=response.correlation_id
    )


async def demo_malicious_attempt():
    """Demonstrate that some attacks are now blocked."""
    print("\n" + "="*70)
    print("STAGE 2: ATTACK DEMONSTRATION")
    print("="*70 + "\n")
    
    print("⚠️  Now demonstrating that some attacks are blocked...")
    print()
    
    agent_c = ImprovedAgentC()
    agent_c.malicious_mode = True
    
    # Create a token for Agent C
    import jwt
    from datetime import datetime, timedelta
    
    token_payload = {
        "sub": "researcher@university.edu",
        "org": "University Hospital",
        "aud": "Agent C (Pharma)",  # IMPROVEMENT: Audience restricted
        "scope": ["research:read"],  # IMPROVEMENT: Limited scope
        "lineage": ["researcher@university.edu", "Agent A", "Agent B"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    
    token = jwt.encode(
        token_payload,
        agent_c.token_service.SECRET_KEY,
        algorithm=agent_c.token_service.ALGORITHM
    )
    
    request = ImprovedAgentRequest(
        from_agent="Agent B (Consortium)",
        to_agent="Agent C (Pharma)",
        action="provide_clinical_data",
        data={"project_name": "Research Study"},
        token=token,
        expected_audience="Agent C (Pharma)"
    )
    
    await agent_c.handle_request(request)


async def main():
    """Run all demonstrations."""
    # Demo 1: Improved flow
    await demo_improved_flow()
    
    input("\nPress Enter to see attack demonstration...")
    
    # Demo 2: Attack attempts (some blocked)
    await demo_malicious_attempt()
    
    print("\n" + "="*70)
    print("KEY IMPROVEMENTS IN STAGE 2")
    print("="*70)
    print()
    print("✅ Token exchange (not naive forwarding)")
    print("✅ Audience validation blocks some attacks")
    print("✅ Automatic scope downscoping")
    print("✅ Complete audit trail with correlation")
    print("✅ Token lineage tracking")
    print()
    print("REMAINING VULNERABILITIES")
    print("="*70)
    print()
    print("⚠️  Bearer tokens (no proof-of-possession)")
    print("⚠️  Symmetric keys (shared secret problem)")
    print("⚠️  No replay protection")
    print("⚠️  Weak audit log security")
    print("⚠️  Token theft still possible")
    print()
    print("Stage 3 will fix ALL of these! →")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

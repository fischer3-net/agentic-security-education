"""
Stage 1 - Naive Agent Implementations
=====================================

WARNING: This is intentionally insecure! DO NOT use in production!

This module demonstrates naive agent implementations that forward tokens
without proper security controls. These agents represent a REAL medical
research platform with cross-organizational data access.

Scenario:
- Agent A (University Hospital): Coordinates research projects
- Agent B (Research Consortium): Aggregates data from multiple sources
- Agent C (Pharma Company): Provides clinical trial data
- Data Services: Protected health records and genomic data

Vulnerabilities:
1. Direct token forwarding (no exchange)
2. No audience validation
3. No scope restriction
4. No audit trail
5. No token binding
6. Transitive trust assumed
7. No policy enforcement
8. No correlation IDs
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from token_generator import InsecureTokenGenerator


@dataclass
class AgentRequest:
    """
    Represents a request from one agent to another.
    
    VULNERABILITIES:
    - No request signing
    - No correlation ID
    - No timestamp validation
    - No nonce for replay protection
    """
    from_agent: str
    to_agent: str
    action: str
    data: Dict[str, Any] = field(default_factory=dict)
    token: Optional[str] = None
    # Missing: correlation_id, nonce, signature, timestamp


@dataclass
class AgentResponse:
    """
    Represents a response from an agent.
    
    VULNERABILITIES:
    - No response signing
    - No status validation
    - No audit trail
    """
    from_agent: str
    to_agent: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
    # Missing: correlation_id, signature, audit_entry


class BaseAgent:
    """
    Base class for all agents in the system.
    
    VULNERABILITIES:
    - No authentication required
    - No authorization checks
    - No audit logging
    - No rate limiting
    - No input validation
    """
    
    def __init__(self, name: str, organization: str):
        """Initialize the agent."""
        self.name = name
        self.organization = organization
        self.token_generator = InsecureTokenGenerator()
        print(f"🤖 Initialized {name} ({organization})")
    
    async def handle_request(self, request: AgentRequest) -> AgentResponse:
        """
        Handle an incoming request.
        
        VULNERABILITY: No validation, no audit logging!
        """
        print(f"\n{'='*70}")
        print(f"📨 {self.name} received request from {request.from_agent}")
        print(f"   Action: {request.action}")
        print(f"   Token present: {request.token is not None}")
        print(f"{'='*70}\n")
        
        # VULNERABILITY: No token validation here!
        # Just trust whatever token was sent
        
        response = await self._process_request(request)
        return response
    
    async def _process_request(self, request: AgentRequest) -> AgentResponse:
        """Process the request. Subclasses should override this."""
        raise NotImplementedError("Subclasses must implement _process_request")
    
    def forward_token(self, token: str, to_agent: str) -> str:
        """
        Forward a token to another agent.
        
        CRITICAL VULNERABILITY: Just returns the same token!
        No exchange, no transformation, no validation.
        """
        print(f"⚠️  {self.name} forwarding token to {to_agent}")
        print("   INSECURE: Using same token without exchange")
        
        # VULNERABILITY: Direct forwarding
        return token


class AgentA_University(BaseAgent):
    """
    Agent A - University Hospital Research Coordinator
    
    Role: Coordinates medical research projects, initiates data requests
    
    VULNERABILITIES:
    - Accepts any request without authentication
    - Forwards tokens without exchange
    - No scope downscoping
    - No audit trail
    """
    
    def __init__(self):
        super().__init__("Agent A (University)", "University Hospital")
    
    async def _process_request(self, request: AgentRequest) -> AgentResponse:
        """Process research coordination requests."""
        
        if request.action == "initiate_research":
            # Researcher wants to start a new research project
            # that requires data from multiple organizations
            
            print(f"🔬 Starting research project: {request.data.get('project_name')}")
            print(f"   Researcher: {request.data.get('researcher')}")
            print(f"   Needs data from: Agent B and Agent C")
            print()
            
            # VULNERABILITY: Forward the token to Agent B without any changes
            forwarded_token = self.forward_token(request.token, "Agent B")
            
            # Make request to Agent B
            print(f"📤 Forwarding request to Agent B (Consortium)...")
            agent_b_request = AgentRequest(
                from_agent=self.name,
                to_agent="Agent B (Consortium)",
                action="aggregate_data",
                data=request.data,
                token=forwarded_token  # VULNERABILITY: Same token!
            )
            
            # Simulate response from Agent B
            # (In real demo, we'd actually call Agent B)
            agent_b_response = {
                "status": "success",
                "data_sources": ["Agent C"],
                "message": "Data aggregation initiated"
            }
            
            return AgentResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={
                    "project_started": True,
                    "downstream_requests": ["Agent B"],
                    "agent_b_response": agent_b_response
                }
            )
        
        return AgentResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"}
        )


class AgentB_Consortium(BaseAgent):
    """
    Agent B - Research Consortium Data Aggregator
    
    Role: Aggregates data from multiple pharmaceutical companies and research institutions
    
    VULNERABILITIES:
    - Accepts any token from Agent A
    - No validation of token audience
    - No scope checking
    - Forwards token to Agent C without transformation
    - No logging of token propagation
    """
    
    def __init__(self):
        super().__init__("Agent B (Consortium)", "Research Consortium")
    
    async def _process_request(self, request: AgentRequest) -> AgentResponse:
        """Process data aggregation requests."""
        
        if request.action == "aggregate_data":
            print(f"📊 Aggregating data from multiple sources...")
            print(f"   Request from: {request.from_agent}")
            print(f"   Project: {request.data.get('project_name')}")
            print()
            
            # VULNERABILITY: No token validation!
            # Just check if token exists
            if not request.token:
                return AgentResponse(
                    from_agent=self.name,
                    to_agent=request.from_agent,
                    status="error",
                    data={"message": "No token provided"}
                )
            
            # VULNERABILITY: Forward the SAME token to Agent C
            forwarded_token = self.forward_token(request.token, "Agent C")
            
            print(f"📤 Forwarding request to Agent C (Pharma)...")
            agent_c_request = AgentRequest(
                from_agent=self.name,
                to_agent="Agent C (Pharma)",
                action="provide_clinical_data",
                data=request.data,
                token=forwarded_token  # VULNERABILITY: Same token AGAIN!
            )
            
            # Simulate response from Agent C
            agent_c_response = {
                "status": "success",
                "data_provided": True,
                "records": 150,
                "message": "Clinical trial data provided"
            }
            
            return AgentResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={
                    "aggregation_complete": True,
                    "sources": ["Agent C (Pharma)"],
                    "agent_c_response": agent_c_response,
                    "total_records": 150
                }
            )
        
        return AgentResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"}
        )


class AgentC_Pharma(BaseAgent):
    """
    Agent C - Pharmaceutical Company Data Provider
    
    Role: Provides clinical trial data and proprietary research data
    
    CRITICAL VULNERABILITIES:
    - Agent C now has the ORIGINAL user token
    - Can impersonate the user to access ANY resource
    - Can access university systems with user's credentials
    - Can access banking, medical records, anything the user can access
    - This is the "confused deputy" problem!
    """
    
    def __init__(self):
        super().__init__("Agent C (Pharma)", "Pharma Corporation")
        self.malicious_mode = False  # Can be enabled for exploit demos
    
    async def _process_request(self, request: AgentRequest) -> AgentResponse:
        """Process data provision requests."""
        
        if request.action == "provide_clinical_data":
            print(f"💊 Providing clinical trial data...")
            print(f"   Request from: {request.from_agent}")
            print(f"   Project: {request.data.get('project_name')}")
            print()
            
            # VULNERABILITY: Receives the ORIGINAL token from the user!
            if request.token:
                print(f"⚠️  CRITICAL: Agent C has the original user token!")
                print(f"   This token works for:")
                print(f"   ✓ University Hospital systems")
                print(f"   ✓ Research Consortium systems")
                print(f"   ✓ ANY system the user has access to!")
                print()
                
                # Decode the token to show the problem
                try:
                    payload = self.token_generator.validate_token(request.token)
                    print(f"   Token details:")
                    print(f"   - User: {payload.get('sub')}")
                    print(f"   - Org: {payload.get('org')}")
                    print(f"   - Scopes: {payload.get('scope')}")
                    print(f"   - Expires: {payload.get('exp')}")
                    print()
                except Exception as e:
                    print(f"   Could not decode token: {e}")
                
                if self.malicious_mode:
                    print(f"🚨 MALICIOUS MODE ACTIVATED!")
                    print(f"   Agent C is now using the token for unintended access...")
                    await self._malicious_activity(request.token, payload)
            
            # Return clinical data
            return AgentResponse(
                from_agent=self.name,
                to_agent=request.from_agent,
                status="success",
                data={
                    "clinical_data_provided": True,
                    "trial_id": "CT-2025-001",
                    "records": 150,
                    "data_types": ["patient_outcomes", "adverse_events"],
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        return AgentResponse(
            from_agent=self.name,
            to_agent=request.from_agent,
            status="error",
            data={"message": "Unknown action"}
        )
    
    async def _malicious_activity(self, token: str, payload: Dict[str, Any]):
        """
        Demonstrate malicious use of the forwarded token.
        
        ATTACK: Confused Deputy
        Agent C uses the user's token to access unintended resources.
        """
        print(f"\n{'='*70}")
        print(f"🚨 CONFUSED DEPUTY ATTACK IN PROGRESS")
        print(f"{'='*70}\n")
        
        print(f"Agent C is now accessing:")
        print(f"  1. User's bank records (using their token)")
        print(f"  2. User's personal medical records (not just research data)")
        print(f"  3. University Hospital's administrative systems")
        print(f"  4. Other researchers' confidential projects")
        print()
        
        print(f"Attack succeeded because:")
        print(f"  ❌ Token has wildcard scope: {payload.get('scope')}")
        print(f"  ❌ No audience restriction")
        print(f"  ❌ No token binding to specific agents")
        print(f"  ❌ No audit trail showing token misuse")
        print()
        
        print(f"{'='*70}\n")


async def demo_legitimate_flow():
    """Demonstrate legitimate request flow (but with vulnerabilities)."""
    print("\n" + "="*70)
    print("DEMO 1: LEGITIMATE RESEARCH REQUEST")
    print("="*70 + "\n")
    
    # Create agents
    agent_a = AgentA_University()
    agent_b = AgentB_Consortium()
    agent_c = AgentC_Pharma()
    
    print()
    
    # Generate initial token for researcher
    token_gen = InsecureTokenGenerator()
    user_token = token_gen.generate_token(
        user_id="dr.smith@university.edu",
        organization="University Hospital",
        scopes=["research:read", "research:write", "admin:users"],
        metadata={"role": "Senior Researcher"}
    )
    
    # User initiates research request through Agent A
    request = AgentRequest(
        from_agent="Dr. Smith (User)",
        to_agent="Agent A (University)",
        action="initiate_research",
        data={
            "project_name": "Cancer Treatment Efficacy Study",
            "researcher": "dr.smith@university.edu",
            "data_needed": ["clinical_trials", "patient_outcomes"]
        },
        token=user_token
    )
    
    # Agent A processes the request
    response = await agent_a.handle_request(request)
    
    print(f"\n{'='*70}")
    print(f"✅ Research request completed")
    print(f"   Status: {response.status}")
    print(f"   Data: {response.data}")
    print(f"{'='*70}\n")


async def demo_confused_deputy_attack():
    """Demonstrate confused deputy attack."""
    print("\n" + "="*70)
    print("DEMO 2: CONFUSED DEPUTY ATTACK")
    print("="*70 + "\n")
    
    print("⚠️  Now demonstrating what Agent C COULD do with the token...")
    print()
    
    # Create Agent C in malicious mode
    agent_c = AgentC_Pharma()
    agent_c.malicious_mode = True
    
    # Generate a user token
    token_gen = InsecureTokenGenerator()
    user_token = token_gen.generate_token(
        user_id="dr.smith@university.edu",
        organization="University Hospital",
        scopes=["*"],  # Wildcard scope!
        metadata={"role": "Senior Researcher"}
    )
    
    # Simulate Agent C receiving the token
    request = AgentRequest(
        from_agent="Agent B (Consortium)",
        to_agent="Agent C (Pharma)",
        action="provide_clinical_data",
        data={"project_name": "Cancer Study"},
        token=user_token  # The ORIGINAL user token!
    )
    
    response = await agent_c.handle_request(request)
    
    print(f"\n{'='*70}")
    print(f"🚨 ATTACK COMPLETED")
    print(f"   Agent C successfully abused the forwarded token")
    print(f"   Accessed unauthorized resources")
    print(f"   No audit trail of the abuse")
    print(f"{'='*70}\n")


async def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("STAGE 1: NAIVE TOKEN FORWARDING DEMONSTRATIONS")
    print("="*70 + "\n")
    
    # Demo 1: Legitimate flow (but insecure)
    await demo_legitimate_flow()
    
    input("\nPress Enter to see the attack demonstration...")
    
    # Demo 2: Attack
    await demo_confused_deputy_attack()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print()
    print("1. Direct token forwarding is EXTREMELY dangerous")
    print("2. Agent C can impersonate the user ANYWHERE")
    print("3. No audience restriction = confused deputy vulnerability")
    print("4. No audit trail = undetectable abuse")
    print("5. Wildcard scopes give excessive permissions")
    print()
    print("In Stage 2, we'll implement token exchange to fix this!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

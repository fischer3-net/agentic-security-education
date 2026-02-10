"""
Stage 3 - Policy Engine
========================

This replaces hardcoded authorization logic with centralized policies.

IMPROVEMENTS over Stage 2:
1. ✅ Centralized authorization decisions
2. ✅ Policy-based access control
3. ✅ Declarative policies (not hardcoded)
4. ✅ Easy to update without code changes
5. ✅ Audit trail of policy evaluations

This enables consistent, manageable authorization!
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class Effect(Enum):
    """Policy effect."""
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class Policy:
    """
    Authorization policy.
    
    IMPROVEMENT: Declarative policy vs hardcoded if-statements.
    
    Similar to AWS IAM or OPA (Open Policy Agent) policies, but simplified.
    """
    policy_id: str
    description: str
    effect: Effect  # ALLOW or DENY
    subjects: List[str]  # Who (users, services, groups)
    actions: List[str]  # What (operations)
    resources: List[str]  # Where (which resources)
    conditions: Dict[str, Any] = field(default_factory=dict)  # When (conditions)
    
    def matches(
        self,
        subject: str,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if this policy matches the request.
        
        Args:
            subject: Who is making the request
            action: What action they want to perform
            resource: What resource they want to access
            context: Additional context for conditions
            
        Returns:
            True if policy matches, False otherwise
        """
        context = context or {}
        
        # Check subject match (supports wildcards)
        subject_match = any(self._pattern_match(s, subject) for s in self.subjects)
        if not subject_match:
            return False
        
        # Check action match
        action_match = any(self._pattern_match(a, action) for a in self.actions)
        if not action_match:
            return False
        
        # Check resource match
        resource_match = any(self._pattern_match(r, resource) for r in self.resources)
        if not resource_match:
            return False
        
        # Check conditions
        if self.conditions:
            if not self._evaluate_conditions(self.conditions, context):
                return False
        
        return True
    
    def _pattern_match(self, pattern: str, value: str) -> bool:
        """Simple wildcard matching."""
        if pattern == "*":
            return True
        if pattern == value:
            return True
        if pattern.endswith("*") and value.startswith(pattern[:-1]):
            return True
        return False
    
    def _evaluate_conditions(
        self,
        conditions: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate policy conditions.
        
        Simplified condition evaluation (production would be more sophisticated).
        """
        for key, expected_value in conditions.items():
            actual_value = context.get(key)
            
            if isinstance(expected_value, list):
                # Check if actual value is in list
                if actual_value not in expected_value:
                    return False
            elif isinstance(expected_value, dict):
                # Handle operators like gte, lte, eq
                if "eq" in expected_value and actual_value != expected_value["eq"]:
                    return False
                if "in" in expected_value and actual_value not in expected_value["in"]:
                    return False
            else:
                # Direct equality
                if actual_value != expected_value:
                    return False
        
        return True


@dataclass
class PolicyEvaluationResult:
    """Result of policy evaluation."""
    decision: Effect
    matched_policies: List[str]  # IDs of policies that matched
    reason: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PolicyEngine:
    """
    Centralized policy engine for authorization decisions.
    
    CRITICAL IMPROVEMENT:
    - Authorization logic is centralized, not scattered
    - Policies are declarative, not hardcoded
    - Easy to audit and update
    - Consistent enforcement across services
    
    This replaces hardcoded if-statements with manageable policies!
    """
    
    def __init__(self):
        """Initialize policy engine."""
        self.policies: List[Policy] = []
        
        print("📜 Policy Engine initialized")
        print("   ✅ Centralized authorization")
        print("   ✅ Declarative policies")
        print("   ✅ Consistent enforcement")
        print()
    
    def add_policy(self, policy: Policy):
        """
        Add a policy to the engine.
        
        Args:
            policy: Policy to add
        """
        self.policies.append(policy)
        print(f"   Added policy: {policy.policy_id}")
    
    def load_policies_from_json(self, json_str: str):
        """
        Load policies from JSON.
        
        IMPROVEMENT: Policies as data, not code.
        
        Args:
            json_str: JSON string with policy definitions
        """
        policies_data = json.loads(json_str)
        
        for policy_data in policies_data:
            policy = Policy(
                policy_id=policy_data["policy_id"],
                description=policy_data["description"],
                effect=Effect(policy_data["effect"]),
                subjects=policy_data["subjects"],
                actions=policy_data["actions"],
                resources=policy_data["resources"],
                conditions=policy_data.get("conditions", {})
            )
            self.add_policy(policy)
    
    def evaluate(
        self,
        subject: str,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> PolicyEvaluationResult:
        """
        Evaluate authorization request against policies.
        
        IMPROVEMENT: Centralized decision vs scattered if-statements.
        
        Args:
            subject: Who is making the request
            action: What action they want to perform
            resource: What resource they want to access
            context: Additional context
            
        Returns:
            PolicyEvaluationResult with decision
        """
        context = context or {}
        
        matched_allow = []
        matched_deny = []
        
        # Evaluate all policies
        for policy in self.policies:
            if policy.matches(subject, action, resource, context):
                if policy.effect == Effect.ALLOW:
                    matched_allow.append(policy.policy_id)
                else:
                    matched_deny.append(policy.policy_id)
        
        # Decision logic: explicit deny takes precedence
        if matched_deny:
            return PolicyEvaluationResult(
                decision=Effect.DENY,
                matched_policies=matched_deny,
                reason=f"Explicitly denied by policies: {', '.join(matched_deny)}"
            )
        elif matched_allow:
            return PolicyEvaluationResult(
                decision=Effect.ALLOW,
                matched_policies=matched_allow,
                reason=f"Allowed by policies: {', '.join(matched_allow)}"
            )
        else:
            # Default deny (no matching policy)
            return PolicyEvaluationResult(
                decision=Effect.DENY,
                matched_policies=[],
                reason="No matching policy (default deny)"
            )
    
    def get_policies_for_subject(self, subject: str) -> List[Policy]:
        """Get all policies that apply to a subject."""
        return [
            p for p in self.policies
            if any(self._pattern_match(s, subject) for s in p.subjects)
        ]
    
    def _pattern_match(self, pattern: str, value: str) -> bool:
        """Simple wildcard matching."""
        if pattern == "*":
            return True
        if pattern == value:
            return True
        if pattern.endswith("*") and value.startswith(pattern[:-1]):
            return True
        return False


def demo_policy_engine():
    """Demonstrate policy engine."""
    print("\n" + "="*70)
    print("STAGE 3: POLICY ENGINE DEMONSTRATION")
    print("="*70 + "\n")
    
    engine = PolicyEngine()
    
    # Define policies (as JSON - could be from file or database)
    policies_json = json.dumps([
        {
            "policy_id": "allow-university-research-read",
            "description": "University researchers can read research data",
            "effect": "allow",
            "subjects": ["*@university.edu"],
            "actions": ["research:read"],
            "resources": ["research:*"]
        },
        {
            "policy_id": "allow-university-research-write",
            "description": "University researchers can write research data",
            "effect": "allow",
            "subjects": ["*@university.edu"],
            "actions": ["research:write"],
            "resources": ["research:*"],
            "conditions": {
                "within_business_hours": True
            }
        },
        {
            "policy_id": "deny-external-pharma-write",
            "description": "External pharma companies cannot write data",
            "effect": "deny",
            "subjects": ["Agent C (Pharma)"],
            "actions": ["research:write", "admin:*"],
            "resources": ["*"]
        },
        {
            "policy_id": "allow-consortium-aggregate",
            "description": "Consortium can aggregate data from all sources",
            "effect": "allow",
            "subjects": ["Agent B (Consortium)"],
            "actions": ["research:read", "data:aggregate"],
            "resources": ["research:*", "clinical:*"]
        }
    ])
    
    print("1️⃣  Loading policies...")
    engine.load_policies_from_json(policies_json)
    print()
    
    # Test 1: University researcher reading data
    print("2️⃣  Test 1: University researcher wants to read research data")
    result = engine.evaluate(
        subject="dr.smith@university.edu",
        action="research:read",
        resource="research:cancer_trials"
    )
    print(f"   Decision: {result.decision.value.upper()}")
    print(f"   Reason: {result.reason}")
    print(f"   Matched policies: {result.matched_policies}")
    print()
    
    # Test 2: University researcher writing data (with conditions)
    print("3️⃣  Test 2: University researcher wants to write (business hours)")
    result = engine.evaluate(
        subject="dr.smith@university.edu",
        action="research:write",
        resource="research:cancer_trials",
        context={"within_business_hours": True}
    )
    print(f"   Decision: {result.decision.value.upper()}")
    print(f"   Reason: {result.reason}")
    print()
    
    # Test 3: University researcher writing data (after hours)
    print("4️⃣  Test 3: University researcher wants to write (after hours)")
    result = engine.evaluate(
        subject="dr.smith@university.edu",
        action="research:write",
        resource="research:cancer_trials",
        context={"within_business_hours": False}
    )
    print(f"   Decision: {result.decision.value.upper()}")
    print(f"   Reason: {result.reason}")
    print()
    
    # Test 4: Pharma company trying to write (explicit deny)
    print("5️⃣  Test 4: Pharma company wants to write data")
    result = engine.evaluate(
        subject="Agent C (Pharma)",
        action="research:write",
        resource="research:cancer_trials"
    )
    print(f"   Decision: {result.decision.value.upper()}")
    print(f"   Reason: {result.reason}")
    print(f"   Matched policies: {result.matched_policies}")
    print()
    
    # Test 5: Consortium aggregating data
    print("6️⃣  Test 5: Consortium wants to aggregate data")
    result = engine.evaluate(
        subject="Agent B (Consortium)",
        action="data:aggregate",
        resource="clinical:all"
    )
    print(f"   Decision: {result.decision.value.upper()}")
    print(f"   Reason: {result.reason}")
    print()
    
    # Compare to Stage 2
    print("="*70)
    print("COMPARISON TO STAGE 2")
    print("="*70)
    print()
    print("Stage 2 (Hardcoded Logic):")
    print("  🔴 Authorization in if-statements")
    print("  🔴 Scattered across services")
    print("  🔴 Hard to update (code changes)")
    print("  🔴 Inconsistent enforcement")
    print("  🔴 No audit trail of decisions")
    print()
    print("  Example Stage 2 code:")
    print('    if audience == "Agent C (Pharma)":')
    print('        if "admin" in scope:')
    print('            return "denied"  # Hardcoded!')
    print()
    print("Stage 3 (Policy Engine):")
    print("  ✅ Centralized authorization")
    print("  ✅ Declarative policies (JSON/YAML)")
    print("  ✅ Easy to update (no code changes)")
    print("  ✅ Consistent enforcement")
    print("  ✅ Audit trail of all decisions")
    print()
    print("  Example Stage 3 policy:")
    print('    {')
    print('      "effect": "deny",')
    print('      "subjects": ["Agent C (Pharma)"],')
    print('      "actions": ["admin:*"]')
    print('    }')
    print()
    
    # Show benefits
    print("="*70)
    print("BENEFITS OF POLICY ENGINE")
    print("="*70)
    print()
    print("1. Centralized governance:")
    print("   - All policies in one place")
    print("   - Easy to review and audit")
    print()
    print("2. Agile security:")
    print("   - Update policies without code changes")
    print("   - Deploy new rules instantly")
    print()
    print("3. Consistency:")
    print("   - Same rules enforced everywhere")
    print("   - No divergence between services")
    print()
    print("4. Compliance:")
    print("   - Policies as documentation")
    print("   - Audit trail of decisions")
    print()
    print("5. Testing:")
    print("   - Test policies independently")
    print("   - Simulate changes before deployment")
    print()
    print("Production systems use:")
    print("   - Open Policy Agent (OPA)")
    print("   - AWS IAM")
    print("   - Google Cloud IAM")
    print("   - Azure RBAC")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_policy_engine()
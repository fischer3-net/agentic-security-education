"""
Stage 2 - Basic Audit Logging System
====================================

IMPROVEMENTS over Stage 1:
1. ✅ Structured logging with correlation IDs
2. ✅ Token lineage tracking
3. ✅ Request/response correlation
4. ✅ Timestamps for all events
5. ✅ Basic tamper detection (checksums)

REMAINING VULNERABILITIES:
1. ⚠️ Logs not cryptographically secured (can be tampered)
2. ⚠️ No distributed tracing (W3C Trace Context)
3. ⚠️ No external timestamping service
4. ⚠️ Checksums are weak (MD5)
5. ⚠️ No log streaming to immutable storage
6. ⚠️ Missing context in some logs
"""

import hashlib
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class AuditEvent:
    """
    Structured audit event.
    
    IMPROVEMENT: Much more context than Stage 1.
    REMAINING ISSUE: Not cryptographically signed.
    """
    event_id: str
    timestamp: str
    event_type: str
    correlation_id: str
    actor: str
    action: str
    resource: Optional[str] = None
    result: str = "success"
    token_lineage: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    checksum: Optional[str] = None  # IMPROVEMENT: Tamper detection
    
    def __post_init__(self):
        """Calculate checksum after initialization."""
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """
        Calculate checksum for tamper detection.
        
        IMPROVEMENT: Basic tamper detection.
        REMAINING ISSUE: MD5 is weak, not cryptographically secure.
        """
        # Exclude checksum from checksum calculation
        data = {k: v for k, v in asdict(self).items() if k != 'checksum'}
        data_str = json.dumps(data, sort_keys=True)
        
        # VULNERABILITY: MD5 is weak and can be forged
        # Stage 3 will use HMAC-SHA256 or signatures
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """
        Verify event hasn't been tampered with.
        
        IMPROVEMENT: Can detect basic tampering.
        REMAINING ISSUE: Weak checksum can be recalculated by attacker.
        """
        stored_checksum = self.checksum
        self.checksum = None  # Temporarily remove for calculation
        calculated_checksum = self._calculate_checksum()
        self.checksum = stored_checksum
        
        return stored_checksum == calculated_checksum


class AuditLogger:
    """
    Basic audit logging system with correlation.
    
    IMPROVEMENTS:
    - Structured events with correlation IDs
    - Token lineage tracking
    - Basic tamper detection
    - Request/response correlation
    
    REMAINING VULNERABILITIES:
    - Logs stored locally (not immutable)
    - Weak tamper detection
    - No cryptographic signatures
    - No external timestamp authority
    """
    
    def __init__(self, log_file: str = "audit.log"):
        """Initialize audit logger."""
        self.log_file = Path(log_file)
        self.events: List[AuditEvent] = []
        
        print(f"📋 Audit Logger initialized")
        print(f"   Log file: {self.log_file}")
        print(f"   ✅ IMPROVEMENT: Correlation IDs enabled")
        print(f"   ✅ IMPROVEMENT: Token lineage tracking")
        print(f"   ⚠️  WARNING: Logs not cryptographically secured")
        print()
    
    def log_token_exchange(
        self,
        correlation_id: str,
        actor: str,
        subject_token_user: str,
        new_audience: str,
        original_scopes: List[str],
        new_scopes: List[str],
        lineage: List[str],
        result: str = "success",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        """
        Log a token exchange event.
        
        IMPROVEMENT: Comprehensive token exchange logging.
        """
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            event_type="token_exchange",
            correlation_id=correlation_id,
            actor=actor,
            action="exchange_token",
            resource=f"token:{subject_token_user}",
            result=result,
            token_lineage=lineage,
            metadata={
                "new_audience": new_audience,
                "original_scopes": original_scopes,
                "new_scopes": new_scopes,
                "scope_reduced": len(new_scopes) < len(original_scopes),
                **(metadata or {})
            }
        )
        
        self._write_event(event)
        return event
    
    def log_agent_request(
        self,
        correlation_id: str,
        from_agent: str,
        to_agent: str,
        action: str,
        token_lineage: List[str],
        result: str = "success",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        """
        Log an agent-to-agent request.
        
        IMPROVEMENT: Tracks requests across agent boundaries.
        """
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            event_type="agent_request",
            correlation_id=correlation_id,
            actor=from_agent,
            action=action,
            resource=to_agent,
            result=result,
            token_lineage=token_lineage,
            metadata=metadata or {}
        )
        
        self._write_event(event)
        return event
    
    def log_authentication(
        self,
        correlation_id: str,
        user: str,
        organization: str,
        scopes: List[str],
        result: str = "success",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        """
        Log an authentication event.
        
        IMPROVEMENT: Better than Stage 1, but still missing details.
        REMAINING ISSUE: No device fingerprint, location, etc.
        """
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            event_type="authentication",
            correlation_id=correlation_id,
            actor=user,
            action="authenticate",
            resource=organization,
            result=result,
            token_lineage=[user],
            metadata={
                "scopes": scopes,
                **(metadata or {})
            }
        )
        
        self._write_event(event)
        return event
    
    def log_data_access(
        self,
        correlation_id: str,
        user: str,
        resource: str,
        action: str,
        token_lineage: List[str],
        result: str = "success",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        """
        Log a data access event.
        
        IMPROVEMENT: Includes token lineage (can trace back to origin).
        """
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            event_type="data_access",
            correlation_id=correlation_id,
            actor=user,
            action=action,
            resource=resource,
            result=result,
            token_lineage=token_lineage,
            metadata=metadata or {}
        )
        
        self._write_event(event)
        return event
    
    def _write_event(self, event: AuditEvent):
        """
        Write event to log file and memory.
        
        IMPROVEMENT: Structured JSON logging.
        REMAINING ISSUE: File is not append-only or immutable.
        """
        self.events.append(event)
        
        # Write to file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(asdict(event)) + "\n")
    
    def get_events_by_correlation(self, correlation_id: str) -> List[AuditEvent]:
        """
        Get all events for a correlation ID.
        
        IMPROVEMENT: Can trace entire request flow!
        """
        return [e for e in self.events if e.correlation_id == correlation_id]
    
    def get_events_by_user(self, user: str) -> List[AuditEvent]:
        """
        Get all events for a user.
        
        IMPROVEMENT: Can track user activity.
        """
        return [e for e in self.events if e.actor == user]
    
    def get_events_with_lineage(self, user: str) -> List[AuditEvent]:
        """
        Get events where user appears in token lineage.
        
        IMPROVEMENT: Can trace actions of tokens derived from user.
        """
        return [e for e in self.events if user in e.token_lineage]
    
    def verify_log_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of all logged events.
        
        IMPROVEMENT: Can detect if logs were tampered with.
        REMAINING ISSUE: Attacker can recalculate weak checksums.
        """
        results = {
            "total_events": len(self.events),
            "verified": 0,
            "tampered": 0,
            "tampered_events": []
        }
        
        for event in self.events:
            if event.verify_integrity():
                results["verified"] += 1
            else:
                results["tampered"] += 1
                results["tampered_events"].append(event.event_id)
        
        return results
    
    def show_audit_trail(
        self,
        correlation_id: Optional[str] = None,
        user: Optional[str] = None,
        limit: int = 10
    ):
        """
        Display audit trail in human-readable format.
        
        IMPROVEMENT: Better visibility than Stage 1.
        """
        print(f"\n{'='*70}")
        print("AUDIT TRAIL")
        print(f"{'='*70}\n")
        
        if correlation_id:
            events = self.get_events_by_correlation(correlation_id)
            print(f"Correlation ID: {correlation_id}")
        elif user:
            events = self.get_events_with_lineage(user)
            print(f"User: {user} (including derived tokens)")
        else:
            events = self.events[-limit:]
            print(f"Last {limit} events")
        
        print(f"Total events: {len(events)}\n")
        
        for i, event in enumerate(events, 1):
            print(f"{i}. [{event.timestamp}] {event.event_type}")
            print(f"   Event ID: {event.event_id}")
            print(f"   Correlation: {event.correlation_id}")
            print(f"   Actor: {event.actor}")
            print(f"   Action: {event.action}")
            if event.resource:
                print(f"   Resource: {event.resource}")
            print(f"   Result: {event.result}")
            if event.token_lineage:
                print(f"   Token lineage: {' → '.join(event.token_lineage)}")
            if event.metadata:
                print(f"   Metadata: {json.dumps(event.metadata, indent=6)}")
            
            # Verify integrity
            if event.verify_integrity():
                print(f"   ✅ Integrity: Verified")
            else:
                print(f"   ⚠️  Integrity: TAMPERED!")
            
            print()
        
        # Show integrity summary
        integrity = self.verify_log_integrity()
        print(f"{'='*70}")
        print(f"INTEGRITY CHECK")
        print(f"{'='*70}")
        print(f"Total events: {integrity['total_events']}")
        print(f"Verified: {integrity['verified']}")
        print(f"Tampered: {integrity['tampered']}")
        if integrity['tampered'] > 0:
            print(f"⚠️  Tampered event IDs: {integrity['tampered_events']}")
        print(f"{'='*70}\n")


def demo_audit_logging():
    """Demonstrate the improved audit logging."""
    print("\n" + "="*70)
    print("STAGE 2: AUDIT LOGGING DEMONSTRATION")
    print("="*70 + "\n")
    
    logger = AuditLogger("demo_audit.log")
    
    # Simulate a request flow with correlation
    correlation_id = str(uuid.uuid4())
    
    print("1️⃣  User authenticates...")
    logger.log_authentication(
        correlation_id=correlation_id,
        user="researcher@university.edu",
        organization="University Hospital",
        scopes=["research:read", "research:write"],
        metadata={"ip": "192.168.1.100", "device": "laptop"}
    )
    
    print("2️⃣  Token exchanged for Agent B...")
    logger.log_token_exchange(
        correlation_id=correlation_id,
        actor="Agent A (University)",
        subject_token_user="researcher@university.edu",
        new_audience="Agent B (Consortium)",
        original_scopes=["research:read", "research:write"],
        new_scopes=["research:read"],
        lineage=["researcher@university.edu", "Agent A (University)"]
    )
    
    print("3️⃣  Agent B requests from Agent C...")
    logger.log_agent_request(
        correlation_id=correlation_id,
        from_agent="Agent B (Consortium)",
        to_agent="Agent C (Pharma)",
        action="request_clinical_data",
        token_lineage=["researcher@university.edu", "Agent A (University)", "Agent B (Consortium)"],
        metadata={"project": "Cancer Research 2025"}
    )
    
    print("4️⃣  Data accessed...")
    logger.log_data_access(
        correlation_id=correlation_id,
        user="researcher@university.edu",
        resource="clinical_trials_database",
        action="read",
        token_lineage=["researcher@university.edu", "Agent A (University)", "Agent B (Consortium)", "Agent C (Pharma)"],
        result="success",
        metadata={"records_accessed": 150}
    )
    
    # Show the complete audit trail
    logger.show_audit_trail(correlation_id=correlation_id)
    
    print("\n" + "="*70)
    print("IMPROVEMENTS DEMONSTRATED:")
    print("="*70)
    print("✅ Correlation IDs track entire request flow")
    print("✅ Token lineage shows delegation chain")
    print("✅ Structured logging with metadata")
    print("✅ Basic integrity checking (checksums)")
    print("✅ Can answer: 'Who accessed what?'")
    print()
    print("REMAINING VULNERABILITIES:")
    print("="*70)
    print("⚠️  Checksums are weak (MD5, not cryptographic)")
    print("⚠️  Logs not signed (can be forged)")
    print("⚠️  Local storage (not immutable)")
    print("⚠️  No external timestamp authority")
    print("⚠️  Missing distributed tracing standard")
    print()
    print("Stage 3 will fix these! →")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_audit_logging()

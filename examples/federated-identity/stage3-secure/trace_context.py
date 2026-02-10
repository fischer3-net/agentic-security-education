"""
Stage 3 - W3C Trace Context
============================

This replaces Stage 2's custom correlation IDs with industry standard.

IMPROVEMENTS over Stage 2:
1. ✅ W3C Trace Context standard (not custom UUIDs)
2. ✅ Interoperates with observability tools (Jaeger, Zipkin, etc.)
3. ✅ Distributed tracing across service boundaries
4. ✅ Automatic span creation
5. ✅ Trace state propagation

This enables proper distributed tracing!
"""

import secrets
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class TraceContext:
    """
    W3C Trace Context as defined in W3C Recommendation.
    
    IMPROVEMENT: Industry standard vs custom correlation IDs.
    
    Format:
        traceparent: 00-{trace-id}-{parent-id}-{trace-flags}
        tracestate: vendor1=value1,vendor2=value2
    """
    version: str = "00"  # Current W3C standard version
    trace_id: str = ""   # 32 hex characters (128 bits)
    parent_id: str = ""  # 16 hex characters (64 bits)
    trace_flags: str = "01"  # 2 hex characters (sampled=01, not sampled=00)
    trace_state: Dict[str, str] = None  # Optional vendor-specific state
    
    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = secrets.token_hex(16)  # 128 bits
        if not self.parent_id:
            self.parent_id = secrets.token_hex(8)  # 64 bits
        if self.trace_state is None:
            self.trace_state = {}
    
    def to_traceparent_header(self) -> str:
        """
        Generate traceparent header value.
        
        Format: 00-{trace-id}-{parent-id}-{trace-flags}
        Example: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
        """
        return f"{self.version}-{self.trace_id}-{self.parent_id}-{self.trace_flags}"
    
    def to_tracestate_header(self) -> Optional[str]:
        """
        Generate tracestate header value.
        
        Format: vendor1=value1,vendor2=value2
        Example: congo=t61rcWkgMzE,rojo=00f067aa0ba902b7
        """
        if not self.trace_state:
            return None
        
        parts = [f"{key}={value}" for key, value in self.trace_state.items()]
        return ",".join(parts)
    
    @classmethod
    def from_traceparent_header(cls, header_value: str) -> 'TraceContext':
        """
        Parse traceparent header.
        
        Args:
            header_value: traceparent header value
            
        Returns:
            TraceContext object
            
        Raises:
            ValueError: If header format is invalid
        """
        parts = header_value.split("-")
        
        if len(parts) != 4:
            raise ValueError(f"Invalid traceparent format: {header_value}")
        
        version, trace_id, parent_id, trace_flags = parts
        
        # Validate lengths
        if len(trace_id) != 32:
            raise ValueError(f"Invalid trace_id length: {len(trace_id)}, expected 32")
        if len(parent_id) != 16:
            raise ValueError(f"Invalid parent_id length: {len(parent_id)}, expected 16")
        
        return cls(
            version=version,
            trace_id=trace_id,
            parent_id=parent_id,
            trace_flags=trace_flags
        )
    
    @classmethod
    def from_tracestate_header(cls, trace_context: 'TraceContext', header_value: str) -> 'TraceContext':
        """
        Parse tracestate header and add to existing TraceContext.
        
        Args:
            trace_context: Existing TraceContext
            header_value: tracestate header value
            
        Returns:
            Updated TraceContext
        """
        if not header_value:
            return trace_context
        
        parts = header_value.split(",")
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                trace_context.trace_state[key.strip()] = value.strip()
        
        return trace_context
    
    def create_child_span(self) -> 'TraceContext':
        """
        Create a child span context.
        
        IMPROVEMENT: Proper parent-child relationship for distributed tracing.
        
        Returns:
            New TraceContext with same trace_id but new parent_id
        """
        return TraceContext(
            version=self.version,
            trace_id=self.trace_id,  # Same trace
            parent_id=secrets.token_hex(8),  # New span ID
            trace_flags=self.trace_flags,
            trace_state=self.trace_state.copy()  # Inherit state
        )


class TraceContextPropagator:
    """
    Propagates W3C Trace Context across service boundaries.
    
    IMPROVEMENT: Standard propagation vs custom correlation ID passing.
    
    This enables:
    - Distributed tracing across services
    - Integration with APM tools (Datadog, New Relic, etc.)
    - Standard observability practices
    """
    
    @staticmethod
    def inject(trace_context: TraceContext) -> Dict[str, str]:
        """
        Inject trace context into HTTP headers.
        
        Args:
            trace_context: TraceContext to inject
            
        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            "traceparent": trace_context.to_traceparent_header()
        }
        
        tracestate = trace_context.to_tracestate_header()
        if tracestate:
            headers["tracestate"] = tracestate
        
        return headers
    
    @staticmethod
    def extract(headers: Dict[str, str]) -> Optional[TraceContext]:
        """
        Extract trace context from HTTP headers.
        
        Args:
            headers: HTTP request headers
            
        Returns:
            TraceContext if present, None otherwise
        """
        # Headers are case-insensitive, normalize
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        traceparent = headers_lower.get("traceparent")
        if not traceparent:
            return None
        
        try:
            trace_context = TraceContext.from_traceparent_header(traceparent)
            
            # Extract tracestate if present
            tracestate = headers_lower.get("tracestate")
            if tracestate:
                trace_context = TraceContext.from_tracestate_header(
                    trace_context, tracestate
                )
            
            return trace_context
            
        except ValueError as e:
            print(f"⚠️  Invalid trace context in headers: {e}")
            return None


def demo_trace_context():
    """Demonstrate W3C Trace Context."""
    print("\n" + "="*70)
    print("STAGE 3: W3C TRACE CONTEXT DEMONSTRATION")
    print("="*70 + "\n")
    
    # Create root trace context
    print("1️⃣  Creating root trace context...")
    root_context = TraceContext()
    print(f"   Trace ID: {root_context.trace_id}")
    print(f"   Span ID: {root_context.parent_id}")
    print(f"   Traceparent: {root_context.to_traceparent_header()}")
    print()
    
    # Simulate Agent A -> Agent B
    print("2️⃣  Agent A calling Agent B...")
    print()
    
    # Agent A creates child span
    agent_b_context = root_context.create_child_span()
    print(f"   New Span ID: {agent_b_context.parent_id}")
    print(f"   (Same Trace ID: {agent_b_context.trace_id})")
    print()
    
    # Agent A injects into HTTP headers
    headers_to_b = TraceContextPropagator.inject(agent_b_context)
    print(f"   HTTP Headers sent to Agent B:")
    for key, value in headers_to_b.items():
        print(f"      {key}: {value}")
    print()
    
    # Agent B receives and extracts
    print("3️⃣  Agent B receives request...")
    extracted_context = TraceContextPropagator.extract(headers_to_b)
    print(f"   Extracted Trace ID: {extracted_context.trace_id}")
    print(f"   Extracted Span ID: {extracted_context.parent_id}")
    print()
    
    # Agent B -> Agent C
    print("4️⃣  Agent B calling Agent C...")
    agent_c_context = extracted_context.create_child_span()
    headers_to_c = TraceContextPropagator.inject(agent_c_context)
    
    print(f"   New Span ID: {agent_c_context.parent_id}")
    print(f"   (Still same Trace ID: {agent_c_context.trace_id})")
    print()
    
    # Show the complete trace
    print("="*70)
    print("COMPLETE TRACE")
    print("="*70)
    print()
    print(f"Trace ID: {root_context.trace_id}")
    print()
    print("Spans:")
    print(f"  1. Root:    {root_context.parent_id}")
    print(f"  2. Agent B: {agent_b_context.parent_id}")
    print(f"  3. Agent C: {agent_c_context.parent_id}")
    print()
    print("All three spans are part of the same distributed trace!")
    print()
    
    # Compare to Stage 2
    print("="*70)
    print("COMPARISON TO STAGE 2")
    print("="*70)
    print()
    print("Stage 2 (Custom Correlation IDs):")
    print("  ⚠️  UUID correlation IDs (custom format)")
    print("  ⚠️  No standard parent-child relationships")
    print("  ⚠️  Cannot integrate with APM tools")
    print("  ⚠️  Manual correlation ID passing")
    print()
    print("Stage 3 (W3C Trace Context):")
    print("  ✅ Industry standard format")
    print("  ✅ Proper span hierarchy")
    print("  ✅ Works with Jaeger, Zipkin, DataDog, etc.")
    print("  ✅ Automatic propagation via HTTP headers")
    print("  ✅ Observability tooling integration")
    print()
    
    # Show integration benefits
    print("="*70)
    print("OBSERVABILITY BENEFITS")
    print("="*70)
    print()
    print("With W3C Trace Context, you can:")
    print()
    print("1. Visualize request flows:")
    print("   User → Agent A → Agent B → Agent C")
    print("   With timing for each hop")
    print()
    print("2. Find bottlenecks:")
    print("   Which service is slow?")
    print("   Where is latency introduced?")
    print()
    print("3. Debug failures:")
    print("   Which service failed?")
    print("   What was the error?")
    print()
    print("4. Use standard tools:")
    print("   - Jaeger: Distributed tracing UI")
    print("   - Zipkin: Trace visualization")
    print("   - DataDog/New Relic: Full APM")
    print("   - OpenTelemetry: Telemetry collection")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_trace_context()
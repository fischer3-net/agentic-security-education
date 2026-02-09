# Stage 5: ADK Orchestrated — Structure & Design

> **Location**: `examples/a2a_credit_report_example/adk_orchestrated/`  
> **Builds on**: Stage 4 (AI-Integrated) — all Stage 3 security + Gemini AI  
> **New capability**: Google ADK orchestration layer with multi-agent coordination  
> **Security Rating target**: 10/10 (production orchestrated deployment)

---

## Directory Structure

Mirrors Stage 4's layout, adding ADK-specific layers:

```
adk_orchestrated/
├── orchestrator/
│   ├── credit_orchestrator.py          # Root ADK agent (Custom Agent)
│   ├── routing_policy.py               # Orchestrator routing logic & guardrails
│   └── session_security.py            # Shared state protection (session.state)
├── agents/
│   ├── validation_agent.py             # Sub-agent: input/file validation
│   ├── analysis_agent.py               # Sub-agent: AI credit analysis (wraps Stage 4)
│   ├── compliance_agent.py             # Sub-agent: FCRA/GDPR checks
│   └── report_agent.py                 # Sub-agent: final report generation
├── security/
│   ├── authentication.py              # (from Stage 3) RSA + nonce
│   ├── validation.py                  # (from Stage 3) 8-layer validation
│   ├── protection.py                  # (from Stage 3) rate limiting, RBAC, PII
│   ├── ai_security.py                 # (from Stage 4) prompt injection, PII scrub
│   ├── orchestrator_security.py       # NEW: ADK-specific security controls
│   └── callback_guards.py             # NEW: ADK callback hooks for security checks
├── tools/
│   ├── credit_lookup_tool.py          # FunctionTool: external credit bureau lookup
│   ├── compliance_check_tool.py       # FunctionTool: regulatory rule engine
│   └── report_generator_tool.py       # FunctionTool: PDF/JSON report output
├── config/
│   ├── agent_definitions.py           # ADK agent hierarchy definitions
│   └── security_policy.yaml           # Trust policy: what orchestrator can delegate
├── tests/
│   ├── test_orchestration_flow.py     # End-to-end orchestration tests
│   ├── test_trust_boundaries.py       # Verify sub-agent isolation
│   └── test_attack_scenarios.py       # Orchestrator-specific attack tests
├── requirements.txt                   # google-adk, google-generativeai, google-auth
└── README.md
```

---

## ADK Architecture — Mapped to Credit Report

!["ADK Architecture Mapped to Credit Report"](/docs/images/diagrams/adk_orchesterated_design.jpg "ADK Architecture Mapped to Credit Report")

### Why These Four Sub-Agents

Each maps to a distinct phase of credit report processing that the current monolithic Stage 4 agent handles in a single class. Splitting them demonstrates the core ADK value — and creates the trust boundary questions that make the threat model exercise rich.

**ValidationAgent** — receives raw input, runs the 8-layer validation stack. First line of defense. Nothing else runs until this passes.

**AnalysisAgent** — the Stage 4 Gemini integration, now isolated as a sub-agent. It only sees sanitized, PII-scrubbed data passed to it via session.state. This is the agent where prompt injection against the orchestrator becomes interesting — can an attacker craft input that, after passing validation, manipulates the orchestrator into feeding the analysis agent a poisoned context?

**ComplianceAgent** — checks the analysis result against FCRA adverse action requirements, GDPR data minimization rules. Runs after analysis, before the report is finalized. Acts as a gate.

**ReportAgent** — assembles the final output. Only runs if compliance passes. Generates the customer-facing credit decision with required disclosures.

---

## ADK Primitives in Play

| Primitive | Used For | Security Implication |
|-----------|----------|---------------------|
| `Custom Agent` | CreditOrchestrator — explicit routing logic | Orchestrator logic is deterministic, not LLM-driven. Reduces routing-based prompt injection risk. |
| `LlmAgent` | Each sub-agent | Each has its own `instruction` and `output_key`. Instructions are attack surface — learners must audit them. |
| `FunctionTool` | Credit lookup, compliance check, report gen | Tools execute with the permissions of the invoking agent. Tool-level auth needed. |
| `AgentTool` | (optional) Wrapping sub-agents as callable tools for the orchestrator | Exposes sub-agent as a tool — changes trust model vs. direct sub_agents list. |
| `session.state` | Data flow between agents | **Shared mutable state.** All sub-agents in the same invocation can read/write. Primary cross-agent attack surface. |
| `Callbacks` | Security hooks at agent lifecycle points | `on_agent_start`, `on_tool_start`, etc. Where Stage 3/4 controls plug in. |
| `output_key` | Each sub-agent writes results here | Determines what flows to the next stage. Poisoning an output_key value = poisoning downstream agents. |

---

## New Trust Boundaries (Not in Stages 1–4)

These are the boundaries that don't exist in the standalone agent and that learners need to identify in the threat model exercise.

### Boundary 1: Orchestrator → Sub-Agent Delegation

The orchestrator decides which sub-agent runs, in what order, and what context it receives. A compromised orchestrator can skip validation, feed poisoned state to the analysis agent, or suppress compliance checks entirely.

**Question for learners**: What prevents the orchestrator from bypassing the ValidationAgent and sending raw user input directly to the AnalysisAgent?

**Answer**: Nothing architectural — it's a policy enforcement problem. This is what `routing_policy.py` and `session_security.py` address.

### Boundary 2: Shared session.state

ADK's state is designed for convenience — agents pass data to each other through a shared dictionary. But it means any sub-agent can read or overwrite any other sub-agent's output.

**Question for learners**: If the ValidationAgent writes `state['validated_report']` and the AnalysisAgent reads it, what stops the ValidationAgent from writing a malicious value that the AnalysisAgent will trust?

**Answer**: Sub-agent isolation policies enforced via callbacks. Each agent should only write to its designated output_key, and reads should be type-checked.

### Boundary 3: Tool Execution Authority

When the AnalysisAgent invokes the Gemini AI tool, it runs with whatever permissions the agent has. The tool doesn't know or care whether the agent was given legitimate context or poisoned context.

**Question for learners**: How does the system ensure that sensitive PII doesn't reach the external Gemini API call, even though the tool is invoked by the agent (not directly by the orchestrator)?

**Answer**: PII scrubbing happens in a callback guard before any tool with an external endpoint fires. This is `callback_guards.py` — the ADK equivalent of Stage 4's `AISecurityManager`.

### Boundary 4: Cross-Sub-Agent Influence via Orchestrator

A prompt injection in user input might not compromise ValidationAgent directly. But if it manipulates the orchestrator's routing decision (e.g., causes it to run AnalysisAgent before validation completes), the effect cascades.

**Question for learners**: In an LLM-driven routing scenario (vs. the deterministic Custom Agent pattern used here), how would prompt injection in a user's credit report filename influence which sub-agent runs next?

**Answer**: This is why the Stage 5 example deliberately uses a Custom Agent (deterministic routing) rather than LLM-driven transfer. The lesson contrasts both approaches.

---

## Security Controls — What's New vs. Inherited

### Inherited from Stage 3 (via callbacks)

| Control | Stage 3 Location | Stage 5 Integration Point |
|---------|-----------------|--------------------------|
| RSA + nonce auth | `authentication.py` | ADK `on_agent_start` callback — validates caller before any agent runs |
| 8-layer validation | `validation.py` | ValidationAgent wraps this entirely. Runs as first sub-agent. |
| Rate limiting | `protection.py` | Applied at Runner level — limits total invocations per session |
| RBAC | `protection.py` | Mapped to ADK agent roles: which callers can trigger which sub-agents |
| PII sanitization | `protection.py` | Callback guard: strips PII before any state write |

### Inherited from Stage 4

| Control | Stage 4 Location | Stage 5 Integration Point |
|---------|-----------------|--------------------------|
| Prompt injection detection | `ai_security.py` | Callback guard on AnalysisAgent's tool invocations |
| PII scrubbing for AI | `ai_security.py` | Runs before AnalysisAgent writes to session.state |
| AI rate limiting | `ai_security.py` | Separate rate limiter on AnalysisAgent tool calls |
| AI output validation | `ai_security.py` | Callback on AnalysisAgent output_key write |

### New in Stage 5

| Control | File | What It Does |
|---------|------|-------------|
| Orchestrator routing policy | `routing_policy.py` | Enforces execution order. ValidationAgent must complete successfully before any other agent runs. No skipping. |
| Shared state protection | `session_security.py` | Each sub-agent gets a write-only view of its designated output_key. Read access is scoped per agent. Prevents cross-agent state poisoning. |
| Callback guards | `callback_guards.py` | Security hooks at `on_agent_start`, `on_tool_start`, `on_tool_end`. PII checks, auth checks, and output validation all fire here. |
| Sub-agent isolation policy | `orchestrator_security.py` | Defines which sub-agent can call which tools. AnalysisAgent cannot invoke the report generator tool directly — must go through orchestrator. |
| Trust policy configuration | `security_policy.yaml` | Declarative policy: what the orchestrator is allowed to delegate, to whom, under what conditions. Single source of truth for the trust model. |

---

## Execution Flow — Happy Path
!["Execution Flow"](/docs/images/diagrams/execution_flow_happy_path.jpg "Execution Flow")

---

## Threat Model Implications for the Lesson

This is the section that connects directly to the evaluation exercise. These are the questions the Stage 5 system is designed to surface.

**STRIDE categories expanded by ADK:**

| STRIDE | New Threats from Orchestration | Not Present in Stages 1–4 |
|--------|-------------------------------|---------------------------|
| Spoofing | Sub-agent impersonation within the hierarchy | ✅ New |
| Tampering | Poisoning session.state between agents | ✅ New |
| Repudiation | Orchestrator denies it delegated a specific task | ✅ New |
| Info Disclosure | Sub-agent reads state it shouldn't have access to | ✅ New |
| Denial of Service | Infinite loop via LoopAgent misconfiguration | ✅ New |
| Elevation of Privilege | Sub-agent invokes tool outside its authorized scope | ✅ New |

**Ground truth development needed:**
- CVSS scores for each orchestrator-specific threat
- CWE mappings (CWE-94 for state injection, CWE-610 for external resource delegation, etc.)
- Exploitation scenarios with code
- Mitigation mapping to specific controls in Stage 5

---

## Relationship to Existing Stages

!["Relationship to Existing Stages"](/docs/images/diagrams/relationship_to_existing_stages.jpg)

Stage 5 does not replace Stages 1–4. It wraps them. The credit agent logic from Stage 4 becomes the AnalysisAgent. The validation stack from Stage 3 becomes the ValidationAgent. The orchestrator is the new surface area.

---

## Dependencies

```
# requirements.txt
google-adk>=0.5.0                    # ADK framework
google-generativeai>=0.3.0           # Gemini (carried from Stage 4)
google-auth>=2.0.0                   # GCP auth (service accounts, ADC)
google-cloud-logging>=3.0.0          # Audit logging (optional, from adversarial example)
pyyaml>=6.0                          # Security policy config
```

**Local execution**: ADK CLI supports local agent execution without GCP deployment. Demo mode pattern from Stage 4 applies here — all external calls can be mocked.

---

## Implementation Priority

Build order matters — each piece depends on the previous:

1. **Agent definitions** (`config/agent_definitions.py`) — the skeleton. Defines hierarchy, output_keys, instructions. Everything else hangs off this.
2. **Orchestrator** (`orchestrator/credit_orchestrator.py`) — the routing logic. Deterministic Custom Agent, not LLM-driven.
3. **Sub-agents** (`agents/*.py`) — wrap existing Stage 3/4 logic into ADK agent classes.
4. **Callback guards** (`security/callback_guards.py`) — plug Stage 3/4 security into ADK lifecycle hooks.
5. **State protection** (`orchestrator/session_security.py`) — enforce write isolation on session.state.
6. **Routing policy** (`orchestrator/routing_policy.py`) — enforce execution order and delegation rules.
7. **Trust policy config** (`config/security_policy.yaml`) — declarative policy document.
8. **Tools** (`tools/*.py`) — FunctionTool wrappers for external calls.
9. **Tests** (`tests/*.py`) — verify both happy path and attack scenarios.
10. **Security analysis** (`SECURITY_ANALYSIS.md`) — document all ADK-specific threats with CVSS/CWE. This is the ground truth for the lesson.
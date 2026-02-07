# Stage 1: Insecure Federated Identity Implementation

## ⚠️ WARNING: INTENTIONALLY INSECURE

This implementation is **deliberately vulnerable** for educational purposes. **NEVER use this code in production!**

## 📚 Overview

This stage demonstrates the catastrophic failures that occur when implementing federated identity without proper security controls. The implementation uses naive token forwarding across organizational boundaries, creating multiple critical vulnerabilities.

### Scenario: Multi-Organization Medical Research Platform

**Actors:**
- **User:** Medical researcher at University Hospital
- **Agent A (Research Coordinator):** University Hospital's agent system
- **Agent B (Data Aggregator):** Research consortium's shared agent
- **Agent C (Data Provider):** Pharmaceutical company's agent
- **Data Services:** Protected health records, clinical trial data, genomic databases

**Token Flow:**
```
User → Agent A → Agent B → Agent C → Data Services
     [Token 1]  [Token 1]  [Token 1]  [Token 1]
     
PROBLEM: All agents use the SAME token!
```

## 🎯 Learning Objectives

By studying this stage, you will learn:

1. **Why naive token forwarding fails** (confused deputy problem)
2. **The dangers of wildcard scopes** (privilege escalation)
3. **Why replay protection is critical** (token theft)
4. **The importance of audit logging** (forensic analysis)
5. **Non-repudiation requirements** (compliance)

## 🚨 Critical Vulnerabilities (20+)

### Token Exchange and Propagation

1. ❌ **Direct token forwarding** - No token exchange
2. ❌ **No audience restriction** - Token works anywhere
3. ❌ **No scope limitation** - Wildcard scopes (`*`)
4. ❌ **Bearer tokens** - No proof-of-possession
5. ❌ **24-hour expiration** - Extremely long-lived

### Trust Boundary Paradox

6. ❌ **Transitive trust assumed** - All agents trusted equally
7. ❌ **No trust level differentiation** - One size fits all
8. ❌ **Agent credentials reused** - Shared secrets
9. ❌ **No policy enforcement** - No boundaries
10. ❌ **Single point of compromise** - Affects all organizations

### Auditability

11. ❌ **No correlation IDs** - Can't trace requests
12. ❌ **Missing token lineage** - Can't track propagation
13. ❌ **No distributed tracing** - Lost context
14. ❌ **Insufficient logging** - Missing critical events
15. ❌ **Can't determine original requestor** - Lost in chain

### Non-Repudiation

16. ❌ **No cryptographic proof** - Can't prove actions
17. ❌ **Logs can be tampered** - No integrity protection
18. ❌ **No timestamping service** - No trusted time
19. ❌ **Can't prove who accessed what** - Deniability
20. ❌ **No receipts** - No acknowledgments

## 📁 File Structure

```
stage1-insecure/
├── token_generator.py      # Insecure JWT generator
├── naive_agents.py          # Agent implementations with naive forwarding
├── exploits/                # Attack demonstrations
│   ├── confused_deputy.py   # Exploit 1: Confused deputy attack
│   ├── token_replay.py      # Exploit 2: Token replay attack
│   ├── scope_escalation.py  # Exploit 3: Scope escalation attack
│   ├── audit_evasion.py     # Exploit 4: Audit evasion attack
│   ├── token_leakage.py     # Exploit 5: Token exposure attack
│   └── symmetric_key_compromise.py  # Exploit 6: Key compromise attack
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── docker-compose.yml      # Docker setup (optional)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip or uv for package management

### Installation

```bash
# Navigate to stage1-insecure directory
cd stage1-insecure

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or with uv (faster):
uv pip install -r requirements.txt
```

### Running the Examples

#### 1. Basic Token Generation Demo

```bash
python token_generator.py
```

**What you'll see:**
- Token generation with weak security
- Naive token forwarding
- Same token used across all hops

#### 2. Agent Interaction Demo

```bash
python naive_agents.py
```

**What you'll see:**
- Legitimate request flow (but insecure)
- Confused deputy attack demonstration
- Token forwarding without transformation

#### 3. Individual Exploits

```bash
# Confused Deputy Attack
python exploits/confused_deputy.py

# Token Replay Attack
python exploits/token_replay.py

# Scope Escalation Attack
python exploits/scope_escalation.py

# Audit Evasion Attack
python exploits/audit_evasion.py

# Token Leakage Attack
python exploits/token_leakage.py

# Symmetric Key Compromise Attack
python exploits/symmetric_key_compromise.py
```

## 🎯 Attack Demonstrations

### Exploit 1: Confused Deputy Attack

**Demonstrates:** How Agent C can impersonate the user to access ANY resource

**Key Points:**
- Agent C receives the original user token
- Can access university systems, bank records, etc.
- No audit trail of abuse
- Complete account takeover possible

**Run:**
```bash
python exploits/confused_deputy.py
```

**Expected Output:**
- Shows 4 successful unauthorized accesses
- Financial data exposed
- Patient privacy violated (HIPAA)
- Research IP stolen
- Persistent backdoor created

### Exploit 2: Token Replay Attack

**Demonstrates:** How intercepted tokens can be replayed indefinitely

**Key Points:**
- No nonce/jti for replay protection
- 24-hour expiration window
- Works from any location
- No binding to original context

**Run:**
```bash
python exploits/token_replay.py
```

**Expected Output:**
- Token intercepted at 2 points
- Immediate replay succeeds
- Replay 8 hours later succeeds
- Replay from foreign country succeeds
- All replays undetected

### Exploit 3: Scope Escalation Attack

**Demonstrates:** How wildcard scopes enable privilege escalation

**Key Points:**
- Wildcard scopes (`*`, `admin:*`)
- Read-only → Write access
- User role → Admin role
- No scope downscoping

**Run:**
```bash
python exploits/scope_escalation.py
```

**Expected Output:**
- 3 scenarios of scope abuse
- Read escalated to write
- User escalated to admin
- Research access → Finance access

### Exploit 4: Audit Evasion Attack

**Demonstrates:** How inadequate logging enables undetectable attacks

**Key Points:**
- No correlation IDs
- Missing token lineage
- Can't trace multi-hop requests
- Can't prove unauthorized access

**Run:**
```bash
python exploits/audit_evasion.py
```

**Expected Output:**
- Inadequate audit log displayed
- 5 questions that can't be answered
- Compliance failures highlighted
- Forensic analysis impossible

### Exploit 5: Token Leakage Attack

**Demonstrates:** How tokens are exposed through logs, URLs, and other channels

**Key Points:**
- Tokens logged in plain text
- Tokens in URL query parameters
- Tokens in error messages
- Tokens sent to third parties
- 8+ exposure vectors

**Run:**
```bash
python exploits/token_leakage.py
```

**Expected Output:**
- Token leaked in 8+ locations
- Log files created with tokens
- Browser history exposure shown
- Third-party analytics exposure
- Backup/archive risks demonstrated

### Exploit 6: Symmetric Key Compromise Attack

**Demonstrates:** Catastrophic impact when shared secret is compromised

**Key Points:**
- Forge tokens for any user/organization
- 5 ways to obtain the secret
- Complete system compromise
- Cannot detect forged tokens
- $5-10M remediation cost

**Run:**
```bash
python exploits/symmetric_key_compromise.py
```

**Expected Output:**
- Forged CEO token accepted
- Forged government agent token
- Backdoor admin created
- Rogue agent inserted
- Complete trust breakdown

## 📊 Vulnerability Summary Table

| Category | Vulnerabilities | CWE References | Severity |
|----------|----------------|----------------|----------|
| **Token Handling** | Direct forwarding, no exchange, no binding | CWE-441, CWE-668 | CRITICAL |
| **Authentication** | Weak secrets, symmetric keys, no rotation | CWE-321, CWE-798 | HIGH |
| **Authorization** | Wildcard scopes, no downscoping | CWE-269, CWE-266 | HIGH |
| **Replay Protection** | No nonce, long expiration, no revocation | CWE-294, CWE-384 | HIGH |
| **Audit Logging** | No correlation, missing context | CWE-778, CWE-223 | CRITICAL |
| **Non-Repudiation** | No signatures, tamperable logs | CWE-778 | HIGH |
| **Token Exposure** | Logs, URLs, errors, third parties | CWE-532, CWE-200, CWE-598 | CRITICAL |
| **Cryptographic** | Symmetric keys, weak secrets, shared secrets | CWE-321, CWE-326, CWE-327 | CATASTROPHIC |

## 🎓 Study Guide

### For Beginners (3-4 hours)

1. **Read this README** (15 min)
2. **Run token_generator.py** (15 min)
   - Understand JWT structure
   - See weak security parameters
3. **Run naive_agents.py** (30 min)
   - Follow legitimate flow
   - See confused deputy attack
4. **Run two exploits** (1 hour)
   - confused_deputy.py (recommended)
   - token_leakage.py (high impact)
5. **Compare to Stage 2** (1 hour)

### For Intermediate (5-7 hours)

1. **Complete beginner path** (3-4 hours)
2. **Run all 6 exploits** (2.5 hours)
   - Take notes on each vulnerability
   - Map to CWE references
   - Compare attack techniques
3. **Code review** (1-2 hours)
   - Read token_generator.py
   - Read naive_agents.py
   - Identify all vulnerabilities
4. **Plan fixes** (1 hour)
   - What needs to change in Stage 2?
   - Draft improvement list

### For Advanced (10-12 hours)

1. **Complete intermediate path** (5-7 hours)
2. **Write your own exploit** (2-3 hours)
   - Combine multiple vulnerabilities
   - Create a new attack scenario
3. **Analyze audit logs** (1 hour)
   - What's missing?
   - Design ideal log structure
4. **Study RFCs** (2-3 hours)
   - RFC 8693 (Token Exchange)
   - RFC 9449 (DPoP)
   - RFC 3161 (Timestamping)
5. **Start Stage 2** implementation plan

## 🔄 Progression to Stage 2

In Stage 2, we'll implement:

1. **Token Exchange** (basic, symmetric keys)
   - Replace direct forwarding
   - Add audience restriction
   - Implement scope validation

2. **Improved Logging**
   - Add correlation IDs
   - Track token lineage
   - Structured logging

3. **Basic Trust Boundaries**
   - Define trust levels
   - Implement boundary checks

**Note:** Stage 2 is still vulnerable but shows incremental improvements!

## 📚 References

### Security Standards
- **OAuth 2.0 Token Exchange:** RFC 8693
- **Proof-of-Possession:** RFC 9449 (DPoP)
- **Timestamping:** RFC 3161
- **Distributed Tracing:** W3C Trace Context

### CWE References
- **CWE-441:** Unintended Proxy or Intermediary (Confused Deputy)
- **CWE-294:** Authentication Bypass by Capture-replay
- **CWE-269:** Improper Privilege Management
- **CWE-778:** Insufficient Logging
- **CWE-668:** Exposure of Resource to Wrong Sphere

### Compliance
- **SOC 2 Type II:** Logging and monitoring requirements
- **HIPAA:** Audit trails for PHI access
- **GDPR:** Right to know who accessed data
- **PCI DSS:** Forensic data requirements

## 🤔 Discussion Questions

1. **Why is direct token forwarding so dangerous?**
   - What trust assumptions are violated?
   - What's the worst-case scenario?

2. **How would you explain the confused deputy problem to non-technical stakeholders?**
   - What analogy works best?
   - What's the business impact?

3. **Why isn't expiration time enough for security?**
   - What attacks still work within expiration?
   - How short would expiration need to be?

4. **What makes audit logs "good enough" for compliance?**
   - What questions must they answer?
   - How do you prove integrity?

5. **If you could fix only ONE vulnerability, which would it be and why?**
   - Consider impact vs. effort
   - Think about compliance requirements

## 🆘 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'jwt'`
**Solution:**
```bash
pip install PyJWT
# or
uv pip install PyJWT
```

**Issue:** `ImportError: cannot import name 'InsecureTokenGenerator'`
**Solution:** Make sure you're running exploits from the stage1-insecure directory:
```bash
cd stage1-insecure
python exploits/confused_deputy.py
```

**Issue:** Exploits run but show no output
**Solution:** Check that print statements are working. Try:
```bash
python -u exploits/confused_deputy.py
```

## 📝 Notes for Instructors

### Teaching Approach

1. **Start with demonstrations, not theory**
   - Run exploits first
   - Show the "wow" factor
   - Then explain why it happened

2. **Use the medical research scenario**
   - Relatable and realistic
   - Clear stakes (patient privacy)
   - Multiple organizations (trust boundaries)

3. **Connect to compliance**
   - HIPAA violations resonate
   - SOC 2 requirements concrete
   - GDPR fines are motivating

4. **Emphasize "this is real"**
   - Show CVE examples of confused deputy
   - Discuss OAuth 1.0 → 2.0 evolution
   - Share breach case studies

### Assessment Ideas

- Have students identify all 20+ vulnerabilities
- Ask them to write their own exploit
- Have them design Stage 2 improvements
- Create a compliance checklist
- Write an incident response plan

## 🔗 What's Next?

Ready to see improvements? → **[Stage 2: Improved Implementation](../stage2-improved/)**

Want to jump to security? → **[Stage 3: Secure Implementation](../stage3-secure/)**

Curious about production? → **[Stage 4: Okta Integration](../stage4-okta/)**

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Status:** ⚠️ Intentionally Insecure - Educational Use Only

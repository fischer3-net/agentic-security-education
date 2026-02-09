# Stage 2: Partial Security - Sophisticated Attacks Succeed

## Overview

**Security Rating**: 4/10 ⚠️  
**Attack Success Rate**: 40-60% (sophisticated attacks)  
**Time to Compromise**: 2-5 minutes  
**Purpose**: Demonstrate that "better" ≠ "secure"

---

## What This Example Teaches

Stage 2 adds **partial security controls** to the Stage 1 system:

- ✅ JWT authentication added
- ✅ RBAC authorization added
- ✅ Schema validation added
- ✅ Basic logging added

**But sophisticated attacks still succeed**, teaching that incomplete security creates **false confidence**.

---

## Security Improvements Over Stage 1

### Added: JWT Authentication

```python
# Agents must register with password
auth_manager.register_agent("worker-001", "password", role="worker")
# Returns: JWT token (24-hour expiration)

# All operations require token
message = {
    "type": "status_update",
    "auth_token": "eyJ0eXAiOiJKV1Qi...",  # Required!
    ...
}
```

**Blocks**:
- ✅ Anonymous access (100% prevented)
- ✅ Simple identity spoofing (100% prevented)

**Doesn't Block**:
- ⚠️ Token replay (no nonces)
- ⚠️ Role escalation (trusted requests)

---

### Added: Role-Based Access Control

**Three Roles**:

| Role | Permissions |
|------|-------------|
| **Worker** | Read/update own tasks only |
| **Manager** | Read/update all tasks, create tasks |
| **Admin** | Everything (full control) |

**Blocks**:
- ✅ Workers accessing other agents' tasks (100% prevented)
- ✅ Unauthorized deletions (100% prevented)

**Doesn't Block**:
- ⚠️ Self-granted admin roles (no verification)
- ⚠️ Malicious use of granted permissions

---

### Added: Input Validation

```python
# Validates message structure
validator.validate_message({
    "type": "status_update",
    "task_id": "task-001",      # ✅ Required field
    "status": "in_progress",    # ✅ Type checked
    "details": {...}            # ⚠️ Only top-level validated!
})
```

**Blocks**:
- ✅ Malformed messages (100% prevented)
- ✅ Wrong field types (100% prevented)
- ✅ Obvious credential leakage (95% prevented)

**Doesn't Block**:
- ⚠️ Deep-nested malicious data (100% bypass)

---

## Four Bypass Attacks

### Attack 1: Role Escalation via Unverified Requests

**CWE**: [CWE-269: Improper Privilege Management](https://cwe.mitre.org/data/definitions/269.html)  
**CVSS**: 9.1 (Critical)  
**Success Rate**: 100% ✅

**How it bypasses Stage 2 security**:

```python
# Stage 2 blocks simple attacks...
register_as_worker()  # ✅ Works fine

# But doesn't verify role requests!
response = manager.register_agent({
    "type": "register",
    "agent_id": "attacker",
    "password": "password",
    "requested_role": "admin"  # System grants it!
})

# Result: Instant admin access
```

**Why it works**:
- System trusts `requested_role` field
- No approval workflow
- No identity verification
- No admin authorization

**Impact**: Complete system compromise in 30 seconds

**Demo Output**:
```
Step 2: Register ANOTHER Agent as Admin
✅ ATTACK SUCCESSFUL!
   Granted role: admin
   Agent ID: attacker-admin-001
   Has admin token: eyJ0eXAiOiJKV1QiLCJh...

Impact Assessment:
❌ CRITICAL: Instant admin access without verification
❌ Can read all data
❌ Can modify all tasks
❌ Can delete anything
❌ Complete system compromise
```

---

### Attack 2: Deep-Nested Data Exfiltration

**CWE**: [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)  
**CVSS**: 8.6 (High)  
**Success Rate**: 100% ✅

**How it bypasses Stage 2 security**:

```python
# Stage 2 validates top-level fields...
status_update = {
    "type": "status_update",
    "task_id": "task-001",
    "status": "in_progress",      # ✅ Validated
    "details": {                   # ✅ Allowed field
        "message": "Working...",   # ✅ Top-level validated
        "metadata": {              # ⚠️ NOT deeply checked!
            "technical_info": {    # ❌ Level 3: ignored
                "debug_data": {    # ❌ Level 4: ignored
                    "internal": {  # ❌ Level 5: ignored
                        "stolen_data": {
                            "customer_records": [...],  # Exfiltrated!
                            "credentials": {...},       # Stolen!
                            "api_keys": {...}          # Compromised!
                        }
                    }
                }
            }
        }
    }
}
```

**Why it works**:
- Validator only checks top-level
- No recursive validation
- No depth limits
- No size limits on nested content

**Nesting visualization**:
```
details                    ← Level 1: ✅ Validated
└── metadata               ← Level 2: ⚠️ Allowed but not validated
    └── technical_info     ← Level 3: ❌ Completely unchecked
        └── debug_data     ← Level 4: ❌ Invisible to validator
            └── stolen     ← Level 5+: ❌ Perfect hiding spot!
```

**Impact**: Unlimited data exfiltration (~2MB per message)

**Demo Output**:
```
Step 3: Send Malicious Update
✅ ATTACK SUCCESSFUL!
   Status update accepted
   Stolen data stored in system
   Payload size: ~1847 bytes

Step 4: Verify Data Was Stored
Confirmed: Malicious data stored in database
   Nested levels deep: 5+
   Contains: 2 customer records
   Contains: 3 API keys
```

---

### Attack 3: Token Replay Attack

**CWE**: [CWE-294: Authentication Bypass via Capture-Replay](https://cwe.mitre.org/data/definitions/294.html)  
**CVSS**: 8.1 (High)  
**Success Rate**: 100% ✅

**How it bypasses Stage 2 security**:

```python
# Intercept a legitimate message (network sniffing)
intercepted_message = {
    "type": "status_update",
    "agent_id": "legitimate-worker",
    "task_id": "task-001",
    "status": "completed",
    "auth_token": "eyJ0eXAiOiJKV1Qi..."  # Valid token
}

# Replay the SAME message multiple times
for i in range(100):
    send(intercepted_message)  # All accepted!
```

**Why it works**:
- No nonces (number used once)
- No request signing
- No timestamp verification beyond token expiry
- Same token reusable for 24 hours

**Impact**: 24-hour replay window, unlimited reuse

**Demo Output**:
```
Step 3: Replay Message Multiple Times
Replaying same message 5 times...
   Replay 1: ✅ ACCEPTED
   Replay 2: ✅ ACCEPTED
   Replay 3: ✅ ACCEPTED
   Replay 4: ✅ ACCEPTED
   Replay 5: ✅ ACCEPTED

✅ ATTACK SUCCESSFUL!
   5/5 replays accepted
   Same token reused multiple times
   No replay detection
```

---

### Attack 4: Legitimate API Abuse

**CWE**: [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html)  
**CVSS**: 7.5 (High)  
**Success Rate**: 100% ✅

**How it bypasses Stage 2 security**:

```python
# After gaining admin role (via Attack 1)
if has_admin_permissions():
    # Use legitimate API maliciously
    all_tasks = get_all_tasks()
    
    for task in all_tasks:
        # Sabotage with "authorized" operations
        task["priority"] = "low"           # Deprioritize everything
        task["assigned_to"] = "attacker"   # Steal all work
        task["description"] = "CANCELLED"  # Sabotage
        update_task(task)  # ✅ Allowed - has permission!
```

**Why it works**:
- No behavioral analysis
- No anomaly detection
- No rate limiting
- No pattern recognition
- Permissions used maliciously

**Impact**: System-wide sabotage using "legitimate" access

**Demo Output**:
```
Step 2: Mass Sabotage Using Admin API
Using legitimate WRITE_ALL_TASKS permission maliciously...
   Task task-a3f8c2... sabotaged ✅
   Task task-7b2e91... sabotaged ✅
   Task task-4d9f3a... sabotaged ✅
   Task task-8c1b76... sabotaged ✅
   Task task-2e5a94... sabotaged ✅

✅ ATTACK SUCCESSFUL!
   Sabotaged 5/5 tasks
   All changes legitimate (has WRITE_ALL_TASKS)
   No behavioral monitoring detected abuse
```

---

## Attack Success Matrix

| Attack Type | Stage 1 | Stage 2 | Improvement |
|-------------|---------|---------|-------------|
| **Simple Attacks** | | | |
| Anonymous access | ✅ 100% | ❌ 0% | ✅ Blocked |
| Identity spoofing | ✅ 100% | ❌ 0% | ✅ Blocked |
| Malformed messages | ✅ 100% | ❌ 0% | ✅ Blocked |
| Obvious data leaks | ✅ 100% | ❌ 5% | ✅ Mostly blocked |
| **Sophisticated Attacks** | | | |
| Role escalation | ✅ 100% | ✅ 100% | ❌ No improvement |
| Deep-nested exfil | ✅ 100% | ✅ 100% | ❌ No improvement |
| Token replay | N/A | ✅ 100% | ⚠️ New vulnerability |
| API abuse | ✅ 100% | ✅ 100% | ❌ No improvement |
| **Overall** | **100%** | **45%** | **55% improvement** |

**Key Insight**: Simple attacks blocked, sophisticated attacks succeed

---

## Running the Attacks

### Installation

```bash
# Clone repository
git clone https://github.com/robertfischer3/fischer3_a2a_introduction.git
cd fischer3_a2a_introduction/examples/adversarial_agents/stage2_partial

# Install dependencies
pip install -r requirements.txt

# Run attack demonstrations
python agents/malicious_worker.py
```

### Expected Output

```
═══════════════════════════════════════════════════════
 STAGE 2 BYPASS ATTACKS
═══════════════════════════════════════════════════════

Demonstrating sophisticated attacks that bypass Stage 2 security

[Attack 1: Role Escalation]
✅ ATTACK SUCCESSFUL!
   Granted role: admin
   Complete system compromise

[Attack 2: Deep-Nested Exfiltration]
✅ ATTACK SUCCESSFUL!
   Stolen data stored in system
   Contains: 2 customer records, 3 API keys

[Attack 3: Token Replay]
✅ ATTACK SUCCESSFUL!
   5/5 replays accepted

[Attack 4: API Abuse]
✅ ATTACK SUCCESSFUL!
   Sabotaged 5/5 tasks

═══════════════════════════════════════════════════════
 ATTACK SUMMARY
═══════════════════════════════════════════════════════

✅ Successful Attacks: 4/4

🎓 LESSON: Partial security creates false confidence
   Simple attacks blocked, but sophisticated attacks succeed
   Stage 3 addresses these with comprehensive defense
```

---

## Code Structure

```
stage2_partial/
├── README.md                        # Quick reference
├── auth/
│   ├── auth_manager.py             # JWT authentication (HS256)
│   └── __init__.py
├── security/
│   ├── permission_manager.py       # RBAC (3 roles)
│   ├── validator.py                # Schema validation (top-level)
│   └── __init__.py
├── core/
│   ├── protocol.py                 # Auth-enabled messages
│   ├── utils.py                    # Security utilities
│   ├── task_queue.py               # Permission-integrated queue
│   ├── project_manager.py          # Fully integrated
│   └── __init__.py
├── agents/
│   ├── malicious_worker.py         # 4 bypass attacks
│   ├── legitimate_worker.py        # Proper usage
│   └── __init__.py
├── requirements.txt                # PyJWT, bcrypt
└── SECURITY_ANALYSIS.md            # Detailed analysis
```

**Total Code**: ~3,500 lines  
**Security Modules**: 3 (Auth, Authz, Validation)  
**Bypass Attacks**: 4 complete demonstrations  
**Documentation**: ~2,100 lines

---

## Learning Objectives

After completing this module, you should understand:

### Technical Implementation
- [ ] How JWT authentication works
- [ ] How RBAC is implemented
- [ ] How schema validation operates
- [ ] How security layers integrate

### Security Concepts
- [ ] Why partial security fails
- [ ] Defense in depth necessity
- [ ] Importance of comprehensive validation
- [ ] Why behavioral analysis is needed

### Attack Evolution
- [ ] How attackers adapt to defenses
- [ ] Data hiding in nested structures
- [ ] TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities
- [ ] Legitimate API abuse patterns

---

## Comparison with Other Stages

| Feature | Stage 1 | Stage 2 | Stage 3 |
|---------|---------|---------|---------|
| **Authentication** | ❌ None | ✅ JWT (HS256) | ✅ JWT (RS256) + MFA |
| **Authorization** | ❌ None | ⚠️ RBAC | ✅ Capability-based |
| **Validation** | ❌ None | ⚠️ Top-level | ✅ Deep recursive |
| **Replay Protection** | ❌ None | ❌ None | ✅ Nonce-based |
| **Behavioral Analysis** | ❌ None | ❌ None | ✅ Real-time monitoring |
| **Logging** | ❌ None | ⚠️ Basic | ✅ Comprehensive + HMAC |
| **Attack Success** | 100% | 45% | 0% |
| **Security Rating** | 0/10 | 4/10 | 10/10 |

---

## Next Steps

### Understand the Vulnerabilities

1. **Study the bypass attacks**: See how they work
2. **Run the demonstrations**: Experience the exploits
3. **Read the security analysis**: Understand the gaps

### Progress to Stage 3

Ready to see complete security?

👉 [Stage 3: Production Security](stage3-adversarial.md)

Learn how comprehensive defense in depth blocks **all** attacks.

### Deep Dive

For complete technical details:

- [Security Analysis](https://github.com/robertfischer3/fischer3_a2a_introduction/blob/main/examples/adversarial_agents/stage2_partial/SECURITY_ANALYSIS.md)
- [Source Code](https://github.com/robertfischer3/fischer3_a2a_introduction/tree/main/examples/adversarial_agents/stage2_partial)
- [README](https://github.com/robertfischer3/fischer3_a2a_introduction/blob/main/examples/adversarial_agents/stage2_partial/README.md)

---

## Video Walkthrough

📹 Coming soon: Bypass attack demonstrations

---

## Key Takeaway

> **Partial security is dangerous because it creates false confidence while sophisticated attacks still succeed.**

Stage 2 demonstrates why security must be:
- **Comprehensive** (all layers complete)
- **Deep** (recursive validation)
- **Behavioral** (anomaly detection)
- **Proactive** (automated response)

This motivates the complete approach in Stage 3.

---

## Credits

**Created by**: Robert Fischer (robert@fischer3.org)  
**License**: MIT - Educational use  
**Status**: Complete ✅  
**Part of**: [Multi-Agent Security Education Project](../index.md)

---

**Last Updated**: January 2026  
**Version**: 2.0  
**Difficulty**: Intermediate  
**Time to Complete**: 4-6 hours
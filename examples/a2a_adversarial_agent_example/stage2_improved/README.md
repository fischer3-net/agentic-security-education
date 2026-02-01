# Stage 2: Improved Security - Adversarial Agent Attack

## ⚠️ Educational Implementation with Partial Security

**Security Rating**: 4/10 ⚠️  
**Attack Success Rate**: 40-60% (sophisticated attacks still work)  
**Purpose**: Demonstrate that **"Better ≠ Secure"**

---

## 🎯 Purpose

Stage 2 demonstrates what happens when a system adds **partial security controls**. While simple attacks are blocked, sophisticated attackers can still compromise the system by:

1. **Escalating privileges** via unverified role requests
2. **Exfiltrating data** through deep-nested structures
3. **Replaying tokens** due to lack of nonce protection
4. **Abusing legitimate APIs** with granted permissions

**Key Teaching Point**: Partial security creates false confidence while sophisticated attacks still succeed.

---

## 📊 Stage 1 vs Stage 2 Comparison

| Feature | Stage 1 | Stage 2 | Improvement |
|---------|---------|---------|-------------|
| **Authentication** | None ❌ | JWT (HS256) ✅ | Added |
| **Authorization** | None ❌ | RBAC (3 roles) ✅ | Added |
| **Input Validation** | None ❌ | Schema + Patterns ✅ | Added |
| **Audit Logging** | None ❌ | Basic logging ✅ | Added |
| **Simple Attacks** | 100% succeed | 20% succeed ✅ | Blocked |
| **Sophisticated Attacks** | 100% succeed | 70% succeed ⚠️ | Still vulnerable |
| **Overall Security** | 0/10 | 4/10 | Partial improvement |

---

## 🔐 Security Improvements Over Stage 1

### ✅ Added: JWT Authentication

**What it does**:
- Agents must register with password (bcrypt hashed)
- JWT token issued on registration/login
- Token required for all operations
- 24-hour token expiration
- Simple token blacklist for revocation

**What it blocks**:
- ✅ Anonymous access
- ✅ Identity spoofing (simple)
- ✅ Unauthenticated operations

**What it doesn't block**:
- ⚠️ Token replay (no nonces)
- ⚠️ Token theft (if intercepted)
- ⚠️ Role escalation (trusted roles)

---

### ✅ Added: Role-Based Access Control (RBAC)

**Three roles defined**:

**Worker** (default):
- Read own tasks
- Update own tasks
- Complete own tasks

**Manager**:
- All worker permissions
- Read all tasks
- Update all tasks
- Create new tasks

**Admin**:
- All permissions
- Can do anything

**What it blocks**:
- ✅ Workers modifying other agents' tasks
- ✅ Unauthorized task creation
- ✅ Unauthorized deletions

**What it doesn't block**:
- ⚠️ Self-granted admin roles
- ⚠️ Malicious use of granted permissions
- ⚠️ Privilege escalation during registration

---

### ✅ Added: Input Validation

**Validates**:
- Message type and structure (5 schemas)
- Field types (string, int, dict, etc.)
- Required fields present
- Suspicious patterns (API keys, SSNs, credit cards)
- Top-level field whitelisting

**What it blocks**:
- ✅ Malformed messages
- ✅ Wrong field types
- ✅ Obvious credential leakage
- ✅ Missing required fields

**What it doesn't block**:
- ⚠️ **Deep-nested malicious data**
- ⚠️ Data hidden in nested structures
- ⚠️ Large payloads in nested fields
- ⚠️ Semantic attacks

---

## 🔴 Remaining Vulnerabilities (Intentional)

### V1: Role Escalation via Unverified Requests

**CWE**: CWE-269 (Improper Privilege Management)  
**CVSS**: 9.1 (Critical)

**How it works**:
```python
# Request admin role during registration
response = manager.register_agent({
    "type": "register",
    "agent_id": "attacker",
    "password": "password123",
    "requested_role": "admin"  # ⚠️ Granted without verification!
})
# System trusts the request and grants admin
```

**Impact**: Instant admin access, can do anything

**Why it works**: No verification of who should have what role

**Fix in Stage 3**: Role verification workflow with approval

---

### V2: Deep-Nested Data Exfiltration

**CWE**: CWE-20 (Improper Input Validation)  
**CVSS**: 8.6 (High)

**How it works**:
```python
# Validator only checks top-level
status_update = {
    "type": "status_update",
    "task_id": "task-001",
    "status": "in_progress",
    "details": {  # ✅ Allowed top-level field
        "message": "Processing...",  # ✅ Validated
        "metadata": {  # ⚠️ Not deeply validated!
            "technical": {
                "debug_info": {
                    "customer_records": [...],  # ❌ Hidden data!
                    "credentials": {...}  # ❌ Exfiltrated!
                }
            }
        }
    }
}
# Top-level validated, nested content ignored
```

**Impact**: Complete data breach via nested structures

**Why it works**: Validator only checks top-level fields

**Fix in Stage 3**: Recursive deep validation at all nesting levels

---

### V3: Token Replay Attacks

**CWE**: CWE-294 (Authentication Bypass via Capture-Replay)  
**CVSS**: 8.1 (High)

**How it works**:
```python
# Intercept a legitimate message with token
intercepted_message = {
    "type": "status_update",
    "agent_id": "legitimate-worker",
    "auth_token": "eyJ0eXAiOiJKV1Qi...",  # Valid token
    "task_id": "task-001",
    "status": "completed"
}

# Replay the same message multiple times
for i in range(100):
    send(intercepted_message)  # ✅ All accepted!
```

**Impact**: Can replay legitimate requests, modify data

**Why it works**: No nonces or request signing

**Fix in Stage 3**: Nonce-based replay protection

---

### V4: Legitimate API Abuse

**CWE**: CWE-863 (Incorrect Authorization)  
**CVSS**: 7.5 (High)

**How it works**:
```python
# If attacker escalated to admin role (via V1)
if has_admin_role(attacker_id):
    # Use legitimate API maliciously
    for task in get_all_tasks():
        task["priority"] = "low"  # Sabotage
        task["assigned_to"] = attacker_id  # Steal work
        update_task(task)  # ✅ All allowed!
```

**Impact**: System-wide sabotage using "legitimate" permissions

**Why it works**: No behavioral analysis or anomaly detection

**Fix in Stage 3**: Behavioral monitoring + automated quarantine

---

## 📂 File Structure

```
stage2_improved/
├── README.md                      # This file
├── SECURITY_ANALYSIS.md          # Detailed vulnerability analysis
├── requirements.txt              # Dependencies
│
├── auth/
│   ├── __init__.py
│   └── auth_manager.py           # JWT authentication (HS256)
│
├── security/
│   ├── __init__.py
│   ├── permission_manager.py     # RBAC with 3 roles
│   └── validator.py              # Schema + pattern validation
│
├── core/
│   ├── __init__.py
│   ├── protocol.py               # Message definitions
│   ├── utils.py                  # Security utilities
│   ├── task_queue.py             # SQLite queue with access control
│   └── project_manager.py        # Coordinator with security
│
└── agents/                        # (To be added)
    ├── malicious_worker.py       # Demonstrates bypass attacks
    └── legitimate_worker.py      # Shows proper usage
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone repository
git clone https://github.com/robertfischer3/fischer3_a2a_introduction.git
cd fischer3_a2a_introduction/a2a_adversarial_agent_example/stage2_improved

# Install dependencies
pip install -r requirements.txt
```

**Dependencies**:
- `PyJWT==2.8.0` - JWT token generation and verification
- `bcrypt==4.1.2` - Password hashing

---

## 💻 Usage Examples

### Basic Setup

```python
from core.task_queue import TaskQueue
from core.project_manager import ProjectManager

# Initialize system
queue = TaskQueue()
manager = ProjectManager(queue)
```

### Register a Worker Agent

```python
# Register with password
response = manager.register_agent({
    "type": "register",
    "agent_id": "worker-001",
    "password": "secure_password",
    "requested_role": "worker"
})

# Extract token for future requests
token = response["auth_token"]
print(f"Registered: {response}")
```

### Assign a Task (Manager Required)

```python
# First, register a manager
manager_response = manager.register_agent({
    "type": "register",
    "agent_id": "manager-001",
    "password": "manager_password",
    "requested_role": "manager"
})

manager_token = manager_response["auth_token"]

# Create task
task = manager.assign_task(
    description="Process customer data for Q4",
    assigned_to="worker-001",
    agent_id="manager-001",
    auth_token=manager_token,
    priority="high"
)

print(f"Task assigned: {task['task_id']}")
```

### Update Task Status

```python
# Worker updates their task
response = manager.handle_status_update({
    "type": "status_update",
    "agent_id": "worker-001",
    "task_id": task["task_id"],
    "status": "in_progress",
    "progress": 50,
    "details": {
        "message": "Processing batch 5 of 10..."
    },
    "auth_token": token
})

print(f"Update: {response}")
```

### Complete a Task

```python
response = manager.handle_task_completion({
    "type": "task_complete",
    "agent_id": "worker-001",
    "task_id": task["task_id"],
    "result": "Successfully processed 1,000 records",
    "metrics": {
        "records_processed": 1000,
        "processing_time": "5.2s",
        "accuracy": 99.8
    },
    "auth_token": token
})

print(f"Completion: {response}")
```

---

## 🔍 Testing Security Features

### Test 1: Authentication Required

```python
# Try to update without token
response = manager.handle_status_update({
    "type": "status_update",
    "agent_id": "worker-001",
    "task_id": "task-001",
    "status": "completed"
    # No auth_token!
})

# Result: {"error": "Authentication failed"}
```

### Test 2: Permission Checks

```python
# Worker tries to access another worker's task
other_task = {...}  # Task assigned to worker-002

response = manager.handle_status_update({
    "type": "status_update",
    "agent_id": "worker-001",  # Different agent
    "task_id": other_task["task_id"],
    "status": "completed",
    "auth_token": worker_001_token
})

# Result: {"error": "Permission denied"}
```

### Test 3: Validation Blocking Simple Attacks

```python
# Try to send malformed message
response = manager.handle_message({
    "type": "status_update",
    "agent_id": "worker-001",
    # Missing required fields
})

# Result: {"error": "Validation failed: Missing required field: task_id"}
```

### Test 4: Role Escalation (Vulnerability)

```python
# ⚠️ Request admin role - gets granted!
response = manager.register_agent({
    "type": "register",
    "agent_id": "attacker",
    "password": "password",
    "requested_role": "admin"  # No verification!
})

# Result: {"status": "registered", "role": "admin"} ⚠️
# Attacker now has full admin access!
```

### Test 5: Deep-Nested Bypass (Vulnerability)

```python
# ⚠️ Hide sensitive data in nested structure
response = manager.handle_status_update({
    "type": "status_update",
    "agent_id": "worker-001",
    "task_id": "task-001",
    "status": "in_progress",
    "details": {
        "message": "Working...",  # ✅ Validated
        "metadata": {  # ⚠️ Not deeply checked
            "technical_info": {
                "customer_records": [
                    {"ssn": "123-45-6789", "cc": "4532-..."},
                    # ... stolen data
                ]
            }
        }
    },
    "auth_token": token
})

# Result: {"status": "acknowledged"} ✅
# Malicious data stored in system! ⚠️
```

---

## 📊 Attack Success Matrix

| Attack Type | Stage 1 | Stage 2 | Blocked? |
|-------------|---------|---------|----------|
| **Anonymous Access** | ✅ 100% | ❌ 0% | ✅ Yes |
| **Simple Identity Spoofing** | ✅ 100% | ❌ 0% | ✅ Yes |
| **Obvious Data Leakage** | ✅ 100% | ❌ 0% | ✅ Yes |
| **Invalid Message Format** | ✅ 100% | ❌ 0% | ✅ Yes |
| **Role Escalation** | ✅ 100% | ✅ 100% | ❌ No |
| **Deep-Nested Exfiltration** | ✅ 100% | ✅ 100% | ❌ No |
| **Token Replay** | N/A | ✅ 100% | ❌ No |
| **Legitimate API Abuse** | ✅ 100% | ✅ 100% | ❌ No |

**Simple Attacks**: 80% blocked ✅  
**Sophisticated Attacks**: 0% blocked ⚠️  
**Overall**: 40% blocked, 60% still vulnerable

---

## 🎓 Learning Objectives

After studying Stage 2, you should understand:

### Security Concepts
- [ ] How JWT authentication works in practice
- [ ] What RBAC provides (and its limitations)
- [ ] Why input validation must be comprehensive
- [ ] The difference between surface and deep validation
- [ ] Why partial security creates false confidence

### Attack Evolution
- [ ] How attackers adapt to partial defenses
- [ ] Why sophisticated attacks bypass simple controls
- [ ] Data hiding in nested structures
- [ ] TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities
- [ ] Legitimate API abuse patterns

### Design Lessons
- [ ] Defense in depth is critical
- [ ] Validation must be recursive
- [ ] Role assignment needs verification
- [ ] Behavioral analysis is essential
- [ ] Why Stage 3's comprehensive approach is needed

---

## 🛡️ What Stage 3 Adds

Preview of complete security in Stage 3:

**Deep Validation** ✅
- Recursive validation at all nesting levels
- Size limits on nested structures
- Semantic validation

**Behavioral Analysis** ✅
- Anomaly detection
- Risk scoring
- Pattern recognition

**Automated Response** ✅
- Automatic quarantine
- Real-time threat mitigation
- Self-defending system

**Capability-Based Security** ✅
- Time-limited permissions
- Scope-limited access
- Single-use capabilities

**Result**: All attacks blocked, 0% success rate

---

## 📚 Additional Resources

### Documentation
- [SECURITY_ANALYSIS.md](../../a2a_crypto_example/SECURITY_ANALYSIS.md) - Detailed vulnerability analysis
- [Stage 1 README](../stage1_insecure/README.md) - Completely vulnerable baseline
- [Stage 3 README](../../../README.md) - Production security (coming soon)

### External Resources
- [JWT Introduction](https://jwt.io/introduction)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

### Related Examples
- Crypto Price Agent - API security progression
- Credit Report Agent - File upload security
- Task Collaboration - Session management

---

## ❓ FAQ

### Q: Why is this still vulnerable if it has security?
**A**: Partial security is the point! This demonstrates that adding some security isn't enough. Sophisticated attackers adapt and find new ways around incomplete defenses.

### Q: Can I use this code in production?
**A**: **NO!** This is educational code with intentional vulnerabilities. Use Stage 3 patterns for production, or better yet, use established frameworks.

### Q: What's the most critical vulnerability?
**A**: Deep-nested data bypass (V2). It allows complete data exfiltration despite all the security controls.

### Q: How does this compare to real systems?
**A**: Many real systems have similar partial security. They add authentication and basic validation but miss deep validation, behavioral analysis, or proper role verification.

### Q: How long to understand Stage 2?
**A**: Plan 4-6 hours:
- 1-2 hours: Setup and basic usage
- 2-3 hours: Understanding security components
- 1-2 hours: Testing vulnerabilities

---

## 🤝 Contributing

Found an issue or want to improve the examples? This is an educational project, so:

1. **Don't** fix the intentional vulnerabilities (they're for teaching)
2. **Do** suggest better explanations or examples
3. **Do** report actual bugs in the implementation
4. **Do** propose additional attack demonstrations

---

## ⚖️ License

MIT License - See LICENSE file in repository root

**Educational Use Only**: This code contains intentional security vulnerabilities for teaching purposes.

---

## 📞 Questions or Feedback?

**Project Maintainer**: Robert Fischer  
**Email**: robert@fischer3.org  
**Repository**: [GitHub](https://github.com/robertfischer3/fischer3_a2a_introduction)

---

## 🎯 Remember

**Stage 2 teaches**: 
> "Partial security is dangerous because it creates false confidence while sophisticated attacks still succeed."

**Next Step**: Study Stage 3 to see comprehensive defense in depth!

---

**Last Updated**: January 2026  
**Version**: 2.0  
**Status**: Educational - Partial Security  
**Security Rating**: 4/10 ⚠️
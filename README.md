# fischer³ Agentic AI Security Education

**Practical, hands-on education for building secure AI agent systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://learn-a2a-security.fischer3.net)

---

## What This Project Is

AI agents are already talking to each other. The Agent-to-Agent (A2A) protocol and the Model Context Protocol (MCP) are the emerging standards for how autonomous systems communicate and collaborate. But most existing resources give you a glossy overview and wish you good luck figuring out the security implications.

**This project is different.** It teaches agentic AI security the way security should be taught: by starting with deliberately vulnerable code, showing you exactly what breaks and why, then progressively building up to production-ready implementations that withstand real attacks.

Every example follows the same pattern: **vulnerable → improved → secure**. By the time you reach the production stages, you won't just know *what* controls to implement — you'll deeply understand *why* each one exists and *what* happens without it.

---

> ### 🚨 CRITICAL PRODUCTION DISCLAIMER
> 
> **Stage 1-2 Code**: ❌ NEVER use in production - intentionally vulnerable for education only
> 
> **Stage 3+ Code**: ⚠️ Production-quality patterns but require YOUR validation before production use
> 
> **NO WARRANTIES**: This project is provided "AS IS" under MIT License with no warranties of any kind, express or implied. You assume ALL responsibility for production deployments including:
> - Independent security testing and penetration testing
> - Code review and vulnerability scanning  
> - Compliance verification for your specific requirements
> - Infrastructure security and operational procedures
> 
> **This project provides education only, not production support or security guarantees.**
> 
> 📋 [Read Full Disclaimer](./DISCLAIMER.md) before using any code in production.

---

## What You'll Learn

<div align="center">

### 🎯 Core Topics

</div>

**Agent-to-Agent (A2A) Protocol Security**
- Agent identity, discovery, and registration patterns
- Message validation and the eight-layer framework
- Authentication mechanisms and threat modeling
- Session management and state security
- Defense-in-depth across distributed agent systems

**Model Context Protocol (MCP) Security**
- How agents connect to tools and resources
- Secure server and client implementation patterns
- The agent-tool security boundary
- Tool access validation and authorization

**Integration & Architecture**
- How A2A and MCP work together
- Multi-agent system design patterns
- Distributed session management with Redis
- Web framework integration (Flask, JWT)
- Behavioral analysis and automated threat response

**Security Frameworks**
- Eight-layer input validation
- Three-stage security analysis (vulnerable → partial → comprehensive)
- Adversarial agent scenarios
- Compliance mapping (PCI-DSS, GDPR, HIPAA, SOX)

---

## Four Complete Learning Journeys

Each example demonstrates security evolution through multiple stages. All examples are production-quality in their final stages and include comprehensive documentation, attack demonstrations, and security analyses.

### 🪙 [Cryptocurrency Price Agent](./examples/a2a_crypto_example/)

**Focus**: Query security and basic A2A protocol fundamentals  
**Best For**: Beginners to A2A, API developers, foundational security patterns

**What You'll Learn**:
- Core A2A protocol mechanics
- Basic authentication and authorization
- Input validation and injection prevention
- API security patterns
- Real-time data security

**Progression**:
- **Stage 1**: No security, 15+ vulnerabilities
- **Stage 2**: Registry and basic authentication
- **Stage 3**: Production security with cryptographic controls

**Time**: 4-6 hours

---

### 📊 [Credit Report Analysis Agent](./examples/a2a_credit_report_example/)

**Focus**: File upload security, PII protection, and compliance  
**Best For**: Document processing systems, compliance-heavy applications, AI integration

**What You'll Learn**:
- File upload security and validation
- PII protection (GDPR/HIPAA patterns)
- Eight-layer validation framework
- Path traversal and magic byte validation
- Secure file handling
- AI integration security (Gemini)

**Progression**:
- **Stage 1**: Vulnerable file handling, no validation
- **Stage 2**: Basic validation, limited PII protection
- **Stage 3**: Production-ready file security
- **Stage 4**: Secure AI integration

**Time**: 19-26 hours

---

### 🤝 [Task Collaboration System](./examples/a2a_task_collab_example/)

**Focus**: Session management, state security, distributed systems  
**Best For**: Multi-agent coordination, session security, production scaling

**What You'll Learn**:
- Session management fundamentals
- State security and binding
- Multi-agent coordination patterns
- Distributed sessions with Redis
- Web framework integration (Flask + JWT)
- Session hijacking and fixation prevention

**Progression**:
- **Stage 1**: 25+ session vulnerabilities
- **Stage 2**: Partial session fixes
- **Stage 3**: SessionManager with comprehensive security
- **Stage 4**: Distributed Redis-backed sessions
- **Stage 5**: Web framework integration

**Time**: 17-22 hours

---

### 🤖 [Adversarial Agent System](./examples/a2a_adversarial_agent_example/)

**Focus**: Attack patterns, behavioral analysis, automated defense  
**Best For**: Security professionals, threat modeling, adversarial scenarios

**What You'll Learn**:
- Real attack vectors against agent systems
- Data exfiltration techniques
- Privilege escalation patterns
- Behavioral anomaly detection
- Automated quarantine systems
- Zero-trust architecture

**Progression**:
- **Stage 1**: 5 attacks succeed, all defenses fail
- **Stage 2**: Partial security, 4 sophisticated attacks still succeed
- **Stage 3**: Comprehensive defense, behavioral analysis, zero attacks succeed

**Time**: 8-12 hours

---

## Quick Start

> ### ⚠️ Before You Begin
> 
> **For Learning (Stage 1-2)**:
> - ✅ Use in isolated test environments only
> - ✅ Never connect to production systems
> - ✅ Use synthetic data only
> 
> **For Production (Stage 3+)**:
> - ⚠️ Independent security testing required
> - ⚠️ Code review by your security team required
> - ⚠️ Compliance verification required
> - ⚠️ No warranties - you assume all responsibility
> 
> 📋 [Full Disclaimer & Checklist](./DISCLAIMER.md)

### Prerequisites

```bash
# Python 3.10 or higher
python --version

# Basic understanding of:
# - Async programming
# - HTTP/REST APIs
# - JSON data formats
# - Basic cryptography concepts
```

### Installation

```bash
# Clone repository
git clone https://github.com/fischer3-net/agentic-security-education.git
cd agentic-security-education

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (example-specific)
# See individual example READMEs for specific requirements
```

### Choose Your Starting Point

```bash
# Example 1: Cryptocurrency Agent (foundational)
cd examples/a2a_crypto_example
python insecure_agent.py

# Example 2: Credit Report Agent (file security & PII)
cd examples/a2a_credit_report_example/stage1_insecure
python server.py

# Example 3: Task Collaboration (session management)
cd examples/a2a_task_collab_example/stage1_insecure
python server/task_coordinator.py

# Example 4: Adversarial Agent (attack & defense)
cd examples/a2a_adversarial_agent_example/stage1_insecure
python demo_attacks.py
```

---

## Learning Paths

### For Complete Beginners

**Goal**: Understand agentic AI security fundamentals

1. [A2A Overview](./docs/a2a/00_A2A_OVERVIEW.md) — What is agent-to-agent communication?
2. [Core Concepts](./docs/a2a/01_FUNDAMENTALS/01_core_concepts.md) — Building blocks of A2A systems
3. [Cryptocurrency Agent - Stage 1](./examples/a2a_crypto_example/) — First hands-on example
4. [MCP Summary](./docs/mcp_summary.md) — How agents connect to tools

**Time**: 4-6 hours

---

### For Developers Building Agents

**Goal**: Build secure agents from day one

1. [A2A Overview](./docs/a2a/00_A2A_OVERVIEW.md) — Protocol orientation
2. [Security Best Practices](./docs/a2a/03_SECURITY/04_security_best_practices.md) — Critical controls
3. [Message Validation Patterns](./docs/a2a/04_COMMUNICATION/04_message_validation_patterns.md) — Eight-layer defense
4. [MCP Fundamentals](./docs/mcp_fundamentals.md) — Tool integration security
5. Work through all stages of at least two examples

**Time**: 20-30 hours

---

### For Security Professionals

**Goal**: Audit and secure agentic systems

1. [Threat Model](./docs/a2a/03_SECURITY/03_threat_model.md) — Attack vectors
2. [Authentication Tags](./docs/a2a/03_SECURITY/02_authentication_tags.md) — Cryptographic verification
3. [Code Walkthrough](./docs/a2a/03_SECURITY/05_code_walkthrough_comparison.md) — Vulnerable vs. secure
4. [Session State Security](./docs/a2a/03_SECURITY/06_session_state_security.md) — State management attacks
5. [Adversarial Agent - All Stages](./examples/a2a_adversarial_agent_example/) — Complete attack/defense analysis
6. [Security Checklist](./docs/presentations/agent_security_article_enhanced/security_checklist.md) — 200+ item audit tool

**Time**: 12-16 hours

---

### For Non-Technical Stakeholders

**Goal**: Understand risks and make informed decisions

1. [AI Collaboration Fundamentals](./docs/non-technical/01_fundamentals/AI_Collaboration_Fundamentals.md) — No code required
2. [Security for Non-Technical Audiences](./docs/non-technical/02_security/Security_for_Non_Technical_Audiences.md) — Plain language risk
3. [Agent Security Article - Executive Summary](./docs/presentations/agent-security/agent_security_article_enhanced.md) — Business case
4. [Presentation Materials](./docs/presentations/index.md) — Briefing decks

**Time**: 2-3 hours

---

## The Eight-Layer Security Framework

A central theme throughout this project is **defense in depth** — no single control is sufficient. The eight-layer framework provides structure:

| Layer | Control | Protection Against |
|-------|---------|-------------------|
| **1** | Transport Security (TLS 1.3) | Eavesdropping, interception |
| **2** | Authentication | Impersonation, identity fraud |
| **3** | Session Management | Hijacking, state manipulation |
| **4** | Authorization (RBAC) | Unauthorized operations |
| **5** | Message Integrity (HMAC) | Tampering |
| **6** | Replay Protection | Message reuse |
| **7** | Rate Limiting | Brute-force, volume attacks |
| **8** | Input Validation | Injection, malformed data |

Every Stage 3 example implements all eight layers. The [presentation materials](./docs/presentations/index.md) provide extensive training content around this framework.

---

## Project Structure

```
📁 agentic-security-education/
│
├── 📖 Documentation (docs/)
│   ├── a2a_summary.md              # A2A protocol entry point
│   ├── mcp_summary.md              # MCP protocol entry point
│   ├── integration_summary.md      # How they work together
│   ├── index.md                    # Main documentation site
│   │
│   ├── a2a/                        # A2A Protocol deep dives
│   │   ├── 00_A2A_OVERVIEW.md
│   │   ├── INDEX.md
│   │   ├── 01_FUNDAMENTALS/        # Core concepts
│   │   ├── 02_DISCOVERY/           # Service discovery
│   │   ├── 03_SECURITY/            # Security deep dives ⭐
│   │   ├── 04_COMMUNICATION/       # Protocol messages
│   │   └── 05_REFERENCE/           # Technical reference
│   │
│   ├── presentations/               # Training materials
│   │   ├── index.md
│   │   ├── eight-layer-validation/ # Input validation framework
│   │   └── agent-security/         # Comprehensive security
│   │
│   ├── guides/                      # How-to guides
│   ├── non-technical/               # Non-developer resources
│   └── supplementary/               # Tools and utilities
│
├── 💻 Example 1: Cryptocurrency Agent (examples/a2a_crypto_example/)
│   ├── Stage 1: Vulnerable baseline
│   ├── Stage 2: Registry + basic auth
│   └── Stage 3: Production security
│
├── 💻 Example 2: Credit Report Agent (examples/a2a_credit_report_example/)
│   ├── stage1_insecure/            # Vulnerable file handling
│   ├── stage2_improved/            # Basic validation
│   ├── stage3_secure/              # Production security
│   └── stage4_ai/                  # AI integration
│
├── 💻 Example 3: Task Collaboration (examples/a2a_task_collab_example/)
│   ├── stage1_insecure/            # 25+ vulnerabilities
│   ├── stage2_improved/            # Partial fixes
│   ├── stage3_secure/              # SessionManager
│   ├── stage4_distributed/         # Redis integration
│   └── stage5_web_framework/       # Flask + JWT
│
├── 💻 Example 4: Adversarial Agent (examples/a2a_adversarial_agent_example/)
│   ├── stage1_insecure/            # All attacks succeed
│   ├── stage2_improved/            # Partial defenses
│   └── stage3_secure/              # Comprehensive defense
│
├── 🛠️ MCP Examples (mcp_examples/)
│   ├── mcp_client_w_sql_lite/      # Complete MCP client/server
│   └── your_first_mcp_server/      # Tutorial implementation
│
└── 🔧 Utilities (utils/)
    ├── check_markdown_links.py     # Documentation QA
    └── fix_markdown_links.py       # Link maintenance
```

---

## Project Statistics

### Documentation
- **Total Files**: 50+ comprehensive guides
- **Security Deep Dives**: 8 major topics
- **Learning Paths**: 4 audience-specific journeys
- **Lines of Documentation**: 30,000+

### Code Examples
- **Total Stages**: 15 progressive implementations
- **Lines of Code**: 15,000+ (across all stages)
- **Vulnerabilities Demonstrated**: 90+ unique security issues
- **Attack Scenarios**: 35+ with working demonstrations

### Coverage
- **A2A Protocol**: Complete specification and implementation
- **MCP Integration**: Fundamentals through production patterns
- **Security Domains**: Query, file, session, adversarial, distributed, web
- **Real-World Patterns**: Multi-agent, distributed systems, AI integration

---

## Additional Resources

### Official Documentation
- [Documentation Site](https://learn-a2a-security.fischer3.net) — Full documentation
- [Model Context Protocol Specification](https://modelcontextprotocol.io) — MCP official docs
- [Agent2Agent Protocol Design](./docs/references.md) — A2A specification

### Presentation Materials
- [Presentations Index](./docs/presentations/index.md) — Training resources
- [Eight-Layer Validation](./docs/presentations/eight-layer-validation/) — Input validation framework
- [Agent Security](./docs/presentations/agent-security/) — Comprehensive security training

### Utility Tools
- [UV Python Environment Guide](./docs/supplementary/tools/UBUNTU_QUICKSTART.md) — Modern dependency management
- [Markdown Link Checker](./utils/check_markdown_links.py) — Documentation QA

---

## Contributing

Contributions are welcome and encouraged!

- **Found a bug?** [Open an issue](https://github.com/fischer3-net/agentic-security-education/issues)
- **Want to contribute?** Submit a pull request
- **Have questions?** [Start a discussion](https://github.com/fischer3-net/agentic-security-education/discussions)
- **Security issue?** Email robert@fischer3.net (responsible disclosure)

### Ways to Help

- Improve documentation clarity
- Add new examples or extend existing ones
- Report security findings
- Translate to other languages
- Share your implementations
- Create tutorial videos
- Write blog posts about your learning experience

See [Contributing Guidelines](./docs/about/contributing.md) for details.

---

## How to Use This Project

### As a Learning Course
Follow the examples sequentially, completing all stages. Work through attack scenarios and read the security analyses. Estimated time for complete mastery: **50-60 hours**.

### As a Reference
Jump to specific security topics as needed. Each documentation page and security analysis stands alone with full context.

### As a Production Template
Stage 3 implementations from any example provide production-ready starting points. Review the security analyses to understand the controls and adapt to your needs.

### As Training Material
The [presentation materials](./docs/presentations/index.md) are designed for team training, security reviews, and executive briefings. Includes slide decks, articles, and comprehensive checklists.

---

## License

This project is released under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

## Production Use & Warranties

### Educational Use Disclaimer

⚠️ **Stage 1 and Stage 2 code contains intentional vulnerabilities for educational purposes.**

**Critical Requirements**:
- ❌ **DO NOT** deploy Stage 1 or Stage 2 code in production
- ✅ **DO** use Stage 3+ implementations as production templates (with appropriate validation)
- ✅ **DO** use this material for educational purposes
- ✅ **DO** practice attacks only in isolated test environments

### No Warranties - Your Responsibility

**This project is provided "AS IS" under the MIT License with NO WARRANTIES of any kind.**

If you choose to use Stage 3+ code as a foundation for production systems, you must:
- Conduct independent security testing
- Perform code reviews by qualified security professionals
- Verify compliance with your regulatory requirements
- Implement your own operational security procedures
- Test thoroughly in your specific environment

**The project maintainers assume NO responsibility or liability for production deployments.**

📋 **[Read the complete disclaimer and production checklist →](./DISCLAIMER.md)**

This comprehensive document covers:
- Detailed warranty disclaimers
- Your responsibilities for production use
- Required security testing procedures
- Compliance verification requirements
- When to seek professional help

---

## Contact

**Project Maintainer**: Robert Fischer  
**Email**: robert@fischer3.net  
**Website**: [https://learn-a2a-security.fischer3.net](https://learn-a2a-security.fischer3.net)  
**GitHub**: [https://github.com/fischer3-net/agentic-security-education](https://github.com/fischer3-net/agentic-security-education)

---

## Acknowledgments

This project builds on and references:
- The Model Context Protocol specification from Anthropic
- OWASP security guidelines and best practices
- CWE/CVSS vulnerability classification systems
- Research on multi-agent systems security
- Community feedback and contributions

---

**Last Updated**: January 2026  
**Version**: 3.0  
**Status**: Active Development

---

<div align="center">

**Learn security by breaking it first, then building it right.**

[Get Started →](./docs/index.md)

</div>
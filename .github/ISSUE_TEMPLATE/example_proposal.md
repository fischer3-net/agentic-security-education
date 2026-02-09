---
name: 🎓 New Example Proposal
about: Propose a new educational example demonstrating A2A or MCP concepts
title: '[EXAMPLE] '
labels: ['example', 'needs-discussion', 'enhancement']
assignees: ''
---

## Example Overview
<!-- Provide a brief, compelling description of your proposed example -->


## Security Concepts Demonstrated
<!-- What specific security concepts or vulnerabilities will this example teach? -->
- 
- 
- 

## Learning Objectives
<!-- After completing this example, what should students be able to do? -->
- [ ] 
- [ ] 
- [ ] 

## Example Structure
<!-- Will this follow the standard 3-stage pattern? -->
- [ ] **Stage 1 (Vulnerable)**: Intentionally insecure implementation
- [ ] **Stage 2 (Partial)**: Some security controls, but bypassable
- [ ] **Stage 3 (Secure)**: Production-ready with comprehensive security
- [ ] Alternative structure (please describe):

## Vulnerabilities to Demonstrate
<!-- For Stage 1, what vulnerabilities will you intentionally include? -->

### Stage 1 (Vulnerable)
- [ ] **Vulnerability 1**: [CWE-XXX] Description
- [ ] **Vulnerability 2**: [CWE-XXX] Description
- [ ] **Vulnerability 3**: [CWE-XXX] Description

**Attack Demonstrations**:
- 
- 

### Stage 2 (Partial)
<!-- What security controls will be added, and what bypasses will still work? -->

**Security Improvements**:
- 
- 

**Remaining Vulnerabilities**:
- 
- 

### Stage 3 (Secure)
<!-- What comprehensive security controls will be implemented? -->

**Security Controls**:
- [ ] Authentication
- [ ] Authorization
- [ ] Input validation
- [ ] Output encoding
- [ ] Rate limiting
- [ ] Logging and monitoring
- [ ] Session management
- [ ] Encryption
- [ ] Other (specify):

## Technical Architecture
<!-- Describe the agents, components, and interactions -->

**Components**:
- **Server Agent**: 
- **Client Agent**: 
- **Other Components**: 

**Communication Flow**:
```
[Describe or diagram the interaction flow]
```

## Prerequisites / Dependencies
<!-- What should students know before starting this example? -->
- **Knowledge Prerequisites**: 
- **Technical Prerequisites**: 
- **Dependencies**: 

## Complexity Level
<!-- How difficult is this example? -->
- [ ] 🟢 Beginner (2-4 hours to complete)
- [ ] 🟡 Intermediate (4-8 hours to complete)
- [ ] 🔴 Advanced (8+ hours to complete)

## Real-World Relevance
<!-- What real-world scenarios or incidents does this relate to? -->


## Similar Examples or References
<!-- Are there existing examples this builds upon or complements? -->
- 
- 

## Proposed File Structure
<!-- Outline the directory and file structure -->
```
examples/your_example_name/
├── README.md
├── SECURITY_ANALYSIS.md
├── stage1_vulnerable/
│   ├── README.md
│   ├── server.py
│   ├── client.py
│   ├── demo_attacks.py
│   └── requirements.txt
├── stage2_partial/
│   ├── README.md
│   ├── server.py
│   ├── client.py
│   ├── demo_bypasses.py
│   └── requirements.txt
└── stage3_secure/
    ├── README.md
    ├── server.py
    ├── client.py
    ├── demo_defenses.py
    └── requirements.txt
```

## Documentation Plan
<!-- What documentation will you provide? -->
- [ ] Main README with overview
- [ ] Stage-specific READMEs
- [ ] SECURITY_ANALYSIS.md with detailed vulnerability analysis
- [ ] Code comments explaining security implications
- [ ] Attack demonstration scripts
- [ ] Setup and installation guide
- [ ] Quick reference guide
- [ ] FAQ or troubleshooting guide

## Deliverables Checklist
<!-- What will you deliver? -->
- [ ] Working code for all stages
- [ ] Comprehensive documentation
- [ ] Attack/bypass/defense demonstrations
- [ ] Security analysis with CWE/CVE mappings
- [ ] Test cases
- [ ] Fictitious sample data (no real credentials)
- [ ] Integration with existing documentation

## Timeline
<!-- When can you deliver this? -->
- **Stage 1**: 
- **Stage 2**: 
- **Stage 3**: 
- **Documentation**: 
- **Final Review**: 

## Volunteer Commitment
<!-- Your involvement -->
- [ ] I will implement all stages
- [ ] I will create all documentation
- [ ] I will maintain this example
- [ ] I need help with: 

## Questions for Maintainers
<!-- What do you need feedback on? -->


## Additional Context
<!-- Mockups, diagrams, references, related research -->


## Checklist
- [ ] I have reviewed existing examples
- [ ] This provides unique educational value
- [ ] I understand the security implications
- [ ] I commit to completing all stages
- [ ] I will follow project standards and guidelines
- [ ] I will use only fictitious data (per FICTITIOUS_DATA_NOTICE.md)
- [ ] This is for educational purposes only

---

**Note**: Example proposals typically require discussion before approval. Please be prepared to refine your proposal based on maintainer feedback.

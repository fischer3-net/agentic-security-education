# Commit Message Conventions

> **Purpose**: Establish clear, consistent commit messages for better collaboration, code review, and project history.
>
> **Status**: Active
> **Last Updated**: December 2025

---

## 📋 Quick Reference

### Standard Format
```
<type>: <subject>

[optional body]

[optional footer]
```

### Example
```
feat: Add SQL injection demonstration to Stage 1

Implemented a vulnerable login endpoint that demonstrates 
SQL injection attacks. Includes demo script showing multiple
attack vectors and their impacts.

Closes #42
```

---

## 🎯 Commit Types

### Primary Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature or functionality | `feat: Add MFA implementation guide` |
| `fix` | Bug fix | `fix: Correct broken link in README` |
| `docs` | Documentation only | `docs: Update installation instructions` |
| `refactor` | Code change without fixing/adding | `refactor: Extract auth logic to module` |
| `test` | Adding or updating tests | `test: Add integration tests for Stage 3` |
| `chore` | Maintenance tasks | `chore: Update dependencies` |
| `style` | Code formatting (not CSS) | `style: Fix indentation in auth.py` |
| `perf` | Performance improvement | `perf: Optimize session lookup` |

### Stage-Specific Types

For staged examples:

| Type | Purpose | Example |
|------|---------|---------|
| `stage1` | Stage 1 changes | `stage1: Add CSRF vulnerability demo` |
| `stage2` | Stage 2 changes | `stage2: Implement partial auth` |
| `stage3` | Stage 3 changes | `stage3: Add comprehensive validation` |

---

## ✍️ Writing the Subject Line

### Rules
1. **Limit to 50 characters** (hard limit: 72)
2. **Use imperative mood** ("Add feature" not "Added feature")
3. **Don't end with a period**
4. **Capitalize first letter**
5. **Be specific but concise**

### Good Examples
```
feat: Add prompt injection attack example
fix: Resolve session timeout in Stage 2
docs: Create MCP resources deep dive guide
refactor: Simplify error handling in client
test: Add security validation tests
chore: Update Python dependencies to 3.11
```

### Bad Examples
```
❌ Added some stuff
❌ Fixed bugs
❌ Update documentation.
❌ WIP
❌ Implementing the comprehensive multi-stage security validation framework
❌ updates
```

---

## 📝 Writing the Body

### When to Include a Body
- Complex changes needing explanation
- Breaking changes
- Changes affecting multiple components
- Security-related changes
- Context that's not obvious from code

### Body Guidelines
1. **Wrap at 72 characters** per line
2. **Explain the "what" and "why"**, not the "how"
3. **Separate from subject with blank line**
4. **Use bullet points for multiple items**
5. **Reference issues and PRs**

### Example with Body
```
feat: Implement eight-layer validation framework

Add comprehensive input validation across eight layers:
- Layer 1: Input syntax validation
- Layer 2: Data type verification
- Layer 3: Range and boundary checks
- Layer 4: Business logic validation
- Layer 5: Security constraint validation
- Layer 6: Cross-field validation
- Layer 7: External dependency validation
- Layer 8: Final consistency verification

This framework provides defense-in-depth against multiple
attack vectors including injection attacks, data tampering,
and business logic exploitation.

Closes #78
Related to #65, #71
```

---

## 🔖 Writing the Footer

### Common Footer Types

#### Issue References
```
Closes #123
Fixes #456
Resolves #789
Relates to #101
See also #102
```

#### Breaking Changes
```
BREAKING CHANGE: Authentication endpoint now requires OAuth2

The /auth endpoint no longer accepts basic authentication.
All clients must be updated to use OAuth2 flow.

Migration guide: docs/migration/oauth2.md
```

#### Co-authored
```
Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

#### Security Notices
```
Security: Fixes critical SQL injection vulnerability

CVE: Pending
CWE-89: SQL Injection
CVSS Score: 9.8 (Critical)
```

---

## 🎨 Type-Specific Examples

### Feature Commits
```
feat: Add OAuth2 authentication to Stage 3

Implement OAuth2 password grant flow with:
- Token generation and validation
- Refresh token support  
- Token revocation endpoint
- Rate limiting on auth attempts

Includes comprehensive tests and documentation.

Closes #42
```

### Fix Commits
```
fix: Correct session timeout calculation

Session timeout was calculating incorrectly due to timezone
mismatch. Now uses UTC consistently throughout.

The bug caused sessions to expire prematurely in certain
timezones, affecting approximately 15% of users.

Fixes #156
```

### Documentation Commits
```
docs: Create quick start guide for beginners

Add comprehensive quick start guide covering:
- Environment setup
- First agent implementation
- Tool connection
- Hello world example

Estimated completion time: 3-4 hours

Closes #89
```

### Refactor Commits
```
refactor: Extract validation logic to separate module

Move all input validation functions from server.py to new
validation.py module. No functional changes.

This improves:
- Code organization
- Testability
- Reusability across stages

Part of code organization initiative (#67)
```

### Test Commits
```
test: Add comprehensive security tests for Stage 3

Add 47 new security tests covering:
- Authentication bypass attempts
- Authorization failures
- Input validation edge cases
- Session hijacking prevention
- Rate limiting enforcement

All tests pass. Coverage increased from 73% to 91%.
```

### Chore Commits
```
chore: Update dependencies for security patches

Update the following packages to latest secure versions:
- requests: 2.31.0 → 2.32.0 (CVE-2024-XXXX)
- cryptography: 41.0.0 → 42.0.0 (Security update)
- flask: 2.3.0 → 3.0.0 (Multiple CVEs)

All tests pass after updates.
```

### Stage-Specific Commits
```
stage1: Add command injection vulnerability demo

Implement vulnerable file upload endpoint that allows
command injection through filename manipulation.

Attack demonstration shows:
- Remote code execution
- File system access
- Data exfiltration

This intentionally insecure code is for educational
purposes only.

Related to #45
```

```
stage2: Implement basic file type validation

Add MIME type checking for uploads. However, this can
still be bypassed with:
- Double extension attacks
- MIME type spoofing
- Magic byte manipulation

Bypass demonstrations included in demo_bypasses.py

Part of progressive security series (#67)
```

```
stage3: Add comprehensive upload validation

Implement eight-layer validation for file uploads:
- File size limits
- Extension whitelist
- MIME type verification
- Magic byte validation
- Virus scanning (ClamAV)
- Content security policy
- Quarantine system
- Detailed audit logging

All known bypass attempts now fail.

Closes #67
```

---

## 🔐 Security-Related Commits

### Vulnerability Fixes
```
fix: Patch critical authentication bypass

SECURITY: Fix authentication bypass allowing unauthorized
access to admin endpoints.

Impact: High - Allows complete system compromise
CWE-287: Improper Authentication
CVSS: 9.1 (Critical)

The flaw existed in JWT token validation where expired
tokens were still accepted under certain conditions.

Fixes #SECURITY-001
```

### Security Enhancements
```
feat: Add rate limiting to authentication endpoints

Implement token bucket rate limiting:
- 5 attempts per minute per IP
- 20 attempts per hour per IP
- Exponential backoff on failures
- Admin bypass capability

Prevents brute force and credential stuffing attacks.

CWE-307: Improper Restriction of Excessive Authentication
Attempts

Closes #134
```

---

## 📊 Project-Specific Examples

### Documentation Reorganization
```
docs: Split implementation patterns into focused guides

Break down the large implementation_patterns_deep_dive.md
into four focused documents:
- mcp_resources_deep_dive.md
- mcp_tools_deep_dive.md  
- mcp_prompts_deep_dive.md
- mcp_sampling_deep_dive.md

Part of Phase 2 reorganization initiative.

Relates to learning_course_structure.md tracking
```

### Example Creation
```
example: Add adversarial agent demonstration

Create comprehensive three-stage example showing:
- Stage 1: Multiple vulnerability classes
- Stage 2: Partial mitigation attempts
- Stage 3: Production-ready security

Includes 12 attack demonstrations, detailed security
analysis, and comprehensive documentation.

Estimated learning time: 8-10 hours

Closes #78
```

### Tool Development
```
feat: Create automated security testing tool

Add security_scanner.py that automatically tests for:
- SQL injection
- XSS vulnerabilities
- CSRF weaknesses
- Authentication bypasses
- Session security issues

Generates detailed reports in JSON and HTML formats.

Usage: python tools/security_scanner.py <target>

Closes #156
```

---

## ✅ Commit Checklist

Before committing, verify:
- [ ] Type is appropriate and lowercase
- [ ] Subject is under 50 chars (72 hard limit)
- [ ] Subject uses imperative mood
- [ ] Subject starts with capital letter
- [ ] No period at end of subject
- [ ] Body wraps at 72 characters
- [ ] Body explains what and why
- [ ] Footer references related issues
- [ ] Security changes are clearly marked
- [ ] Breaking changes are documented

---

## 🔄 Commit Workflow

### 1. Stage Your Changes
```bash
# Stage specific files
git add file1.py file2.md

# Or stage all changes
git add .

# Review what's staged
git status
git diff --staged
```

### 2. Write the Commit
```bash
# Simple commit
git commit -m "feat: Add user authentication"

# Commit with body (opens editor)
git commit

# Commit with inline body
git commit -m "feat: Add user authentication" -m "
Implement JWT-based authentication with:
- Token generation
- Token validation
- Refresh tokens

Closes #42"
```

### 3. Amend if Needed
```bash
# Fix last commit message
git commit --amend

# Add forgotten files to last commit
git add forgotten_file.py
git commit --amend --no-edit
```

### 4. Push Changes
```bash
# Push to remote
git push origin your-branch-name

# Force push after amend (use carefully!)
git push origin your-branch-name --force-with-lease
```

---

## 🚫 Common Mistakes

### Vague Messages
```
❌ git commit -m "updates"
❌ git commit -m "fixed stuff"
❌ git commit -m "WIP"

✅ git commit -m "docs: Update installation instructions"
✅ git commit -m "fix: Resolve session timeout in Stage 2"
✅ git commit -m "feat: Add SQL injection demo to Stage 1"
```

### Wrong Type
```
❌ git commit -m "update: Added new feature"
❌ git commit -m "bug: Fixed the bug"

✅ git commit -m "feat: Add MFA support"
✅ git commit -m "fix: Correct validation logic"
```

### Too Long
```
❌ git commit -m "feat: Implementing a comprehensive multi-stage security validation framework with eight layers of defense"

✅ git commit -m "feat: Add eight-layer validation framework"
```

### Missing Context
```
❌ git commit -m "fix: Fixed it"

✅ git commit -m "fix: Resolve authentication bypass in token validation"
```

---

## 📖 Multi-Commit Best Practices

### Atomic Commits
Each commit should be a single logical change:

```bash
# Good: Separate commits for separate concerns
git commit -m "feat: Add user model"
git commit -m "feat: Add user authentication"
git commit -m "test: Add user model tests"
git commit -m "docs: Document authentication flow"

# Bad: Everything in one commit
git commit -m "Added user stuff and docs and tests"
```

### Commit Often
```bash
# Make small, frequent commits
git commit -m "feat: Add User model structure"
git commit -m "feat: Add User validation methods"
git commit -m "feat: Add User database methods"
git commit -m "feat: Add User serialization"

# Before pushing, can squash related commits if needed
git rebase -i main
```

---

## 🔗 Related Documentation

- [Branch Naming Conventions](./BRANCH_NAMING.md)
- [Contributing Guide](../docs/about/contributing.md)
- [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 💡 Tips

1. **Write commits for humans**: Future you will thank present you
2. **Be specific**: "Fix bug" → "Fix session timeout calculation"
3. **Explain why**: The code shows what, commits explain why
4. **Use present tense**: "Add feature" not "Added feature"
5. **Reference issues**: Always link to related issues/PRs
6. **Keep it atomic**: One logical change per commit
7. **Review before commit**: Use `git diff --staged`

---

**Document Version**: 1.0  
**Maintained By**: Robert Fischer  
**Last Updated**: December 2025
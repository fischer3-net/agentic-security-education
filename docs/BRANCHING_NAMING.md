# Branch Naming Conventions

> **Purpose**: Establish consistent branch naming to improve collaboration, code review, and project management.
>
> **Status**: Active
> **Last Updated**: December 2025

---

## 📋 Quick Reference

### Standard Format
```
<type>/<scope>/<description>

Examples:
feature/adversarial-agent/sql-injection-demo
docs/mcp-summary/add-security-patterns
fix/stage1/broken-demo-script
```

### Branch Type Prefixes

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `feature/` | New functionality or content | `feature/docs/quick-start-guide` |
| `docs/` | Documentation changes | `docs/a2a-summary/update-diagrams` |
| `fix/` | Bug fixes | `fix/crypto-example/api-timeout` |
| `refactor/` | Code reorganization | `refactor/tools/consolidate-scripts` |
| `example/` | New educational examples | `example/a2a/prompt-injection` |
| `stage/` | Stage-specific work | `stage/stage3/enhance-validation` |
| `test/` | Testing additions | `test/adversarial/add-integration-tests` |
| `chore/` | Maintenance tasks | `chore/deps/update-requirements` |

---

## 🎯 Detailed Guidelines

### 1. Feature Branches

**Purpose**: Add new functionality, content, or capabilities

**Format**: `feature/<scope>/<description>`

**Examples**:
```bash
# New learning content
feature/docs/quick-start-guide
feature/docs/mcp-implementation-guide

# New security patterns
feature/security/eight-layer-validation
feature/auth/mfa-implementation

# New tools or utilities
feature/tools/automated-testing
feature/tools/security-scanner

# Integration work
feature/integration/a2a-mcp-bridge
```

**Best Practices**:
- Keep descriptions concise but meaningful
- Use lowercase with hyphens
- Be specific about what's being added
- Include scope when it clarifies the change

---

### 2. Documentation Branches

**Purpose**: Documentation updates, improvements, or reorganization

**Format**: `docs/<scope>/<description>`

**Examples**:
```bash
# Content creation
docs/mcp-deep-dive/resources-guide
docs/a2a-security/threat-model-update

# Reorganization (Phase 2 work)
docs/reorganize/split-implementation-patterns
docs/restructure/create-progressive-learning

# Improvements
docs/examples/add-architecture-diagrams
docs/contributing/update-guidelines

# Specific document work
docs/readme/add-getting-started
docs/security-analysis/expand-cwe-mappings
```

**Best Practices**:
- Clearly indicate what documentation is affected
- Use section names from the doc structure
- Be specific about the type of change

---

### 3. Fix Branches

**Purpose**: Bug fixes, corrections, broken links, errors

**Format**: `fix/<scope>/<description>`

**Examples**:
```bash
# Code fixes
fix/stage1/broken-demo-script
fix/crypto-example/api-timeout
fix/task-collab/session-handling

# Documentation fixes
fix/docs/broken-links
fix/readme/typos-and-formatting
fix/security-analysis/incorrect-cwe

# Configuration fixes
fix/setup/dependency-conflicts
fix/config/environment-variables
```

**Best Practices**:
- Reference the issue number in commits
- Keep scope specific to affected component
- Describe what's being fixed, not the cause

---

### 4. Refactor Branches

**Purpose**: Code reorganization without changing functionality

**Format**: `refactor/<scope>/<description>`

**Examples**:
```bash
# Code structure
refactor/server/extract-auth-module
refactor/client/simplify-error-handling

# Project organization
refactor/structure/consolidate-configs
refactor/tools/unified-setup-script

# Documentation reorganization
refactor/docs/hierarchical-structure
refactor/examples/consistent-formatting
```

**Best Practices**:
- No functional changes or new features
- Focus on improving code quality or organization
- Document the reorganization clearly

---

### 5. Example Branches

**Purpose**: New educational examples or extending existing ones

**Format**: `example/<protocol>/<description>`

**Examples**:
```bash
# New A2A examples
example/a2a/prompt-injection-attack
example/a2a/credential-stuffing
example/a2a/session-hijacking

# New MCP examples
example/mcp/resource-validation
example/mcp/tool-security

# Integration examples
example/integration/a2a-mcp-workflow
example/integration/multi-protocol-agent
```

**Best Practices**:
- Always include the protocol (a2a/mcp/integration)
- Describe the security concept demonstrated
- Create comprehensive examples (all stages)

---

### 6. Stage-Specific Branches

**Purpose**: Work specific to a particular stage

**Format**: `stage/<stage-number>/<description>`

**Examples**:
```bash
# Stage improvements
stage/stage1/add-sql-injection-demo
stage/stage2/partial-auth-implementation
stage/stage3/comprehensive-validation

# Stage-specific fixes
stage/stage1/fix-attack-demonstrations
stage/stage2/update-bypass-scripts
stage/stage3/enhance-security-controls
```

**Best Practices**:
- Always specify the stage number
- Focus on stage-specific content
- Maintain stage progression consistency

---

### 7. Test Branches

**Purpose**: Adding or improving tests

**Format**: `test/<scope>/<description>`

**Examples**:
```bash
# New test suites
test/adversarial/integration-tests
test/security/penetration-tests

# Test improvements
test/stage1/attack-validation
test/stage3/security-verification

# Test infrastructure
test/tools/automated-ci
test/framework/test-harness
```

**Best Practices**:
- Clearly indicate what's being tested
- Include test type (unit/integration/e2e)
- Document test coverage

---

### 8. Chore Branches

**Purpose**: Maintenance, dependencies, configuration

**Format**: `chore/<scope>/<description>`

**Examples**:
```bash
# Dependency updates
chore/deps/update-requirements
chore/deps/security-patches

# Configuration
chore/config/update-gitignore
chore/config/improve-editorconfig

# Repository maintenance
chore/cleanup/remove-deprecated-files
chore/automation/github-actions
```

**Best Practices**:
- Use for non-code, non-docs maintenance
- Keep changes focused
- Document reason for changes

---

## 🏷️ Special Cases

### Multi-Scope Work
When work spans multiple areas:
```bash
# Prefer the primary type
feature/integration/a2a-mcp-full-example

# Or combine with descriptive scope
refactor/project-wide/consistent-naming
```

### Hotfixes
For urgent production issues:
```bash
hotfix/<description>
hotfix/critical-security-patch
hotfix/broken-deployment
```

### Experimental Work
For trying out ideas:
```bash
experiment/<description>
experiment/new-auth-pattern
experiment/alternative-architecture
```

### Personal Branches
For work in progress:
```bash
<username>/<description>
robertf/exploring-new-validation
```

---

## ❌ Anti-Patterns

### Don't Do This:
```bash
# Too vague
fix/bugs
update-docs
my-changes

# Too long
feature/add-comprehensive-multi-stage-adversarial-agent-example-with-sql-injection

# Inconsistent casing
Feature/NewExample
DOCS/update-readme
Fix/Stage-1/Bug

# Non-descriptive
branch1
temp
test
wip
```

### Do This Instead:
```bash
# Specific and clear
fix/stage1/sql-demo-timeout
docs/readme/add-installation-steps
feature/auth/oauth2-implementation

# Concise but meaningful
example/a2a/sqli-attack
docs/security/update-threat-model
refactor/structure/simplify-dirs
```

---

## 🔄 Branch Lifecycle

### 1. Create Branch
```bash
# From main/develop
git checkout main
git pull origin main
git checkout -b feature/your-scope/description
```

### 2. Work on Branch
```bash
# Make changes
git add .
git commit -m "feat: Add initial implementation"

# Push regularly
git push origin feature/your-scope/description
```

### 3. Keep Updated
```bash
# Periodically sync with main
git checkout main
git pull origin main
git checkout feature/your-scope/description
git rebase main
```

### 4. Create Pull Request
- Use the PR template
- Link related issues
- Request reviews

### 5. After Merge
```bash
# Delete local branch
git checkout main
git pull origin main
git branch -d feature/your-scope/description

# Delete remote branch (usually done by GitHub)
git push origin --delete feature/your-scope/description
```

---

## 📊 Examples by Project Area

### Documentation Reorganization (Current Phase 2 Work)
```bash
docs/reorganize/mcp-deep-dives
docs/reorganize/create-summaries
docs/reorganize/update-navigation
docs/structure/progressive-learning
```

### Security Examples
```bash
example/a2a/sqli-attack
example/a2a/xss-vulnerability
example/a2a/csrf-demonstration
stage/stage1/add-vulnerabilities
stage/stage3/comprehensive-defense
```

### Tool Development
```bash
feature/tools/security-scanner
feature/tools/automated-testing
fix/tools/setup-script-errors
refactor/tools/consolidate-utilities
```

### Integration Work
```bash
feature/integration/a2a-mcp-example
docs/integration/use-cases
example/integration/multi-protocol
```

---

## ✅ Checklist

Before creating a branch:
- [ ] Chose appropriate type prefix
- [ ] Included meaningful scope
- [ ] Used descriptive, concise name
- [ ] Used lowercase with hyphens
- [ ] Checked for similar existing branches
- [ ] Branch name is under 50 characters
- [ ] Name clearly conveys the purpose

---

## 📞 Questions?

If you're unsure about branch naming:
1. Check existing branches for patterns
2. Ask in the PR discussion
3. Refer to this guide
4. When in doubt, be descriptive and consistent

---

## 🔗 Related Documentation

- [Commit Conventions](./COMMIT_CONVENTIONS.md)
- [Contributing Guide](../docs/about/contributing.md)
- [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)

---

**Document Version**: 1.0  
**Maintained By**: Robert Fischer  
**Last Updated**: December 2025
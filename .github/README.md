# GitHub Configuration & Automation

This directory contains GitHub-specific configuration files, templates, and automated workflows for the A2A/MCP Security Education Project.

---

## 📋 Contents

### Templates
- **[PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md)** - PR submission template
- **[ISSUE_TEMPLATE/](ISSUE_TEMPLATE/)** - Issue templates for different types
  - `bug_report.md` - Report bugs or issues
  - `feature_request.md` - Suggest new features
  - `example_proposal.md` - Propose new educational examples
  - `documentation.md` - Suggest documentation improvements
  - `config.yml` - Issue template configuration

### Workflows
- **[workflows/link-checker.yml](workflows/link-checker.yml)** - Automated link checking
- **[workflows/pr-labeler.yml](workflows/pr-labeler.yml)** - Automatic PR labeling

### Configuration
- **[labeler.yml](labeler.yml)** - PR auto-labeling rules

---

## 🎫 Issue Templates

### Bug Report
**When to use**: Something isn't working correctly

**Includes**:
- Bug description
- Environment details
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

[Create Bug Report →](https://github.com/robertfischer3/fischer3_a2a_introduction/issues/new?template=bug_report.md)

---

### Feature Request
**When to use**: Suggesting new functionality or improvements

**Includes**:
- Feature description
- Problem it solves
- Proposed solution
- Educational value
- Success criteria

[Create Feature Request →](https://github.com/robertfischer3/fischer3_a2a_introduction/issues/new?template=feature_request.md)

---

### Example Proposal
**When to use**: Proposing a new educational security example

**Includes**:
- Example overview
- Security concepts demonstrated
- 3-stage structure plan
- Vulnerability details
- Implementation timeline

[Propose Example →](https://github.com/robertfischer3/fischer3_a2a_introduction/issues/new?template=example_proposal.md)

---

### Documentation Improvement
**When to use**: Suggesting documentation enhancements

**Includes**:
- Issue description
- Location of problem
- Current vs suggested content
- Impact assessment

[Suggest Doc Improvement →](https://github.com/robertfischer3/fischer3_a2a_introduction/issues/new?template=documentation.md)

---

## 📝 Pull Request Template

**Automatically loaded** when creating a PR

**Sections**:
- Description of changes
- Type of change (docs, feature, fix, etc.)
- Testing completed
- Documentation updates
- Security checklist
- Related issues

**Tips**:
- Fill out all applicable sections
- Link related issues
- Check all relevant boxes
- Be thorough but concise

---

## 🤖 Automated Workflows

### Link Checker
**File**: `workflows/link-checker.yml`

**Runs**:
- On PRs that modify `.md` files
- Weekly (Mondays at 9am UTC)
- Manually via workflow dispatch

**Actions**:
- Checks all markdown files for broken links
- Validates internal and external links
- Creates issue if broken links found
- Also runs markdown linting

**Why**: Keeps documentation reliable and professional

---

### PR Labeler
**File**: `workflows/pr-labeler.yml`

**Runs**: On PR open, sync, or reopen

**Actions**:
- Adds labels based on changed files
- Adds size label (XS/S/M/L/XL)
- Detects breaking changes
- Flags security-related PRs

**Labels Applied**:
- `documentation` - Docs changes
- `a2a` / `mcp` - Protocol specific
- `stage-1/2/3` - Stage specific
- `examples` - Example code
- `tools` - Utilities and scripts
- `python` - Python code changes
- `security` - Security related
- `size/*` - PR size (based on lines changed)
- `breaking-change` - Breaking changes

**Why**: Improves organization and makes reviews easier

---

## 🏷️ Labeler Configuration

**File**: `labeler.yml`

Defines rules for automatic PR labeling based on file paths.

**Example Rules**:
```yaml
documentation:
  - changed-files:
    - any-glob-to-any-file: 
      - 'docs/**/*.md'
      - '*.md'

a2a:
  - changed-files:
    - any-glob-to-any-file:
      - 'docs/a2a/**'
      - 'examples/a2a_*/**'
```

**To modify**: Edit `labeler.yml` and add new patterns as needed

---

## 🛠️ Customization Guide

### Adding a New Issue Template

1. Create new file in `ISSUE_TEMPLATE/`:
   ```bash
   touch .github/ISSUE_TEMPLATE/your_template.md
   ```

2. Add frontmatter:
   ```markdown
   ---
   name: Template Name
   about: Description of when to use this
   title: '[PREFIX] '
   labels: ['label1', 'label2']
   assignees: ''
   ---
   ```

3. Add template content

4. Update `config.yml` if needed

---

### Adding a New Workflow

1. Create file in `workflows/`:
   ```bash
   touch .github/workflows/your-workflow.yml
   ```

2. Define workflow:
   ```yaml
   name: Your Workflow
   
   on:
     pull_request:
     push:
       branches: [main]
   
   jobs:
     your-job:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Your step
           run: echo "Hello"
   ```

3. Test on a PR

4. Document in this README

---

### Modifying Labeler Rules

1. Edit `.github/labeler.yml`

2. Add new label rules:
   ```yaml
   your-label:
     - changed-files:
       - any-glob-to-any-file:
         - 'your/path/**'
   ```

3. Test on a PR

---

## 📊 Metrics & Insights

### Link Checker Results
- View in [Actions tab](https://github.com/robertfischer3/fischer3_a2a_introduction/actions)
- Check for issues labeled `broken-links`
- Review weekly reports

### PR Label Statistics
- Most common labels
- Size distribution
- Review time by label
- Available in GitHub Insights

---

## 🔧 Maintenance

### Regular Tasks
- [ ] Review link checker results weekly
- [ ] Update labeler rules for new patterns
- [ ] Keep workflows up to date
- [ ] Add new issue templates as needed
- [ ] Test workflows on test PRs

### Updates Needed When
- New documentation sections added → Update labeler
- New file types introduced → Update link checker exclusions
- New contribution types → Add issue templates
- Process changes → Update PR template

---

## 📚 Related Documentation

- [Contributing Guide](../docs/about/contributing.md)
- [Contribution Workflow](../docs/CONTRIBUTING_WORKFLOW.md)
- [Branch Naming](../docs/BRANCH_NAMING.md)
- [Commit Conventions](../docs/COMMIT_CONVENTIONS.md)
- [Quick Reference](../docs/QUICK_REFERENCE.md)

---

## 🤝 Contributing to Automation

Have ideas for better automation?

1. Open a discussion
2. Propose the workflow/template
3. Submit a PR with changes
4. Update this README

**Ideas we're open to**:
- Automated testing workflows
- Security scanning
- Dependency updates (Dependabot)
- Automated changelog generation
- Code quality checks
- More sophisticated labeling

---

## 📞 Questions?

- Ask in [Discussions](https://github.com/robertfischer3/fischer3_a2a_introduction/discussions)
- Open an [Issue](https://github.com/robertfischer3/fischer3_a2a_introduction/issues)
- Email: robert@fischer3.org

---

**Maintained By**: Robert Fischer  
**Last Updated**: December 2025  
**Version**: 1.0

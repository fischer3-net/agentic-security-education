# Contributor Quick Reference Card

> **Print this** and keep it handy while contributing!

---

## 🔀 Branch Naming Cheat Sheet

```
<type>/<scope>/<description>

feature/auth/oauth2-support
docs/readme/improve-setup
fix/stage1/demo-script
example/a2a/csrf-demo
refactor/server/extract-module
test/security/add-validation
chore/deps/update-requirements
stage/stage3/enhance-validation
```

**Types**: feature, docs, fix, refactor, example, stage, test, chore

---

## 💬 Commit Message Cheat Sheet

```
<type>: <subject>

[optional body]

[optional footer]
```

**Types**: 
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code restructure
- `test:` Tests
- `chore:` Maintenance
- `stage1:`, `stage2:`, `stage3:` Stage work

**Example**:
```
feat: Add OAuth2 authentication

Implement password grant flow with:
- Token generation/validation
- Refresh tokens
- Rate limiting

Closes #42
```

**Rules**:
- ✅ 50 chars or less for subject
- ✅ Imperative mood ("Add" not "Added")
- ✅ No period at end
- ✅ Capitalize first letter
- ✅ Wrap body at 72 chars

---

## 🚀 Quick Workflow

```bash
# 1. Fork & Clone
git clone https://github.com/YOUR_USERNAME/repo.git
git remote add upstream https://github.com/original/repo.git

# 2. Create Branch
git checkout main
git pull upstream main
git checkout -b type/scope/description

# 3. Make Changes
# ... edit files ...

# 4. Commit
git add .
git commit -m "type: description"

# 5. Push
git push origin type/scope/description

# 6. Create PR on GitHub

# 7. After merge, cleanup
git checkout main
git pull upstream main
git branch -d type/scope/description
git push origin main
```

---

## 📋 PR Checklist

Before submitting:
- [ ] Branch name follows convention
- [ ] Commits follow convention
- [ ] Code tested and works
- [ ] Documentation updated
- [ ] No sensitive data included
- [ ] Fictitious data only
- [ ] PR template filled out
- [ ] Related issues linked

---

## 🔧 Common Git Commands

```bash
# Check status
git status

# See what changed
git diff
git diff --staged

# Undo uncommitted changes
git checkout -- filename.py
git reset HEAD filename.py

# Amend last commit
git commit --amend

# Update from upstream
git fetch upstream
git merge upstream/main

# Rebase branch
git rebase main

# Resolve conflicts
git add <resolved-files>
git rebase --continue

# Force push (careful!)
git push origin branch-name --force-with-lease

# Delete branch
git branch -d branch-name
git push origin --delete branch-name
```

---

## 🏷️ Useful Labels

GitHub will auto-label, but know these:
- `documentation` - Docs changes
- `bug` - Something broken
- `enhancement` - New feature
- `good-first-issue` - Beginner friendly
- `security` - Security related
- `a2a` / `mcp` - Protocol specific
- `stage-1/2/3` - Stage specific
- `size/XS-XL` - PR size

---

## 🚨 Emergency Procedures

### Pushed Sensitive Data
```bash
# 1. Remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# 2. Force push
git push origin --force --all

# 3. Email maintainer immediately
# 4. Rotate all exposed credentials
```

### Wrong Branch
```bash
# Save work to new branch
git checkout -b correct-branch

# Reset main
git checkout main
git reset --hard upstream/main
```

---

## 📞 Get Help

- 💬 [Discussions](https://github.com/robertfischer3/fischer3_a2a_introduction/discussions)
- 🐛 [Issues](https://github.com/robertfischer3/fischer3_a2a_introduction/issues)
- 📧 Email: robert@fischer3.org
- 📚 [Full Workflow Guide](./CONTRIBUTING_WORKFLOW.md)

---

## ✅ Quality Standards

**Code**:
- Clear variable names
- Comprehensive docstrings
- Type hints (Python)
- Error handling
- Security considerations
- No real credentials

**Documentation**:
- Clear headings
- Practical examples
- Cross-references
- No broken links
- Proper grammar
- Diagrams where helpful

**Examples**:
- All stages complete
- Attack demonstrations
- Security analysis
- Comprehensive README
- Fictitious data only
- Educational explanations

---

## 🎯 Remember

- One logical change per PR
- Clear commit messages
- Complete testing before submitting
- Security first, always
- Be respectful and collaborative
- Have fun learning! 🚀

---

**Version**: 1.0 | **Updated**: Dec 2025
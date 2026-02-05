# Development Tools & Utilities

**Essential tools and utilities for Agentic AI Security project development**

This directory contains documentation for tools that make developing, testing, and maintaining the project easier. Whether you're setting up your environment, checking documentation quality, or managing Python dependencies, you'll find the resources you need here.

---

## 🎯 Quick Navigation

<div class="grid cards" markdown>

-   :material-package-variant:{ .lg .middle } __Python Environment Management__

    ---

    Fast, modern Python package management with UV - the recommended tool for this project.

    [:octicons-arrow-right-24: UV Quick Start](#python-environment-management-uv)

-   :material-link-variant:{ .lg .middle } __Documentation Quality Tools__

    ---

    Scripts to find and fix broken links in markdown documentation.

    [:octicons-arrow-right-24: Link Checkers](#documentation-quality-tools)

-   :material-ubuntu:{ .lg .middle } __Ubuntu/Linux Setup__

    ---

    Specific guidance for Ubuntu and Linux development environments.

    [:octicons-arrow-right-24: Ubuntu Guide](#ubuntulinux-specific-tools)

</div>

---

## Python Environment Management (UV)

**Why UV?** UV is a blazing-fast Python package manager (10-100x faster than pip) written in Rust. It's the recommended tool for managing Python dependencies in this project.

### Available Resources

**Quick References**:
- 📋 **[UV Quick Reference Card](./UV_QUICK_CARD.txt)** - Single-page cheat sheet (1 minute)
- 📝 **[UV Cheat Sheet](./uv_cheatsheet.md)** - Common commands and workflows (5 minutes)

**Comprehensive Guides**:
- 📖 **[UV Complete Guide](./UV_COMPLETE_GUIDE.md)** - Overview of all UV documentation (10 minutes)
- 📘 **[UV Guide](./uv_guide.md)** - Full usage guide with examples (20 minutes)
- 🔄 **[pip vs UV Comparison](./pip_vs_uv_comparison.md)** - Migration guide from pip

**Automation Scripts**:
- 🚀 **[Setup with UV](./setup_with_uv.sh)** - Automated MCP server setup demo
- 🏗️ **[Complete Project Setup](./complete_project_setup.sh)** - Full project scaffolding

### Quick Start with UV

```bash
# Install UV
pip install uv --break-system-packages

# Create virtual environment for this project
cd agentic-security-education
uv venv
source .venv/bin/activate

# Install project dependencies
uv pip install -r requirements.txt

# Speed comparison: UV is 10-100x faster than pip!
```

### Common UV Commands for This Project

```bash
# Create environment
uv venv                              # Create .venv/

# Install packages
uv pip install mcp httpx pydantic    # Install MCP dependencies
uv pip install -r requirements.txt   # Install from requirements

# Manage dependencies
uv pip list                          # List installed packages
uv pip freeze > requirements.txt     # Save current state

# Work with examples
cd examples/a2a_crypto_example
uv venv                              # Separate environment per example
source .venv/bin/activate
uv pip install -r requirements.txt
```

### When to Use UV vs pip

| Scenario | Recommended Tool | Why |
|----------|-----------------|-----|
| New project setup | UV | 10-100x faster |
| Installing dependencies | UV | Better resolution |
| CI/CD pipelines | UV | Faster builds |
| Legacy projects | pip | If UV not available |
| Documentation building | Either | Speed less critical |

**Bottom line**: Use UV for all Python development in this project unless you have a specific reason not to.

---

## Documentation Quality Tools

These tools help maintain high-quality documentation by finding and fixing broken links.

### Link Checker Scripts

Located in `utils/` directory (not `docs/supplementary/tools`):

**Primary Tool**:
- 🔍 **[markdown_link_checker.py](../../utils/markdown_link_checker.py)** - All-in-one checker with fix suggestions
  - Finds broken links
  - Suggests similar files as fixes
  - Calculates relative paths
  - Generates detailed reports

**Supporting Tools**:
- ✅ **[check_markdown_links.py](../../utils/check_markdown_links.py)** - Basic link validation
- 🔧 **[fix_markdown_links.py](../../utils/fix_markdown_links.py)** - Fix suggester with auto-fix for 100% matches

**Documentation**:
- 📖 **[Link Checker README](../../utils/README_LINK_CHECKER.md)** - Complete usage guide
- 📋 **[Fix Links Guide](../../utils/fix_markdown_links_guide.md)** - Auto-fix documentation

### Using Link Checkers

```bash
# From project root

# Check all documentation
python3 utils/markdown_link_checker.py docs/

# Check specific directory
python3 utils/markdown_link_checker.py docs/a2a/

# Auto-fix 100% matches (dry run first!)
python3 utils/fix_markdown_links.py docs/ --fix-100 --dry-run

# Actually fix
python3 utils/fix_markdown_links.py docs/ --fix-100
```

### When to Run Link Checkers

- ✅ Before committing documentation changes
- ✅ After restructuring documentation
- ✅ Before major releases
- ✅ When adding new examples
- ✅ Periodically (monthly) to catch link rot

---

## Ubuntu/Linux Specific Tools

Special resources for Ubuntu and Linux development environments.

### Available Resources

- 🐧 **[Ubuntu Quickstart Guide](./UBUNTU_QUICKSTART.md)** - Getting started on Ubuntu
- 🛠️ **[MCP Testing on Ubuntu](../../mcp_examples/your_first_mcp_server/MCP_TESTING_UBUNTU.md)** - Testing MCP servers without Claude Desktop

### Ubuntu-Specific Notes

**Package Installation**:
```bash
# Use --break-system-packages for UV
pip install uv --break-system-packages

# Or use pipx (recommended for Ubuntu 24.04+)
sudo apt install pipx
pipx install uv
pipx ensurepath
```

**MCP Server Testing**:
- Claude Desktop is not available for Linux
- Use MCP Inspector (web-based) instead
- See [MCP Testing Ubuntu Guide](../../mcp_examples/your_first_mcp_server/MCP_TESTING_UBUNTU.md)

---

## Tools by Use Case

### Setting Up Development Environment

1. **[UV Complete Guide](./UV_COMPLETE_GUIDE.md)** - Modern Python environment
2. **[Ubuntu Quickstart](./UBUNTU_QUICKSTART.md)** - Ubuntu-specific setup
3. **[Complete Project Setup Script](./complete_project_setup.sh)** - Automated scaffolding

### Working with Examples

1. **[UV Quick Card](./UV_QUICK_CARD.txt)** - Fast dependency management
2. Example-specific requirements.txt files
3. Virtual environment per example (recommended)

### Maintaining Documentation

1. **[Markdown Link Checker](../../utils/markdown_link_checker.py)** - Find broken links
2. **[Fix Markdown Links](../../utils/fix_markdown_links.py)** - Suggest/apply fixes
3. **[Link Checker README](../../utils/README_LINK_CHECKER.md)** - Full documentation

### Contributing to the Project

1. **[UV Guide](./uv_guide.md)** - Dependency management
2. **[Link Checker](../../utils/markdown_link_checker.py)** - Validate documentation
3. **[Contributing Guidelines](../../about/contributing.md)** - Contribution process

---

## Tool Comparison

### Python Package Managers

| Feature | pip | UV | Recommendation |
|---------|-----|----|--------------| 
| Speed | Baseline | 10-100x faster | ⭐ Use UV |
| Dependency resolution | Basic | Advanced | ⭐ Use UV |
| Lock files | Manual | Built-in | ⭐ Use UV |
| Python version management | No | Yes | ⭐ Use UV |
| Legacy support | Excellent | Good | Use pip if needed |

### Link Checkers

| Script | Purpose | Best For |
|--------|---------|----------|
| markdown_link_checker.py | All-in-one | ⭐ Most users |
| check_markdown_links.py | Basic checking | Simple validation |
| fix_markdown_links.py | Auto-fixing | Bulk updates |

---

## Recommended Workflow

### Initial Setup

```bash
# 1. Install UV
pip install uv --break-system-packages

# 2. Create project environment
cd agentic-security-education
uv venv
source .venv/bin/activate

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Verify installation
python -c "import mcp; print('MCP installed successfully')"
```

### Daily Development

```bash
# Activate environment
source .venv/bin/activate

# Install new packages as needed
uv pip install <package>

# Update requirements
uv pip freeze > requirements.txt

# Check documentation links before committing
python3 utils/markdown_link_checker.py docs/
```

### Before Committing

```bash
# Check for broken links
python3 utils/markdown_link_checker.py docs/

# Fix 100% matches
python3 utils/fix_markdown_links.py docs/ --fix-100 --dry-run

# Update requirements if dependencies changed
uv pip freeze > requirements.txt

# Git commit
git add .
git commit -m "Your changes"
```

---

## Additional Resources

### Official Documentation
- **[UV Documentation](https://github.com/astral-sh/uv)** - Official UV repository
- **[Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)** - Python venv docs

### Project Documentation
- **[Installation Guide](../../guides/installation.md)** - Complete installation instructions
- **[Quick Start](../../guides/quickstart.md)** - Get running fast
- **[A2A Documentation](../../index.md)** - Protocol documentation

### Related Tools
- **[MCP Examples](../../mcp_examples/)** - MCP server examples
- **[A2A Examples](../../examples/)** - A2A implementation examples

---

## Contributing

Found a bug in these tools? Have a suggestion for improvement?

1. **Documentation issues**: Edit the relevant guide
2. **Tool enhancements**: Submit improvements via pull request
3. **New tools**: Propose in [GitHub Discussions](https://github.com/fischer3-net/agentic-security-education/discussions)

See **[Contributing Guidelines](../../about/contributing.md)** for details.

---

## Questions?

**For UV/Python questions**:
- Read the **[UV Complete Guide](./UV_COMPLETE_GUIDE.md)**
- Check the **[UV Cheat Sheet](./uv_cheatsheet.md)**
- See **[pip vs UV Comparison](./pip_vs_uv_comparison.md)**

**For link checker questions**:
- Read the **[Link Checker README](../../utils/README_LINK_CHECKER.md)**
- See **[Fix Links Guide](../../utils/fix_markdown_links_guide.md)**

**For general setup**:
- See **[Installation Guide](../../guides/installation.md)**
- Ubuntu users: **[Ubuntu Quickstart](./UBUNTU_QUICKSTART.md)**

**Still stuck?**
- Email: robert@fischer3.net
- GitHub: [Open an issue](https://github.com/fischer3-net/agentic-security-education/issues)

---

**Last Updated**: January 2026  
**Maintainer**: Robert Fischer  
**Status**: Active Maintenance
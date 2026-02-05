# UV for Agentic AI Security Development - Complete Guide

**Fast Python package management for A2A Protocol and MCP development**

---

## 📚 What is UV?

UV is an extremely fast Python package installer and resolver written in Rust - **10-100x faster than pip**. It's the recommended dependency management tool for this project due to its speed and superior dependency resolution.

---

## 🎯 Why UV for This Project?

### Speed Matters

When working with multiple examples and stages:
- **Stage 1-5 examples**: Each may need separate environments
- **Multiple Python versions**: Testing across Python 3.10, 3.11, 3.12
- **Rapid iteration**: Faster installs = faster development

### Better Dependency Resolution

Agent development involves complex dependencies:
- **MCP SDK**: Tools and resource management
- **A2A Libraries**: Protocol implementation
- **Security libraries**: cryptography, PyJWT, bcrypt
- **AI SDKs**: When integrating with LLMs

UV resolves these dependencies more reliably than pip.

---

## 🚀 Quick Start for This Project

### Install UV

```bash
# Ubuntu/Linux
pip install uv --break-system-packages

# Or use the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

### Set Up Project Environment

```bash
# Navigate to project root
cd agentic-security-education

# Create virtual environment
uv venv

# Activate
source .venv/bin/activate  # Linux/Mac

# Install project dependencies
uv pip install -r requirements.txt
```

### Work with Examples

Each example can have its own environment:

```bash
# Example 1: Cryptocurrency Agent
cd examples/a2a_crypto_example
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python insecure_agent.py

# Example 2: Credit Report Agent
cd examples/a2a_credit_report_example/stage1_insecure
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python server.py
```

---

## 📖 UV Documentation Files

This guide is part of a complete UV documentation package:

### Quick References (Start Here!)
1. **[UV_QUICK_CARD.txt](./UV_QUICK_CARD.txt)** - 1-page visual reference card
2. **[uv_cheatsheet.md](./uv_cheatsheet.md)** - Common commands table

### Comprehensive Guides
3. **[uv_guide.md](./uv_guide.md)** - Full usage documentation
4. **[pip_vs_uv_comparison.md](./pip_vs_uv_comparison.md)** - Migration from pip

### Automation Scripts
5. **[setup_with_uv.sh](./setup_with_uv.sh)** - MCP server demo setup
6. **[complete_project_setup.sh](./complete_project_setup.sh)** - Full project scaffold

### Platform-Specific
7. **[UBUNTU_QUICKSTART.md](./UBUNTU_QUICKSTART.md)** - Ubuntu/Linux setup

---

## 💻 Common Workflows for This Project

### Scenario 1: Working with A2A Examples

```bash
# Navigate to an example
cd examples/a2a_task_collab_example/stage1_insecure

# Create isolated environment
uv venv

# Activate
source .venv/bin/activate

# Install dependencies (if requirements.txt exists)
uv pip install -r requirements.txt

# Or install manually
uv pip install asyncio socket json

# Run the example
python server/task_coordinator.py
```

### Scenario 2: Developing MCP Servers

```bash
# Create new MCP server project
mkdir my-mcp-server && cd my-mcp-server

# Create environment with specific Python version
uv venv --python 3.12

# Activate
source .venv/bin/activate

# Install MCP SDK and dependencies
uv pip install mcp httpx pydantic

# Start coding
# (See mcp_examples/ for templates)
```

### Scenario 3: Working Across Multiple Stages

```bash
# Each stage can have its own environment
cd examples/a2a_crypto_example

# Stage 1
cd stage1_vulnerable
uv venv
source .venv/bin/activate
# ... work on stage 1

# Stage 2
deactivate
cd ../stage2_improved
uv venv
source .venv/bin/activate
# ... work on stage 2

# Stage 3
deactivate
cd ../stage3_secure
uv venv
source .venv/bin/activate
uv pip install cryptography PyJWT bcrypt
# ... work on stage 3
```

### Scenario 4: Testing Security Controls

```bash
# Set up environment for security testing
cd examples/a2a_crypto_example/stage3_secure

uv venv
source .venv/bin/activate

# Install security libraries
uv pip install cryptography PyJWT bcrypt pycryptodome

# Install testing tools
uv pip install pytest pytest-asyncio

# Run security tests
pytest tests/
```

---

## 🔑 Essential UV Commands

### Environment Management

```bash
# Create virtual environment
uv venv                        # In .venv/
uv venv myenv                  # Custom name
uv venv --python 3.12          # Specific Python version

# Activate (Linux/Mac)
source .venv/bin/activate

# Deactivate
deactivate
```

### Package Installation

```bash
# Install single package
uv pip install requests

# Install MCP dependencies
uv pip install mcp httpx pydantic

# Install A2A security libraries
uv pip install cryptography PyJWT bcrypt

# Install from requirements
uv pip install -r requirements.txt

# Install for development (editable)
uv pip install -e .
```

### Package Management

```bash
# List installed packages
uv pip list

# Show package details
uv pip show cryptography

# Check for updates
uv pip list --outdated

# Update package
uv pip install --upgrade cryptography

# Save current state
uv pip freeze > requirements.txt
```

---

## 📦 Project-Specific Dependencies

### Core A2A Protocol Dependencies

```bash
# Basic A2A implementation (Stage 1-2)
uv pip install asyncio  # Included in Python
uv pip install socket   # Included in Python

# Stage 3 Security
uv pip install cryptography PyJWT bcrypt

# For examples with web frameworks
uv pip install flask flask-cors

# For Redis-based sessions (Task Collab Stage 4)
uv pip install redis
```

### MCP Development Dependencies

```bash
# Core MCP
uv pip install mcp

# HTTP clients
uv pip install httpx requests

# Data validation
uv pip install pydantic

# For SQLite examples
# (sqlite3 included in Python)

# For testing
uv pip install pytest pytest-asyncio
```

### Documentation Building

```bash
# MkDocs with Material theme
uv pip install mkdocs-material

# Plugins
uv pip install mkdocs-minify-plugin
```

---

## 🎓 Best Practices for This Project

### 1. One Virtual Environment Per Example

```bash
# DON'T: Use one environment for all examples
cd agentic-security-education
uv venv
# Install everything here ❌

# DO: Separate environment per example
cd examples/a2a_crypto_example
uv venv
source .venv/bin/activate
# Install only what this example needs ✅
```

**Why?** Prevents dependency conflicts and keeps examples isolated.

### 2. Lock Your Dependencies

```bash
# After getting an example working
uv pip freeze > requirements.txt

# Commit requirements.txt
git add requirements.txt
git commit -m "Lock dependencies for stage 1"
```

**Why?** Ensures reproducible builds and helps others run your code.

### 3. Use Specific Python Versions

```bash
# Stage 3 uses newer security features
cd stage3_secure
uv venv --python 3.12
source .venv/bin/activate
```

**Why?** Some security libraries work better with newer Python versions.

### 4. Separate Development Dependencies

Create `requirements-dev.txt`:
```
# requirements-dev.txt
-r requirements.txt
pytest>=7.0
pytest-asyncio>=0.21
black>=23.0
mypy>=1.0
```

Install for development:
```bash
uv pip install -r requirements-dev.txt
```

### 5. Keep Environments Clean

```bash
# When switching between examples
deactivate  # Always deactivate first

cd ../different-example
uv venv
source .venv/bin/activate
```

---

## 🔬 Example: Full Workflow

Let's walk through setting up the Task Collaboration example:

```bash
# 1. Navigate to example
cd examples/a2a_task_collab_example

# 2. Set up Stage 1 (insecure)
cd stage1_insecure
uv venv
source .venv/bin/activate

# 3. Check if requirements.txt exists
ls requirements.txt  # If not, create it

# 4. Install dependencies
uv pip install -r requirements.txt
# Or manually if no requirements.txt:
# uv pip install asyncio  # Built-in

# 5. Run the coordinator
python server/task_coordinator.py

# 6. In another terminal, run worker
cd examples/a2a_task_collab_example/stage1_insecure
source .venv/bin/activate
python worker/task_worker.py

# 7. Test with client
cd examples/a2a_task_collab_example/stage1_insecure
source .venv/bin/activate
python client/client.py
```

---

## 🐛 Troubleshooting

### Issue: "uv: command not found"

```bash
# Reinstall
pip install uv --break-system-packages

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Make permanent (add to ~/.bashrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Issue: "Module not found" errors

```bash
# Make sure environment is activated
source .venv/bin/activate

# Verify activation (should show .venv path)
which python

# Reinstall dependencies
uv pip install -r requirements.txt
```

### Issue: Dependency conflicts

```bash
# Create fresh environment
deactivate
rm -rf .venv
uv venv
source .venv/bin/activate

# Install with UV's better resolution
uv pip install -r requirements.txt
```

### Issue: Wrong Python version

```bash
# Specify version explicitly
uv venv --python 3.12

# Or use specific Python
uv venv --python /usr/bin/python3.12
```

---

## 📊 Speed Comparison (Real Project Data)

Based on actual usage in this project:

**Setting up Stage 3 Crypto Example**:
- pip: ~45 seconds (cryptography, PyJWT, bcrypt)
- UV: ~4 seconds
- **Speedup: 11x faster** ⚡

**Setting up Stage 4 Task Collab (Redis)**:
- pip: ~60 seconds (redis, flask, cryptography)
- UV: ~5 seconds
- **Speedup: 12x faster** ⚡

**Building Documentation (MkDocs)**:
- pip: ~90 seconds (mkdocs-material, plugins)
- UV: ~8 seconds
- **Speedup: 11x faster** ⚡

---

## 🎯 Quick Command Reference

### Daily Use

| Task | Command |
|------|---------|
| Create environment | `uv venv` |
| Activate | `source .venv/bin/activate` |
| Install package | `uv pip install <package>` |
| Save state | `uv pip freeze > requirements.txt` |
| Install from file | `uv pip install -r requirements.txt` |
| Deactivate | `deactivate` |

### Development

| Task | Command |
|------|---------|
| List packages | `uv pip list` |
| Check updates | `uv pip list --outdated` |
| Update package | `uv pip install --upgrade <package>` |
| Remove package | `uv pip uninstall <package>` |
| Show details | `uv pip show <package>` |

---

## 🔗 Related Documentation

### In This Directory
- **[UV Quick Card](./UV_QUICK_CARD.txt)** - Fast reference
- **[UV Cheat Sheet](./uv_cheatsheet.md)** - Command tables
- **[UV Guide](./uv_guide.md)** - Comprehensive guide
- **[pip vs UV](./pip_vs_uv_comparison.md)** - Comparison

### Project Documentation
- **[Installation Guide](../../guides/installation.md)** - Full setup
- **[Quick Start](../../guides/quickstart.md)** - Get running fast
- **[Running Examples](../../guides/running-example.md)** - Example usage

### Examples
- **[A2A Examples](../../examples/)** - All A2A examples
- **[MCP Examples](../../../mcp_examples/)** - MCP servers

---

## 🤝 Contributing

Improvements to UV documentation welcome!

- Found an error? Open an issue
- Have a tip? Submit a PR
- Questions? Start a discussion

See **[Contributing Guidelines](../../CONTRIBUTORS_WANTED.md)** for details.

---

**Last Updated**: January 2026  
**Project**: Agentic AI Security Education  
**Maintainer**: Robert Fischer  
**Email**: robert@fischer3.org
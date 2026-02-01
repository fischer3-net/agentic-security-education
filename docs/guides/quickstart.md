# Quick Start Guide

Get up and running with the Agent2Agent (A2A) protocol in under 10 minutes.

## What You'll Build

By the end of this quick start, you'll have:
- ✅ A running A2A agent registry
- ✅ A cryptocurrency price agent
- ✅ A client that discovers and connects to the agent
- ✅ Understanding of basic A2A concepts

## Prerequisites

```bash
# Python 3.10 or higher
python3 --version

# pip package manager
pip --version
```

## 5-Minute Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/robertfischer3/fischer3_a2a_introduction.git
cd fischer3_a2a_introduction
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install core dependencies
pip install httpx asyncio
```

### Step 3: Start the Registry

The registry is the central directory where agents register themselves.

```bash
cd examples/a2a_crypto_simple_registry_example_1/registry
python registry_server.py
```

You should see:
```
🚀 Starting Agent Registry Server...
✅ Registry is ready
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal running.

### Step 4: Start the Agent

In a **new terminal**, start the cryptocurrency price agent:

```bash
cd examples/a2a_crypto_simple_registry_example_1/server
python crypto_agent_server.py
```

You should see:
```
✅ Registered with A2A Registry
🚀 Crypto Agent Server started on 127.0.0.1:8888
💰 Supported currencies: BTC, ETH, XRP
💓 Heartbeat sent to registry
```

Keep this terminal running.

### Step 5: Run the Client

In a **third terminal**, run the client to interact with the agent:

```bash
cd examples/a2a_crypto_simple_registry_example_1/client
python a2a_client.py
```

You should see:
```
🔍 Discovering agents with 'get_price' capability...
✅ Found 1 agent(s)
📡 Selected: CryptoPriceAgent
🔗 Connecting to localhost:8888...
✅ Connected successfully

💱 A2A Crypto Price Client
──────────────────────────────────────────
Commands:
  price <currency>  - Get current price
  list             - List supported currencies
  help             - Show this help
  quit             - Exit

crypto> price BTC
```

## Try It Out

Now that everything is running, try these commands:

```bash
# Get Bitcoin price
price BTC

# Get Ethereum price  
price ETH

# List all supported currencies
list

# View agent information
info
```

## What Just Happened?

1. **Registry Started**: Central directory for agent discovery
2. **Agent Registered**: Crypto agent announced its capabilities (price_query)
3. **Client Discovered**: Client found the agent via capability search
4. **Connection Established**: Client connected directly to the agent
5. **Messages Exchanged**: Using A2A protocol for communication

## Architecture Overview

!["What just happened"](/docs/images/diagrams/what_just_happened.jpg "What just happened")
## View the Registry Dashboard

Open your browser to see registered agents:
- **Registry Info**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs
- **List Agents**: http://localhost:8000/agents

## Common Commands

### List Available Agents

```bash
python a2a_client.py --list
```

### Test Registry Directly

```bash
# Check registry health
curl http://localhost:8000/health

# List all agents
curl http://localhost:8000/agents

# Discover by capability
curl "http://localhost:8000/agents/discover?capability=get_price"
```

## Troubleshooting

### "Could not connect to registry"
**Solution**: Start the registry first:
```bash
cd registry && python registry_server.py
```

### "No agents found"
**Solution**: Start the agent server:
```bash
cd server && python crypto_agent_server.py
```

### "ImportError: No module named 'httpx'"
**Solution**: Install dependencies:
```bash
pip install httpx
```

### "Port already in use"
**Solution**: Either stop the existing process or change the port:
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in code
```

## Next Steps

Now that you have the basics working:

1. **[Installation Guide](installation.md)** - Set up a production environment
2. **[First Agent Tutorial](first-agent.md)** - Build your own agent from scratch
3. **[A2A Overview](../a2a/00_A2A_OVERVIEW.md)** - Understand the protocol deeply
4. **[Security Best Practices](../a2a/03_SECURITY/04_security_best_practices.md)** - Learn secure patterns

## What You've Learned

✅ How to start an A2A registry  
✅ How agents register their capabilities  
✅ How clients discover agents dynamically  
✅ Basic A2A message protocol  
✅ Service discovery patterns  

## Experiment Further

Try these to learn more:

1. **Start multiple agents** on different ports
2. **Stop one agent** and watch the registry mark it unhealthy
3. **Modify the agent** to add new capabilities
4. **Create a new agent** for a different service (weather, news, etc.)

## Getting Help

- 📖 **Documentation**: Browse the [complete documentation](../a2a/INDEX.md)
- 💬 **Examples**: Explore the [example projects](../../examples/)
- 🔒 **Security**: Read the [security guides](../a2a/03_SECURITY/01_authentication_overview.md)

---

**🎉 Congratulations!** You've successfully set up your first A2A multi-agent system.

Ready to build your own agent? Continue to the **[First Agent Tutorial](first-agent.md)**.
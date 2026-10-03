# 🤖 AI DevOps Engineer From Scratch

Build your own local **AI DevOps Engineer** using:

* 🧠 Ollama
* ⚡ Qwen3 4B
* 🔌 Model Context Protocol (MCP)
* 🐍 Python
* 🐳 Docker
* 🐧 Linux

This project demonstrates how an AI agent can inspect a Linux server through MCP tools and generate a DevOps health report using a local LLM.

---

## 🎥 YouTube Video

**Video:** I Built an AI DevOps Engineer From Scratch 🤖 | Python + Ollama + MCP

📺 **Channel:** Techserverglobal

The project is demonstrated step-by-step in the YouTube video, including:

1. Setting up Ollama
2. Running Qwen3 locally
3. Building an MCP server
4. Creating read-only DevOps tools
5. Connecting the MCP client
6. Connecting Qwen3 to MCP
7. Calling DevOps tools through AI
8. Generating a server health report

---

# 🏗️ Architecture

```text
                         User
                           │
                           │
                           ▼
                 ┌──────────────────┐
                 │   AI DevOps      │
                 │      Agent       │
                 │     Python       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Ollama       │
                 │    Qwen3 4B      │
                 └────────┬─────────┘
                          │
                    Tool Calling
                          │
                          ▼
                 ┌──────────────────┐
                 │    MCP Client    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    MCP Server    │
                 │   Python/MCP     │
                 └────────┬─────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
     System Info        Disk          Processes
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                       Docker
```

---

# 🚀 What Can the AI Do?

The AI DevOps Engineer currently has four read-only tools.

### 1. System Information

```text
get_system_info()
```

Collects:

* Hostname
* Operating system
* Kernel version
* CPU count
* CPU utilization
* Total memory
* Used memory
* Available memory
* Memory utilization

---

### 2. Disk Usage

```text
get_disk_usage()
```

Collects:

* Root filesystem
* Total disk
* Used disk
* Free disk
* Disk utilization percentage

---

### 3. Top Processes

```text
get_top_processes()
```

Returns the top processes based on CPU utilization.

Information includes:

* PID
* Process name
* CPU utilization
* Memory utilization

---

### 4. Docker Containers

```text
list_docker_containers()
```

Returns currently running Docker containers.

Information includes:

* Container name
* Docker image
* Container status

---

# 🔐 Security Design

This first version intentionally uses **read-only DevOps operations**.

The AI does **not** have an unrestricted command execution tool.

For example, the agent does not expose:

```text
execute_command("rm -rf /")
```

or:

```text
docker rm ...
```

The available tools are explicitly defined by the MCP server.

This provides a safer foundation before introducing write operations and automated remediation in future episodes.

---

# 🧰 Technology Stack

| Technology  | Purpose                        |
| ----------- | ------------------------------ |
| Python 3.12 | AI agent and MCP server        |
| Ollama      | Local LLM runtime              |
| Qwen3 4B    | AI model                       |
| MCP         | AI ↔ DevOps tool communication |
| psutil      | System monitoring              |
| Docker CLI  | Container information          |
| Linux       | Host environment               |

---

# 💻 Environment

The project was developed and tested on:

```text
Ubuntu 24.04 LTS
Python 3.12
Docker 29.x
Ollama 0.15.x
MCP Python SDK 2.x
Qwen3 4B
```

The project can also be adapted to other Linux distributions.

---

# 📁 Project Structure

```text
ai-devops-engineer/
│
├── agent/
│   ├── __init__.py
│   └── main.py
│
├── mcp_server/
│   ├── __init__.py
│   └── server.py
│
├── tests/
│   └── test_tools.py
│
├── .gitignore
├── README.md
└── requirement.txt
```

---

# ⚙️ Prerequisites

Install the following:

* Ubuntu/Linux
* Python 3.10+
* Git
* Docker
* Ollama

Verify:

```bash
python3 --version
docker --version
ollama --version
git --version
```

---

# 🧠 Install Qwen3

Pull the Qwen3 4B model:

```bash
ollama pull qwen3:4b
```

Verify:

```bash
ollama list
```

You should see:

```text
qwen3:4b
```

Test the model:

```bash
ollama run qwen3:4b
```

Example:

```text
You are a DevOps engineer.
Explain what Kubernetes is.
```

Exit:

```text
/bye
```

---

# 🐍 Setup Python Environment

Clone the repository:

```bash
git clone https://github.com/<YOUR_USERNAME>/ai-devops-engineer.git
cd ai-devops-engineer
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install "mcp[cli]" ollama psutil python-dotenv
```

---

# 🔌 MCP Server

The MCP server exposes the DevOps monitoring tools.

Start it through the AI agent:

```bash
python3 agent/main.py
```

The agent starts the MCP server automatically.

---

# 🧪 Test MCP Connectivity

When the agent starts successfully, you should see:

```text
============================================================
 AI DEVOPS ENGINEER
============================================================

Available MCP tools:

✓ get_system_info
✓ get_disk_usage
✓ get_top_processes
✓ list_docker_containers
```

This confirms that the Python MCP client can communicate with the MCP server.

---

# 🤖 Run the AI DevOps Engineer

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run:

```bash
python3 agent/main.py
```

You can then ask:

```text
Give me a complete DevOps health report of this server.
Check CPU, memory, disk usage, running processes and Docker containers.
```

The AI can decide which MCP tools are required.

---

# 🔄 AI Tool Calling Flow

For example:

```text
User
 │
 │ "Give me a server health report"
 ▼
Qwen3
 │
 │ decides tools are required
 ▼
MCP Client
 │
 ▼
MCP Server
 │
 ├── get_system_info()
 │
 ├── get_disk_usage()
 │
 ├── get_top_processes()
 │
 └── list_docker_containers()
 │
 ▼
Tool Results
 │
 ▼
Qwen3
 │
 ▼
DevOps Health Report
```

---

# 📊 Example

Example user request:

```text
Give me a complete DevOps health report.
```

The agent can collect information such as:

```text
CPU Usage: 18%
Memory Usage: 46%
Disk Usage: 61%

Top Processes:
python
docker
ollama
...

Docker Containers:
kind-control-plane
kind-worker
kind-worker2
```

Qwen3 then analyzes the collected information and presents it as a human-readable DevOps report.

---

# 🐳 Docker Environment

If Docker containers are running:

```bash
docker ps
```

The MCP tool:

```text
list_docker_containers()
```

retrieves the currently running containers.

For example:

```text
kind-control-plane
kind-worker
kind-worker2
```

The AI can therefore include container information in its server health analysis.

---

# 🧪 Manual Tool Testing

You can independently verify Docker:

```bash
docker ps
```

Disk:

```bash
df -h
```

Memory:

```bash
free -h
```

CPU/processes:

```bash
top
```

The MCP server provides programmatic access to equivalent monitoring information.

---

# 🛡️ Why MCP?

Without MCP, an AI application would need custom integrations for every DevOps system.

MCP provides a standardized interface between the AI model and external tools.

Conceptually:

```text
AI Model
   │
   ▼
MCP
   │
   ├── Linux
   ├── Docker
   ├── Kubernetes
   ├── AWS
   ├── Jenkins
   └── Monitoring
```

This makes it possible to progressively expand the AI DevOps Engineer.

---

# 🚧 Current Limitations

This is **Episode 01**, so the agent intentionally has limited capabilities.

Currently:

* Read-only operations
* Linux system information
* Disk monitoring
* Process monitoring
* Docker container monitoring
* Local LLM

It does not currently:

* Restart containers
* Delete containers
* Modify Kubernetes resources
* Deploy applications
* Execute arbitrary shell commands
* Modify AWS infrastructure
* Modify Jenkins pipelines

These capabilities will be introduced progressively in future episodes.

---

# 🗺️ AI DevOps Series Roadmap

### Episode 01

**I Built an AI DevOps Engineer From Scratch**

Python + Ollama + MCP

---

### Episode 02

**I Gave AI Access to My Kubernetes Cluster**

AI + Kubernetes + MCP

---

### Episode 03

**AI Troubleshoots a Broken Kubernetes Pod**

AI-powered Kubernetes troubleshooting.

---

### Episode 04

**I Built a Self-Healing Kubernetes Cluster**

AI detects and performs controlled remediation.

---

### Episode 05

**MCP + Kubernetes: AI Controls My Cluster**

Expand MCP capabilities for Kubernetes.

---

### Episode 06

**AI Deploys a Docker Application to Kubernetes**

AI-assisted deployment workflow.

---

### Episode 07

**AI Builds a CI/CD Pipeline With Jenkins**

AI + Jenkins + CI/CD.

---

### Episode 08

**AI Finds the Most Expensive AWS Resources**

AI + AWS cost analysis.

---

### Episode 09

**I Built a Local AI SRE Using Ollama**

Combine monitoring, troubleshooting and automation.

---

### Episode 10

**Can AI Actually Replace a DevOps Engineer?**

Explore what AI can and cannot automate in DevOps.

---

# 🎯 Learning Objectives

After completing this project, you should understand:

* What MCP is
* How MCP clients and servers communicate
* How AI models use tools
* How Ollama can run LLMs locally
* How Qwen3 can participate in tool calling
* How Python can expose DevOps capabilities to an AI
* How to build read-only infrastructure agents
* Why tool permissions and security boundaries matter

---

# 🔮 Future Improvements

Potential future tools include:

```text
Kubernetes
├── get_pods()
├── get_nodes()
├── get_deployments()
└── describe_pod()

AWS
├── get_ec2_instances()
├── get_cost_report()
├── get_s3_usage()
└── get_cloudwatch_metrics()

Jenkins
├── get_jobs()
├── get_build_status()
└── get_build_logs()

Monitoring
├── get_cpu_metrics()
├── get_memory_metrics()
└── get_alerts()
```

Write operations should be introduced with appropriate authorization and human approval rather than unrestricted execution.

---

# ⭐ Support the Project

If you find this project useful:

⭐ Star the repository

🍴 Fork the repository

📺 Subscribe to Techserverglobal

💬 Share your feedback and ideas for future AI DevOps episodes.

---

# 📜 License

This project is provided for educational and demonstration purposes.

Add an appropriate open-source license to the repository if you plan to distribute the code publicly.

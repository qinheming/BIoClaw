<div align="center">

# 🧬 BloClaw: The Omniscient Scientific Agent
> **The Next-Gen Agentic Workspace for Life Sciences.**

*“We don't need a calculator with 200 predefined buttons. We need a digital scientist that writes its own code, envisions folded molecules in the void, and projects them onto your desk.”*
</div>

---

## 🌌 The Philosophy (Why BloClaw?)

Current AI-for-Science (AI4S) agents focus on *quantity*—manually hardcoding hundreds of fragile Python scripts (APIs) for an LLM to blindly invoke. They trap users in rigid, split-screen web forms. 

**BloClaw transcends this paradigm.**  
We abandoned the outdated "Tool-Calling" approach and engineered an **Agentic Code Sandbox** paired with an **Omniscient Dynamic Canvas**. BloClaw is not a chatbot; it is a **Clinical-Tech GUI Workspace** where natural language commands seamlessly trigger real-time Python execution, 2D topology generation, and 3D molecular holograms.

---

## 🔥 Apex Features

### 1. 🖥️ Dynamic Canvas UI (The Command Deck)
Inspired by top-tier developer tools like Cursor and Notion, BloClaw features a **Top-Mounted Command Deck**. 
- During literature reviews, it operates as a 100% full-width immersive chat stream. 
- The moment the LLM renders a 2D molecule or 3D protein, a physical **Hologram Chamber smoothly unfolds on the right**. Done viewing? Click the toggle button, and the screen retracts effortlessly.

### 2. ⚕️ "Void Creation" - Zero-Shot 3D ECM Folding
BloClaw doesn't just query known PDB databases (`1TSR`). 
Provide it with a completely novel, artificially designed sequence of amino acids (e.g., `MVLSPADKT...`). BloClaw routes this to the **Meta ESMFold Supercomputing Cluster**, simulates its force field in real-time, and projects a fully interactive 3D protein crystal directly into your chat stream. *Creation from nothingness.*

### 3. 🐍 Infinite Capabilities via Agentic Sandbox
Need to plot a Michaelis-Menten kinetic curve? 
Don't write an API for it. BloClaw’s core engine features a highly isolated `Python Execute Sandbox`. The LLM **writes the Python code on the fly in its 'Thought' process**, imports `numpy`/`matplotlib`, executes it silently, and returns the high-definition scientific chart as an attachment right before your eyes. **Skill count: ∞.**

### 4. 🛡️ Bulletproof XML Routing & Regex Purification
LLMs hallucinate JSON structures constantly. BloClaw uses a custom, multi-layered **XML Tag Protocol** combined with **Regex Maximal Extraction**. No matter how many conversational artifacts the LLM mixes into a SMILES string, BloClaw surgically extracts the valid chemical sequence and feeds it safely into the local RDKit engine. **Zero red screens of death.**

---

## ⚡ Quick Start

Deploy your personal Bio-Hacker workstation locally in under 60 seconds:

```bash
# 1. Clone the repository
git clone https://github.com/qinheming/BloClaw.git
cd BloClaw

# 2. Install core dependencies
pip install openai eval python-dotenv gradio rdkit requests

# 3. Configure your API Keys safely
cp .env.example .env
# Edit .env and add your LLM API Key 

# 4. Ignite the Engine
python3 web_ui.py
# The Command Deck will automatically open in your browser at 127.0.0.1:7860

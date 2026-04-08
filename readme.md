# 🧬 BloClaw

<div align="center">
  <p><b>The Privacy-First, Multi-Agent OS for Biological & Pharma Labs</b></p>
  <p><i>Building the local super-brain for wet & dry labs, beyond monolithic AI.</i></p>
</div>

## 🥊 Why BloClaw 
While existings scientific agents dump fragile tools into a single context window and rely on Cloud LLMs, **BioClaw** approaches AI-for-Science differently:
- 🔒 **Zero-Trust Privacy:** Compute molecular docking and genomics entirely locally. Your SME data never leaves the hardware.
- 🧫 **Wet-Lab Safety Sandbox:** Uses AST parsing to strictly prevent AI-generated destructive code from crashing your physical automated liquid handlers.
- 🧩 **Decentralized Micro-Agents:** Mathematical deterministic evaluations (like Lipinski Rules via `rdkit`) handle data, while the LLM purely routes intent.

## 🚀 Quick Start (No Dependency Hell)
The easiest way to run BioClaw is via standard Python or Docker:

```bash
git clone https://github.com/qinheming/BloClaw.git
cd BloClaw
poetry install

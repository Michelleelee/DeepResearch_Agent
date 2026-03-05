# DeepResearchAgent (Multi-Agent Research Assistant)

A multi-agent research assistant designed to decompose complex research questions into executable subtasks, orchestrate tool usage, and produce evidence-grounded structured reports.

The system coordinates specialized agents for planning, summarization, verification, and reporting. It supports both sequential and parallel execution modes and incorporates self-reflection mechanisms to improve report quality over time.

---

# Overview

DeepResearchAgent is a **multi-agent research system** designed to assist with complex research workflows.

The system breaks down high-level research questions into smaller executable tasks, performs iterative information gathering and synthesis, and produces structured reports with traceable intermediate artifacts.

Key capabilities include:

* **Task decomposition for complex research questions**
* **Tool-augmented evidence retrieval**
* **Multi-agent orchestration**
* **Iterative quality improvement via self-reflection**

The system enables an automated research pipeline that integrates planning, retrieval, synthesis, verification, and reporting.

---

# Core Ideas

## Multi-Agent Task Decomposition

The system decomposes complex research questions into structured subtasks using a dedicated **Planner agent**.

Each task is then processed through a multi-agent pipeline that allows independent reasoning and synthesis before final aggregation.

This design enables modular reasoning and improves robustness when handling open-ended research queries.

---

## Specialized Research Sub-Agents

The system coordinates four specialized agents:

* **Planner**
  Decomposes the research question into structured subtasks and determines execution strategy.

* **Summarizer**
  Collects evidence from tools and produces intermediate summaries.

* **QA Auditor**
  Performs verification and self-reflection to detect inconsistencies, missing evidence, or hallucinated claims.

* **Reporter**
  Compiles final outputs into structured research reports.

These agents communicate through a unified orchestration pipeline.

---

## Tool-Oriented Multi-Agent Orchestration

A unified **tool-calling listener** coordinates tool usage across agents.

This architecture allows:

* extensible tool integration
* modular agent design
* transparent intermediate artifacts

The orchestration layer manages communication between agents and ensures that tool outputs are properly integrated into reasoning steps.

---

## Self-Reflection and Iterative Quality Improvement

The **QA Auditor** enables a self-reflection loop.

The system performs:

1. Initial synthesis from retrieved evidence
2. Verification of claims and evidence coverage
3. Identification of missing or weak reasoning steps
4. Iterative improvement of intermediate outputs

This mechanism helps mitigate hallucinations and improves report reliability.

---

## Adaptive Execution Modes

The system supports two execution strategies:

* **Sequential Mode**
  Agents execute in a strict pipeline to maximize reasoning coherence.

* **Parallel Mode**
  Subtasks are processed concurrently to reduce latency and adapt to token budget constraints.

This flexibility allows the system to balance **quality, speed, and token efficiency**.

---

# Quality Improvements

Compared to a naive search-based agent baseline under **GPT-5.1**, the system achieved:

* **~30% higher average report usability**, evaluated using **LLM-as-a-judge**
* **~91% reduction in token budget** through context refactoring and compression

These improvements demonstrate more efficient reasoning and better structured research outputs.

---

# Tech Stack

* **Language:** Python
* **Agent Framework:** HelloAgents
* **LLM:** GPT-5.1 (via OpenAI API)
* **Search Tools:** DuckDuckGo / external search APIs
* **Frontend:** React + Node.js
* **Backend:** Python API service

---

# High-Level Workflow

1. User submits a research question
2. Planner agent decomposes the question into subtasks
3. Subtasks trigger tool calls and evidence retrieval
4. Summarizer produces structured intermediate findings
5. QA Auditor verifies reasoning and evidence coverage
6. Reporter compiles the final structured report
7. Iterative improvements are applied when necessary

---

# Repository Structure

Example repository layout:

```text
.
├── backend/             # multi-agent backend logic
├── frontend/            # web interface
├── agents/              # Planner / Summarizer / QA Auditor / Reporter
├── tools/               # search and tool integrations
├── orchestration/       # multi-agent coordination logic
└── config/              # environment and configuration
```

---

# Environment Requirements

* Python **>= 3.10**
* Node.js **>= 18**
* npm **>= 9**

---

# Backend Setup

```bash
cd chapter14/helloagents-deepresearch/backend

python3 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -e .
```

---

# Running the System

Start the backend service:

```bash
cd chapter14/helloagents-deepresearch/backend
source .venv/bin/activate
python main.py
```

---

# Running the Frontend

In another terminal:

```bash
cd chapter14/helloagents-deepresearch/frontend
npm install
npm run dev
```

The frontend will connect to the backend API and provide an interface for submitting research questions and viewing generated reports.

---

# Future Work

Potential improvements include:

* improved hallucination detection in multi-agent reasoning
* better trajectory-aware evaluation metrics
* integration of additional research tools
* more advanced agent coordination strategies

---

# License

MIT License

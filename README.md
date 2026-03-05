# DeepResearchAgent

A multi-agent research assistant that decomposes complex research questions into structured subtasks, orchestrates tool usage, and generates evidence-grounded research reports with traceable intermediate artifacts.

The system simulates a research workflow pipeline — planning, evidence collection, summarization, verification, and final reporting — using coordinated LLM agents.

---

# Overview

DeepResearchAgent is a multi-agent system designed to transform an open-ended research question into a structured investigation workflow.

The system automatically:

- Decomposes complex research questions into executable subtasks
- Coordinates tool calls for information retrieval and processing
- Synthesizes evidence from multiple sources
- Performs self-reflection and quality auditing
- Produces structured reports with traceable reasoning artifacts

The goal is to improve the reliability and usability of long-form research synthesis while maintaining transparency across intermediate reasoning steps.

---

# Architecture

The system is organized as a multi-agent orchestration pipeline consisting of four specialized agents:


User Query
↓
Planner Agent
(Task Decomposition)
↓
Tool Execution Layer
(Search / Retrieval / Processing)
↓
Summarizer Agent
(Evidence Synthesis)
↓
QA Auditor
(Self-Reflection & Verification)
↓
Reporter Agent
(Structured Research Report)


Each agent focuses on a specific role in the research pipeline, enabling modularity and extensibility.

---

# Core Components

## Planner Agent

Transforms an open-ended research question into structured subtasks.

Responsibilities include:

- Task decomposition  
- Tool planning  
- Execution ordering  

The planner generates execution plans that can run in **sequential or parallel modes** depending on token budget constraints.

---

## Summarizer Agent

Aggregates tool outputs and intermediate findings into coherent evidence summaries.

Key functions include:

- Multi-source evidence synthesis  
- Context compression  
- Structured intermediate notes  

This allows downstream agents to operate on **high-density summarized context** rather than raw tool outputs.

---

## QA Auditor

Introduces a self-reflection loop to improve answer reliability.

Responsibilities include:

- Detecting unsupported claims or hallucinations  
- Identifying missing evidence  
- Requesting refinement when necessary  

The QA Auditor acts as an internal reviewer before final report generation.

---

## Reporter Agent

Compiles validated intermediate artifacts into a structured research report.

Typical outputs include:

- Research overview  
- Key findings  
- Supporting evidence  
- Synthesized conclusions  

The final report maintains **traceability to intermediate reasoning steps and evidence sources**.

---

# Multi-Agent Orchestration

The system implements a **unified tool-calling listener** that allows agents to interact with external tools through a standardized interface.

Key orchestration capabilities:

- Modular agent architecture  
- Extensible tool interface  
- Sequential and parallel execution modes  
- Event-driven monitoring of tool calls  

This design enables scalable multi-agent coordination.

---

# Key Features

### Multi-Agent Research Pipeline

Implements a coordinated research workflow using specialized agents for planning, summarization, verification, and reporting.

### Self-Reflection via QA Auditor

Introduces an auditing loop that evaluates intermediate outputs and triggers iterative refinement.

### Token-Efficient Context Management

Refactors context packing and summarization prompts to significantly reduce token consumption while preserving information density.

---

# Experimental Results

The system was evaluated against a naive search-based baseline agent using the same LLM model.

Evaluation setup:

- Model: GPT-5.1  
- Evaluation method: LLM-as-a-judge for report usability  

Results:

- ~30% higher average report usability compared with the baseline agent  
- ~91% reduction in token budget through context refactoring and compression  

These results indicate that **agent orchestration and context engineering significantly improve both research quality and efficiency**.

---





## Project Structure

```text
DeepResearchAgent
├── backend
│   ├── agents          # planner / summarizer / qa auditor / reporter
│   ├── services        # orchestration & shared logic
│   ├── tools           # tool integrations (search, retrieval, etc.)
│   └── api             # backend API endpoints
│
└── frontend
    ├── components      # UI components
    └── pages           # routes / screens
---

# Backend Setup

```bash
cd backend

# create virtual environment
python3 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

# install dependencies
pip install --upgrade pip
pip install -e .

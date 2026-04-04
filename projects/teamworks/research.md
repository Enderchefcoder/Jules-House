# TeamWorks: Multi-Agent Swarm Collaboration Research

## Overview
The 2026 landscape for multi-agent systems is dominated by several key frameworks that have evolved from 2024-2025 prototypes into production-grade SDKs. The primary challenge identified for TeamWorks is enabling "hundreds of agents" to collaborate effectively without the overhead of massive context bloat or coordination failures.

## Key Frameworks (2026 State)
- **LangGraph (LangChain)**: The leader in production-grade state management and conditional routing. Uses a graph-based orchestration model.
- **CrewAI**: Optimized for role-based collaboration (Manager, Worker, Reviewer). Simple to set up but struggles with fine-grained control at massive scales.
- **OpenAI Agents SDK**: Replaced the experimental 'Swarm'. Focuses on explicit 'handoffs' between agents.
- **Google ADK & Anthropic Agent SDK**: New entrants in 2025/2026, providing native integrations with Gemini and Claude models.
- **AG2 (formerly AutoGen)**: Microsoft's event-driven framework. Excels at "GroupChat" patterns where agents debate and refine outputs.

## Core Problems to Solve for TeamWorks
1. **Merge Conflict Resolution**: Standard Git-based merges are difficult for AI. TeamWorks needs a "Semantic Merge" system that understands code intent, not just text diffs.
2. **Context Fragmentation**: In a swarm of 100+ agents, sharing the entire context is impossible. We need "Shared Memory" vs. "Local Memory" architectures.
3. **Task Delegation**: Hierarchical vs. Peer-to-Peer (Swarm) trade-offs. 2026 trends suggest a hybrid "Orchestrator-Worker" pattern is most stable.

## Proposed TeamWorks Stack
- **Backend**: Rust (for high-speed message passing and shared state).
- **Database**: SQLite (for local agent state and history) + Vector DB (for semantic memory).
- **Orchestration**: Event-driven architecture using a custom implementation of the "Handoff" and "GroupChat" patterns.

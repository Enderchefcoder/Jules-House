# Project DeepThoughts: Security & Systems Strategy

## Objective
To build a massive document corpus of high-fidelity Q/A pairs designed for training LLMs on advanced security, low-level systems (Linux/C/Rust), and modern software development practices.

## Data Collection Plan
1. **Source Discovery**:
    - Identify top 100 recent (2025-2026) CVEs.
    - Research latest language updates for HTML, CSS, JS, Python, Rust, and C++.
    - Document Linux kernel changes and security patch trends.
2. **Analysis**: Perform deep technical deep-dives into each discovery to understand the root cause, exploit mechanism, and mitigation.
3. **Drafting**: Convert analyses into the Instruct-format (Q/A).

## Q/A + CoT Format
Each entry MUST follow this structure to ensure the model learns the "Thinking" process, not just the "Result."

```markdown
Question: [Specific, technical question about a vulnerability or language feature]

Answer:
<think>
1. Identify the core system or language component.
2. Trace the vulnerability path or feature logic.
3. Plan the explanation (Context -> Technical Detail -> Solution/Example).
4. Verify edge cases or security implications.
</think>

[Technical, detailed output here, following the thought process above.]
```

## Initial Corpus Focus (Q2 2026)
- **Linux Security**: eBPF-based sandbox bypasses.
- **Modern Web**: WebAssembly (WASM) security boundaries.
- **Rust/C++**: Memory safety and high-performance concurrency.

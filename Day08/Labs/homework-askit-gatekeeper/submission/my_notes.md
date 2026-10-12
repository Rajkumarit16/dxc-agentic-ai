# My notes

Q1. D1: Yes, VIP read actions need approval from the IT manager so sensitive information is not accessed without oversight. D2: At night, write actions go to the queue so they wait for the service desk. D3: Facts are kept for 10 days to limit how long personal information remains in memory.

Q2. I would never let an LLM decide whether an action needs approval. The approval rules control access and changes, so they should be explicit, consistent, and enforced by code.

Q3. I edited the spec first, then the code. The spec is the source of truth: updating it first makes the intended behavior clear and lets us check that the implementation and tests match the client's rules.

# Demystifying Agent Skills: Architecture & AI Context

When working with Agent Skills, the system uses a **"lazy loading"** architecture. The initial system prompt only contains brief descriptions of available skills, providing instructions in the optimal number of words. This allows the AI to see the menu of options without being confused by the details of every single skill. 

When the agent decides to use a specific skill, it executes a tool call to read the full `SKILL.md` file, thereby exposing the details only when necessary and loading its entire content into the chat context.

However, in a typical workflow where an agent reuses a skill multiple times, the agent will often read that same `SKILL.md` file repetitively. This raises a critical architectural question:

**If the full skill content is already in the context from the first use, why do we re-load it? Alternatively, why don't we delete the old file reads to clean up the context? Or why not just load ALL skills upfront and be done with it?**

The answer lies in the intersection of LLM attention mechanisms, hardware-level KV caching, and "context decay."

---

### 1. Why do we re-load the skill repetitively? (Context Decay)

If a skill was loaded early in a conversation, its text is technically still in the context window 4,000 tokens later. So why not just rely on the agent's memory? 

Because of **Context Decay** (often called "Lost in the Middle"). Even though a model *can* attend to any part of the context in principle, in practice instruction-following reliability tends to degrade as crucial constraints get farther away and the prompt gets more cluttered. If an agent tries to execute a highly structured task using instructions buried deep in the past, it may hallucinate rules, skip steps, or drift on formatting.

Re-reading the file via a tool call immediately before executing the skill brings the strict instructions back to the front of the context window and typically improves compliance (though it can’t strictly guarantee perfect adherence).

---

### 2. Why don't we delete the old reads? (KV Caching & Prefix Integrity)

If we are forced to re-read the file to bring it to the front, the logical next step is: *Let's just delete the old, previous read from the chat history so we aren't duplicating tokens.*

We often avoid doing that because many LLM serving stacks implement **prompt/prefix caching across requests** (sometimes called prompt caching). Separately, models also use **KV caching within a single request** to avoid recomputing attention states while decoding.

For cross-request prompt caching, a common strategy is: if the *prefix* (the exact sequence of tokens up to some point) matches a previously-seen prefix, the server can reuse cached prefill work (or an equivalent cached representation) instead of recomputing it from scratch. If we delete or edit an earlier chunk of the conversation (like an old skill read), that exact-prefix match can be invalidated, increasing the chance of a cache miss and forcing a full re-prefill.

So an append-only conversation log tends to **maximize cacheability** and reduce latency/cost in systems that support prefix caching. (It’s not a universal guarantee: cache behavior varies by provider, model, and eviction policy, and cached prefill is “cheaper,” not free.)

---

### 3. Why not load ALL skills upfront? (Attention Overhead & Concentration)

If prompt/prefix caching can make prefilling much cheaper, does it really matter if we hide the details of the skills? Why don't we just eagerly load the full text of *every single available skill* into the system prompt at the very beginning?

Because prompt/prefix caching (when available) primarily helps with prefilling work across requests, not the generation phase. Keeping the context limited to *only* the skills currently being used provides two massive benefits:

1. **AI Concentration (Preventing Confusion):** Providing instructions in the optimal number of words is crucial for LLM performance. If the context is occupied by the granular details of every single skill, the AI can become confused by overlapping or irrelevant instructions. Lazy importing exposes details *only* when the AI has decided to focus on a specific task, maximizing cognitive concentration.
2. **Decoding Latency (Saving Computation):** During the **auto-regressive decoding phase** (when the AI is actually generating its response one token at a time), the model must calculate attention across the *entire* KV cache for every single new token it generates. If you have 50 unused skills sitting in the cache, the math required to generate every single output token is significantly heavier. This drastically slows down generation speed and wastes computation.

### Conclusion

The architecture of Agent Skills is a carefully balanced trade-off designed for both cognitive focus and modern LLM serving constraints:
- We **lazy load** skills to keep irrelevant instructions out of the prompt, improving concentration and reducing decode-time overhead.
- We **re-read** skills when needed to combat context decay and improve formatting/instruction adherence.
- We often prefer an **append-only** conversation log because it preserves prefix stability, which can increase the hit rate of provider/framework prompt caching and avoid expensive full re-prefills.
from src import kb, llm

SYSTEM_PROMPT = """You are a Style Extractor agent for a cover letter assistant.
Your role is to analyze reference cover letters written by the user and extract their unique writing style.

You will be given the text of one or more past cover letters.

Your task is to produce a comprehensive style_guidelines.md document that captures:
1. **Tone & Voice**: Is the writing formal or conversational? Confident or humble?
2. **Sentence Structure**: Short and punchy, or long and detailed?
3. **Vocabulary Preferences**: Specific power words, phrases, or words to avoid.
4. **Opening & Closing Patterns**: How does the user typically open and close their letters?
5. **Structure & Formatting**: How is the body organized? Paragraph count? Use of bullet points?
6. **Unique Stylistic Quirks**: Any distinctive patterns worth replicating.

Output the COMPLETE updated markdown content of style_guidelines.md, starting with '# Style Guidelines'.
Do not add any preamble before the heading.
"""

def extract_and_save(reference_texts: list[str]) -> str:
    """
    Analyzes a list of reference cover letter texts and saves the resulting
    style guidelines to knowledge/style_guidelines.md.

    Args:
        reference_texts: List of plain text contents of reference cover letters.

    Returns:
        The generated style guidelines as a string.
    """
    combined = "\n\n---\n\n".join(
        [f"## Reference Draft {i+1}\n\n{text}" for i, text in enumerate(reference_texts)]
    )

    existing_guidelines = kb.read_style_guidelines()
    context = f"## Existing style_guidelines.md\n\n{existing_guidelines or '*(empty)*'}\n\n---\n\n{combined}"
    system_with_context = f"{SYSTEM_PROMPT}\n\n---\n\n{context}"

    messages = [{"role": "user", "content": "Please analyze the reference drafts and generate a comprehensive style_guidelines.md."}]
    response = llm.chat(messages=messages, system_prompt=system_with_context)

    marker = "# Style Guidelines"
    idx = response.find(marker)
    if idx != -1:
        guidelines_content = response[idx:]
        kb.write_style_guidelines(guidelines_content)
        return guidelines_content

    return response

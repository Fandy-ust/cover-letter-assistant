from src import kb, llm

SYSTEM_PROMPT = """You are a Writer agent for a cover letter assistant.
Your role is to write and iteratively refine a cover letter based on a provided application brief and style guidelines.

You will be given:
- An application_brief.md with specific angles, matched experiences, and tone notes.
- A style_guidelines.md with the user's personal writing style preferences.

Your responsibilities:
1. **Initial Draft**: On the first request, produce a complete, polished cover letter as final_draft.md.
   - Strictly follow the style_guidelines.md (tone, vocabulary, structure, sentence length).
   - Use the experiences and angles from the application_brief.md.
   - The letter should feel personal and not generic.
2. **Iterative Refinement**: In follow-up turns, the user will give you feedback (e.g., "make paragraph 2 more concise", 
   "add a mention of my Python experience", "change the opening"). Apply ONLY the requested changes 
   and output the COMPLETE updated cover letter.

Always output the complete cover letter starting with '# Cover Letter'.
Do not add any preamble before the heading in your final output.
After the cover letter, you may add a brief note like '---\\n*What would you like to change?*' to invite feedback.
"""

def get_response(messages: list[dict]) -> str:
    """
    Gets a response from the Writer agent.

    Args:
        messages: The full chat history for the writer session.

    Returns:
        The agent's reply containing the full draft.
    """
    brief = kb.read_application_brief()
    guidelines = kb.read_style_guidelines()

    context_parts = [
        f"## application_brief.md\n\n{brief or '*(no brief found — please generate one with the Advisor first)*'}",
        f"## style_guidelines.md\n\n{guidelines or '*(no style guidelines found)*'}",
    ]
    context = "\n\n---\n\n".join(context_parts)
    system_with_context = f"{SYSTEM_PROMPT}\n\n---\n\n{context}"

    return llm.chat(messages=messages, system_prompt=system_with_context)

def save_draft_from_response(response_text: str) -> bool:
    """
    Extracts and saves the cover letter from the agent's response.

    Returns:
        True if a draft was found and saved, False otherwise.
    """
    marker = "# Cover Letter"
    idx = response_text.find(marker)
    if idx != -1:
        # Save everything up to the optional separator note
        draft_content = response_text[idx:]
        # Strip the conversational note at the end if present
        sep_idx = draft_content.find("\n---\n")
        if sep_idx != -1:
            draft_content = draft_content[:sep_idx]
        kb.write_final_draft(draft_content.strip())
        return True
    return False

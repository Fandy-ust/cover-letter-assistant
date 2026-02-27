from pathlib import Path
from src import kb, llm

SYSTEM_PROMPT = """You are a Profile Builder agent for a cover letter assistant.
Your role is to help the user build and maintain their professional profile.

You will be given the current contents of the user's personal_profile.md and may also 
receive raw materials (like a CV or LinkedIn export) that the user has uploaded.

Your responsibilities:
1. When given raw materials, analyze them and extract structured professional information.
2. Engage in conversation to clarify, enrich, or add new experiences to the profile.
3. When asked, produce an UPDATED version of the full personal_profile.md in markdown.
   - The profile should have clear sections: Contact Info, Professional Summary, Experiences, Education, Skills.
   - Each Experience entry should follow a STAR-style summary where possible.
   - Always preserve existing information and only add or improve—never delete without asking.

When the user asks you to save or update the profile, output the COMPLETE updated markdown content
of personal_profile.md, starting with the heading '# Personal Profile'.
"""

def get_response(messages: list[dict], raw_material_text: str | None = None) -> str:
    """
    Gets a response from the Profile Builder agent.

    Args:
        messages: The full chat history (list of role/content dicts).
        raw_material_text: Optional text content from an uploaded raw material file.

    Returns:
        The agent's reply.
    """
    current_profile = kb.read_personal_profile()

    context_parts = [f"## Current personal_profile.md\n\n{current_profile or '*(empty)*'}"]
    if raw_material_text:
        context_parts.append(f"## Uploaded Raw Material\n\n{raw_material_text}")

    context = "\n\n---\n\n".join(context_parts)
    system_with_context = f"{SYSTEM_PROMPT}\n\n---\n\n{context}"

    return llm.chat(messages=messages, system_prompt=system_with_context)

def save_profile_from_response(response_text: str) -> bool:
    """
    Extracts and saves a new personal_profile.md if the agent has generated one.
    Looks for content starting with '# Personal Profile'.

    Returns:
        True if a profile was found and saved, False otherwise.
    """
    marker = "# Personal Profile"
    idx = response_text.find(marker)
    if idx != -1:
        new_profile = response_text[idx:]
        kb.write_personal_profile(new_profile)
        return True
    return False

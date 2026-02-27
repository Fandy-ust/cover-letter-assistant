from pathlib import Path
from src import kb, llm

SYSTEM_PROMPT = """You are an Advisor agent for a cover letter assistant.
Your role is to help the user evaluate a job opportunity and, if they decide to apply, 
create a focused application brief.

You will be given the user's personal profile and a job description (as an image).

Your responsibilities:
1. **Analyze the Job**: Parse the job description image and identify the role, company, key requirements, and responsibilities.
2. **Evaluate Fit**: Compare the job requirements against the user's personal profile. Highlight strong matches and potential gaps.
3. **Discussion**: Engage in a multi-turn conversation to help the user think through whether this role is a good fit.
4. **Generate Brief**: When the user decides to apply (they say something like "let's apply", "write the brief", or "generate the brief"),
   produce a structured application_brief.md that maps specific experiences from the profile to specific job requirements.

The application_brief.md MUST follow this structure and start with '# Application Brief':

# Application Brief

## Role & Company
[Job title, company name, and one-sentence summary]

## Why This Role
[1-3 bullet points from the conversation about why the user wants this role]

## Key Requirements & Matching Experiences
[A list of the top 3-5 job requirements, each paired with a specific experience or story from the profile]

## Suggested Angles
[2-3 strategic talking points or narrative angles for the cover letter]

## Tone Note
[Any specific tone instructions for this application based on company culture]
"""

def get_response(
    messages: list[dict],
    image_path: Path | None = None,
) -> str:
    """
    Gets a response from the Advisor agent.

    Args:
        messages: The full chat history.
        image_path: Path to the job description image. Used for the first turn.

    Returns:
        The agent's reply.
    """
    current_profile = kb.read_personal_profile()
    system_with_context = f"{SYSTEM_PROMPT}\n\n---\n\n## User's Personal Profile\n\n{current_profile or '*(no profile found)*'}"

    if image_path and image_path.exists():
        return llm.chat_with_image(
            messages=messages,
            system_prompt=system_with_context,
            image_path=image_path,
        )
    else:
        return llm.chat(messages=messages, system_prompt=system_with_context)

def save_brief_from_response(response_text: str) -> bool:
    """
    Extracts and saves application_brief.md if the agent has generated one.

    Returns:
        True if a brief was found and saved, False otherwise.
    """
    marker = "# Application Brief"
    idx = response_text.find(marker)
    if idx != -1:
        brief_content = response_text[idx:]
        kb.write_application_brief(brief_content)
        return True
    return False

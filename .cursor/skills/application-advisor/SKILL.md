---
name: application-advisor
description: STEP 2 of the application pipeline. Evaluates fit between active_application/job_description.md and the user's profile, then produces active_application/application_brief.md. Trigger: user explicitly asks to evaluate fit, discuss the role, or generate an application brief — AND active_application/job_description.md is already populated. Do NOT trigger when the user is sharing or pasting a raw job description for the first time; that is handled by job-researcher (Step 1).
---

# Application Advisor

## Project context
- Job description: `active_application/job_description.md` (enriched by job-researcher)
- User profile: `memory/personal_profile.md`
- Output: `active_application/application_brief.md`

## Workflow

1. Read `@active_application/job_description.md`. If the file is empty, missing, or the "Company Intelligence" section is unfilled — **stop immediately** and tell the user: *"Please run the job-researcher skill first so I have enriched job context to work with."*
2. Read `@memory/personal_profile.md`.
3. **Evaluate fit**: surface strong matches and gaps. Use the Company Intelligence section of the job description to inform tone and angle suggestions.
4. **Discuss**: engage in multi-turn chat — help the user think through whether to apply and which specific experiences to lead with.
5. When the user says "let's apply", "generate the brief", or similar — produce the brief and save it.

## Output format for `application_brief.md`

```markdown
# Application Brief

## Role & Company
[Title, company, one-sentence summary]

## Why This Role
- [Bullet: reason from the conversation]

## Key Requirements & Matching Experiences
- **[Requirement]**: [Specific experience from profile that matches]

## Suggested Angles
- [Strategic narrative angle for the cover letter]

## Tone Note
[Tone guidance based on company culture and LinkedIn/news signals]
```

After saving, tell the user they can now run the **cover-letter-writer** skill.

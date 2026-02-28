---
name: job-researcher
description: STEP 1 of the application pipeline. Receives raw job input (files in raw_inputs/job/, pasted text, screenshot, or URL) and produces active_application/job_description.md enriched with company intelligence. Trigger: user asks to process a new job posting. MUST run before application-advisor. Do NOT skip this step even if the user asks to go straight to the advisor.
---

# Job Researcher

Turns a raw job description into a rich, structured `active_application/job_description.md` by combining the posted JD with live company intelligence gathered from the web.

## Inputs
- Files in `raw_inputs/job/` (supported formats: pdf, txt, md; `.md` preferred)
- Pasted text, screenshot, or URL
- Company name (extract from JD if not stated explicitly)

## Workflow

1. Accept either chat input (paste/screenshot/URL) or files in `raw_inputs/job/`.
2. Extract the core job details from the user's input (role, company, location, requirements).
3. Research the company using web search. Target sources in this order:
   - Company website (About, Mission, Product/Services pages)
   - LinkedIn company page (headcount, recent posts, culture)
   - Recent news (funding, launches, press coverage from the last 12 months)
   - Glassdoor or similar (culture signals, interview process if available)
4. Synthesise everything into `active_application/job_description.md` using the output format below.
5. Ask the user: *"Anything missing or worth adding before we move to the Advisor?"*

## Output format for `active_application/job_description.md`

```markdown
# Job Description

## Role & Basics
- **Title**:
- **Company**:
- **Location / Remote**:
- **Employment type**:

## Responsibilities
[Bullet list from the posting]

## Requirements
### Must-have
### Nice-to-have

## Company Intelligence
### What they do
[1–2 sentence summary of the product/service]

### Mission & Values
[From website or LinkedIn]

### Culture signals
[Team size, work style, perks, tone of their communications]

### Recent news & context
[Funding rounds, product launches, notable hires — last 12 months]

### LinkedIn insights
[Headcount, growth trend, key people in the team/department]

## Notes for application
[Any specific angles, buzzwords they use, or things to reference in the cover letter]
```

## Rules
- Always save to `active_application/job_description.md` — this is the single source of truth for all downstream agents.
- Prefer specificity over generality — the more concrete the intelligence, the better the cover letter.

# Natural Voice Reference

Use this file when a cover letter feels polished in the wrong way: generic, over-explained, too symmetrical, or too eager without enough evidence.

## Common AI-Tone Markers

- Broad opener that could fit any company or role.
- Repeated sentence templates across paragraphs.
- Empty admiration for the employer with no concrete observation.
- Buzzword clusters such as "dynamic, innovative, collaborative" with no evidence.
- Inflated self-description before the draft has earned it.
- Over-connected prose full of transition words instead of clear ideas.
- Every sentence being the same length or cadence.

## Natural Rewrite Rules

- Anchor each paragraph in one real example, capability, or observation.
- Replace "I am passionate about" with what the candidate has actually done, noticed, or wants to build.
- Replace praise of the company with a specific product, mission detail, team focus, or hiring signal from `job_description.md`.
- Let the prose be direct. A clean sentence usually sounds more human than a decorated one.
- Use fewer claims about personality and more claims about work.
- If a sentence sounds like branding copy, cut it or make it more concrete.

## Prompt Patterns Adapted From Public Career Guidance

These are adapted from public career guidance so they are short, reusable, and compatible with this repo's pipeline. Treat them as internal drafting prompts, not text to paste into the final letter.

### Prompt 1: Specific, employer-aware draft

Use when starting from the brief and job description.

`Using active_application/application_brief.md and active_application/job_description.md, draft a one-page cover letter that sounds like a thoughtful professional rather than marketing copy. Keep the tone direct and personal. Show interest in the role through 2-3 specific details from the job or company context. Base every strength claim on evidence already present in the brief. Avoid generic praise, buzzwords, and recycled transitions.`

### Prompt 2: Remove AI tone from a draft

Use when `final_draft.md` already exists but feels synthetic.

`Revise this cover letter so it sounds natural, grounded, and written by one person for one employer. Keep all factual claims accurate, but replace generic phrasing with concrete language, vary sentence rhythm, remove empty intensifiers, and cut any line that could fit almost any application.`

### Prompt 3: Keep warmth without sounding performative

Use when the draft is too stiff or too flattering.

`Rewrite this letter to keep warmth and interest without sounding overeager. Show motivation through specific observations about the role, the team, or the work itself. Prefer calm confidence over praise-heavy language.`

### Prompt 4: Strengthen evidence density

Use when the letter feels abstract.

`Tighten this cover letter so each paragraph contains at least one concrete example, outcome, responsibility, or observation drawn from the application brief. Do not invent new achievements. If a sentence is only opinion or self-description, either support it with evidence or remove it.`

### Prompt 5: Preserve the applicant's voice

Use when revising after user feedback or style memories.

`Revise the letter to match the user's existing writing voice. Keep any lines that already sound personal and credible. Only rewrite the sentences that feel templated, over-polished, or AI-generated.`

## Distilled Guidance From Public Sources

### Harvard Faculty of Arts and Sciences Career Services

- Emphasize prompts that ask for role-specific, company-specific letters instead of generic templates.
- Use AI as a drafting or critique aid, then personalize heavily with lived experience and real motivations.
- Ask for stronger examples, tighter wording, and closer alignment to the job rather than asking for "a great cover letter."
- Source: [Harvard FAS Career Services](https://careerservices.fas.harvard.edu/blog/2025/01/18/best-ai-prompts-to-use-when-writing-a-cover-letter/)

### University of Maryland Clark School Career Best Practices for AI

- Treat AI output as a first pass that needs human editing for authenticity, accuracy, and tone.
- Feed the system concrete experience and target-role context if you want useful wording back.
- Review for honesty and personal voice before using any generated draft.
- Source: [UMD Clark School AI Career Development Best Practices PDF](https://eng.umd.edu/sites/clark.umd.edu/files/Best%20Practices%20for%20AI%20in%20Career%20Development%202.0.pdf)

### UK National Careers Service and Similar Career Guidance

- Keep letters positive and confident, but show why you fit through examples and relevant experience.
- Explain why you want that role and employer, not just why you want a job.
- Keep language clear and professional rather than ornate.
- Source: [National Careers Service cover letter guidance](https://nationalcareers.service.gov.uk/careers-advice/covering-letter)

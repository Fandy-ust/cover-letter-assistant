---
name: application-submitter
description: STEP 4 of the application pipeline. Prepares a send-ready submission by exporting the cover letter to PDF and drafting a short application email. Use when the user asks how to submit, asks to convert to PDF, asks for email wording, or wants final send output.
---

# Application Submitter

## Project context
- Active cover letter: `active_application/final_draft.md`
- Active workspace marker: `active_application/.active`
- Submission email draft: `active_application/submission_email.md`
- Output folder: `active_application/submission/` (PDF artifacts)

## Scope boundary (strict)
- This skill prepares final submission outputs; it does **not** research jobs, evaluate fit, or rewrite strategy.
- Do **not** modify `active_application/application_brief.md` or `active_application/job_description.md`.
- Do **not** send email on the user's behalf; provide send-ready output only.

## Workflow

1. Read `@active_application/final_draft.md` and confirm it is final.
2. Propose cover letter filename using a consistent pattern:
   - `[Name]_Cover_Letter.pdf`
3. Export markdown to PDF:
   - Preferred: `pandoc active_application/final_draft.md -o active_application/submission/<target>.pdf`
   - Fallback: `npx md-to-pdf active_application/final_draft.md` then move output into `active_application/submission/`
4. Draft a short application email:
   - Subject line
   - 4-7 line email body
   - Signature block
5. Save the send-ready email to `active_application/submission_email.md`.
6. Ask user to confirm before sending.


## Email template

```text
Subject: Application – [Role Title] – [Full Name]

Dear [Hiring Team / Recruiter Name],

I am writing to apply for the [Role Title] position at [Company].

Please find attached my cover letter for your review.

I would welcome the opportunity to discuss my background and fit for the role.

Yours sincerely,
[Full Name]
[Phone]
[Email]
```

## Submission checklist
- Cover letter exported to PDF and visually checked
- Subject line includes role + full name
- Recipient email verified from source posting
- Email body short and professional
- `submission_email.md` saved in `active_application/`
- Generated PDFs saved in `active_application/submission/`

## Rules
- Keep submission messaging concise and formal; avoid repeating the full cover letter in email body.
- If PDF conversion fails, surface the exact error and provide one fallback command.
- Never claim an application has been submitted unless the user explicitly confirms they sent it.

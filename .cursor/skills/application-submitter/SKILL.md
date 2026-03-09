---
name: application-submitter
description: STEP 4 of the application pipeline. Prepares a send-ready application package by exporting cover letter markdown to PDF, drafting a concise application email, and assembling an attachment checklist. Use when the user asks how to submit, asks to convert to PDF, asks for email wording, or wants a final send package.
---

# Application Submitter

## Project context
- Active cover letter: `active_application/final_draft.md`
- Active workspace marker: `active_application/.active`
- Submission email draft: `active_application/submission_email.md`
- Submission package record: `active_application/submission_package.md`
- Output folder: `active_application/submission/` (PDF artifacts)
- Optional supporting docs: resume, transcript, portfolio links

## Scope boundary (strict)
- This skill prepares the package; it does **not** research jobs, evaluate fit, or rewrite strategy.
- Do **not** modify `active_application/application_brief.md` or `active_application/job_description.md`.
- Do **not** send email on the user's behalf; provide send-ready content and checklist only.

## Workflow

1. Read `@active_application/final_draft.md` and confirm it is final.
2. Propose attachment names using a consistent pattern:
   - `[Name]_Cover_Letter_[Company].pdf`
   - `[Name]_Resume.pdf`
   - Optional: `[Name]_Transcript.pdf`
3. Export markdown to PDF:
   - Preferred: `pandoc active_application/final_draft.md -o active_application/submission/<target>.pdf`
   - Fallback: `npx md-to-pdf active_application/final_draft.md` then move output into `active_application/submission/`
4. Draft application email content:
   - Subject line
   - 6-10 line email body
   - Signature block
5. Save the send-ready email to `active_application/submission_email.md`.
6. Save attachment plan + checklist to `active_application/submission_package.md`:
   - target recipient email
   - attachment filenames
   - whether transcript is included (and why)
   - attachment file paths in `active_application/submission/`
   - final pre-send checklist
7. Ask user to confirm before sending.

## Email template

```text
Subject: Application – [Role Title] – [Full Name]

Dear [Hiring Team / Recruiter Name],

I am writing to apply for the [Role Title] position at [Company].

Please find attached my cover letter and resume for your review.
[Optional: I have also attached my transcript for reference.]

I would welcome the opportunity to discuss my background and fit for the role.

Yours sincerely,
[Full Name]
[Phone]
[Email]
```

## Submission checklist
- Cover letter exported to PDF and visually checked
- Resume attached (PDF)
- Transcript attached only if required or strategically beneficial
- Subject line includes role + full name
- Recipient email verified from source posting
- Email body concise and professional
- `submission_email.md` and `submission_package.md` saved in `active_application/`
- Generated PDFs saved in `active_application/submission/`

## Rules
- Keep submission messaging concise and formal; avoid repeating the full cover letter in email body.
- If PDF conversion fails, surface the exact error and provide one fallback command.
- Never claim an application has been submitted unless the user explicitly confirms they sent it.

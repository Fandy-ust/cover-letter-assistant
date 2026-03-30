---
name: application-submitter
description: STEP 4 of the application pipeline. Prepares a send-ready submission by exporting the cover letter to PDF and drafting a short application email. Use when the user asks how to submit, asks to convert to PDF, asks for email wording, or wants final send output.
---

# Application Submitter

## Project context
- Active cover letter: `active_application/final_draft.md`
- Active workspace marker: `active_application/.active`
- Output folder: `active_application/submission/` (send-ready artifacts)
- PDF renderer: `.codex/skills/application-submitter/scripts/render_cover_letter_pdf.py`

## Scope boundary (strict)
- This skill prepares final submission outputs; it does **not** research jobs, evaluate fit, or rewrite strategy.
- Do **not** modify `active_application/application_brief.md` or `active_application/job_description.md`.
- Do **not** send email on the user's behalf; provide send-ready output only.

## Environment
- Run all commands from the repository root.
- Use any Python environment that has these packages installed:
  - `weasyprint`
  - `markdown`
- Prefer the user's currently active Python environment.
- If the user wants to specify a particular interpreter, allow:

```bash
PDF_PYTHON="${PDF_PYTHON:-python}"
```

- Never use xelatex, pdflatex, pandoc, or npx.
- Use the bundled Python script below; do not switch to other PDF toolchains unless the user asks.

## Workflow

1. Read `@active_application/final_draft.md` and confirm it is final.
2. Determine the output filename: `[FirstName]_[LastName]_Cover_Letter.pdf`
3. Ensure the active Python environment has `markdown` and `weasyprint` available.
4. Run the bundled PDF renderer, replacing `<target>` with the filename.
5. Draft a short application email:
   - Subject line
   - 4–7 line email body
   - Signature block
6. Save the send-ready email to `active_application/submission/submission_email.md`.
7. Confirm outputs with the user before they send.

## PDF rendering command

Run this command from the repository root whenever generating the PDF:

```bash
PDF_PYTHON="${PDF_PYTHON:-python}"
mkdir -p active_application/submission
"$PDF_PYTHON" .codex/skills/application-submitter/scripts/render_cover_letter_pdf.py \
  --out "active_application/submission/<target>.pdf"
```

If dependencies are missing, install them in the chosen environment first:

```bash
PDF_PYTHON="${PDF_PYTHON:-python}"
"$PDF_PYTHON" -m pip install -r requirements.txt
```

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
- [ ] Cover letter exported to PDF and visually checked
- [ ] Subject line includes role + full name
- [ ] Recipient email verified from source posting
- [ ] Email body short and professional
- [ ] `submission/submission_email.md` saved in `active_application/submission/`
- [ ] Generated PDF saved in `active_application/submission/`

## Rules
- Keep submission messaging concise and formal; avoid repeating the full cover letter in the email body.
- If PDF conversion fails, surface the exact error and confirm which Python interpreter or environment the user wants to use.
- Use `memory/cover_letter.css` to control page layout and typography instead of adding formatting logic to the Python snippet.
- Preserve intentional single-line breaks in the sign-off block by using the Markdown `nl2br` extension during HTML conversion.
- Always use the bundled renderer script instead of rewriting the PDF conversion logic inline.
- Prefer the active Python environment by default; allow `PDF_PYTHON` when the user wants a specific interpreter.
- Never claim an application has been submitted unless the user explicitly confirms they sent it.

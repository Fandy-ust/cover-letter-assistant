---
name: application-submitter
description: STEP 4 of the application pipeline. Prepares a send-ready submission by exporting the cover letter to PDF and drafting a short application email. Use when the user asks how to submit, asks to convert to PDF, asks for email wording, or wants final send output.
---

# Application Submitter

## Project context
- Active cover letter: `active_application/final_draft.md`
- Active workspace marker: `active_application/.active`
- Submission email draft: `active_application/submission_email.md`
- Output folder: `active_application/submission/` (bundled send artifacts)

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
- Use the Python-based workflow below; do not switch to other PDF toolchains unless the user asks.

## Workflow

1. Read `@active_application/final_draft.md` and confirm it is final.
2. Determine the output filename: `[FirstName]_[LastName]_Cover_Letter.pdf`
3. Run the exact command sequence in the next section, replacing `<target>` with the filename.
4. Draft a short application email:
   - Subject line
   - 4–7 line email body
   - Signature block
5. Save the send-ready email to `active_application/submission_email.md` and copy it to `active_application/submission/submission_email.md`.
6. Confirm outputs with the user before they send.

## Exact command sequence

Run these commands in order whenever generating the PDF:

```bash
PDF_PYTHON="${PDF_PYTHON:-python}"
mkdir -p active_application/submission
"$PDF_PYTHON" -m pip install markdown weasyprint
"$PDF_PYTHON" - <<'PY'
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

src = Path("active_application/final_draft.md")
out = Path("active_application/submission/<target>.pdf")
css_path = Path("memory/cover_letter.css")

md_text = src.read_text(encoding="utf-8")
html_body = markdown.markdown(md_text, extensions=["nl2br"])

html = f"""
<html>
  <body>
    {html_body}
  </body>
</html>
"""

HTML(string=html, base_url=".").write_pdf(
    out,
    stylesheets=[CSS(filename=str(css_path))]
)
print(f"Wrote {out}")
PY
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
- [ ] `submission_email.md` saved in `active_application/`
- [ ] `submission/submission_email.md` saved for the bundled submission package
- [ ] Generated PDF saved in `active_application/submission/`

## Rules
- Keep submission messaging concise and formal; avoid repeating the full cover letter in the email body.
- If PDF conversion fails, surface the exact error and confirm which Python interpreter or environment the user wants to use.
- Use `memory/cover_letter.css` to control page layout and typography instead of adding formatting logic to the Python snippet.
- Preserve intentional single-line breaks in the sign-off block by using the Markdown `nl2br` extension during HTML conversion.
- Always run the exact command sequence above instead of switching tools or libraries mid-flow.
- Prefer the active Python environment by default; allow `PDF_PYTHON` when the user wants a specific interpreter.
- Never claim an application has been submitted unless the user explicitly confirms they sent it.

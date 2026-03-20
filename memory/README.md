# Memory

This folder stores reusable project memory: profile context, style guidelines, writing strategies, and long-lived submission formatting choices.

You can edit these files manually. In general:

- content files capture information the writing workflow should remember
- CSS files capture presentation preferences the PDF workflow should remember

## Files in this folder

- `README.md`
  This file. It explains what each memory file is for and how the project uses it.

- `personal_profile.md`
  Your long-lived profile: contact details, education, experience, projects, skills, and other reusable background context. This is the main personal reference used to tailor applications.

- `style_guidelines.md`
  Your reusable style guidelines. It captures recurring tone, structure, vocabulary, and formatting preferences extracted from sample letters or established patterns.

- `writing_strategies.md`
  Your reusable writing strategies. This is the place for durable instructions such as phrasing preferences, things to avoid, preferred openings, or recurring corrections. This file may be created or updated over time by the drafting workflow.

- `cover_letter.css`
  The reusable styling file for generated cover letter PDFs. Use it to customize margins, typography, spacing, and other layout details for submission output.

## How the workflow uses memory

- The profile-building step writes and maintains `personal_profile.md`.
- The style-analysis step writes and updates `style_guidelines.md`.
- The writing-feedback step writes and updates `writing_strategies.md`.
- The submission step reads `cover_letter.css` when rendering the PDF.

## Customizing PDF output

Edit `cover_letter.css` when you want to change:

- page margins
- font family
- font size
- line height
- paragraph spacing
- list spacing

Visual formatting changes should usually go in `cover_letter.css`, not in the Python PDF generation snippet.

## Notes

- Some memory files may not exist yet until the relevant step in the workflow has been used.
- The files in `memory/` are meant to be reusable across applications, unlike the role-specific files in `active_application/`.
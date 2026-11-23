# Upload and privacy safeguards

- Accept PDF and TXT only; extensions are allowlisted.
- Check the PDF %PDF- file header; reject binary-looking TXT uploads.
- Enforce 4 MiB per request, 3 MiB per file, and up to 5 files.
- Limit PDF parsing to 15 pages and extracted text to 100,000 characters.
- Read documents into memory; do not persist uploaded files.
- Use sanitized display filenames and DOM textContent for untrusted names.
- Render recommendation text as plain text, not HTML.
- Avoid logging uploaded document text or session secrets.
- Prefix spreadsheet-formula characters before CSV export.
- Set FLASK_SECRET_KEY as a stable secret in the hosting environment.

**Known limitations:** File signatures are not comprehensive malware
detection. Antivirus sandboxing, content disarm, authentication, OCR, audit
retention and multi-tenant controls are outside the scope of this public
educational project.

Reference: OWASP File Upload Cheat Sheet.

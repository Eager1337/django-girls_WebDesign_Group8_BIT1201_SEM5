# GitHub handoff

Destination: https://github.com/EagerBeaversl/django-girls-community-final (private).

The baseline was uploaded on 18 November 2026. The revised delivery includes the approved spectral redesign, eight innovations, 19-table schema, updated five-page A3 PDF/DOCX, and 18-slide editable English PowerPoint with generator scripts and notes. See the latest main commit for the final revision. Private configuration, member uploads, tokens and database dumps are excluded.

## Upload from Windows if preferred
Install Git for Windows with Git Credential Manager, then:

```bat
git clone https://github.com/EagerBeaversl/django-girls-community-final.git
```

Copy this final project into the clone, excluding config.local.php and any actual uploaded photos. The provided .gitignore protects them. Do not copy another .git directory.

```bat
cd django-girls-community-final
git add .
git commit -m "Complete Django Girls PHP MySQL final project"
git push origin main
```

Sign in through Git Credential Manager. Alternatively use GitHub Desktop to clone, copy the files, commit and push. After upload, Code → Download ZIP retrieves the project. Follow README.md for Windows/XAMPP installation.

The GitHub Actions workflow covers PHP syntax, installation and the core/innovation/helper checks. Local checks are verified; do not infer a CI pass from an upload (check Actions separately). Invite the lecturer as a collaborator; never expose credentials or real member data. GitHub Pages does not execute PHP/MySQL. A public live URL remains outstanding.

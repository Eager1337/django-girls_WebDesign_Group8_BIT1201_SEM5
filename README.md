# Django Girls · Freetown Community

**DCOMP207 final project — Alusine G Dumbuya · 905005223 · BIT2101.**

A complete core-PHP/MySQL community-management platform extending the supplied Assignment 1 Django Girls authentication project. Approved spectral black/cyan/pink/amber UI and all eight innovations; no CMS, paid services, Node.js, Composer or PHP plugins required.

## Existing Windows installation — update, do not reinstall

1. Export your populated database in phpMyAdmin and back up the existing project folder.
2. Copy the updated source into `C:\xampp\htdocs\django-girls`, replacing application code but retaining **config.local.php** and the entire **uploads** folder. The package deliberately excludes private files.
3. Start MySQL in XAMPP and run **upgrade-windows.bat**. It invokes `tools/upgrade.php`, adding nine tables and a daily challenge rotation without replacing existing records. Re-running it is safe.
4. Open your existing localhost address and use Ctrl+F5. Your users, password hashes, photos, bookings, discussions and learning progress remain in their existing storage.

Do **not** run install-windows.bat or import database/schema.sql on a populated database. The older UI-only patch does not include these innovations; use this full updated source package.

## Fresh installation only — Start on Windows (XAMPP)

1. Install XAMPP with **PHP 8.2+**, Apache and MySQL/MariaDB. The project was tested on PHP 8.4 and MariaDB 11.8 in Linux; Windows/XAMPP instructions are provided but not executed on an actual Windows machine.
2. Extract the downloaded project ZIP. Rename the extracted folder to **django-girls** and copy it to `C:\xampp\htdocs\django-girls`. `index.php` must be directly in that folder, not in another nested folder.
3. Start **Apache** and **MySQL** in XAMPP Control Panel.
4. Visit `http://localhost/phpmyadmin`. Select **New**, create a database named `django_girls`, and use `utf8mb4_unicode_ci`. Do not import the SQL yet if using the installer.
5. Double-click `install-windows.bat` inside the project folder. It copies `config.example.php` to `config.local.php` and runs the command-line installer. Supply your own administrator name, email and strong password. Password entry is visible in the local terminal; do not screen-share it.
6. Open **http://localhost/django-girls/**. Sign in with the administrator credentials you just chose.
7. Use **Administration** to assign mentors, publish events, add resources and record attendance. Use a separate member account to demonstrate member permissions.

There are **no default passwords** in the delivered application. Installation seeds six trusted learning links, three upcoming workshops, a welcome discussion and seven daily challenge prompts. The fresh installer automatically runs the additive migration. Event dates are calculated at installation time. The database is persistent MySQL, not the old JSON file.

### Manual installation / custom XAMPP path

Copy `config.example.php` to `config.local.php`; edit database host, port, username and password if needed. Open Command Prompt in the project folder:

```bat
C:\xampp\php\php.exe tools\install.php
```

If your XAMPP path differs, replace `C:\xampp` in the commands and batch file. For a fresh manual database only: import `database/schema.sql`, run `tools/create-admin.php`, `tools/seed.php` and **tools/upgrade.php** using PHP. The installer refuses to overwrite existing tables. If admin details were invalid after table creation, use `create-admin.php` to recover, then seed and upgrade.

### Optional sample members

```bat
C:\xampp\php\php.exe tools\demo-data.php
```

This adds **clearly labelled fictional demo members/mentors** and starter administrator progress. Random demo-account passwords are discarded; these are display-only profiles. Create your own second account and promote it to mentor to test mentor login. Disable demo profiles after your demonstration if desired.

### Assignment 1 account migration

```bat
C:\xampp\php\php.exe tools\migrate-assignment1.php "C:\path\to\original\data\users.json"
```

Copies valid existing names/emails/password hashes to MySQL, skips duplicate emails and imports as members. Existing password hashes are preserved; no plaintext passwords are read or created. The supplied Assignment 1 JSON was empty, so the final package contains no old personal account database. Keep the original ZIP separately.

## Features

| Area | Working functionality |
|---|---|
| Accounts | Registration validation, duplicate-email protection, password hashing, throttled login, session regeneration, POST/CSRF logout |
| Dashboard | Personal greeting/interests, registrations, completed lessons, percentage progress, upcoming events, learning suggestions and recent discussions |
| Profiles | Bio, name, interests, uploaded JPG/PNG/WebP photo; optional current-password-verified password change |
| Events | Upcoming/past events, capacity-limited registration, cancellation, attendance status; admin creation/edit/deletion and attendance marking |
| Library | Search and category filters, external learning materials, persistent completed/undo progress |
| Community | Topics and replies with escaped content; administrator moderation |
| Mentorship | Requests, pending/accepted/declined states; assigned mentor accepts or declines own requests |
| Members | Search by name/interests and public member profiles; private member emails not shown in directory |
| Admin | Role assignment, suspension, event/resource CRUD, moderation, participant lists, audit log and engagement/event CSV exports |
| Streaks and badges | Dated meaningful practice, current/best streak and rule-based milestones; no visit credit |
| Daily challenges | Saved text/code, revision until approved, administrator review; code is never executed |
| Discover feed | Actual public milestones and explicit idempotent cheers; no private submissions |
| Project lab | Published description/link, member feedback, owner/admin deletion and admin moderation |
| Calendar | Month view, registered-event markers and JavaScript countdowns |
| Global search | Members, events, resources, topics and projects; excludes private email/inbox/submissions |
| Inbox | Persistent own in-app notifications; no email/push or background reminder service |
| Preferences | Persistent light/dark theme, keyboard-friendly control and reduced-motion-aware motion |

## Files

- `config.php`: PDO queries, session/CSRF/security and reusable layout helpers upgraded from Assignment 1.
- `index.php`, `signup.php`, `dashboard.php`, `logout.php`: original authentication page structure extended.
- `profile.php`, `members.php`, `events.php`, `resources.php`, `community.php`, `mentorship.php`: member features.
- `action.php`: validated POST actions with server-side permission checks and redirects.
- `admin.php`, `report.php`: administration and CSV reporting.
- `assets/`: custom CSS/JS and original Assignment 1 logo.
- `database/schema.sql`: ten InnoDB tables, unique constraints and foreign keys.
- `database/innovations.sql`: nine additive tables; `tools/upgrade.php` is the safe idempotent migration.
- `hub.php`, `challenges.php`, `showcase.php`, `calendar.php`, `search.php`, `achievements.php`, `notifications.php`: innovation screens; `innovate.php` validates their POST actions.
- `tools/`: CLI-only installation, seeds, migration and recovery utilities.
- `tests/`: repeatable integration tests, recorded results and test instructions.
- `docs/`: A3 portfolio PDF/DOCX, screenshots, ERD, wireframes, technical notes, user guide and presentation script.
- `presentation/`: editable 18-slide English PowerPoint, notes and generator scripts. Standard fade entrances/transitions and selected Morph transitions with fallback are included; verify playback in desktop PowerPoint.

## Security and deployment limits

All state-changing forms require CSRF and authentication. Admin permissions are checked on the server, not just hidden in navigation. Suspended accounts lose protected access immediately. Queries use native prepared statements. Passwords are hashed with PHP's default algorithm. Login is limited to five failures per email in a rolling 15-minute window. Event registration locks the event row in a transaction before checking capacity. Uploaded photos are MIME/dimension/size-checked and randomly named. Apache denies executable uploads and access to config/SQL/tool/document files. CSV cells are protected against spreadsheet formula injection.

**Local academic deployment, not a production-ready public service.** Before internet hosting: HTTPS, dedicated least-privilege database account, server-level access controls, upload image re-encoding/malware checks, account recovery/email verification, stronger IP-aware rate limiting, privacy/retention policy, backups, monitoring and a security review. The PHP built-in development server does not enforce `.htaccess`; use it only on a trusted local machine. GitHub Pages cannot execute PHP/MySQL. This repository does not provide a live hosted application.

`config.local.php` and uploaded photos are excluded from Git and the ZIP. Never upload real users, private credentials or database dumps. SQL schema and demo content are safe; admin credentials are chosen on your own PC.

## GitHub and documentation

Repository: https://github.com/EagerBeaversl/django-girls-community-final (private; the owner must invite the lecturer as collaborator for access).

Read `docs/USER_GUIDE.md` for the demo flow and `docs/TECHNICAL.md` for schema/workflows. The portfolio includes actual captured interfaces and separate QR codes for GitHub and the local system. The **local QR only works on the PC running XAMPP**, not on a lecturer's phone. Replace it with a verified public URL if you later host the application. Do not claim a live deployment before hosting.

The source is provided for study, adaptation and demonstration. Review and understand the implementation, disclose assistance as required by university policy, and sign your own assessment form. No grade/ranking is guaranteed.

## Troubleshooting

- **Database not ready / access denied:** start MySQL, create the database, verify credentials in `config.local.php`.
- **Unknown database:** create `django_girls` in phpMyAdmin; database creation is not done by the installer.
- **Tables already exist:** do not reinstall. Existing installations use `upgrade-windows.bat`; only an incomplete fresh install needs `create-admin.php` and seeds. Do not delete a database containing real work.
- **Port conflict:** Apache may conflict with IIS; configure XAMPP and use the actual Apache port, e.g. `http://localhost:8080/django-girls/`.
- **Upload error:** make `uploads` writable by Apache/PHP; images must be real JPG/PNG/WebP, under 2 MB and at most 6000 pixels per side.
- **403 on tools/config:** expected. Run tools using PHP from the command line, not through browser URLs.
- **Too many login attempts:** wait 15 minutes; for a disposable test DB only, reset the corresponding `login_attempts` row through phpMyAdmin.
- **Private repository inaccessible:** sign in to GitHub with the owner/collaborator account.

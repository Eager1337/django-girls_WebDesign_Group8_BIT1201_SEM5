# Technical specification

## Scope and continuity
Assignment 1 used core PHP, helper functions, hashed credentials, sessions, CSRF, a Django Girls SVG and JSON account storage. Final keeps the organisation, source entry-point names, original logo and helper conventions, while migrating storage to MySQL and adding community management. The approved spectral redesign uses black/graphite, cyan/pink/amber highlights, Arial website typography and Tahoma 12 portfolio typography. It is not a third-party template/plugin.

## Architecture
Browser (HTML/CSS/vanilla JS) → Apache/PHP → PDO prepared statements → MySQL/InnoDB.
Pages render HTML server-side. `action.php` is the common mutation controller with POST/redirect/GET. `report.php` streams administrator-only CSV. CLI utilities provision schema and administrator locally. No remote cloud dependencies; external resources open third-party reference pages.
`innovate.php` handles authenticated innovation POST actions; `includes/innovations.php` shares streak/feed/notification logic. `database/innovations.sql` adds nine tables through idempotent `tools/upgrade.php`. Fresh installer runs both schemas; existing databases only run the additive upgrade. No user data backfill or invented activity is performed.

## Tables and relationships
| Table | Purpose / key relations |
|---|---|
| users | Identity, password hash, role, suspension, profile; unique email |
| events | Workshop title/date/location/capacity |
| registrations | Composite user/event key; attendance; cascades when user/event deleted |
| resources | Learning link/category/description |
| progress | Composite user/resource key; completion time |
| topics | Discussion owned by a user |
| replies | User reply to a topic; deleted when topic removed |
| mentorships | Member→mentor request; unique pair; pending/accepted/declined |
| login_attempts | Email attempt counter and last-attempt time |
| audit_log | Actor/action/time; actor set NULL if account removed |
| activity_days | Composite user/date key; meaningful learning activity |
| challenges | Active daily prompt rotation; deterministic by date |
| challenge_submissions | Unique user/date; FK challenge/user; code text and manual review |
| projects | FK user; title/description and optional validated HTTP(S) link |
| project_feedback | FK project/user; cascades with project |
| activity_feed | FK user; actual public topic/project/learning/approval milestone |
| feed_reactions | Composite feed/user key, explicit add/remove |
| notifications | FK user; unique user/dedupe key; owned mark-read controls |
| app_migrations | Independent applied-version marker |

SQL schema is the authoritative ERD. Relationship diagram in `erd.png` and `erd.mmd`. Account deletion is intentionally not offered; suspension preserves records. Event/resource/topic deletion requires confirmation and removes dependent data through foreign keys.
There are 19 tables in total. `activity_feed.source_id` is polymorphic, not a database FK; application hooks remove feed entries for deleted topics/resources/projects. The diagram summarises key fields; consult both SQL files for full column definitions. Mentorship has two user relationships. `login_attempts` and `app_migrations` are independent.

## Navigation
Public: Home/login ↔ Register. Protected: Overview, Events, Library, Community, Mentorship, Members, Profile. Administrator additionally sees Administration. Mentor response buttons are only displayed for the assigned mentor's pending requests. Permission checks are repeated server-side. All roles can use ordinary member features.
Protected innovation navigation: Discover, Daily challenge, Project lab, Calendar, Search, Milestones, Inbox. All roles can use these; manual challenge review/creation and feedback moderation require admin privileges.

## Workflows
- Register → validate name/email/interests/password/confirmation → unique email → hash → insert → login.
- Login → validate CSRF → email throttling → active account/password_verify → regenerate session → dashboard.
- Event join → authenticate/CSRF → transaction → lock event row → reject past/full/duplicate → registration → commit.
- Resource completion → authenticate/CSRF → existing resource → composite-key idempotent insert → personalised counts.
- Mentorship → active different mentor → one request per member/mentor pair → only assigned mentor accepts/declines pending request.
- Admin mutation → verify active admin → validate inputs → write → audit → redirect. Own-role/status edits are forbidden; at least one active administrator must remain.
- Logout → POST/CSRF → clear session and cookie → destroy → public page.
- Daily challenge → validate current prompt → lock user row → one saved solution/date → revise until approved. Admin review uses the same user lock to serialise with submissions. Text is escaped and never executed.
- Streak → dated meaningful completions/topics/replies/submissions/projects/feedback → consecutive dates ending today or yesterday. No login, visits or reaction credit; duplicate already-completed resource writes earn no new day. Best streak persists across gaps.
- Project → validate description/link → publish actual feed entry → feedback → notify owner. Owner/admin deletion removes feed and cascades feedback. Reactions have explicit idempotent add/remove.
- Notification → active recipient and dedupe key → persistent inbox → own single/all mark-read. Registered-event reminder is generated when opening the app within 48 hours; no background scheduler, email or push exists.
- Search → prepared escaped LIKE query → five public domains. Private submissions, email and inbox text are excluded.

## Personalisation
Counts and upcoming events are database queries. Learning suggestions exclude resources already completed; exact/category-text matching of the member's interests is preferred, then resource order. This is simple rule-based personalisation, not AI. Progress measures completion of all library resources, not verified skills or certifications.

## Security design and limitations
Password hashing, escaping, prepared statements, CSRF, HttpOnly/SameSite cookies, HTTPS-aware Secure cookies, login throttling, CSP, no-store responses, role checks and transactional event capacity. Uploads: file MIME, valid dimensions, max 2 MB and 6000×6000, random filename, script execution denied under Apache. In-app notifications are implemented; email verification, forgotten-password flow, per-IP rate limiting, private chats, real-time push and upload re-encoding are not. No untrusted submission execution engine exists.

Profile/password combined form may save ordinary profile fields before a new-password validation failure; the error explicitly says profile changes are saved if the current password is wrong. Upload filenames may leave older photos in the local uploads directory; clean them according to a retention policy before production. Export CSV is administrator-only and neutralises formula prefixes.

## Research and source boundaries
Problem/user needs are inferred design hypotheses from the supplied assignment brief, not interviews. The prototype addresses fragmented event sign-up, learning-resource discovery and beginner support by centralising them. No fabricated survey statistics are included. Seeded links point to official learning resources; their contents are not copied into this project.

References used for implementation rationale:
- PHP manual: https://www.php.net/manual/en/function.password-hash.php ; https://www.php.net/manual/en/pdo.prepared-statements.php
- OWASP CSRF prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP upload guidance: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- Django Girls tutorial: https://tutorial.djangogirls.org/en/
- User-supplied final brief and Assignment 1 report/source ZIP, reviewed 17 November 2026.

## Documentation notes
Portfolio DOCX specifies Tahoma 12 pt with A3 pages. PDF embeds Wine's Tahoma-compatible implementation; Windows Word uses installed Microsoft Tahoma. Screenshots are genuine local test captures with optional clearly labelled demo profiles. GitHub repository is private; local system QR is explicitly not public hosting. No assessment signature is supplied.

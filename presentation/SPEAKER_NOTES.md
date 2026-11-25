# Defence speaker notes

## Slide 1

Introduce the student, module and academic project. This is a PHP/MySQL continuation of Assignment 1, not a Django framework app and not an official Django Girls service. The final brief says Semester 05; the earlier report says Sem4. Confirm the discrepancy with the lecturer.

## Slide 2

Original Assignment 1 source and report are the continuity evidence. The organisation and original logo remain. The CLI migration can preserve valid password hashes from the original JSON store. Existing MySQL installations must use the additive upgrade, not reinstall. No survey results or organisational endorsement are claimed.

## Slide 3

Fragmentation is a design hypothesis: beginners may struggle when event registration, resources and support sit in separate channels. No interviews or engagement measurements were conducted. Explain how the three roles organise the solution, then describe the need for future user testing.

## Slide 4

Demonstrate the requirement mapping with a real account. Dashboard statistics come from the database. User management protects the last active administrator. CSV is administrator-only. A publicly reachable live system URL remains outstanding; localhost does not satisfy that requirement automatically.

## Slide 5

All private screens require a live active account. Mentor responses are limited to the assigned mentor and pending requests. Administrative routes and writes reject members even if a URL is typed manually. Self-demotion and removal of the last administrator are blocked. Explain a member event journey and administrator attendance journey.

## Slide 6

The user-approved visual reference informed the spectral halos, floating panels and CSS three-dimensional auth sculpture. The website uses Arial, while the A3 portfolio follows the brief’s Tahoma 12 requirement. Motion is decorative and reduced-motion-aware. Keyboard focus, explicit labels and theme controls improve access; no formal WCAG certification is claimed.

## Slide 7

Browser requests go to Apache/PHP. Config and helpers enforce sessions, escaping and PDO prepared statements. action.php handles original mutations; innovate.php handles the additive feature actions; report.php streams administrator CSV. CLI tools install or upgrade. MySQL InnoDB transactions protect capacity. PHP 8.4 and MariaDB 11.8 were tested locally; CI targets PHP 8.2/MySQL 8.

## Slide 8

Core: users, events, registrations, resources, progress, topics, replies, mentorships, audit_log, login_attempts. Additive: activity_days, challenges, challenge_submissions, projects, project_feedback, activity_feed, feed_reactions, notifications, app_migrations. Unique keys guard user/day submissions, reactions, notification dedupe and learning days. Full foreign-key ERD is in the portfolio documentation; these are domain groups, not a complete ERD.

## Slide 9

Explain password_hash and password_verify, session regeneration, CSRF for POST, output escaping and parameterised queries. Photos are MIME/dimension/size checked and given random filenames. Login attempts are throttled. Uploaded files are restricted. These checks are not an external penetration test. HTTPS, operational backups, recovery and hosting hardening remain production work.

## Slide 10

When joining, the server locks the event row, checks time, duplicate membership and capacity, then inserts and commits. Administrators record attendance. The 43 core checks include duplicate registration, full capacity, cancellation and attendance. Countdowns are display enhancements, not the source of capacity truth.

## Slide 11

Resource completion is reversible and backed by a unique user/resource record. Discussion bodies and replies are escaped. Mentorship requests are directed to active mentors and can be accepted or declined by the assigned mentor. There is no private chat or email service. Public activity only exposes appropriate milestones; private challenge code stays private.

## Slide 12

List all eight and connect each to a user need. They do not prove engagement gains. Streaks depend on meaningful activity, challenges use manual review, feed contains real entries, projects accept links/text rather than executable uploads, calendar uses event data, search excludes private data, inbox is in-app only, and theme preferences persist locally.

## Slide 13

Representative slide 13 of the planned 18-slide defence. Explain the daily challenge workflow: authenticated member stores text or code; no execution engine exists; administrator manually reviews; milestones use dated meaningful actions. The activity-day key prevents multiple credits on one date. Current streak accepts activity yesterday but breaks at a gap. Evidence: 42 HTTP feature checks and 8 CLI helper checks on a disposable local DB. Baseline also passes 43 checks. Do not claim improved engagement, guaranteed grades, public hosting or desktop PowerPoint playback verification. The final deck will add restrained entrances and Morph-compatible transitions after preview approval.

## Slide 14

A project stores description and an optional validated HTTP(S) link. User text is escaped. Owners and administrators can delete; feedback deletion is administrator-only. Reaction keys prevent duplicates. Project deletion removes its feed and cascades feedback. The displayed screenshot is from a disposable local test installation, not live community adoption.

## Slide 15

Calendar reads actual workshops and current member registrations. Event reminders appear when the app is opened for a registered event within 48 hours, deduplicated per event; no background scheduler or email/push exists. Search covers members/events/resources/topics/projects without private email, submissions or inbox content. Theme storage failures do not break forms. Reduced motion removes decorative animations.

## Slide 16

43 baseline HTTP, 42 innovation HTTP and 8 transactional helper checks passed. Browser matrix: 17 routes × 3 widths × 2 themes = 102 checks. It checked overflow, JavaScript errors, theme persistence and reduced motion. Upgrade ran twice successfully. These are not 102 separate human usability studies or a formal accessibility/security audit. Actual Windows execution and desktop PowerPoint motion playback remain unverified.

## Slide 17

Back up the populated database and existing folder. Copy the updated source but retain config.local.php and uploads. Run upgrade-windows.bat with MySQL running; it invokes tools/upgrade.php and adds tables/seeds only. Fresh users use the fresh installer. GitHub is private and requires lecturer access. localhost works only on the machine running XAMPP. A public live URL is outstanding and needs hosting or explicit lecturer acceptance.

## Slide 18

Conclude with implemented scope, evidence and limitations. No guaranteed grade, ranking or engagement impact. Next priorities: real user feedback, Windows walkthrough, production security/backups, public PHP hosting if required, account recovery, and desktop PowerPoint transition/animation validation. Mention semester discrepancy and academic assistance disclosure. Invite questions about capacity locks, schema integrity, challenge safety and migration preservation.

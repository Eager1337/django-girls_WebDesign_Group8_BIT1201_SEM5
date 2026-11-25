# Spectral redesign and innovations — final safe update

The approved redesign and all eight innovations are implemented. Core data is retained; nine additive tables are required. Use the full final package rather than the obsolete UI-only preview patch.

## Update your existing Windows installation
1. Back up your current project folder and export your database in phpMyAdmin before making changes.
2. Extract the final Windows ZIP into a temporary folder.
3. Copy the updated application source into C:\xampp\htdocs\django-girls, replacing matching application code.
4. Do NOT delete or replace config.local.php or uploads. Do NOT run install-windows.bat again. Start MySQL and run upgrade-windows.bat to apply the idempotent additive migration.
5. Keep Apache and MySQL running. Open http://localhost/django-girls/ and press Ctrl+F5 to refresh cached assets.
6. Sign out to view the new sign-in page. Click Join the community to view sign-up.

Your existing users, password hashes, uploaded photos, bookings, discussions and learning progress remain in your local database and uploads folder. config.php is shared application code; config.local.php is your private database connection configuration and must be retained.

## What changed
- Near-black/graphite visual identity with spectral halos and orange actions.
- Auth pages: rotating CSS perspective cube, floating decorative chips, subtle fine-pointer form tilt, password-strength indicator on sign-up.
- All authenticated pages: reworked navigation, cards, forms, tables, page accents and staggered entry effects.
- Responsive layouts; reduced-motion support; no external animation library, fonts or tracking.
- All eight additions: real activity feed/reactions, milestones, manually reviewed challenges, projects/feedback, calendar/countdowns, global search, own persistent inbox and light/dark/reduced-motion preferences.

## Verification
43 core HTTP + 42 innovation HTTP + 8 helper checks passed. 102 viewport/theme combinations passed; no JS errors, reduced motion and theme persistence checked. PHP syntax passed. Actual Windows/XAMPP still needs checking on your PC.

## Portfolio status
The PDF/DOCX now contains final screenshots and the 19-table ERD. Both exports were verified as five A3 pages. The English defence deck contains 18 editable slides with notes; verify animation/Morph playback in desktop PowerPoint.

## GitHub status
See docs/GITHUB_UPLOAD.md for the private repository and verification status. The localhost URL is not public hosting; the live-system requirement needs hosting or lecturer approval.
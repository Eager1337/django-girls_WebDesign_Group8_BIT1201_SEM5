# Verification

Final recorded checks: **43 core HTTP + 42 innovation HTTP + 8 transactional helper tests passed**, on disposable Linux PHP 8.4/MariaDB 11.8. Browser: **102** combinations (17 routes × 390/768/1440 px × dark/light), no page overflow or JS errors; reduced motion and theme persistence passed. PHP syntax passed; additive upgrade ran twice successfully. Earlier baseline photo-upload valid/invalid checks passed; they are not part of the 102 final visual combinations. Actual Windows/XAMPP and desktop PowerPoint motion remain unverified.

`results.json` contains individual HTTP results. Do not run integration tests against real member data: they create accounts, change roles/status, create/update/delete content and update attendance. Use a separate database configured in `config.local.php`, run the installer with a temporary administrator, and start a local server:

```sh
php -S 127.0.0.1:8088
```

In another terminal set `DG_TEST_ADMIN_EMAIL` and `DG_TEST_ADMIN_PASSWORD` to the disposable administrator credentials, then:

```sh
python tests/integration.py http://127.0.0.1:8088
python tests/innovations.py http://127.0.0.1:8088
php tests/innovation-helpers.php
```

Requires Python 3 standard library only; no Python is required to run the application itself. Test uses first seeded event/resource id 1 and requires an otherwise fresh database. Keep recorded results separately if rerunning.
`innovation-results.json` records 42 new HTTP checks. The eight helper checks use a transaction and roll back their temporary user/activity. `docs/visual-results.json` records the final browser matrix. To reproduce visual checks, install Playwright and Chrome and run `tools/check-visual.py` with the same admin environment variables; `DG_TEST_URL`, `CHROME_PATH` and `DG_SCREENSHOT_DIR` are configurable. Tests must never run against real member data.

Manual checks before submission: create real member/mentor accounts; capacity concurrency; mobile keyboard operation; original-user migration on a COPY of any real data; Apache access-denial rules; your actual Windows setup. No concurrency/load/performance or production penetration testing is claimed.

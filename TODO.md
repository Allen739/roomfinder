# Room Finder TODO

## Linting Issues (Flake8)
To be addressed in Version 2 or future PRs. Currently ignored in CI (`.github/workflows/ci.yml`) to prioritize deployment.

### Errors to Fix
- **E501: Line too long (>120 characters)**:
  - `finder/management/commands/load_timetable.py:80` (123 chars)
  - `finder/views.py:172` (127 chars)
  - `finder/views.py:187` (139 chars)
  - `finder/views.py:192` (135 chars)
  - `finder/views.py:216` (150 chars)
  - **Fix**: Split long lines (e.g., regex with `\`, wrap strings in parentheses).
- **F401: Unused import**:
  - `finder/tests.py:1` (`django.test.TestCase` imported but unused)
  - **Fix**: Remove import or add tests to `tests.py`.
- **E261: At least two spaces before inline comment**:
  - `room_finder/roomfinder/settings.py:41`
  - **Fix**: Add two spaces before comment (e.g., `DEBUG = True  # Comment`).
- **W291: Trailing whitespace**:
  - `room_finder/roomfinder/settings.py:41`
  - **Fix**: Remove trailing spaces (editor: "Trim trailing whitespace").
- **E303: Too many blank lines**:
  - `room_finder/roomfinder/settings.py:84` (3 blank lines)
  - `room_finder/roomfinder/settings.py:104` (3 blank lines)
  - **W504: Line break after binary operator**:
  - `finder/views.py:54`
  - **Fix**: Move operator to previous line.
  - **Fix**: Reduce to 1–2 blank lines.

**CI Test Database**:
  - Issue: `DATABASE_URL` not set in CI, using SQLite fallback.
  - Fix: Configure PostgreSQL in CI (e.g., GitHub Actions `services: postgres`) for realistic tests.
  - Ref: GitHub issue #TBD


### Plan
- Created GitHub issue to track (see #1).
- Fix in Version 2 or dedicated PR (e.g., "Code cleanup: Resolve flake8 errors").
- Update CI to remove `--ignore` after fixes.
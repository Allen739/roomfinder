```markdown
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
Describe the Bug
A clear description of what the bug is.
To Reproduce
Steps to reproduce:
Go to '...'

Click on '...'

See error

Expected Behavior
What should happen?
Screenshots
Add screenshots if applicable.
Environment
OS: [e.g., Windows 10]

Python: [e.g., 3.8]

Django: [e.g., 5.0.6]

Browser: [e.g., Chrome]

Additional Context
Any other details (e.g., error messages).

**Action 2**: Create Feature Request Template.
```bash
touch .github/ISSUE_TEMPLATE/feature_request.md

Content (.github/ISSUE_TEMPLATE/feature_request.md):
```markdown
name: Feature Request
about: Suggest an idea for Room Finder
title: '[FEATURE] '
labels: enhancement
assignees: ''
Problem
What problem does this feature solve?
Proposed Solution
Describe the feature you want.
Alternatives
Any alternative solutions you considered?
Additional Context
Add examples, mockups, or references.

**Action 3**: Create PR Template.
```bash
touch .github/pull_request_template.md

Content (.github/pull_request_template.md):
markdown

**Description**
What does this PR do?

**Related Issues**
Closes #issue-number

**Changes**
- List major changes (e.g., "Added incremental uploads").
- Updated tests/docs?

**Testing**
- How did you test this? (e.g., "Ran `python manage.py test`, checked `/upload/`.")
- Any manual steps?

**Checklist**
- [ ] Code follows PEP 8 (checked with flake8).
- [ ] Tests pass (`python manage.py test`).
- [ ] README updated if needed.
- [ ] Ran locally, no errors.

Action 4: Stage and Commit:
bash

git add .github/ISSUE_TEMPLATE/bug_report.md
git add .github/ISSUE_TEMPLATE/feature_request.md
git add .github/pull_request_template.md
git commit -m "Add issue and PR templates"
git push origin main


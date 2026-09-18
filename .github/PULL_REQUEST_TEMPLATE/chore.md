## Chore / Infrastructure Description
<!-- Provide a clear, concise summary of the maintenance or pipeline work you completed. -->
This PR implements a automated `pytest` suite within our GitHub Actions workflow. This ensures all unit tests run automatically on every push and pull request to maintain codebase stability.

Fixes / Closes #<!-- Insert Issue Number here, e.g. #12 -->

## Type of Maintenance
Check all that apply:
- [x] CI/CD Pipeline / Automation Configuration
- [ ] Dependency Update (Adding/updating packages)
- [ ] Code Quality / Linting / Formatting
- [ ] Refactoring / Tech Debt (No logic changes)
- [ ] Other (Please describe):

## How Has This Been Tested?
<!-- Describe how you verified that these infrastructure or pipeline changes work correctly. -->
- [x] Verified workflow runs successfully in this PR branch.
- [x] Confirmed the pipeline correctly fails if a unit test is intentionally broken.
- [x] Ran `pytest` locally to ensure no local environment breakage.

## Chore Checklist
- [x] This change does **not** introduce any user-facing feature updates or bug fixes.
- [x] All automated jobs (linting, security, testing) pass successfully in the pipeline.
- [x] Any new dependencies have been added to the relevant lockfiles (`requirements.txt`, etc.).
- [x] No sensitive credentials or real production keys have been leaked in the configuration files.

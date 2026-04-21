# Maintainer Setup

This document is for @cvander (or whoever owns the `cvander/Maya`
GitHub repository). It lists the one-time settings toggles and
external-service applications that complement the CI hardening
delivered in issue #7 — the items that cannot be expressed as
files in a pull request.

All links assume the repository is `cvander/Maya`; adjust if the
path changes.

## 1. Repository settings (GitHub UI)

Open <https://github.com/cvander/Maya/settings> and enable:

- [ ] **Secret scanning** (Settings → Code security and analysis → Secret scanning → Enable)
- [ ] **Push protection** (same section → Push protection → Enable)
- [ ] **Private vulnerability reporting** (same section → Private vulnerability reporting → Enable)
- [ ] **Dependency graph** (same section → Dependency graph → Enable)
- [ ] **Dependabot alerts** (same section → Dependabot alerts → Enable)
- [ ] **Default `GITHUB_TOKEN` permissions** (Settings → Actions → General → Workflow permissions → "Read repository contents and packages permissions")

### Branch protection on `main`

Settings → Branches → Add rule → Branch name pattern `main`. Enable:

- [ ] Require a pull request before merging, with at least 1 approval
- [ ] Require signed commits
- [ ] Require linear history
- [ ] Block force-pushes
- [ ] Block deletions
- [ ] Do not allow bypassing the above settings ("Apply to administrators")

Rationale: "Apply to administrators" ensures the signed-commit
guarantee is tamper-evident; without it, admins could push unsigned
commits and break the audit trail.

## 2. OpenSSF Best Practices Bronze

Apply at <https://www.bestpractices.coreinfrastructure.org/en/projects/new>.

Items already satisfied by the issue #7 PR bundle:

- [x] Public version-controlled source repository (GitHub)
- [x] Open-source license (MIT)
- [x] Code of conduct (CODE_OF_CONDUCT.md)
- [x] Contributing guide (CONTRIBUTING.md)
- [x] Security policy (SECURITY.md)
- [x] Automated testing / static analysis in CI (shellcheck, CodeQL, gitleaks, Scorecard)
- [x] Secret scanning / credential hygiene (gitleaks workflow + secret scanning toggle above)
- [x] Citation metadata (CITATION.cff)

Items you will need to provide during the application:

- [ ] Project description (1–2 sentences)
- [ ] Public issue tracker URL (GitHub Issues)
- [ ] Contact email for security reports (already in SECURITY.md)

After submission, update the badge placeholder in `README.md` (commented
TODO block) with the project ID returned by OpenSSF.

## 3. Scorecard pre-reqs

The `.github/workflows/scorecard.yml` workflow requires:

- `id-token: write` permission — this is granted at the workflow level
  in the YAML and needs no repo-settings change beyond the "Read"
  default above.
- First run is scheduled weekly (Tuesday 06:00 UTC). The public report
  surfaces at
  <https://api.securityscorecards.dev/projects/github.com/cvander/Maya>
  and the README badge pulls from `img.shields.io/ossf-scorecard/...`.
- `step-security/harden-runner` starts in `audit` mode. After one month
  of clean audit logs, a follow-up PR can flip it to `block`.

## 4. Optional secrets

None of the workflows *require* repository secrets. Two optional ones
exist:

- **`GITLEAKS_LICENSE`** — only needed if the repo is ever moved under
  a GitHub Organization account (gitleaks-action is free for personal
  accounts). Leaving it unset is correct for the current personal-account
  setup.
- **`GITLEAKS_PRIVATE_CONFIG`** — optional overlay of bar-specific
  gitleaks rules (regulars' names, local PII patterns, etc.) that must
  not be committed to the public repo. See the `.github/workflows/gitleaks.yml`
  comment block for format. Leaving it unset is a safe default.

## 5. Once everything above is done

Close issue #7 with a comment linking the three PRs and this document.
Future hardening follow-ups (flipping lychee to blocking, flipping
harden-runner to block mode, adding Python/JS dependabot ecosystems)
are tracked as separate sub-issues.

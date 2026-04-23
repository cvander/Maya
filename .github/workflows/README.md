# GitHub Actions Workflows

This directory contains the repository's CI workflows. All workflows
follow these conventions.

## Pin every action to a full 40-char SHA

Every `uses:` line pins the action to a commit SHA, with the human
readable version in a trailing comment:

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.7
```

This prevents a silent supply-chain swap if an upstream tag is moved.

To bump an action, resolve the new SHA from its tag:

```bash
gh api repos/OWNER/REPO/git/ref/tags/VERSION --jq '.object.sha'
```

Dependabot opens weekly PRs that do this automatically; manual bumps
use the same command.

## Minimize `permissions:`

Every workflow sets `permissions: {}` at the top level and re-grants
only what a job needs at the job or step scope.

## First step is harden-runner (audit mode)

Every job's first step is `step-security/harden-runner` in `audit` mode.
Logs surface at the Actions run page. After the egress baseline is
known, a follow-up PR flips audit → block.

## Where results surface

| Workflow       | Results appear in                                                            |
|----------------|------------------------------------------------------------------------------|
| shellcheck     | Checks tab (PR annotations)                                                  |
| lint-prose     | Checks tab (yamllint / markdownlint / lychee annotations)                    |
| codeql         | Security tab → Code scanning alerts                                          |
| gitleaks       | Checks tab; PR inline summary when `pull-requests: write` is available       |
| scorecard      | Security tab → Code scanning alerts, plus the public OpenSSF Scorecard report |

## Fork-PR caveat

PRs opened from a fork run with a read-only `GITHUB_TOKEN` and no
repository secrets. The workflows are designed to function under this
constraint: none use `pull_request_target`, and gitleaks degrades its
inline-comment behaviour to workflow annotations when it cannot post
PR comments.

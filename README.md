# AI for the messy bits

Parsing, cleaning, normalizing: the hands-on workshop from Extract Summit
2026. Everything here runs offline.

## Setup

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).
2. `git clone https://github.com/zytedata/messy-bits-workshop && cd messy-bits-workshop`
3. `uv sync`

Run `uv sync` as soon as you can: it downloads Python and all dependencies,
which takes a while on conference Wi-Fi.

## Running things

From the directory of the script:

```
cd demo && uv run 01_parsing.py
cd exercise && uv run starter.py
```

For the `# %%` cells in VS Code, open this folder and pick `.venv` as the
interpreter.

## Layout

- `hook/`: two LLM answers to the same prompt, quoted on the opening and
  closing slides, plus the prompt that produced them.
- `demo/`: the three live-coding scripts and the sample pages they read.
- `exercise/`: the hands-on. Start from `starter.py`, see `README.md` there.
- `slides.md`: the deck, in [Marp](https://marp.app/) format.
- `tests/`: `uv run pytest` checks that every script still prints what the
  slides say it does.

## Governance model

This repository is **governed**. When the portal created it, it set the org
custom property `governed=true` (plus `production`, `contains_code`, and
`lifecycle`). Org-level **rulesets** in your GitHub org then apply automatically,
based on those properties — you don't configure branch protection per repo:

| Ruleset | Applies when | Effect on the default branch |
|---------|--------------|------------------------------|
| `baseline` | `governed=true` | No force-push, no branch deletion |
| `require-pr-production` | `governed=true` AND `production=true` | PRs required, ≥1 approval, stale reviews dismissed |
| `require-secrets-scan` | `governed=true` AND `contains_code=true` | The `secrets / detect-secrets` check must pass |

### Secrets scanning

`.github/workflows/secrets.yml` calls the **central** reusable workflow in
`zytedata/governance`. The required status check is **`secrets / detect-secrets`**.
You cannot weaken this:

- The scan logic lives in the governance repo, not here.
- The check is required by the org ruleset, so a missing/failed check blocks merge.
- New secrets must be explicitly audited into `.secrets.baseline` (and reviewed)
  before a PR can merge.

Run the scan locally before pushing:

```bash
pip install detect-secrets pre-commit
pre-commit install
pre-commit run --all-files
# If you add a legitimate, reviewed value that trips the scanner, audit it:
#   detect-secrets scan > .secrets.baseline   # then review the diff in your PR
```

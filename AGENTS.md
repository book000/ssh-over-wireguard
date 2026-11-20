# AGENTS.md

Guidance for AI coding agents and contributors. `CLAUDE.md` imports this file, and `.github/copilot-instructions.md` adds the review checklist.

## Language

- All deliverables are written in **English**: commit messages, PR/Issue titles and bodies, review comments, code comments, and documentation (`README.md`, `AGENTS.md`, etc.).
- `README-ja.md` is an intentionally kept Japanese translation of `README.md`. Keep it in sync with `README.md`.
- Exceptions (keep as is): quotations, technical identifiers, generated files, and external source text.
- Runtime messages (logs, errors) are English.
- Do not rewrite Git history to change the language of past commits.

## Overview

`book000/ssh-over-wireguard` is a GitHub composite action. It brings up a WireGuard tunnel on the runner (`wg-quick up` on a uniquely named interface, configured from a private temporary directory), then runs an SSH command or an SCP transfer over it, and tears everything down in a final `if: always()` step. There is no application source code: all logic is Bash in `runs.steps` of `action.yml`.

## Commands

Run `python -m unittest discover -s tests` for the operation selection tests; they require PyYAML. Verify integration changes by running the action from a GitHub Actions workflow on a Linux runner (the steps use `sudo` and `apt-get`).

## Structure

- `action.yml`: inputs and the composite steps (validate inputs, install WireGuard, write the WireGuard config to a private temporary directory, start VPN, write the SSH key, an action-owned SSH config (used with `ssh -F` / `scp -F`) and `known_hosts`, optional ping, SSH or SCP, cleanup).
- `tests/test_operation_selection.py`: input validation and work-step selection tests.
- `README.md`: usage, input tables and examples. `README-ja.md`: its Japanese translation.

## Conventions

- Inputs use kebab-case (e.g. `ssh-host-ip`). Every `run` step sets `shell: bash`.
- When you add, change or remove an input in `action.yml`, update the input tables and examples in both `README.md` and `README-ja.md`.
- Keep host key verification: the SSH host key from `ssh-host-key` is written to `known_hosts`; never disable `StrictHostKeyChecking`.
- Keep the `Cleanup` step with `if: always()` so the VPN, the WireGuard config, the SSH private key, the SSH config and their temporary directories are removed even on failure.
- Never read or write `/etc/wireguard/` or `~/.ssh/config`, and never use a fixed interface name such as `wg0`: the action must not overwrite or delete state it did not create. `Cleanup` runs `wg-quick down` only if this invocation brought the interface up (`wg-started`), and removes only paths recorded in this invocation's step outputs.
- Create the SSH private key with `umask 077` inside a `mktemp -d` directory; never write it to a fixed path such as `/tmp/id_rsa`.
- Failing to install the full `wireguard` package and continuing with `wireguard-tools` only is intentional (container-like runners).
- Never put keys in the repository or print them to logs; callers pass them through GitHub Secrets.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/); branches follow [Conventional Branch](https://conventional-branch.github.io) short form (`feat/...`, `fix/...`).
- Do not commit to Renovate PRs.

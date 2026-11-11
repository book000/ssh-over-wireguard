# AGENTS.md

Guidance for AI coding agents and contributors. `CLAUDE.md` imports this file, and `.github/copilot-instructions.md` adds the review checklist.

## Language

- All deliverables are written in **English**: commit messages, PR/Issue titles and bodies, review comments, code comments, and documentation (`README.md`, `AGENTS.md`, etc.).
- `README-ja.md` is an intentionally kept Japanese translation of `README.md`. Keep it in sync with `README.md`.
- Exceptions (keep as is): quotations, technical identifiers, generated files, and external source text.
- Runtime messages (logs, errors) are English.
- Do not rewrite Git history to change the language of past commits.

## Overview

`book000/ssh-over-wireguard` is a GitHub composite action. It brings up a WireGuard tunnel on the runner (`wg-quick up wg0`), then runs an SSH command or an SCP transfer over it, and tears everything down in a final `if: always()` step. There is no application source code: all logic is Bash in `runs.steps` of `action.yml`.

## Commands

There is no build, lint or test tooling. Verify changes by running the action from a GitHub Actions workflow on a Linux runner (the steps use `sudo` and `apt-get`).

## Structure

- `action.yml`: inputs and the composite steps (validate inputs, install WireGuard, write `/etc/wireguard/wg0.conf`, start VPN, write SSH config, key and `known_hosts`, optional ping, SSH or SCP, cleanup).
- `README.md`: usage, input tables and examples. `README-ja.md`: its Japanese translation.

## Conventions

- Inputs use kebab-case (e.g. `ssh-host-ip`). Every `run` step sets `shell: bash`.
- When you add, change or remove an input in `action.yml`, update the input tables and examples in both `README.md` and `README-ja.md`.
- Keep host key verification: the SSH host key from `ssh-host-key` is written to `known_hosts`; never disable `StrictHostKeyChecking`.
- Keep the `Cleanup` step with `if: always()` so the VPN, `/tmp/id_rsa` and `~/.ssh/config` are removed even on failure.
- Failing to install the full `wireguard` package and continuing with `wireguard-tools` only is intentional (container-like runners).
- Never put keys in the repository or print them to logs; callers pass them through GitHub Secrets.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/); branches follow [Conventional Branch](https://conventional-branch.github.io) short form (`feat/...`, `fix/...`).
- Do not commit to Renovate PRs.

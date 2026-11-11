# GitHub Copilot Instructions

Follow `AGENTS.md` at the repository root for project guidance. Review checklist for this composite action (all logic is Bash in `action.yml`):

## Security (highest priority)

- No hard-coded credentials; WireGuard/SSH keys and the host key come only from `inputs`.
- Secrets must not leak to logs (`echo`, command output, `sudo tee` without `> /dev/null`), and files holding them keep `chmod 600` (`/tmp/id_rsa`, `~/.ssh/config`, `/etc/wireguard/wg0.conf`).
- SSH host key verification stays enabled (no `StrictHostKeyChecking=no`, `known_hosts` entry from `ssh-host-key` kept).
- The `Cleanup` step keeps `if: always()`.

## Composite action rules

- Every `run` step sets `shell: bash`; new inputs are kebab-case with consistent `required`/`default`.
- `${{ inputs.* }}` expanded into shell commands (`command`, `scp-source`, etc.) is a command-injection risk: the expression is substituted before Bash parses the script, so quoting does not neutralize it. Prefer passing values through `env:` and referencing shell variables in new code.
- `if:` conditions on `operation` / `scp-direction` stay consistent with the inputs.
- Changes to `inputs` must also update `README.md` and `README-ja.md`.

## Known patterns, do not flag

- Continuing with `wireguard-tools` only when the full `wireguard` package fails to install is intentional.
- Status emojis in step output are accepted style.

## Language

Write review comments in English. Deliverables are English; `README-ja.md` is the only intentionally Japanese file (translation of `README.md`).

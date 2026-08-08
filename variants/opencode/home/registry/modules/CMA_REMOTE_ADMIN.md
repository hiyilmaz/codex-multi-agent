# CMA Remote Administration Module

## Load When

Load for SSH, root access, deployments, remote services, systemd, PM2, remote
backups, migrations, or live runtime verification.

## Do Not Load When

Do not load for local-only work or when remote access is outside scope.

## Rules

- Start with `ssh -G <alias>` and verify user, host, port, exact path, and
  service unit.
- Keep discovery read-only until mutation is explicitly approved.
- Preserve dirty remote state with a recoverable backup; never reset or clean
  unrelated work.
- Use fixed binaries, canonical paths, clean environments, bounded arguments,
  stdin isolation, and negative tests for privileged wrappers.
- Treat source state, pushed Git state, deployed artifact identity, service
  health, and route health as separate checks.
- Bind and verify the exact database before any migration.
- Redact credentials and stop when authority must expand beyond approval.

# Evidence: EXP-20260810-002 Active Repository Tool Router

Date: 2026-08-10
Status: Passed

## Claims

- The rollback directory has mode `0700`.
- The completion marker reports 35,557 recoverable paths.
- The payload contains no socket or FIFO object.
- Active `AGENTS.md` is byte-identical to its approved repository source.
- Active `CMA_REPO_TOOLS.md` is byte-identical to its approved repository source.
- The activation fixture passed both partial-publication rollback cases.
- The activation fixture rejected target drift without overwriting it.
- The focused CMA lazy-runtime suite passed 26 tests.
- The full repository suite passed 157 tests.
- The independent code review passed.
- The independent security review passed.

## Initial RED Evidence

Before activation, `cmp -s ~/.codex/AGENTS.md GLOBAL_AGENTS_TEMPLATE.md`
returned exit `1`, and the active module existence check returned exit `1`.
The active policy differed only by the approved router row.

The first disposable copy attempt exposed a socket error and FIFO hang in
direct `ditto`. The process was stopped. Real rsync and bsdtar staging attempts
were rejected because macOS metadata parity was insufficient; neither received
a completion marker, and both remain private for audit.

## Backup Verification

Rollback point:
`/Users/iyilmaz/CodexBackups/20260810T023951Z-cma-repo-tools-active-rollback`

- Directory mode: `0700`.
- Copy method: recoverable-path BOM filtered `ditto --clone`.
- Recoverable paths captured: 35,557.
- Payload: 25,789 regular files, 9,650 directories, 118 symlinks.
- Excluded special objects: one live IPC socket before and after copying; no
  socket or FIFO exists in the payload.
- Live final drift scan: 33 private lines, retained as volatile evidence.
- Payload mtree SHA-256:
  `367447c95e98658f7f8ae7ad3ed06149bae412d7d89a11a9bb5b59fb6d240c45`.
- Bound manifest-index SHA-256:
  `67c4be90834885673f34e9272f2795a8b90dbe4c673c6467ba7c1aeabf353dd5`.
- Payload mtree self-check and post-rename self-check returned exit `0`.

Verbatim proof excerpts:

```text
$ stat -f 'mode=%Lp' /Users/iyilmaz/CodexBackups/20260810T023951Z-cma-repo-tools-active-rollback
mode=700
```

```text
$ grep '^recoverable_paths=' BACKUP_COMPLETE
recoverable_paths=35557
```

```text
$ find payload -type s -o -type p | wc -l
0
```

The live socket/FIFO types, changing files, creation times, and protected
`com.apple.provenance` values are not represented as restorable point-in-time
state. macOS reassigns provenance at the copy location. All such limitations
are explicit in the private metadata and completion marker.

## Final Verification Evidence

The active policy was derived from its exact preimage by inserting the approved
row once. The module was published first with atomic no-overwrite semantics;
the policy was published last after a second preimage check.

Active SHA-256 values:

- `AGENTS.md`:
  `682c40cbe51b026c7d23f00e9c64b48cf141e9d564563552a9fda7c2178e540a`
- `CMA_REPO_TOOLS.md`:
  `38e464dcf4c5be473afe48ee0b27fe5dda5355311bf07ac7a365d05c7fdce214`

Both active files are regular files owned by `iyilmaz:staff`, mode `0644`, and
byte-identical to their approved repository sources. No staging temp remains.

```text
$ cmp -s ~/.codex/AGENTS.md GLOBAL_AGENTS_TEMPLATE.md; echo $?
0
```

```text
$ cmp -s ~/.codex/registry/modules/CMA_REPO_TOOLS.md variants/codex/home/registry/modules/CMA_REPO_TOOLS.md; echo $?
0
```

```text
$ /usr/bin/python3 -I -S -B tools/sync_tool.py fixture --repo /Users/iyilmaz/WebStorm/Codex-Multi-Agent --active-agents payload/AGENTS.md
fixture: module-publication rollback passed
fixture: policy-publication rollback passed
fixture: target-drift rejection passed
fixture: positive postimage passed
```

The fixture contains separate assertions for failure after module publication,
failure after policy publication, and injected target drift. The latter must
leave the drifted policy bytes untouched.

Validation results:

- Atomic sync fixture: passed.
- Focused CMA lazy-runtime suite: 26 tests, `OK`.
- Full repository suite: 157 tests, `OK`.
- Independent code review: `PASS`.
- Independent security review: `PASS`.

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_cma_lazy_runtime.py'
Ran 26 tests in 0.565s
OK
```

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
Ran 157 tests in 31.093s
OK
```

```text
Code review: PASS — Manifest hash, executable fixture command, and verbatim
26/157 test evidence match the verified current state.
```

```text
Security review: PASS — no blocking security findings.
```

No route or repository tool was executed. Runtime behavior and cost remain a
future usage observation, not a success claim in this activation task.

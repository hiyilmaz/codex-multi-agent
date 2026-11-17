# Improvement Experiments Archive

[Back to active experiments](EXPERIMENTS.md)

## EXP-20260827-004 - ESXi Native Tools Media Alias Validation

Date: 2026-08-27
Status: ACCEPTED

Problem:
The first native VMware Tools mount succeeded on `ALM-OFF-DC01`, but the
fail-closed validator rejected the ESXi-reported backing
`[] /usr/lib/vmware/isoimages/windows.iso` because it expected a ProductLocker
path literal.

Evidence:
`vim-cmd vmsvc/tools.install 6` returned success, the VM remained Powered On
with an unchanged boot time, the Evaluation ISO disappeared from its device
backing, and the CD/DVD became connected to the ESXi system ISO path. The
validator then stopped before touching `ALM-LAB-DC01`.

Hypothesis:
On this ESXi 8.0 U2 host, `/usr/lib/vmware/isoimages/windows.iso` is the native
alias for the same VMware Tools media stored under ProductLocker. Verifying
path resolution and content identity will allow the validator to recognize the
native backing without weakening it to arbitrary ISO paths.

Solution Attempt:
Resolve the ESXi-reported system ISO and ProductLocker paths read-only, compare
their file identity or SHA-256, then accept only that exact verified native
alias for the completed first-VM check and the second native mount.

Test:
Require either equal file identity plus canonical path resolution or equal
SHA-256 values for the ESXi system ISO and ProductLocker Windows Tools ISO.
Then require unchanged target hardware/network and normalized Lab integrity
before performing the same native Tools mount on VMID 7. Verify both final
CD/DVD backings match the exact verified native path and no Evaluation ISO
remains attached.

Success Criteria:
- The ESXi system ISO is proven identical to the ProductLocker Windows Tools
  ISO by canonical resolution and inode identity; the ProductLocker hash is
  captured while the file is readable.
- Both DC VMs remain Powered On without a boot-time change.
- Both CD/DVD devices are connected only to the verified native Tools media.
- Disk, CPU, RAM, NIC, snapshot, isolation, and normalized Lab fields remain
  unchanged.

Result:
The ESXi system path and ProductLocker path both reported inode `16779972`, and
the system alias resolved directly to the ProductLocker datastore object. A
second hash read was unavailable while the ISO was mounted because ESXi
returned `Device or resource busy`; the pre-mount ProductLocker SHA-256 remains
`532a3edf4faccdc93355c9810385c320d152ce8cf5ebed35a8bd45c4ce90029b`.
The revised exact-alias validator then accepted VMID 6 without retrying its
native mount, and VMID 7 completed the same native operation successfully.
Both VMs remained Powered On with unchanged boot times, reported
`toolsInstallerMounted=true`, and connected only to
`[] /usr/lib/vmware/isoimages/windows.iso`. The Evaluation ISO remained on the
datastore but was absent from both devices. CPU, RAM, thin disks, single-NIC
port-group mappings, snapshots, and normalized Lab integrity were unchanged.
Independent code review passed and security review reported no security impact.

Decision:
ACCEPT

Notes:
No retry is permitted on VMID 6; its actual state is read back instead. The
experiment does not authorize guest operations, VMX edits, reboot, shutdown,
network changes, or ISO file changes. The validator revision accepts only the
exact same-inode canonical ESXi alias, not arbitrary ISO paths.

## EXP-20260827-003 - ESXi HW21 PCI Root Bridge Repair

Date: 2026-08-27
Status: ACCEPTED

Problem:
Both new Windows Server HW21/UEFI VM shells fail Power On because ESXi cannot
allocate a PCIe slot for `scsi0`.

Evidence:
Both target VMX files omit the secondary PCI root-bridge topology, expose only
generic bus-slot data for SCSI and NIC devices, and log `No PCIe slot available
for SCSI0`, PCI SCSI allocation failure, and `DevicePowerOn` failure. A healthy
read-only HW21/UEFI reference on the same host contains the standard
`pciBridge0` and `pciBridge1` root-bridge structure.

Hypothesis:
Adding only the verified `pciBridge0/1` root-bridge structure and removing the
three failed-attempt slot values will let ESXi assign native, collision-free
PCI slots without changing either VM's disk, controller, NIC, or network.

Solution Attempt:
After a normalized Lab integrity gate and per-VM hash-verified VMX backups, add
the six verified bridge fields, remove only `scsi0.pciSlotNumber`,
`ethernet0.pciSlotNumber`, and `sata0.pciSlotNumber`, reload each powered-off
VM, and allow ESXi to assign supported slots during controlled Power On.

Test:
Require an exact allowlisted VMX diff, then test one target VM at a time. Verify
successful Power On, actual Powered On state, no new DevicePowerOn/PCI/SCSI
error in the test log window, valid device slot assignments, preserved disk and
single-NIC network mappings, successful Power Off, and unchanged normalized
Lab integrity before proceeding to the second VM.

Success Criteria:
- Each backup matches its pre-fix VMX hash and is protected with mode `0600`.
- Only the approved bridge and failed-slot fields change before Power On.
- Both VM hardware-start tests complete without DevicePowerOn, PCI, or SCSI
  configuration errors.
- Both targets finish Powered Off with their original disk and network mapping.
- The normalized Lab integrity signature remains unchanged throughout.

Result:
Both VMX backups matched their pre-fix SHA-256 values and were stored as
`root:root` mode `0600`. Exact pre-power diffs contained only the six verified
root-bridge additions and removal of the three failed-attempt slot values.
Separate Power On tasks returned success and each VM reached Powered On; the
fresh rotated `vmware.log` window for each test contained no DevicePowerOn,
PCI allocation, or SCSI configuration error. ESXi assigned `scsi0=32`,
`ethernet0=33`, and `sata0=34`, then both Power Off tasks succeeded and the VMs
finished Powered Off. The 100 GiB thin LSI SAS disks, single VMXNET3 mappings,
empty CD backing, and normalized Lab signature remained unchanged. Independent
code review passed and security review reported no security impact.

Decision:
ACCEPT

Notes:
Scope is limited to the two new DC VMX files. Production VMs, VMDKs, network
configuration, ISO media, guest installation, routing, NAT, and bridging are
excluded.

## EXP-20260827-002 - ESXi Large Datastore Capacity Gate

Date: 2026-08-27
Status: ACCEPTED

Problem:
The Phase 2 fail-closed precondition rejected a datastore with approximately
2.53 TB free before any VM write occurred.

Evidence:
The read-only pre-check reported `2532764024832` free bytes, while the remote
BusyBox integer `test` comparison against `322122547200` returned false. The
mutation script stopped at `final-preconditions`; both target VM names and
datastore paths were absent before the attempt.

Hypothesis:
ESXi BusyBox integer comparison overflowed or cannot reliably represent these
large byte values; an `awk` numeric comparison will evaluate the same captured
values correctly without weakening the 300 GiB safety threshold.

Solution Attempt:
Change only the datastore capacity predicate from shell integer `test` to an
`awk` numeric comparison. Keep the threshold, all other fail-closed gates, VM
specifications, and Lab integrity checks unchanged.

Test:
Reconfirm both target names and paths are absent, print the live free-byte
value, prove the 300 GiB predicate with `awk`, then rerun the unchanged Phase 2
workflow with normalized Lab checks before and after every write.

Success Criteria:
- The live free-byte value is at least 322122547200 according to `awk`.
- No pre-existing or partial target VM object is adopted or overwritten.
- Both requested VM shells pass independent hardware and isolation read-back.
- The normalized Lab baseline remains identical throughout the workflow.

Result:
The live value `2532764024832` passed the unchanged 300 GiB threshold when
evaluated with `awk`. Both target names and paths were still absent before the
retry. The workflow then created `ALM-OFF-DC01` and `ALM-LAB-DC01` as Powered
Off Windows Server 2022 x64 VM shells. Independent read-back confirmed 2 vCPU,
8192 MB RAM, UEFI, one LSI SAS controller, one 100 GiB thin disk, one VMXNET3
NIC on the assigned single port group, and no CD-ROM, ISO, or snapshot. The
normalized Lab pre/post SHA-256 remained
`35983b18a32e5f91586efee0f6728f802db2d8cdb750918834fa0f2512a42b83`.
Code review passed and security review reported no security impact.

Decision:
ACCEPT

Notes:
The first attempt made no remote write, so no rollback or cleanup was required.
Later validation false negatives for the empty snapshot representation and
case-sensitive API field names stopped fail-closed and were corrected from
read-only host evidence without destructive cleanup.

## EXP-20260827-001 - ESXi Lab Integrity Normalization

Date: 2026-08-27
Status: ACCEPTED

Problem:
The first Office vSwitch attempt stopped after a raw Lab signature comparison
reported a difference even though the printed critical Lab configuration fields
were unchanged.

Evidence:
The attempt created only an empty `vSwitch-OFFICE`, stopped before uplink and
port-group changes, proved zero consumers, removed that run-owned switch, and
reverified `vmnic0`, `vSwitch0`, `vmk0`, and the four Shimadzu VM network
mappings. Code and security review found no Lab impact.

Hypothesis:
Comparing only normalized, sorted, persistent configuration fields will reject
real Lab changes without treating ordering, counters, object IDs, timestamps,
or other runtime metadata as configuration drift.

Solution Attempt:
Create a normalized baseline for the approved critical fields, apply only
`vmnic1 -> vSwitch-OFFICE -> PG-OFFICE` with VLAN 0 and no VMkernel, then run
the same normalized comparison after every write and at final verification.

Test:
Require pre-change target absence, `vmnic0` and `vmnic1` link gates, normalized
Lab baseline stability, exact Office topology read-back, no Office VMkernel or
VM consumer, and deterministic Office-only rollback on any real Lab mismatch.

Success Criteria:
- Critical Lab fields compare identically before and after every write.
- `vSwitch-OFFICE` has MTU 1500 and only `vmnic1` as uplink.
- `PG-OFFICE` exists only on that switch with VLAN ID 0.
- No VMkernel or VM is attached to the Office topology.
- `DEFERRED-NET-001` remains open for the accepted 100 Mbps link.
- Independent code and security reviews find no blocking issue.

Result:
The normalized pre-change and post-change Lab snapshots matched exactly for
every approved critical field. Live read-back confirmed `vSwitch-OFFICE` with
MTU 1500 and only `vmnic1`, plus `PG-OFFICE` with VLAN ID 0 and zero active
clients. No Office VMkernel or VM consumer exists. All four Shimadzu VMs
remained powered on with their original `VM Network` mappings, and the
independent post-check found no new Lab network log event. Independent code
review passed and security review reported no security impact. The signed
reference captures are retained on `VM_DATASTORE/ADMIN-BACKUP` with SHA-256
digests `56331e2408dbb59ab5beb41e4eb6262ebac33715b4372ae0514b9a7ab90e5ae2`
and `75767a39537110d4ad8d09dc5a7f465457caee4b91fc905475ddbad0238df5f4`.

Decision:
ACCEPT

Notes:
The experiment does not authorize VM, guest, ISO, routing, NAT, bridge, Lab
network, or physical-link changes.

## EXP-20260821-001 - Context7 General Setup And Node 22 Preflight

Date: 2026-08-21
Status: ACCEPTED

Problem:
The CMA general setup does not run Context7's official multi-agent setup flow,
and mutating setup entry points do not fail closed when Node.js is older than
the required major version 22.

Evidence:
The current `bin/codex-setup` completes without invoking `npx ctx7 setup`, and
neither it nor `bin/codex-user-install` validates Node.js or `npx` before
runtime mutations. A real Context7 setup configured MCP, rules, and skills for
Claude Code, OpenCode, and Codex under the process user's global home.

Hypothesis:
An early Node.js 22 and `npx` preflight on mutating entry points, followed by an
explicit default-yes `npx ctx7 setup` step at the end of the general wizard,
will provide the requested multi-agent Context7 setup without leaking
credentials or reporting false completion.

Solution Attempt:
Add equivalent fail-closed runtime preflights to `codex-setup` and
`codex-user-install`, preserve read-only help and variant listing without the
preflight, and let the Context7 CLI exclusively own its interactive
authentication and global configuration flow.

Test:
Capture RED and GREEN with real setup scripts and hermetic fake `node` and
`npx` executables. Cover missing, malformed, too-old, boundary, and newer Node
versions; missing `npx`; exact unpinned Context7 argv; explicit skip; exact
failure propagation; secret-free argv/output; custom runtime HOME behavior;
focused regressions; shell syntax; diff checks; and the full repository suite.

Success Criteria:
- Node.js below 22, malformed versions, missing Node.js, and missing `npx` fail
  before runtime or network mutation.
- Node.js 22 and newer allow mutating setup flows to continue.
- Read-only help and variant listing remain available without Node.js or `npx`.
- The accepted Context7 step invokes exactly `npx ctx7 setup` once; an explicit
  rejection invokes nothing.
- Context7 failures preserve their exit status and suppress CMA completion.
- CMA never adds the Context7 API key or token value to argv or its own output.
- Focused and full regression suites pass without real network access.

Result:
The pre-change focused suite produced meaningful RED: Node.js below 22,
malformed versions, missing Node.js, and missing `npx` did not stop mutation;
`codex-setup --list-variants` was unavailable; no Context7 command or exit
propagation occurred; and the required documentation was absent. After the
implementation, the new focused suite passed 8/8, variant-install regressions
passed 31/31, codex-tools integration regressions passed 7/7, and shell syntax
validation passed. The first full regression passed 397/397. Code review then
found that a valid-looking Node version printed by a failing `node --version`
process was accepted because its exit status was swallowed. A dedicated RED
reproduced the false continuation. The revised preflight now treats that exit
status as terminal; the focused suite passes 9/9 and the full regression passes
398/398. Code re-review passed after the fix. Security review passed with no blocking
finding and retained the explicitly accepted risks of unpinned remote `npx`
execution, user-controlled `PATH` resolution, and no transactional rollback for
third-party partial writes. ShellCheck was unavailable; Bash syntax validation
passed instead. The record archive regression passed 19/19, the focused suite
remained 9/9, and the post-archive check reported every managed record below
its compaction threshold.

Decision:
ACCEPT

Notes:
The Context7 command remains interactive and unpinned by explicit user request.
It targets the process user's global agent locations even when CMA uses a
custom runtime home. CMA does not install Node.js or modify shell profiles.

## EXP-20260818-001 - Cross-Platform Atomic Rename

Date: 2026-08-18
Status: ACCEPTED

Problem:
The native Codex activator uses Darwin-only `renameatx_np`, so its fail-closed
atomic publication path is unavailable on Linux and blocks CMA activation.

Evidence:
On blockmanpro Ubuntu 24.04 x86_64, libc exposes `renameat2` but not
`renameatx_np`; the full repository suite ran 385 tests with 13 failures and
5 errors rooted in `atomic_rename_unavailable`.

Hypothesis:
Dispatching the existing exclusive-publish and atomic-exchange semantics to
Darwin `renameatx_np` or Linux `renameat2`, with platform-specific flags, will
restore Linux activation without weakening no-overwrite, descriptor anchoring,
rollback, or cleanup guarantees.

Solution Attempt:
Introduce an explicit semantic-to-platform syscall adapter: Darwin uses
`RENAME_EXCL=4` and `RENAME_SWAP=2`; Linux uses `RENAME_NOREPLACE=1` and
`RENAME_EXCHANGE=2`. Unsupported platforms, symbols, semantics, or kernel and
filesystem support remain fail-closed without a plain rename fallback.

Test:
Capture RED for Linux symbol and flag dispatch before implementation; then run
platform/errno/fallback unit tests, real-host atomic publish/no-overwrite tests,
the focused native-activation suite, Python compilation, whitespace checks,
and the full repository suite. Re-run the focused and full suites on
blockmanpro after separately approved deployment.

Success Criteria:
- Darwin and Linux select their correct libc symbol and exact flags.
- Both source and target remain anchored to the supplied directory FD.
- Existing targets are never overwritten and staging files are cleaned.
- Missing or unsupported atomic operations fail closed without fallback.
- Race, rollback, cleanup, and idempotency regressions remain green.
- The Ubuntu focused and 385-test full suites pass without skips.

Result:
The pre-change focused suite produced the required RED with exit 1: Linux
dispatch attempted no `renameat2` call and raised `atomic_rename_unavailable`;
unsupported syscall and semantic cases also failed. The platform adapter then
passed all 23 focused native-activation tests. Python compilation and
`git diff --check` passed, the full repository suite passed 389/389, and
focused branch coverage for the activator measured 82 percent. Darwin real-host
publication remained idempotent, preserved descriptor anchoring, rejected an
existing target, and left no hidden staging artifact. Commit `85e0412` was then
pushed to both the working branch and `main` and fast-forwarded into the clean
blockmanpro repository. On Ubuntu 24.04 x86_64, the real `renameat2` focused
suite passed 23/23 and the full repository suite passed 389/389, both with exit
0. Independent code and security reviews found no blocking issue.

Decision:
ACCEPT

## EXP-20260828-001 - AD DS Functional Level Enum Compatibility

Date: 2026-08-28
Status: ACCEPTED

Problem:
The first `Install-ADDSForest` invocation stopped before requesting the DSRM
password because the Windows Server 2022 ADDSDeployment module rejected
`Win2016` as a `ForestMode` value.

Evidence:
The live PowerShell parameter-binding error listed the accepted enum values as
`Win2008`, `Win2008R2`, `Win2012`, `Win2012R2`, `WinThreshold`, and `Default`.
No forest or domain was created, and no DSRM credential was entered.

Hypothesis:
On this Windows Server 2022 build, `WinThreshold` is the module's enum name for
the Windows Server 2016 forest and domain functional level requested by the
approved design.

Solution Attempt:
Change only `ForestMode` and `DomainMode` from `Win2016` to `WinThreshold` in
the otherwise unchanged `Install-ADDSForest` invocation.

Test:
Require the revised command to accept both functional-level parameters and
reach the interactive DSRM password prompt without creating a forest first.
After user-controlled credential entry and promotion, verify the resulting
forest and domain modes report Windows Server 2016.

Success Criteria:
- The revised invocation reaches the DSRM password prompt without a parameter
  binding error.
- The user alone enters and confirms the DSRM password and approves promotion.
- Post-promotion `Get-ADForest` and `Get-ADDomain` report Windows Server 2016
  functional levels.
- No Lab or Shimadzu critical field changes.

Result:
The revised invocation accepted `WinThreshold`, reached the interactive DSRM
credential prompts, and completed promotion after the user alone entered and
confirmed the secret. Post-promotion inspection reported
`Windows2016Forest` and `Windows2016Domain`; the writable DC is a Global
Catalog with AD DS, DNS, Netlogon, KDC, and DFSR running. SYSVOL and NETLOGON
are shared, the domain and `_msdcs` zones and required SRV records are
present, and the single-DC `dcdiag` and `repadmin` checks found no blocking
error. The DNS client now uses only `192.168.1.10`. Normalized ESXi and
Shimadzu critical fields remained unchanged.

Decision:
ACCEPT

Notes:
This experiment changes only the ADDSDeployment functional-level enum spelling;
it does not authorize changes to IP, routing, firewall, ALM-LAB-DC01, or any
Lab/Shimadzu system.

## EXP-20260817-009 - Blockmanpro Fix Commit Deployment

Date: 2026-08-17
Status: ACCEPTED

Problem:
Blockmanpro still reports the Go-installed scanners as missing after a Git pull
and runs the old repair semantics.

Evidence:
The server repository and installed UV package have identical source hashes,
but both are at main commit `85ca147` while the accepted codex-tools fix is at
descendant commit `b45ddc7` on `origin/agent/cma-project-defaults`. The real
scanner binaries exist under `/root/go/bin` with executable modes.

Hypothesis:
Fast-forwarding the clean server main branch to the accepted fix commit and
reinstalling the user-scoped UV package from that exact repository will make
the existing Go tools healthy without changing Codex config or credentials.

Solution Attempt:
Capture exact Git, package, config-hash, and permission pre-state; fast-forward
only to `b45ddc7`; take a private UV-tool backup; force-reinstall the package
from the repository; and run standalone install in MCP `verify-only` mode.

Test:
Compare repository and installed source hashes, execute the real scanner
version commands, compare config hash and metadata before and after, and require
JSON to distinguish `AUTH_REQUIRED` from genuine failures while continuing all
selected CLI tools.

Success Criteria:
- The server repository and installed package both identify the accepted fix.
- `osv-scanner` and `betterleaks` execute and report `HEALTHY` without profile edits.
- All selected CLI tools are healthy; credential-gated MCP tools remain typed `AUTH_REQUIRED` when unavailable.
- Codex config hash and credentials metadata remain unchanged in verify-only mode.
- Any incomplete selected tool keeps the overall exit status nonzero without a false success claim.

Result:
The clean server main branch fast-forwarded from `85ca147` to the accepted
`b45ddc7` fix, and the user-scoped UV package was rebuilt from that exact
repository after an owner-only backup. Repository and installed `cli.py`
hashes match. The real `osv-scanner` 2.5.0 and Betterleaks version commands
execute, and both `check` and non-interactive MCP `verify-only` install report
nine tools `HEALTHY`, two credential-gated MCP tools `AUTH_REQUIRED`, zero
generic failures, and exact config preservation. Install exits 1 as required
while selected credential-gated tools remain incomplete. Config hash, inode,
mode, and mtime plus credential-file metadata remained unchanged; the server
repository is clean at the expected commit. Independent code review found no
behavioral or deployment defect. Security review then found that manage-mode
rollback captured its pre-state before credential resolution, allowing a user
edit made during the prompt to be overwritten after a later verification
failure. A meaningful RED reproduced the overwrite. The revised implementation
now carries the updater's actual original bytes in its transaction result; the
new regression and all 72 package tests pass with 85 percent branch coverage,
and the 385-test repository suite remains green. Final re-reviews and live
deployment of this revision are pending. The first live manage-mode run then
repaired Context7 but exposed a second input-boundary defect: a stored GitHub
credential containing a control character reached subprocess environment
construction and produced a generic config failure. An isolated transaction
confirmed a `ValueError` cause without printing the value. New unit and E2E
RED tests require invalid environment, secure-store, and prompt values to be
rejected before subprocess use and reported as typed `AUTH_REQUIRED` in
non-interactive mode. Review then extended the same boundary to configured MCP
discovery and verification and rejected Unicode whitespace/control/format
bypasses by requiring printable ASCII token values. Meaningful CLI and unit
RED tests covered stored NUL, environment NUL, NEL, NBSP, line separator, and
bidi override inputs. The revised credential boundary passes all 75 package
tests with 85 percent branch coverage and the 385-test repository suite;
independent code and security re-reviews pass. Final live deployment remained
pending at that point. The final `65309d6` revision was then fast-forwarded to
the clean server repository and rebuilt into the user-scoped UV environment
from the exact source. Repository and installed credential-module hashes
match. A live normal non-interactive install reports ten functionally healthy
tools, zero generic failures, and only the corrupted stored GitHub value as typed
`AUTH_REQUIRED`; Context7 passes functional verification. The expected exit 1
truthfully reflects that one incomplete selected tool. Config hash, inode,
mode, and mtime and credential-file inode, mode, and mtime remained unchanged
during the final run. The real scanner version commands still pass, and the
server repository is clean at `65309d6`.

Decision:
ACCEPT

## EXP-20260817-008 - Transactional MCP Credentials

Date: 2026-08-17
Status: ACCEPTED

Problem:
Standalone MCP installation can persist a prompted credential before config
and functional verification succeed, and empty credentials become `FAILED`.

Evidence:
The blockmanpro run left a private credential file after GitHub failed, while
Context7 was reported as `FAILED` instead of `AUTH_REQUIRED`.

Hypothesis:
Deferring credential persistence until config and functional verification
succeed, with per-tool config rollback and typed outcomes, will prevent partial
state while allowing later independent tools to continue.

Solution Attempt:
Add a per-tool pending transaction that commits the prompted credential only
after verification and restores that tool's config pre-state on failure.

Test:
Capture RED for deferred persistence, exact rollback, typed `AUTH_REQUIRED`,
continued execution, idempotency, and secret-free output.

Success Criteria:
- Failed MCP setup leaves config bytes and credential storage unchanged.
- Successful setup commits config and prompted credential once.
- `AUTH_REQUIRED` remains distinct from `FAILED`; later tools still run.
- Secrets never appear in output, status details, config, or backups.

Result:
Prompted credentials now remain in memory until config and read-only functional
verification pass. Failed MCP setup restores only that tool's owned config
state, preserves earlier successful MCP changes, cleans the process credential
even when rollback is refused, and reports missing credentials as the typed
`AUTH_REQUIRED` outcome. Rollback verifies expected bytes and inode first, so
a concurrent user edit is preserved. Secret-bearing success, functional
failure, store failure, concurrent edit, empty prompt, later-tool continuation,
and idempotency regressions passed without exposing test secrets. Package tests
passed 71/71 with 85 percent branch coverage; the CMA adapter passed 7/7 and
the full repository passed 385/385. Independent code and security re-reviews
passed.

Decision:
ACCEPT

## EXP-20260817-007 - Truthful Config Preservation

Date: 2026-08-17
Status: ACCEPTED

Problem:
`config_preserved` currently mirrors config validity rather than whether the
config bytes changed.

Evidence:
The blockmanpro output claimed existing settings were preserved even though a
new DeepWiki MCP table was present after standalone installation.

Hypothesis:
Comparing the exact config pre-state and post-state will make preservation
reporting independent from TOML validity and reject false success.

Solution Attempt:
Capture config bytes before lifecycle execution and pass their exact equality
to the summary renderer.

Test:
Require `preserved=true` for byte-identical and exact rollback cases, and
`preserved=false` for valid but changed config.

Success Criteria:
- Validity and preservation are independently reported.
- Whitespace or comment-only byte changes count as changed.
- A successful exact rollback reports preserved.

Result:
The lifecycle now compares exact config bytes captured before and after the
selected operation. Validity and preservation are reported independently:
the first managed DeepWiki write reports changed, an idempotent repeat reports
preserved, and an exact rollback reports preserved. Non-regular or unreadable
capture fails closed with structured evidence instead of crashing. Package
tests passed 71/71 with 85 percent branch coverage; the CMA adapter passed 7/7
and the full repository passed 385/385. Independent code and security
re-reviews passed.

Decision:
ACCEPT

## EXP-20260817-006 - Installed Binary Rediscovery

Date: 2026-08-17
Status: ACCEPTED

Problem:
Go tools can install successfully into `GOBIN` or `GOPATH/bin` but be reported
as failed when that directory is absent from the invoking shell's `PATH`.

Evidence:
On blockmanpro both Go binaries existed under `/root/go/bin` and became healthy
when that directory was added only to the check process environment.

Hypothesis:
Resolving managed user bin directories inside the installer process will make
same-run verification accurate without editing shell profiles.

Solution Attempt:
Use a scoped effective environment for install, discovery, and verification,
including explicit `GOBIN` or the first `GOPATH/bin` plus the user-local bin.

Test:
Capture RED where a binary exists only outside the original PATH, then require
healthy discovery, nonzero-version failure handling, and no profile mutation.

Success Criteria:
- Successfully installed Go tools are healthy in the same lifecycle run.
- Missing or broken binaries remain missing or broken.
- Caller environment and shell profile files remain unchanged.

Result:
The installer now appends the user-local bin directory and active absolute
`GOBIN` or first `GOPATH/bin` to a process-only effective PATH while preserving
the caller's command precedence. It refreshes that environment after installing
Go as a missing dependency, so both preinstalled-Go and fresh-host scenarios
rediscover and verify `osv-scanner` in the same run. Relative Go paths are
ignored and no caller environment or shell profile is written. Package tests
passed 71/71 with 85 percent branch coverage; the CMA adapter passed 7/7 and
the full repository passed 385/385. Independent code and security re-reviews
passed.

Decision:
ACCEPT

## EXP-20260817-005 - Turkish Dialogue And Simple Decisions

Date: 2026-08-17
Status: ACCEPTED

Problem:
Agents can answer the user in English, and `CRITICAL DECISION` blocks can be
too technical or difficult to choose between.

Evidence:
The user reported both behaviors directly and approved a bounded policy change.
The current policies say only `User dialogue: Turkish` and define English,
placeholder-heavy decision fields without an explicit simplicity contract.

Hypothesis:
An explicit always-Turkish user-dialogue rule plus a short Turkish six-line
decision template with two concrete options will make runtime communication
consistent and decisions easier to understand.

Solution Attempt:
Update the canonical Codex, Claude, and OpenCode policies and orchestration-gate
projections with one shared dialogue and decision-simplicity contract.

Test:
Add contract and portable-install tests before production edits. Require all
user-facing message classes to remain Turkish, reject language-switching and
verbose decision mutants, and preserve the six-line stop boundary.

Success Criteria:
- Every packaged runtime requires Turkish for all user-facing dialogue.
- The decision block uses short Turkish labels, exactly two options, and one
  short recommendation.
- Tests reject partial, English-only, and verbose replacement policies.
- Focused and full regressions pass without changing approval or safety scope.

Result:
The new contract failed against the old policies, then passed across all four
packaged runtime policies, all three orchestration-gate projections, and all
three portable installer variants. Focused orchestration, variant, Claude, and
OpenCode suites passed 80/80. The final full suite passed 382/382 in 93.173 seconds.
Active Codex, Claude, and OpenCode global policies match their packaged sources;
the active Codex and Claude orchestration gates also match their projections.

Decision:
ACCEPTED

Notes:
The user approved one bounded exception to append this record while the active
experiment file is over 800 lines. No other record maintenance is authorized.

## EXP-20260817-004 - Qualified Plugin Skill Disable Selectors

Date: 2026-08-17
Status: ACCEPTED

Problem:
The approved Vercel plugin disablement removed Vercel skills from a fresh
Codex prompt, but nine Build iOS Apps skills remained visible after unqualified
skill-name disable entries were added to the global configuration.

Evidence:
`codex debug prompt-input` returned all nine `build-ios-apps:*` qualified skill
names after the first configuration attempt, while no `vercel:*` skill remained.

Hypothesis:
Plugin-provided skills are matched by their model-visible qualified names, so
changing only the nine selectors from unqualified names to
`build-ios-apps:<skill>` will remove them without disabling unrelated skills or
changing the already-disabled XcodeBuildMCP server.

Solution Attempt:
Replace the nine unqualified `skills.config` names with their exact
`build-ios-apps:`-qualified names. Keep the Vercel plugin override and every
unrelated global configuration entry unchanged.

Test:
Run strict configuration validation, render a fresh model-visible prompt, and
search it for both `vercel:*` and `build-ios-apps:*` skill names.

Success Criteria:
- Strict configuration validation passes.
- A fresh prompt contains no Vercel skill names.
- A fresh prompt contains no Build iOS Apps skill names.
- Existing unrelated configuration and owner-only file mode remain unchanged.

Result:
Codex 0.147.0 strict configuration validation passed with 17 checks OK and no
warnings or failures. A fresh model-visible prompt contained zero `vercel:*`
skills and zero `build-ios-apps:*` skills. The global configuration retained
its owner-only `0600` mode, and the existing XcodeBuildMCP disable override
remained unchanged.

Decision:
ACCEPT

Notes:
The initial unqualified selectors were schema-valid but behaviorally
ineffective for plugin-qualified skills.

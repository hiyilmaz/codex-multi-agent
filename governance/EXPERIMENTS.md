# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

## EXP-20260831-001 - ALM-MILA01 Private Egress Isolation

Date: 2026-08-31
Status: ACCEPTED

Problem:
The first security review blocked closure because `ALM-MILA01` shares the
untagged `PG-OFFICE` Layer-2 segment with the Office domain controller and the
dual-homed management VM while its UFW outbound policy allows every
destination. A future externally driven Hermes compromise could therefore
initiate lateral connections to private infrastructure.

Evidence:
Live ESXi inventory maps `ALM-MILA01`, `ALM-OFF-DC01`, and one
`ALM-MGMT01` adapter to `PG-OFFICE`. Guest UFW is active with default incoming
deny and outgoing allow. The user approved private-egress isolation after the
mandatory security review returned `BLOCK`.

Hypothesis:
Allowing DNS to the Office gateway before denying new outbound traffic to
private, carrier-grade NAT, IPv4 link-local, local global-IPv6, and IPv6
link-local ranges will remove the direct lateral-movement path while preserving
established administrative SSH, DHCP, DNS, and public HTTPS.

Solution Attempt:
Back up the effective UFW user rules, add only the ordered gateway-DNS allows
and private/link-local destination denies, and leave ESXi networking and every
other VM unchanged.

Test:
Confirm a second key-only SSH connection, DNS and public HTTPS after applying
the rules. Prove blocked new connections to the Office DC with UFW output-rule
counters, reboot once, and repeat SSH, DNS, HTTPS, rule, and service checks.

Success Criteria:
- New private-network connections from `ALM-MILA01` are denied for IPv4 and
  the observed local IPv6 ranges.
- Existing and new authorized SSH management access remain functional.
- DHCP address, default route, gateway DNS, public HTTPS, UFW, and
  open-vm-tools remain healthy after one reboot.
- No ESXi switch, port group, uplink, vmkernel interface, or existing VM is
  changed.

Result:
The first UFW user-output attempt preserved a second authorized SSH session,
gateway DNS, and public HTTPS. A new IPv4 connection to the Office DC timed
out and the `192.168.0.0/16` DROP counter increased from zero to three packets.
The first local-prefix IPv6 echo test still succeeded because UFW's built-in
`ufw6-before-output` chain accepted echo requests before user-output rules.
The revised rule placement added exact private/local IPv6 drops after
established-connection handling and before generic ICMPv6 accepts. The same
local-prefix echo test then failed and its DROP counter reached one packet and
104 bytes. After a clean reboot, authorized SSH, DHCP `192.168.1.185/24`,
gateway DNS, public HTTPS, UFW, and open-vm-tools remained healthy; both IPv4
and IPv6 negative tests still failed with the same persistent DROP counters.

Decision:
ACCEPT

Notes:
The initial IPv6 mechanism was revised rather than accepted on partial
evidence. Root-only pre-change UFW backups remain available for recovery.
Hermes, Telegram, model-provider configuration, static addressing, DHCP
reservation, and ESXi autostart remain outside this experiment.

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

## EXP-20260811-007 - Native TDD Simplification Evaluation

Date: 2026-08-11
Status: NEED_MORE_DATA

Problem:
EXP-20260811-006 showed that static fixtures and token proxies cannot prove
whether a smaller TDD contract preserves real native-agent output quality or
reduces actual runtime cost across Codex, Claude, and OpenCode.

Evidence:
The Phase 10 candidate was rolled back after independent review found its
quality and tool-use evidence self-declared. All three native CLIs are locally
available, but their raw traces must first prove comparable input/output token,
tool-call, repository-read/search, core-skill, wall-clock, and final-output
measurement. The user approved exactly one bounded line-limit exception for
EXP-20260811-007 in the already over-800-line experiment log. This exception
applies only to this record and does not authorize editing, reordering,
refactoring, archiving, cleaning, or maintaining existing experiment records.

Hypothesis:
Running one fixed baseline and one fixed temporary Phase 10 candidate through
the real native TDD-agent mechanism on four identical bounded tasks can provide
trustworthy cost and behavior evidence without permanently modifying TDD,
runtime configuration, permissions, orchestration, or core skills.

Solution Attempt:
Freeze exactly four task inputs and two prompt contracts before scored runs.
Use ephemeral or isolated invocation inputs only, execute baseline and
candidate natively for Codex, Claude, and OpenCode, retain raw redacted traces
outside active runtime configuration, and score actual final TDD contracts with
one fixed rubric. Do not tune prompts after seeing results or implement the
candidate even if it passes.

Test:
First run a non-scored bounded preflight for each native runtime. Continue to
the 24 scored runs only if every runtime exposes trustworthy actual input and
output tokens, tool calls, repository reads/searches, core-skill invocations,
wall-clock, and final output without persistent runtime/config mutation. Use
the same four inputs for baseline and candidate. Compare acceptance mapping,
meaningful RED, positive, negative, boundary, regression, anti-hardcode, and
missing-information behavior. Require candidate quality to be component-wise
no weaker, repository discovery to decrease, tool calls and input tokens not to
increase, and semantic alignment across all variants.

Success Criteria:
- Baseline and candidate execute as real native TDD agents in all three
  variants with attributable raw measurements.
- The fixed four task inputs and fixed prompt contracts do not change after the
  first scored result.
- Candidate quality is not weaker for any task, dimension, or variant.
- Repository discovery decreases; tool calls and input tokens decrease or stay
  equal; no core skill, scanner, or external knowledge route is invoked.
- Active TDD, runtime configuration, permissions, orchestration, and core-skill
  files remain unchanged.
- If any native trace cannot support trustworthy measurement, stop before
  scored comparison and report `UNVERIFIED` with `success=false`.

Result:
Preflight stopped before any native model evaluation or scored run. The
installed Codex CLI (`codex-cli 0.147.0`) exposes no named-agent selector for
`codex exec`, so a direct native `tdd-guide` run and agent-attributable token
and tool measurements could not be established. OpenCode (`1.18.16`) exposes
`--agent`, but its plugin-free active runtime reported `Agent tdd-guide not
found`; creating or activating a temporary runtime agent definition would
change the evaluation surface prohibited by this phase. Claude exposes native
agent and stream-event options, but all three variants are required, so no
Claude model call was made in isolation. Consequently there are no real
baseline/candidate token, tool, discovery, wall-clock, or quality measurements.
The evaluation is `UNVERIFIED` with `success=false`.

Decision:
NEED_MORE_DATA

Notes:
The line-limit exception is exclusive to EXP-20260811-007. Experiment-log
maintenance remains a separately approved task. This phase evaluates only and
does not authorize permanent candidate installation or later work.

## EXP-20260806-003 - PTY Package Install Stdin Continuation

Date: 2026-08-06
Status: TESTING

Problem:
The approved apt installation completed, but the SSH PTY session returned to a
shell prompt without executing the remaining pinned Codex npm installation and
version-verification commands from the submitted stdin stream.

Evidence:
A separate read-only SSH check confirms `nodejs` 18.19.1 and `npm` 9.2.0 are
installed, no apt or dpkg process remains, and `codex` is still missing. The
original PTY session remains open at a root shell prompt after `needrestart`.

Hypothesis:
The interactive apt/needrestart path consumed or interrupted the remaining
heredoc stdin. Sending the bounded remaining commands directly to the already
open PTY session will complete the approved package step without rerunning apt.

Solution Attempt:
Write only the exact pinned npm install and version/path verification commands
to the existing SSH session, followed by `exit`. Do not rerun apt, open another
package source, or restart services.

Test:
Require the existing session to exit zero, then use a fresh read-only SSH
connection to verify the installed package version, executable path, and
`codex --version` output.

Success Criteria:
- Apt is not invoked again.
- `@openai/codex@0.146.1` is installed through npm's verified global prefix.
- `codex --version` reports the pinned release.
- The original SSH session exits successfully.
- No service or host restart is performed.

Result:
The tool rejected the write with `stdin is closed for this session`; no npm
command was delivered and Codex remained uninstalled. The open-session
continuation mechanism is therefore unavailable even though the remote shell
had previously displayed a prompt.

Decision:
REVISE

Notes:
This experiment addresses only stdin continuation after the already completed
approved package transaction.

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

## EXP-20260828-002 - RDP Keyboard-Safe PowerShell Command Delivery

Date: 2026-08-28
Status: NEED_MORE_DATA

Problem:
The Windows App RDP keyboard path converted uppercase Base64 characters to
lowercase, corrupting a read-only PowerShell EncodedCommand before execution.

Evidence:
The remote console displayed the encoded payload in lowercase and PowerShell
returned CommandNotFoundException. No requested Windows Time configuration was
applied.

Hypothesis:
Short commands containing only lowercase letters, digits, spaces, hyphens,
slashes, and periods will pass through the current keyboard mapping unchanged
and can safely collect pre-check evidence. Configuration requiring punctuation
will remain blocked until its exact input can be independently verified.

Solution Attempt:
Run only short, lowercase, read-only native commands one at a time. Do not
apply the NTP configuration until both Google stripchart tests pass and a
keyboard-safe exact configuration command is available.

Test:
Compare each visible command with the intended text and review its live output.
Reject the method on any character mutation or ambiguous execution result.

Success Criteria:
- PDC, service, profile, DNS, share, and current time evidence is captured.
- Both Google NTP peers return three stripchart samples.
- No configuration mutation occurs during method validation.
- The no-touch scope for ALM-LAB-DC01, ALM-MGMT01, Shimadzu, and networking is
  preserved.

Result:
Short lowercase native commands passed visual command comparison and captured
the PDC role, AD service, DomainAuthenticated profile, IPv4 DNS, SYSVOL,
NETLOGON, Windows Time, DCDIAG, and DFSR evidence without configuration
mutation. Shifted punctuation remained unreliable: colon input became a
semicolon and the screen-keyboard coordinate path was unavailable. Independent
live evidence showed the requested target state was already active: both
Google peers were Active, Type was NTP, the configured peer list contained
`time1.google.com,0x8 time2.google.com,0x8`, and the synchronized source moved
from time1 to time2 with current Stratum 2 status. The requested NTP
configuration was therefore not rewritten.

Decision:
NEED_MORE_DATA

Notes:
This experiment authorizes no network, firewall, DNS, AD promotion, or Lab
change.

## EXP-20260828-003 - Test VM DHCP Interface Matching

Date: 2026-08-28
Status: ACCEPTED

Problem:
The two temporary Ubuntu cloud-image test VMs power on with VMware Tools and
their single VMXNET3 NICs connected to the correct port groups, but neither VM
obtains a DHCP lease or reports an IPv4 address.

Evidence:
VMIDs 9 and 10 are Powered On with `guestToolsRunning`, no ESXi VM question,
and exactly one connected NIC each. Their generated MAC addresses are
`00:0c:29:bc:a3:79` on `PG-OFFICE` and `00:0c:29:e6:e6:ec` on `VM Network`.
Repeated guest-info and ALM-MGMT01 neighbor-table checks show no IPv4 address
or ARP entry for either MAC.

Hypothesis:
The released cloud image's baked network configuration does not match the
VMware interface name. Supplying a NoCloud `network-config` that matches each
generated MAC and requests only DHCPv4 will create normal single-interface
clients without adding static routes or using ALM-MGMT01 as a gateway.

Solution Attempt:
Power off only VMIDs 9 and 10, replace only their temporary `CIDATA` seed ISOs
with MAC-bound DHCPv4 network configuration and new instance IDs, then power
them on again. Do not change production VMs, port groups, gateways, or
ALM-MGMT01.

Test:
Require each VM to report one IPv4 address, one DHCP-derived subnet/default
gateway/DNS set, and no extra NIC or static cross-subnet route. Verify SSH using
the existing ephemeral key before running isolation probes.

Success Criteria:
- TEST-OFFICE01 receives a normal Office DHCP lease on `PG-OFFICE`.
- TEST-LAB01 receives a normal Lab DHCP lease on `VM Network`.
- Each VM retains exactly one NIC and no manually added route.
- Protected VM hashes, power state, port groups, vSwitches, uplinks, and vmk0
  remain unchanged.

Result:
The MAC-bound DHCP configuration succeeded for TEST-OFFICE01, which received
`192.168.1.177`. TEST-LAB01 emitted three DHCP requests during a controlled
boot capture on `ens224`, but no DHCP offer was observed and no lease was
assigned. This distinguished an absent Lab DHCP service from an interface
matching failure. After three conflict-free ARP probes, the revised Lab seed
assigned `192.168.50.31/24` with the normal `192.168.50.1` gateway and DNS.
Both VMs reported exactly one `ens192` NIC. Office routed Lab destinations
through `192.168.1.1`; Lab routed Office destinations through
`192.168.50.1`; neither used ALM-MGMT01 or a manual cross-subnet route.

From TEST-OFFICE01, ICMP to `192.168.50.10` and `192.168.50.100` failed, and
TCP 3389, 443, and 22 probes were blocked. From TEST-LAB01, ICMP to
`192.168.1.10` and `192.168.1.1` failed, and TCP 3389, 80, and 443 probes were
blocked. The same services remained reachable from the MacBook over the two
approved Tailscale routes. Both test VMs then completed normal shutdown,
contained no snapshots, were unregistered, and their two exact datastore
directories were removed. Protected VM power states and VMX hashes, port
groups, vSwitch/uplink mappings, vmk0, and ALM-MGMT01 remained unchanged.

Decision:
ACCEPT

Notes:
This experiment is limited to the two named temporary test VM seed ISOs and
their power cycles.

Acceptance boundary:
The approved test instructions prohibited manual cross-subnet routes and
prohibited using ALM-MGMT01 as either test client's gateway. The behavioral
result therefore proves normal-client/default-gateway isolation. It does not
claim a forced behavioral traversal of ALM-MGMT01; that host's Office/Lab DROP
enforcement is supported separately by the live priority `-10` nftables rules,
absence of bridge/inter-subnet NAT, and reviewed Tailscale hook ordering.

Revision 1:
Use `192.168.50.31/24` with the established normal Lab gateway
`192.168.50.1` and DNS `192.168.50.1` only on TEST-LAB01. Three ARP duplicate
address probes from `ens224` returned no conflict. Keep TEST-OFFICE01 on its
DHCP lease and do not add any cross-subnet route or use ALM-MGMT01 as a
gateway. Success requires SSH access to both test VMs and exact route/DNS
inspection before negative service probes.

## EXP-20260828-004 - Windows Activation Rollback Watchdog Delivery

Date: 2026-08-28
Status: ACCEPTED

Problem:
The first manually delivered multi-line PowerShell block did not create the
required Windows rollback watchdog. The user reported that it did not work,
but the PowerShell error buffer contained no retained error details.

Evidence:
Read-only checks confirmed that the rollback directory, rollback script,
scheduled task, temporary firewall rule, and temporary IPv4 gateway are all
absent. No network or firewall state changed.

Hypothesis:
The long pasted block failed during command delivery or parsing before its
first mutation. Splitting the watchdog into short, independently verified
PowerShell steps will avoid clipboard and parser ambiguity while preserving
the same exact rollback scope.

Solution Attempt:
Deliver one short step at a time: create and ACL the rollback directory, write
the exact rollback script, register the SYSTEM scheduled task, and verify each
artifact before any firewall, route, NAT, or egress change.

Test:
Each step must return its real object state. The final pre-egress gate requires
the secured directory, script hash, armed task deadline, absent temporary
firewall rule, and absent temporary IPv4 gateway.

Success Criteria:
- The rollback directory grants full control only to SYSTEM and Administrators.
- The rollback script targets only the named activation firewall rule and the
  ActiveStore default route via `192.168.50.30` on interface index 13.
- The SYSTEM task is armed before any network change.
- No temporary firewall, route, NAT, or egress state exists during setup.

Result:
The split delivery succeeded: the secured directory, three-line rollback
script, and SYSTEM/Highest scheduled task were created and verified before any
network change. The first live rollback exposed a second issue: querying the
dynamic Windows Firewall rule without `-PolicyStore ActiveStore` did not find
the rule, and the pipeline-based route removal did not remove the exact
ActiveStore route. Linux filter/NAT rollback succeeded immediately. Direct,
fully qualified `Remove-NetRoute` and `Remove-NetFirewallRule` commands against
`ActiveStore` then removed both Windows objects, with explicit absence checks.

Decision:
ACCEPT

Notes:
The activation scope remains limited to ALM-LAB-DC01 and ALM-MGMT01. The
Windows IPv6 binding and AD/DNS configuration remain unchanged.

Revision 1:
Keep the split delivery, but replace the rollback script with direct removal
commands that specify `-PolicyStore ActiveStore` and every exact route/rule
selector. Re-arm and verify the task before any second egress attempt. The
first egress window was rolled back without activation after the generic
`www.microsoft.com` curl probe timed out; router counters nevertheless showed
exact-source HTTP/HTTPS accepts, masquerade, and established return traffic.
The next connectivity gate must probe Microsoft activation endpoints directly
instead of treating the generic homepage as the activation service.

Final Reconciliation:
Live key-safe checks supersede the earlier activation-incomplete/Notification
snapshot. `ALM-LAB-DC01` reports ServerStandard, Retail channel, license status
Licensed, and permanent activation. It remains in WORKGROUP with no AD DS or
DNS role installed, no temporary IPv4 default route, its original DNS servers,
and IPv6 binding enabled. `ALM-OFF-DC01` reports ServerStandard, Retail channel,
and permanent activation; it is the running Global Catalog and DNS domain
controller for `ad.almilafarma.com`.

Cleanup Result:
The exact activation-only Linux filter/NAT rules, rollback service/timer and
runtime script were removed after their ownership and targets were verified.
The exact Windows `ALM-ACTIVATION-ROLLBACK` task and its single hash-verified
rollback file/directory were removed; the activation ActiveStore gateway and
Windows Firewall rule were already absent. A local activation-only temporary
workspace was also removed. Post-checks found no activation-specific runtime
objects. Permanent Tailscale routes and firewall rules were unchanged, both
physical transit directions remain explicitly dropped, MacBook service probes
to Office and Lab passed through the Tailscale tunnel, and protected ESXi VMX,
power, vSwitch/uplink, and vmk0 baselines matched. `LAB-IPV6-EGRESS-001` remains
OPEN; no IPv6 remediation or AD deployment change was performed.

## EXP-20260830-001 - Idempotent AD OU Absence Detection

Date: 2026-08-30
Status: ACCEPTED

Problem:
The Phase 8A identity-foundation PowerShell block stopped on the first missing
OU because `Get-ADOrganizationalUnit -Identity` raised
`ADIdentityNotFoundException` while the session used
`$ErrorActionPreference = "Stop"`.

Evidence:
The user captured `Directory object not found` for
`OU=Users,DC=ad,DC=almilafarma,DC=com` at the lookup line. Execution stopped
before `New-ADOrganizationalUnit`, so no Phase 8A object was created.

Hypothesis:
Handling the missing-object lookup with an explicit `try/catch` will preserve
fail-closed behavior for unexpected AD errors while allowing an absent target
OU to be created idempotently.

Solution Attempt:
Change only the `Ensure-OU` lookup mechanism to catch
`ADIdentityNotFoundException`; preserve the approved OU, group, user,
credential, membership, and standard-user checks.

Test:
Run the approved root-Employees revision on ALM-OFF-DC01 and require explicit
creation output for four OUs and four groups, followed by verified user
membership and `PHASE8A=PASS`.

Success Criteria:
- Missing OUs are created without swallowing unrelated AD errors.
- Existing OUs and groups are not duplicated or moved.
- The first user is enabled, standard, and belongs to exactly the two approved
  rollout groups plus normal default memberships.
- No local account, endpoint, or network setting changes.

Result:
The collision-aware root-Employees revision created `OU=Employees`, the
Workstations/Office/Lab OU tree, and all four approved Global Security groups.
It created `dogukan.ozuguc` as an enabled standard domain user under
`OU=Employees` and verified both approved group memberships. The block ended
with `PHASE8A=PASS`; the built-in `CN=Users` container remained unchanged.

Decision:
ACCEPT

Notes:
Preserve the built-in `CN=Users` container. Select either a root
`OU=Employees` layout or a differently named parent OU before the next
attempt. Both attempts failed before mutation; no rollback was required.

Revision 1:
The user approved root `OU=Employees`. The next attempt uses a collision-aware
one-level object lookup, creates only `OU=Employees`, `OU=Workstations`,
`OU=Office`, and `OU=Lab`, and stores the four approved security groups in
`OU=Employees`. The built-in `CN=Users` container remains unchanged.

# Changelog

[Older entries](CHANGELOG_ARCHIVE.md)

## Archive Index (Previous 30 Dates)

- [2026-07-27](CHANGELOG_ARCHIVE.md#2026-07-27)
- [2026-07-26](CHANGELOG_ARCHIVE.md#2026-07-26)
- [2026-07-16](CHANGELOG_ARCHIVE.md#2026-07-16)
- [2026-07-14](CHANGELOG_ARCHIVE.md#2026-07-14)
- [2026-06-26](CHANGELOG_ARCHIVE.md#2026-06-26)
- [2026-06-24](CHANGELOG_ARCHIVE.md#2026-06-24)
- [2026-06-11](CHANGELOG_ARCHIVE.md#2026-06-11)
- [2026-06-10](CHANGELOG_ARCHIVE.md#2026-06-10)
- [2026-05-22](CHANGELOG_ARCHIVE.md#2026-05-22)

## 2026-11-18

- [FEAT] EXP-20261118-002 added separate CLI, MCP, and project context results
  to `cma-tools check`, including JSON output. Native Codex setup now runs the
  read-only check by default and reports its result after setup actions.
  Package installation and official Context7 setup require explicit selection.

- [FIX] EXP-20261118-001 aligned the DeepWiki manifest with the live
  `ask_wiki_question` tool name and surfaced read-only MCP verification
  failures in `cma-tools check`. The Serena skill and its tracked projections
  now require active project path verification before the first symbol query
  and report activation failures. A live query located `ektrun`'s `businessDate`.

- [OPS] Completed only approved cleanup items 3, 5, 6, and 7 on `robonets1`:
  Docker build cache, the inactive Codex daemon release
  `0.168.0-x86_64-unknown-linux-musl`, archived journal files in the two
  validated machine-ID directories, and `/root/.npm/_cacache` contents.
  Revalidated exact paths, inactive process references, and the active
  `current` release symlink before removal. Reclaimed 3,173,748,736 bytes;
  available space rose from 733,724,672 to 3,907,473,408 bytes, with disk
  utilization falling from 99% to 90%. Docker build cache is now zero.
  All 29 Docker image references, container states, monitored service PIDs,
  and 20 protected path identities remained unchanged. Preserved the active
  Codex 0.169.0 release, browser installations, application databases, backups,
  volumes, and unarchived journals. No services were restarted; no other
  numbered candidates were cleaned.

- [OPS] Cleared the six explicitly approved cache targets on `robonets1`:
  Hermes uv and pnpm stores, the user uv and pip caches, the Codex remote
  plugin catalog, and APT package archives. Verified no active process
  references and no runtime symlinks in the inspected installation trees
  before cleanup. Preserved cache root directories and confirmed all six
  targets were empty afterward, apart from APT's empty lock and partial
  directory. Used space decreased by 653,209,600 bytes; available space rose
  from 16,523,264 to 669,732,864 bytes, with utilization still at 99%.
  `apt-get clean` emptied the archives but exited 100 on the lists lock held
  by a pre-existing, nearly five-day-old `apt-get update`; that process and
  its locks were left untouched. Five Hermes gateways remained running and
  `wg-easy` remained healthy. No services were restarted. Docker build cache,
  browser installations, application data, and other candidates were not
  cleaned.

## 2026-11-12

- [OPS] Completed the separately approved six-category log cleanup on
  `grpvctr-s1`: truncated five exact log files in place and vacuumed archived
  journals with native journalctl commands. Reclaimed 8,974,336,000 bytes;
  disk utilization fell from 71% to 61%, with 33.17 GiB available. Preserved
  container states, six service PIDs, file inodes, and active journals; no
  services were restarted and no persistent logging settings were changed.
  Updated the existing disk cleanup report with the new results and limits.

- [OPS] Completed the explicitly approved disk cleanup on `grpvctr-s1`
  (`2.27.101.231:11166`): removed four exact temporary test copies and cleared
  Docker build, npm content, VS Code VSIX, and APT package caches. Used space
  decreased by 21,206,855,680 bytes; disk utilization fell from 94% to 71%.
  The same eight container IDs remained running. Preserved application data,
  database volumes, rollback images, backups, and active logs. Saved the
  remaining-candidate inventory and verification in
  `docs/reports/2026-11-12-grpvctr-s1-disk-cleanup.md` and its HTML version.

## 2026-10-06

- [FEATURE] Added the native Grok Build CMA variant to catalog-driven setup,
  portable installation, project initialization, and schema-2 upgrades. The
  variant projects eight native Markdown roles, four workflow skills, ten core
  skill instructions, modules, registry records, and a GROK_HOME launcher.
  Native activation preflights managed paths, rejects conflicts and force,
  preserves existing settings/identity/instructions, creates private recovery
  manifests, and rolls back unchanged files owned by a failed attempt.
  Grok project configs use restricted sections and sensitive diffs are redacted.
  Discovery validation and independent reviews are tracked by
  `EXP-20261006-001`. Focused tests passed 29/29; the full suite ran 435 tests
  with 434 passes and one existing skip. Activator coverage reached 89%, both
  mandatory reviews passed, and native discovery verified the expected CMA
  sources on Grok 0.2.39. Existing 3,745 files/links and 1,470 directory modes
  were preserved; repeated activation created no files. No model/provider
  defaults or credentials were changed; no model request was made.

## 2026-08-31

- [OPS] Provisioned `ALM-MILA01` on the Almila ESXi host with 4 vCPU,
  8 GiB RAM, EFI, one 100 GiB thin PVSCSI disk, and one VMXNET3 NIC on
  `PG-OFFICE`. The Ubuntu 26.04 Server source ISO matched Canonical's
  published SHA-256 value before a task-owned autoinstall copy was created.
  The guest completed installation, rebooted from disk with both installation
  media disconnected, and reported hostname `alm-mila01`, Ubuntu 26.04,
  DHCP address `192.168.1.185/24`, working DNS/HTTPS, active UFW and
  open-vm-tools, and key-only SSH for `milaadmin`. Existing VM inventory,
  VM power states, port groups, vSwitches, uplinks, and vmkernel networking
  remained unchanged except for the newly registered VM. `EXP-20260831-001`
  added persistent private/link-local IPv4 and local IPv6 egress isolation
  after the first security review identified the shared Office Layer-2 risk.
  A second SSH session, gateway DNS, and public HTTPS survived rule activation
  and a clean reboot, while Office-DC IPv4 and local-prefix IPv6 negative
  probes incremented the intended DROP counters. Hermes, Telegram,
  model-provider configuration, ESXi autostart, static addressing, and DHCP
  reservation were intentionally not configured.

## 2026-08-28

- [SECURITY] Added a transactional, persistent ALM-MGMT01 nftables exception
  for stateful AD/DC traffic only between `192.168.1.10/32` and
  `192.168.50.10/32`. The rules precede the existing physical-subnet DROP
  rules and allow only the approved DNS, Kerberos, NTP, RPC, LDAP, SMB,
  password-change, Global Catalog, dynamic RPC, and limited ICMPv4 traffic.
  Syntax and active ordering passed; the two broad Office/Lab DROP rules and
  Tailscale forwarding rules remain active, IPv4/IPv6 NAT hashes did not
  change, and both DC RDP endpoints remain reachable locally from the
  management VM. The pre-change configuration is retained under root-only
  backup, and the upstream physical Layer-2 overlap is tracked separately as
  `DEFERRED-NET-L2-001` without blocking the approved AD rollout.

- [SECURITY] Applied the scoped `SEC-NET-IPv6-001` host control on
  `ALM-LAB-DC01`: a persistent, all-profile outbound Windows Firewall block
  for global-unicast IPv6 destination range `2000::/3`. Before the change,
  ICMPv6 to Google DNS succeeded; afterward both ICMPv6 and TCP/443 tests to
  public IPv6 targets failed. IPv4 `192.168.50.10/24`, absence of an IPv4
  default route, Lab reachability, RDP, the IPv6 binding, and link-local IPv6
  remained intact. PersistentStore and ActiveStore read-back, a SHA-256
  verified firewall export, and independent configuration/security reviews
  passed. Upstream VLAN 50 IPv6 isolation and NAT64/transition-path coverage
  remain open under `DF-20260828-0000-001` pending the dedicated physical
  stateful firewall/router.

- [SECURITY] Reconciled both Windows Server activation and AD states from live,
  key-safe evidence and completed the approved activation-helper cleanup.
  `ALM-OFF-DC01` is ServerStandard Retail, permanently activated, and is the
  running Global Catalog/DNS DC for `ad.almilafarma.com`; `ALM-LAB-DC01` is
  ServerStandard Retail, permanently activated, remains a standalone WORKGROUP
  server, and has neither AD DS nor DNS installed. Any earlier snapshot that
  reported `ALM-LAB-DC01` as Notification or activation-incomplete is
  superseded by the live 2026-08-28 reconciliation. Exact activation-only
  nftables filter/NAT objects, rollback units, runtime script, Windows
  scheduled task, rollback directory, ActiveStore gateway, Windows Firewall
  rule, and local temporary workspace are absent after cleanup. The permanent
  Tailscale/Office-Lab guard remained unchanged; MacBook routes and real SSH,
  RDP, and HTTPS probes passed through the Tailscale tunnel. Protected VM power
  states, VMX hashes, vSwitch/uplink mappings, and `vmk0` matched baseline.
  `LAB-IPV6-EGRESS-001` remains OPEN and is now tracked as
  `DF-20260828-0000-001`; no IPv6 or AD configuration was changed.

- [SECURITY] EXP-20260828-003 completed normal-client/default-gateway
  bidirectional physical-subnet isolation validation with two temporary,
  single-NIC Ubuntu 26.04 cloud-image VMs.
  TEST-OFFICE01 received DHCP `192.168.1.177/24`, gateway/DNS
  `192.168.1.1`; TEST-LAB01 used conflict-checked `192.168.50.31/24` because
  packet capture proved the Lab network had no DHCP offer, with its normal
  gateway/DNS `192.168.50.1`. Neither client used ALM-MGMT01 or a manual
  cross-subnet route. Office-to-Lab RDP/HTTPS/SSH and Lab-to-Office
  RDP/HTTP/HTTPS probes were blocked, while MacBook Tailscale probes to both
  networks remained successful. Per the approved test constraint, no manual
  route used ALM-MGMT01 as a gateway; these probes validate normal network-path
  isolation, while ALM-MGMT01's explicit physical-interface DROP rules and
  earlier hook-order review remain configuration evidence rather than a forced
  transit behavior test. Both VMs shut down normally, had no snapshots, were
  unregistered, and their exact datastore directories and local ephemeral
  key/image workspace were removed. User-supplied ZTE screenshots show DMZ off
  and no active port-forward entry. Protected VM power/VMX hashes, network
  backings, vSwitch/uplink mappings, vmk0, and ALM-MGMT01 remained unchanged.

- [SECURITY] Prepared `ALM-MGMT01` for interactive Tailscale authentication.
  A persistent native nftables forward guard was installed before enabling
  IPv4 forwarding: Office-to-Lab and Lab-to-Office transit are explicitly
  dropped, only `tailscale0`-initiated forwarding to the two physical networks
  is allowed, return traffic is stateful, and all other forwarding fails
  closed. IPv6 forwarding remains disabled and no bridge or physical-subnet
  NAT was added. Tailscale 1.102.3 was installed from its official Ubuntu
  26.04 `resolute` repository; `tailscaled` is active and requires the
  nftables service at startup. User-interactive authentication completed and
  the node now advertises exactly `192.168.1.0/24` and `192.168.50.0/24` with
  default subnet-router SNAT retained. Control-plane approval is active: the
  MacBook receives both routes as peer `AllowedIPs`/`PrimaryRoutes` and installs
  both `/24` networks on its Tailscale tunnel. Office service probes from that
  client reached ZTE HTTPS, ALM-OFF-DC01 RDP, and ALM-MGMT01 SSH through the
  tunnel, with nftables counters confirming Tailscale ingress and stateful
  replies. After the MacBook physical Lab interface was removed, Lab probes
  were repeated with both route checks pinned to the Tailscale tunnel. Both
  Lab servers, ESXi HTTPS/SSH, WIN-SRV2022 RDP, and ACQ01-03 RDP passed; the
  `tailscale0` to Lab counter increased by 30 packets and the stateful Lab
  reply counter by 20 packets during the test. Tailscale SSH and exit-node
  operation remain disabled. User-supplied ZTE configuration screenshots show
  DMZ disabled and no active port-forward entry; only the empty new-entry form
  is visible, with no observed WAN-to-LAN forwarding rule. Normal Office/Lab
  client negative transit tests remain unverified because no suitable
  non-production client is currently attached to either physical subnet.

- [OPS] Completed the post-install static network preparation for
  `ALM-MGMT01`. MAC-bound netplan configuration assigns
  `192.168.1.30/24` with the sole default route and Office DNS through
  `192.168.1.1`, plus `192.168.50.30/24` on the Lab NIC with no gateway,
  DNS, DHCP, or IPv6 router acceptance. Duplicate-address probes were clean
  before both assignments. A normal guest shutdown allowed the Lab NIC's
  connect-at-power-on setting to be enabled, and reboot verification confirmed
  both addresses, SSH, open-vm-tools, Office internet/DNS, ZTE web, both DC RDP
  ports, and ESXi web/SSH access. IPv4 forwarding remained disabled; no bridge,
  NAT, firewall rule, or Tailscale package was introduced. Protected VM power
  states and VMX hashes, vSwitch/uplink topology, port groups, and `vmk0`
  remained unchanged; credentials were consumed only in process memory and
  were not recorded.

- [OPS] Prepared `ALM-MGMT01` for a manual clean Ubuntu installation after
  confirming that it was stalled at the UEFI `No Media` screen with no guest
  OS running. A controlled power-off was followed by exactly two persistent
  connection changes: the Lab NIC now remains disconnected at power-on and
  the verified Ubuntu Server ISO connects at power-on. The Office NIC remains
  connected to `PG-OFFICE`; the 30 GiB thin VMDK, PVSCSI controller/unit,
  backing UUID, inode, size, and descriptor hash were preserved. The VM was
  powered on, UEFI handed off to the SATA CD-ROM, and the Ubuntu live installer
  reported a running guest with VMware Tools. Protected VM power states and
  VMX hashes, both vSwitch/uplink chains, port groups, and `vmk0` were unchanged.

- [SECURITY] EXP-20260828-001 promoted `ALM-OFF-DC01` as the first writable
  Global Catalog and DNS server for the new `ad.almilafarma.com` forest with
  NetBIOS name `ALMILA` and Windows Server 2016 forest/domain functional
  levels. The DSRM secret was entered only by the user, the NIC DNS client was
  restricted to `192.168.1.10`, and AD DS/DNS services, SYSVOL/NETLOGON,
  integrated DNS zones and SRV records, `dcdiag`, and expected single-DC
  `repadmin` state were verified. `ALM-LAB-DC01`, ESXi Lab networking, and all
  Shimadzu VM power/network mappings remained unchanged. Firewall rule scope
  and DNS root-hints/recursion egress remain deferred read-only validation
  items; no firewall, routing, NAT, bridge, or second-DC change was made.

- [OPS] Created the Powered Off `ALM-MGMT01` Ubuntu 26.04 LTS VM shell on
  `VM_DATASTORE` with 2 vCPU, 2 GB RAM, UEFI, one 30 GiB thin PVSCSI disk,
  and exactly two VMXNET3 NICs mapped to `PG-OFFICE` and `VM Network`. The
  attached Ubuntu Server ISO matched Canonical's signed SHA-256 manifest.
  Protected VM power states, VMX hashes, NIC backings, port groups, vSwitches,
  vmkernel networking, and uplinks remained unchanged. Guest installation,
  IP assignment, firewall, forwarding, Tailscale authentication, route
  advertisement, and end-to-end validation remain pending user console work.

## 2026-08-27

- [OPS] EXP-20260827-004 detached `SERVER_EVAL_x64FRE_en-us.iso` from the two
  powered-on DC VM CD/DVD devices and mounted the ESXi-native Windows VMware
  Tools media with `vim-cmd vmsvc/tools.install`. The ESXi system backing was
  proven to be the same ProductLocker object by canonical resolution and inode
  identity; the pre-mount Tools ISO SHA-256 was retained. Both VMs stayed
  Powered On with unchanged boot times, original CPU/RAM/thin disks/single-NIC
  port groups, and no snapshots. The Evaluation ISO file was not modified or
  deleted, normalized Lab integrity remained unchanged, and independent code
  and security reviews passed. Guest-side Tools installation remains manual.

- [FIX] EXP-20260827-003 repaired the missing HW21 PCI root-bridge topology in
  `ALM-OFF-DC01` and `ALM-LAB-DC01`. Hash-verified `root:root` mode `0600`
  VMX backups were retained, and the minimal pre-power diff added only the
  verified `pciBridge0/1` structure while removing three invalid failed-attempt
  slot values. Separate controlled Power On tests succeeded without new
  DevicePowerOn, PCI, or SCSI errors; ESXi assigned collision-free native slots
  and both VMs were returned to Powered Off. Their 100 GiB thin LSI SAS disks,
  single VMXNET3 network mappings, empty CD backing, and the normalized Lab
  integrity signature remained unchanged. Independent code and security
  reviews passed.

- [SECURITY] Removed the prohibited `SERVER_EVAL_x64FRE_en-us.iso` backing
  that had been manually attached to both Powered Off DC VM shells. The CD/DVD
  devices remain present as empty client-backed AHCI devices with
  connect-at-power-on enabled; no production ISO was attached. Two full ISO
  SHA-256 reads matched, both target VM backups were restricted to `root:root`
  with mode `0600`, the normalized Lab hash remained unchanged, and independent code and
  security reviews passed. Production Windows Server 2022 media remains
  blocked pending positive boot, WIM, edition, architecture, and non-Evaluation
  verification.

- [OPS] Prepared `ALM-OFF-DC01` and `ALM-LAB-DC01` for manual installation by
  adding one empty client-backed AHCI CD/DVD device to each Powered Off VM with
  connect-at-power-on enabled. No ISO, boot-order change, power-on, guest
  configuration, or network change was performed. The available Windows
  Server Evaluation ISO was explicitly excluded; independent device read-back,
  normalized Lab comparison, code review, and security review passed. A
  licensed non-Evaluation Windows Server 2022 x64 ISO remains pending.

- [OPS] EXP-20260827-002 created the Powered Off `ALM-OFF-DC01` and
  `ALM-LAB-DC01` Windows Server 2022 x64 VM shells on `VM_DATASTORE`. Each VM
  has 2 vCPU, 8 GB RAM, UEFI, one LSI SAS controller, one 100 GiB thin disk,
  and one VMXNET3 NIC on its isolated assigned port group. No ISO, CD-ROM,
  snapshot, power-on, VMkernel, routing, NAT, bridge, or shared uplink was
  introduced. Independent post-check, normalized Lab comparison, code review,
  and security review passed. The 100 Mbps Office uplink remains tracked as
  `DEFERRED-NET-001`.

- [OPS] EXP-20260827-001 created the isolated ESXi Office topology
  `vmnic1 -> vSwitch-OFFICE -> PG-OFFICE` with MTU 1500 and VLAN ID 0.
  Normalized pre/post comparisons and an independent live read-back confirmed
  that the Lab uplink, `vSwitch0`, port groups, `vmk0`, and all four Shimadzu
  VM network mappings remained unchanged. No Office VMkernel, VM consumer,
  bridge, routing, NAT, or shared uplink was created. Independent code and
  security reviews passed; `DEFERRED-NET-001` remains open for the accepted
  100 Mbps Full link speed.

## 2026-08-24

- [FEAT] Added `bin/cma-tool-check`, a portable read-only Codex host inventory
  command. It verifies Node.js 22+, records executable paths and versions for
  common runtime tools, checks `codex mcp list` when Codex is available, marks
  optional missing tools truthfully, and returns a nonzero status for required
  Node/Codex/MCP or version failures. Focused fake-PATH regression coverage,
  shell syntax validation, a local smoke run, and independent code/security
  reviews were completed.

## 2026-08-21

- [FEAT] EXP-20260821-001 added a Node.js 22 and `npx` fail-closed preflight
  to mutating CMA user-global setup entry points while keeping help and variant
  discovery read-only. The general wizard now offers the exact interactive
  `npx ctx7 setup` flow with a default answer of yes, propagates Context7
  failures without a false completion message, and leaves authentication to
  Context7 without putting API keys in command arguments. Focused tests passed
  9/9, the full suite passed 398/398, shell syntax and diff checks passed, and
  independent code and security reviews passed. The unpinned remote package,
  process `PATH`, and third-party partial-write risks remain explicitly
  documented; ShellCheck was unavailable.

## 2026-08-18

- [FIX] EXP-20260818-001 added fail-closed Linux `renameat2` support to the
  native Codex activator while preserving Darwin `renameatx_np`, directory-FD
  anchoring, exclusive no-overwrite publication, atomic exchange rollback, and
  staging cleanup. The focused suite passed 23/23 on both Darwin and Ubuntu,
  the full suite passed 389/389 on both platforms, activator branch coverage
  measured 82%, and independent code/security reviews passed.
- [FIX] EXP-20260817-009 deployed the resumable codex-tools fixes to
  blockmanpro through clean fast-forward commits and exact repo-sourced UV
  rebuilds. Go-installed scanners are now discovered without profile edits;
  Context7 passes live functional verification; rollback uses the updater's
  actual config pre-state; and malformed stored/environment/prompt credentials
  are rejected as typed `AUTH_REQUIRED` before subprocess use. The final normal
  install reports ten healthy tools, zero generic failures, and only the
  corrupted GitHub credential as incomplete with truthful exit 1. Package tests
  passed 75/75 with 85% branch coverage, the full suite passed 385/385, and
  independent code/security re-reviews passed.

## 2026-08-17

- [FIX] Standalone `codex-tools install` now rediscovers user-local and Go
  binaries through a process-scoped PATH, refreshes that PATH after installing
  Go as a dependency, preserves caller command precedence, and does not edit
  shell profiles. MCP tools continue independently: prompted credentials are
  persisted only after config and read-only functional verification succeed,
  failed tools roll back only their owned config when byte/inode ownership is
  unchanged, concurrent user edits are preserved, and `AUTH_REQUIRED` remains
  distinct from generic failure. Config preservation now reflects exact byte
  equality instead of validity. The CMA adapter remains MCP `verify-only`.
  Package tests passed 71/71 with 85% branch coverage, adapter tests passed 7/7,
  full regressions passed 385/385, and independent code/security reviews passed.
- [FIX] Project Configuration filling now prefers explicit or detected backend
  facts, falls back to `Python / FastAPI / PostgreSQL / Redis` without asking,
  and always records `docs/CHANGELOG.md` and `docs/reports/`. Project-name and
  other genuinely unresolved non-defaulted questions remain available.
- [CHORE] Aligned the CMA package and Codex, Claude, and OpenCode global policy
  versions at `2.7` after the approved global dialogue-policy change. The
  project template and all schema-2 project manifests remain at `2.2` because
  no project-template content changed.
- [FEAT] EXP-20260817-005 now requires all Codex, Claude, and OpenCode
  user-facing dialogue to remain Turkish, including questions, progress,
  errors, approvals, and final reports. `CRITICAL DECISION` keeps its six-line
  safety boundary while using short Turkish labels, exactly two concrete
  options, and one concise recommendation.
- [CHORE] EXP-20260817-004 disabled the Vercel plugin and all nine Build iOS
  Apps skills in the active user-global Codex configuration. Qualified plugin
  skill selectors were required; strict config validation passed and a fresh
  model-visible prompt contained neither Vercel nor Build iOS Apps skills.
- [FIX] Multi-variant project init now generates the required private snapshot
  and controlled merge prompt for an existing `CLAUDE.md` regardless of the
  Claude variant's position in the selected catalog order. Descriptor-pinned
  state and source hashing distinguishes unchanged managed bridges from
  user-customized Claude instructions without a TOCTOU suppression gate.
- [TEST] Added a legacy `AGENTS.md`-only multi-variant init regression that
  verifies instruction hash and mode preservation, private content-addressed
  snapshots, path-only merge prompts, schema-2 ownership, and repeat-run
  idempotency before live CMA project adoption.
- [FEAT] EXP-20260817-003 added an evaluation-scoped Evidence-First
  Objectivity contract to the Codex, Claude, and OpenCode global policies.
  Material conclusions now prioritize verifiable independent evidence,
  counterevidence, epistemic distinctions, conflicts, risks, and uncertainty
  over user agreement, without imposing research on routine tasks.
- [FEAT] EXP-20260817-002 user-global and project setup now preserve existing Markdown
  instructions, create owner-only content-addressed snapshots, and generate
  path-only AI prompts that propose a reviewed diff instead of merging files.
  Native Claude no longer appends `@registry/CMA_GLOBAL.md` automatically;
  native OpenCode and portable installs use the same controlled merge flow.
  Descriptor-pinned no-follow I/O, encoded metadata, untrusted-document rules,
  and collision-safe prompt names prevent redirection, injection, and overwrite
  of user-owned prompt content.
- [FIX] `bin/cma-tools check` and `dry-run` now execute the bundled Python
  package instead of a potentially stale `codex-tools` executable from
  `PATH`; install still executes UV's newly published entry point. Added a
  dedicated CMA tools usage and troubleshooting guide. Adapter tests passed
  7/7, package tests passed 56/56, full CMA regressions passed 358/358, and
  live read-only `check` / `dry-run` both completed successfully.
- [FEAT] EXP-20260817-001 added the independent Python 3.11+
  `codex-tool-installer` package and opt-in `bin/cma-tools` / setup integration.
  CMA keeps MCP ownership through enforced verify-only mode; standalone mode
  manages only missing or installer-marker-owned MCP tables. Config and release
  paths fail closed on unsafe symlinks, direct releases are version/checksum
  pinned, package sources use immutable versions or commits, and the adapter
  executes only UV's newly installed entry point. Package tests passed 56/56
  with 80% branch coverage, full CMA regressions passed 355/355, isolated UV
  install/uninstall passed, and independent code/security reviews passed.

## 2026-08-16

- [FEAT] EXP-20260816-001 interactive setup and project init now ask whether all active catalog
  variants should be applied. Yes applies every variant without follow-up
  selection prompts; no asks each variant individually. Explicit `--variant`
  calls remain single-variant compatible, and batched project init preserves
  additive ownership and records one ordered schema-2 variant set. Setup now
  validates each runtime registry and writes its generated files through a
  no-follow atomic path, preventing symlinked registry redirection.

## 2026-08-15

- [FEAT] EXP-20260815-003 replaced per-task transition pauses with one approved
  ordered main plan across Codex, Claude, and OpenCode policy 2.5. Disclosed
  phases, Low/Medium non-destructive work, and planned orchestration now run
  continuously; plan deviations, destructive work, and High/Critical decisions
  remain separately gated. Public guides, active global policies, private
  rollback material, clause-removal/contradiction tests, 343/343 full tests,
  code review, and security review all passed.
- [FEAT] Added the official Claude project projection to the CMA repository:
  `CLAUDE.md`, `.claude/settings.json`, and the schema-2 manifest now declare
  the ordered `codex`, `claude`, and `opencode` variants. Existing Codex and
  OpenCode project files were preserved; the operation is idempotent and its
  pre-change manifest is retained in an owner-only archive.
- [FEAT] Added the approved user-global MCP parity helper for Codex, Claude,
  and OpenCode. It gates exact supported CLI versions and required environment
  references, applies the four managed identities (`serena`, `deepwiki`,
  `github`, `context7`) with native schemas, removes `xcodebuildmcp` from
  Claude/OpenCode, preserves unmanaged settings, writes owner-only backups,
  and rolls both target files back on a late write failure. Focused parity
  tests, native activation regressions, and live connection checks passed.
- [FEAT] Retired the Dolphin source variant from the install catalog while
  preserving existing user-owned Dolphin runtime directories; new installs now
  expose only Codex, Claude, and OpenCode. Added official-layout native skill
  activators for Claude and OpenCode, including the ten protected CMA tool
  projections and narrow `claude-docs` / `opencode-docs` documentation skills.
  Activation preserves unmanaged configuration and fails closed on conflicting
  managed files or symlinks; it does not add credentials, providers, plugins,
  MCP endpoints, or xcodebuildmcp.
- [MAINT] Reconciled the active global Graphify runtime with the protected
  Codex projection after preserving the legacy ten-file tree in an owner-only
  timestamped backup. Source and active manifests now match with no symlinks;
  the other nine protected skills and enabled/disabled MCP state were verified
  unchanged by code and security review.
- [FEAT] Native Codex installer and setup delegation now run the protected
  core-tool activation only after a successful install to `$HOME/.codex`;
  alternate targets and other variants remain isolated. The Codex template
  declares the four managed MCP entries without credentials, and installation
  guides now document Context7, cplt, xcodebuildmcp, restart, and portability
  boundaries; 24/24 focused and 334/334 full tests passed.
- [FEAT] EXP-20260815-001 activated the ten protected Codex repository-tool
  skills globally with Context7 required, nine conditionally implicit routes,
  cplt explicit-only, local-first single-provider routing, private rollback,
  additive MCP configuration, and xcodebuildmcp kept disabled; 19/19 focused
  and 328/328 full tests passed with 80% activator branch coverage, final code
  and security review, live MCP calls, and fresh-session discovery. Actual
  token-cost reduction remains unverified without a comparable baseline.

## 2026-08-11

- [FEAT] EXP-20260811-005 added the protected instruction-only cplt core skill
  with inactive Codex, Claude, and OpenCode projections, an orthogonal
  execution-isolation route, fail-closed structured authority gates, no host
  fallback, and evidence-based isolation reporting; 16/16 focused and 309/309
  full tests passed with 81% branch coverage, final code/security review, and
  unchanged active runtime manifests without executing cplt.
- [FEAT] EXP-20260811-004 added protected instruction-only GitHub, DeepWiki,
  and optional Context7 core skills with inactive Codex, Claude, and OpenCode
  projections, local-first single-provider routing, untrusted external-content
  boundaries, fail-closed unavailable behavior, semantic parity validation,
  and prompt-injection regressions; 14/14 focused and 293/293 full tests passed
  with 84% branch coverage, final code/security review, and unchanged active
  runtime manifests.
- [FEAT] EXP-20260811-003 added protected instruction-only Opengrep,
  OSV-Scanner, and Betterleaks core skills with inactive Codex, Claude, and
  OpenCode projections, distinct conditional routing, fail-closed unavailable
  behavior, redacted secret findings, semantic/overlap validation, and hardened
  malformed-input handling; 40/40 focused and 279/279 full tests passed with
  85% branch coverage, final code/security review, and unchanged active runtime
  manifests.
- [FEAT] EXP-20260811-002 added protected instruction-only Graphify, Serena,
  and ast-grep core skills with inactive native Codex, Claude, and OpenCode
  projections, compact repository-tool routing, fail-closed unavailable-tool
  behavior, semantic-parity validation, and hardened independent trigger and
  authority checks; 20/20 focused and 239/239 full tests passed with 85% branch
  coverage, final code/security review, and unchanged active runtime manifests.
- [DESIGN] EXP-20260811-001 added the inactive stable-V1 OpenCode core-skill
  profile and fail-closed read-only validator for native `SKILL.md` discovery,
  canonical semantic mapping, protected registry authority, lazy skill-tool
  loading, truthful explicit-only limitations, unavailable-tool behavior, and
  agent/plugin/MCP/config isolation; 14/14 focused, 62/62 Phase 2-5, and
  219/219 full tests passed with 89% branch coverage and final code/security
  review, without projecting skills or changing active OpenCode state.
- [DESIGN] EXP-20260810-011 added the inactive, official-Anthropic-backed
  Claude core-skill profile and read-only validator for native `SKILL.md`
  projection semantics, explicit-only lazy activation, protected registry
  authority, unavailable-tool behavior, routing-only `CLAUDE.md` guidance,
  plugin/MCP/agent boundaries, and active-runtime isolation; 14/14 focused,
  48/48 core-skill, and 205/205 full tests passed with 92% branch coverage and
  final code/security review.

## 2026-08-10

- [DESIGN] EXP-20260810-010 added the inactive, official-doc-backed Codex core
  skill profile and a read-only validator for canonical field mapping,
  explicit-only lazy activation, native discovery, semantic parity,
  unavailable-tool behavior, AGENTS routing, and active-runtime isolation;
  19/19 focused and 191/191 full tests passed with final code/security review.
- [GOVERNANCE] EXP-20260810-009 added the canonical ten-entry CMA core-skill
  registry and a read-only validator for protected removal, missing entries,
  drift, semantic parity, custom separation, and no-prune enforcement; 15/15
  focused and 172/172 full tests passed with 83% validator branch coverage and
  independent code/security review, without skill projections or runtime changes.
- [DOCS] Added CMA Core Skill Standard v1 as the provider-neutral semantic
  contract for protected, lazy Codex, Claude, and OpenCode core skills; no
  tool-specific skill, variant, runtime, automation, or TDD change was made.
- [DESIGN] Added a planning-only CMA Tool Intelligence and TDD optimization
  architecture covering structured shared evidence, deterministic freshness,
  lazy specialized-tool escalation, reviewer independence, benchmark gates,
  and a minimal planner-to-TDD handoff candidate; no implementation or
  activation was performed.
- [DOCS] Added a source- and runtime-trace-backed Graphify trigger problem
  investigation packet covering acceptance criteria, EXP-003 through EXP-007,
  repository-read and process surfaces, observability gaps, and security
  boundaries without proposing a new solution.
- [POLICY] EXP-20260810-002 added the Codex-only lazy repository-tool module,
  created a private verified recoverable rollback point, and synchronized the
  approved policy and module into the active local runtime; tool use remains a
  separate evaluation step.
- [ROLLBACK] EXP-20260810-001 moved the inactive ARK and CMA-ARK implementation, adapter, hook, evidence, and test surfaces into a private checksum-bound external recovery backup; the repository now retains only a non-executable planning proposal and historical audit records.

## 2026-08-09

- [CHANGED] Removed ARK's nested Git boundary and adopted it into the CMA monorepo.
- [DOCS] Consolidated ARK's ignore rules, instructions, changelog, experiment,
  and integration status under authoritative CMA records and policies.
- [TEST] Added a fail-closed ARK monorepo contract covering functional-file
  hashes, record preservation, experiment-ID uniqueness, and removed metadata.
- [FIX] EXP-20260809-001 made ARK unittest discovery monorepo-safe with explicit
  `-t ARK`; all 33 tests passed from the CMA root with 85% branch coverage.
- [FIX] EXP-20260809-002 made root-relative ARK CLI examples executable by
  requiring `--config ARK/ark.json` and verifying the documented doctor command.
- [DOCS] Made ARK coverage validation use an isolated temporary data file so
  root-level coverage state is not created by documented monorepo commands.
- [PILOT] Completed the isolated Phase 2 CMA–ARK read-only compatibility pilot:
  single-tool text and stale-graph routes passed, unavailable `ast-grep` stayed
  fail-closed, 9/9 contract and 33/33 ARK tests passed, and pre/post state was
  byte-identical; network activity, token usage, and tool provenance remain unverified.
- [DESIGN] EXP-20260809-003 approved the passive Phase 3 CMA–ARK adapter API:
  explicit activation, a three-intent allowlist, canonical plan-digest approval,
  bound provenance, deterministic POSIX/macOS exit origins, rollback, and future
  TDD gates; implementation was later separately approved while activation remains unapproved.
- [FEAT] Added the passive stdlib CMA–ARK v1 process adapter with a fixed
  repo-owned ARK boundary, three-intent allowlist, plan-digest approval handshake,
  bound executable provenance, fail-closed protocol normalization, and no activation.
- [TEST] Added RED-first unit, subprocess, real fixed-ARK black-box, and passive
  footprint contracts; 29 adapter tests passed with 82.81% branch coverage.
- [SECURITY] Revalidated fixed ARK resources and selected-tool PATH/content/stat
  identity immediately before execution; independent code and security reviews passed.
- [RECORDS] Rotated five older terminal experiments after the ARK migrations
  reached the deterministic archive threshold; post-check returned below threshold.
- [DESIGN] EXP-20260809-005 defined a repo-local, explicit-only CMA-ARK
  activation boundary with a plan-only text-search pilot, trusted host approval
  gate, isolated bootstrap, outer identity binding, atomic replay/rate control,
  sensitive-output controls, staged Graphify coordination, manifest-bound
  rollback, and no runtime activation.
- [FEAT] Added the inactive EXP-20260809-006 CMA-ARK skill candidate with
  explicit-only metadata, fixed isolated bootstrap, strict query framing, a
  bounded real passive-adapter plan boundary, digest-only query reporting, and
  no discovery or execution authority; future activation remains blocked on
  adapter launcher/interpreter and writable-PATH identity pinning.
- [SECURITY] EXP-20260809-007 pinned CMA-ARK launchers to isolated system Python,
  bound adapter/ARK/interpreter/target/tool identities, and hardened the
  disposable skill pilot against import injection, writable ancestors,
  concurrent state races, symlink and inode drift, and false commit status.
- [TEST] Passed 58/58 adapter and pilot tests with 80% pilot and 91% combined
  branch coverage, 33/33 ARK tests, 14/14 root ARK contracts, skill validation,
  and independent code and security reviews; no real activation occurred.
- [ROLLBACK] EXP-20260809-008 exercised governed repo-local CMA-ARK activation,
  direct plan-only verification, rollback, and fresh-host discovery, then
  removed the discovery surface after three host sessions produced no usable
  plan. Canonical activation operations and the unproven bootstrap revision
  were removed; global and repo-local activation remain absent.
- [FIX] Made disposable pilot rollback use its validated installer-recorded
  manifest so later candidate-source edits cannot strand an unchanged installed
  copy; installed file and directory drift still fails closed.
- [FEAT] EXP-20260809-009 added an inactive repo-local `UserPromptSubmit`
  transport candidate and descriptor-anchored disposable hook lifecycle pilot,
  replacing the failed model-driven skill stdin path without activating hook
  trust, canonical config, skill discovery, or tool execution.
- [SECURITY] Bounded encoded hook config before publication, preserved
  unrelated hook entries, rejected unsafe descriptor/path state, and made
  residual pre/post-commit cleanup failures report their actual mutation state;
  final code and security re-reviews passed.
- [TEST] Passed 18/18 focused hook tests with 85% branch coverage, 78/78 adapter
  tests, a real zero-execution hook-to-ARK plan, disposable CLI install/rollback,
  33/33 ARK tests, 5/5 CMA-ARK root contracts, and 166/166 root regressions.
- [FEAT] EXP-20260809-010 split the CMA-ARK hook pilot into a thin isolated CLI
  and private descriptor lifecycle, then added fixed no-target canonical hook
  install and rollback operations without reactivating the failed repo skill.
- [TEST] Added copied-layout canonical lifecycle, idempotency, rollback,
  reinstall, drift, module-identity, and truthful cleanup-state coverage;
  final 27/27 focused tests passed with 80.47% combined branch coverage,
  alongside 87/87 adapter, 33/33 ARK, and 166/166 root regressions.
- [SECURITY] Closed temp-unlink, descriptor-close, and outer-descriptor cleanup
  paths that could misreport residual or committed hook state; final code and
  security re-reviews passed.
- [ROLLBACK] Installed the canonical prompt hook, restored the exact original
  config during rehearsal, reinstalled and trusted only its displayed
  definition, then removed it after the first fresh-host trace returned a
  generic `rg` plan without required bound digests or explicit zero-execution
  evidence. The original config SHA-256 is restored; no hook or skill is active.
- [DESIGN] EXP-20260809-011 accepted a deterministic same-run CMA-ARK evidence
  contract with independent candidate and Codex lanes, semantic session/thread
  binding, exact fail-closed schemas, stable three-run comparison, and private
  cleanup; wrapper implementation and activation remain separately gated.
- [TEST] Passed 8/8 evidence-design, 6/6 plan-only hook candidate, and 3/3
  passive adapter contract tests; Draft 2020-12 negative validation and final
  independent code/security re-reviews passed without activating any hook.
- [FEAT] EXP-20260809-012 added a disposable deterministic host-evidence
  wrapper/harness with independent candidate and JSONL lanes, reviewed source
  manifest binding, private cleanup, and no canonical activation.
- [SECURITY] Unified the plan-only subprocess tree under one wrapper-owned
  process group, closed timeout/reap and semantic-failure escape paths, and
  passed 27/27 focused tests at 84% combined branch coverage plus 115/115
  adapter tests and final independent code/security reviews.

## 2026-08-08

- [FIX] EXP-20260808-003 made project init additive for Codex, Dolphin, Claude,
  and OpenCode, migrated template state to a multi-variant schema, preserved
  shared/customized project files, and restricted destructive reinitialization
  to explicit `--reset` with collision-safe private recovery archives.
- [POLICY] Added a global Task Transition Gate across the portable Codex,
  Dolphin, Claude, and OpenCode policies. Distinct completed tasks now require
  a short summary, the next task or an explicit statement that none is known,
  and fresh user approval before work continues; already approved steps inside
  the same bounded task remain uninterrupted. Synchronized only the stale
  active policy files through private, permission-preserving backups and passed
  145/145 regressions plus independent code and security review.
- [FEAT] Added a provider-neutral OpenCode CMA variant with an isolated
  `llm-opencode` launcher, eight Markdown agents, four workflow skills, lazy
  registry modules, and preservation-aware project init/upgrade support.
- [SECURITY] Isolated OpenCode config, data, cache, and state roots; rejected
  symlinked state paths; approval-gated governor writes; omitted sensitive
  project-config diffs; and protected init/upgrade archives with private modes.
- [TEST] Captured runtime, isolation, secret-redaction, preservation, and custom
  path RED states; passed 141/141 regressions plus live OpenCode 1.18.15 config,
  path, agent, skill, and single-plugin pilot checks; final code and security
  reviews passed.
- [CHANGED] Relocated the independent ARK repository under `Codex-Multi-Agent/ARK`.
- [ADDED] Created the independent ARK repository with a strict JSON configuration contract.
- [ADDED] Added narrowest-sufficient-tool planning for Graphify, rg, ast-grep, conditional OSV, Serena, GitHub MCP, Opengrep, Betterleaks, cplt, DeepWiki, and Context7.
- [ADDED] Added argv-only execution, fail-closed target containment, private cplt runtime roots, credential stripping, output redaction, and truthful result statuses.
- [TEST] Added RED-first unit and integration coverage for configuration, routing, execution, CLI behavior, injection resistance, and runtime isolation.
- [FIX] Enforced fail-closed configuration types, `.ark/runtime` containment, exact GitHub identities, nonzero no-execution exits, nonempty security evidence, and explicit docs providers (`EXP-20260808-004`).
- [FIX] Rejected non-string Serena mode values with a controlled configuration error (`EXP-20260808-004`).
- [SECURITY] Isolated cplt behind a minimal repo-local environment, suppressed sensitive scanner output, bounded subprocess duration/output while draining streams, terminated timed-out process groups, and rejected Graphify output symlink escapes (`EXP-20260808-004`).

## 2026-08-07

- [DOCS] Aligned CMA project guidance and the managed configuration prompt so
  active-skill declarations exclude disabled-plugin and inactive-registry
  entries, and refreshed the project instruction version to template 2.2.
- [INFRA] EXP-20260807-002 aligned the self-hosted CMA project with Codex
  template 2.2, created managed template state, and synchronized the selected
  active global policy, runtime README, and orchestration gate.
- [SECURITY] Preserved user configuration, setup preferences, status messages,
  audit history, stricter record/archive overrides, credentials, sessions, and
  unrelated runtime state through a verified five-file recovery backup and
  targeted updates only.
- [TEST] Verified project-template and active-runtime parity, preserved hashes,
  valid TOML/JSON, managed upgrade idempotency, 52/52 focused checks, 122/122
  complete regressions, and clean diff integrity.
- [DOCS] Synchronized the English and Turkish runtime guides, command reference,
  Claude variant README, and integration tracker with the completed native
  Claude activation, recovery backup, rollback, force-rejection, and legacy
  runtime preservation behavior.
- [FEAT] EXP-20260807-001 changed Claude's default user-global runtime from the
  isolated `.llm-runtimes/claude` path to native `${HOME}/.claude` with a
  preservation-first CMA policy import and dedicated activation helper.
- [SECURITY] Native activation rejects force, differing managed files,
  incomplete sources, unsafe or equivalent-path bypasses, and partial backup
  failures; new runtime paths use owner-only permissions regardless of umask.
- [MIGRATION] Activated the current user's native Claude CMA surface with a
  byte-identical policy backup while preserving existing settings, modes,
  unrelated user state, and the legacy isolated runtime.
- [TEST] Verified meaningful RED regressions, 10/10 activation checks, 17/17
  installer checks, 17/17 Claude runtime checks, 122/122 complete regressions,
  live source parity and idempotency, plus passing independent code and
  security reviews.

## 2026-08-06

- [FEAT] EXP-20260806-011 added a portable Claude Code subagent restoration
  prompt derived from the verified 12-agent Sonnet/Opus frontmatter matrix.
- [SECURITY] Fail-closed explicit-target restoration unless the effective
  `CLAUDE_CONFIG_DIR` equals the resolved target before delegation or writes.
- [TEST] Verified Claude and installer suites at 17/17 each, complete
  regressions at 112/112, isolated prompt hash parity, native Claude isolation,
  and passing independent code/security reviews.
- [FEAT] EXP-20260806-010 added a portable, token-conscious Codex subagent
  restoration prompt with dynamic runtime-home resolution and the verified
  12-role medium-only Terra/Sol matrix.
- [SECURITY] Extended installer fail-before-write symlink validation to the
  managed prompt directory and preserved existing prompts without force.
- [TEST] Verified meaningful restoration and partial-mutation RED cases,
  focused 5/5 checks, 17/17 installer tests, 21/21 runtime-contract tests,
  11/11 orchestration tests, 111/111 complete regressions, active prompt hash
  parity, and independent code/security review.
- [CHORE] Normalized shared registry file endings across Codex, Dolphin, and
  Claude while preserving byte-identical provider-neutral assets.
- [FEAT] EXP-20260806-009 expanded the portable Claude Code runtime to full
  Core CMA source parity with 12 native agents, four complete skills, eight
  lazy modules, six registry records, and an exact 34-file home manifest.
- [SECURITY] Hardened the shared Codex, Dolphin, and Claude record archive
  helper against managed-parent symlink escapes using `O_NOFOLLOW` directory
  descriptors and rollback registration before atomic writes.
- [TEST] Added semantic Claude parity, truthful audit-history, external path
  escape, and post-replace rollback regressions; verified 48/48 focused tests,
  106/106 complete regressions, and clean independent code/security re-reviews.
- [CHORE] Applied threshold-triggered terminal experiment compaction and
  verified the active and split archives return `BELOW_THRESHOLD` without
  losing experiment records.
- [SECURITY] Extended project containment preflight to every managed template
  parent for dry-run, apply, and initial-state operations.
- [SECURITY] Rejected symlinked or non-directory project runtime parents before
  init/upgrade confirmation or mutation to prevent path escape and partial reset.
- [FIX] Classified terminal-less Claude assistant errors as failed outcomes
  while retaining unverified status for genuinely missing terminal evidence.
- [FIX] Made experiment archiving support contiguous split archive indexes and
  append rotations to the latest validated part.
- [CHORE] Excluded local Graphify indexes and reports from version control.
- [FEAT] EXP-20260806-008 added an optional offline Claude Agent SDK adapter
  pinned to `claude-agent-sdk==0.2.130` with bounded requests, restrictive
  permissions, session contracts, truthful terminal mapping, and usage/cost
  observability.
- [SECURITY] Default-denied credential-backed SDK execution until a separately
  approved Gate C executor provides per-call authorization, isolated state,
  and a minimal child-process environment; fixed cancellation and terminal
  error-metadata fail-closed findings from independent reviews.
- [TEST] Verified 21/21 adapter tests at 92% coverage, frozen lock/sync, Python
  compilation, `git diff --check`, 88/88 root regressions, and independent code
  and security review without credentials or a real Claude request.
- [FEAT] EXP-20260806-007 added a provider-aware native Claude runtime,
  isolated `llm-claude` launcher, Markdown chain agents, safe settings, and an
  `@AGENTS.md` project bridge with preservation-aware init and upgrade support.
- [TEST] Verified 88/88 tests plus syntax, JSON, path-boundary, symlink,
  no-overwrite, launcher, project dry-run, code-review, and security-review
  checks without SDK, credential, active-runtime, commit, push, or deployment
  changes.
- [DOCS] Added a single status-tracked Claude integration task plan covering
  native runtime parity, project migration, optional Agent SDK work, security
  gates, verification, and rollback.
- [INFRA] Installed the approved Codex CMA runtime on `blockmanpro`, preserving
  existing `/root/.codex` state and initializing `/opt/blockman-platform-dev`
  as a multi-repository CMA workspace without deployment or service changes.
- [INFRA] Installed Ubuntu Node.js 18.19.1, npm 9.2.0, and pinned
  `@openai/codex@0.146.1`; authentication remains intentionally unconfigured.
- [TEST] Verified 60/60 local tests, archive integrity, isolated RED/GREEN,
  no-overwrite sentinels, project conflict archiving, exact managed files,
  configuration parsing, root-only artifacts, and Codex CLI startup.
- [FIX] EXP-20260806-001 through EXP-20260806-006 documented executable-mode,
  manifest-scope, SSH stdin-continuation, archive-regression, and scoped
  assertion findings with bounded resolutions.

## 2026-08-05

- [FEAT] EXP-20260805-001: Added fail-closed `EVIDENCE_MODE: enable | disable`
  semantics with missing values defaulting to disabled and explicit user
  requests remaining available.
- [INFRA] EXP-20260805-001: Set all 17 active CMA projects to
  `EVIDENCE_MODE: disable` and activated only the four approved mode clauses in
  the backed-up global records module.
- [TEST] EXP-20260805-001: Verified meaningful 3/3 RED, 60/60 full CMA tests,
  the 17-project manifest, exact global delta, and independent code and
  security reviews.

## 2026-08-04

- [FIX] EXP-20260804-003: Required one independently verifiable outcome and one
  coherent verbatim proof excerpt per evidence claim while prohibiting
  reporting-only semantic downgrades.
- [TEST] EXP-20260804-003: Recorded meaningful source and portable RED failures,
  then passed 17 focused tests, 55 full CMA tests, independent reviews, and EV
  validation of six atomic claims.
- [FIX] EXP-20260804-002: Added a conditional temporal TDD evidence contract
  with one ordered structural RED-to-final pair, final-only success proof, and
  a same-scope post-fix rerun requirement.
- [TEST] EXP-20260804-002: Verified source and portable contracts, fenced and
  quoted proof boundaries, 14 focused tests, and 52 full CMA tests.
- [INFRA] EXP-20260804-002: Backed up and synchronized the validated temporal
  records contract to the active global Codex runtime.
- [FIX] Standardized `ask-approval` final messages on the exact six-line CMA
  decision block so EV can defer only the current non-completion Stop.
- [DOCS] Diagnosed the EV Stop-hook false trigger on structured CMA decision
  waits and recorded the bounded remediation scope without changing runtime
  behavior.
- [FEAT] EXP-20260804-001: Added the prospective CMA `## Claims` evidence
  contract required for EV compatibility.
- [TEST] EXP-20260804-001: Added source, portable-install, and real EV/GLM
  compatibility coverage while preserving fail-closed validation.
- [INFRA] EXP-20260804-001: Backed up and synchronized the validated CMA records
  module to the active local Codex runtime.

## 2026-08-01

- [FIX] EXP-20260801-003: Made global Codex Stop notifications root-only and
  selected distinct spoken messages for completion, failure, and user waiting.
- [TEST] EXP-20260801-003: Verified eight silent hook scenarios, subagent
  suppression, malformed-input safety, executable mode, and config parity.
- [FIX] EXP-20260801-002: Standardized all Codex subagents on medium reasoning
  and replaced six high variants with four Sol/medium routing variants.
- [TEST] EXP-20260801-002: Verified 47 tests, source-active parity, ZIP
  integrity, no project-local high override, and fresh-session routing.
- [INFRA] EXP-20260801-001: Activated compact Core CMA and eight trigger-loaded
  modules in the managed and active local Codex runtime.
- [FIX] EXP-20260801-001: Removed unsupported `display_name` metadata and added
  six static Sol/high variants for reliable conditional escalation.
- [TEST] EXP-20260801-001: Added RED/GREEN contracts and verified the full
  suite, source-active parity, rollback checksums, and fresh-session routing.
- [DOCS] Restricted the CMA optimization plans to this repository and the local
  global Codex directory, and recorded completed, partial, and pending work.
- [INFRA] Applied the approved CMA subagent model matrix to Codex source and
  active global agents, keeping mandatory quality roles on Sol.
- [INFRA] Added friendly identity aliases for Codex subagents while preserving
  role-key runtime naming and orchestration chain compatibility.
- [DOCS] Added the CMA Core and Lazy Modules plan with subagent model and
  reasoning evaluation guidance.
- [DOCS] Added the CMA subagent model pilot implementation plan with file-level
  scope, dry-run checks, and rollback criteria.

## 2026-07-28

- [FEAT] EXP-20260728-001: Added a minimal truthful outcome-reporting contract
  to Codex and Dolphin runtime policies.
- [TEST] EXP-20260728-001: Added RED/GREEN source and portable-install checks
  for verified status-to-success mappings.
- [INFRA] EXP-20260728-001: Activated the validated Codex policy locally with a
  checksum-verified rollback backup.

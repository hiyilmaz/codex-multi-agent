# Improvement Experiments

[Terminal experiment archive](EXPERIMENTS_ARCHIVE.md)

## EXP-20261118-001 - MCP Tool Verification and Serena Project Context

Date: 2026-11-18
Status: ACCEPTED

Problem: The DeepWiki manifest expects a tool name absent from the live server,
and the Serena workflow does not require evidence of the active project path.

Evidence: DeepWiki `tools/list` returned `ask_wiki_question`, and its
`read_wiki_structure` call returned content. Serena reported the CMA project
as active while the requested symbol check targets `ektrun`.

Hypothesis: Aligning the manifest and reporting the failing MCP stage will
make the health check diagnostic. Confirming the active absolute project path
before symbol lookups will prevent queries against the wrong project.

Solution Attempt: Update the manifest and read-only check diagnostics. Add
the same on-demand project verification workflow to the Serena skill and its
tracked projections.

Test: Exercise tool discovery, the functional call, and their failure paths.
Verify the Serena skill projections and run the `businessDate` lookup in a
separate Serena session on `ektrun`.

Success Criteria: The check reports a healthy DeepWiki only after the live
read-only call and explains failures. Serena confirms the exact project path
before returning the symbol location.

Result: The new tests failed against the previous manifest, health output,
and Serena instructions. The installer suite passed 78 tests. The repository
suite reported 436 tests with 1 skipped because it requires a root process.
`bin/cma-tools check` exited 0 with 11 healthy tools and preserved Codex
settings. An isolated Serena 1.7.0 session reported the
invalid-path reason, confirmed the absolute `ektrun` path after activation,
and located `businessDate` at `src/domain/rules.ts:3`. Serena created project-local
configuration and symbol cache files under `.serena`. The queried source file's
checksum matched before and after the lookup. Code and security reviews closed
with no blocking findings.

Decision: ACCEPT

## EXP-20261006-001 - Native Grok CMA Variant

Date: 2026-10-06
Status: ACCEPTED

Problem:
Grok is not a catalog variant, and its native CMA asset discovery and
preservation behavior have not been verified against the installed CLI.

Evidence:
The catalog contains Codex, Claude, and OpenCode. Installed Grok is 0.2.39.
An isolated inspection discovers Grok agents/project config as well as external
compatibility assets; instruction paths can use case and filesystem aliases.

Hypothesis:
A Grok-native projection of approved CMA assets, combined with additive project
integration and a preservation-first activator, will provide discoverable CMA
instructions, agents, and skills without altering existing settings or identity.

Solution Attempt:
Add one native Grok variant with no provider/model pins, a GROK_HOME launcher,
and safe activation that treats configuration and authentication as opaque.

Test:
Capture test-first RED, focused and lifecycle regression tests, independent code
and security review, and redacted real CLI inspect metadata after activation.

Success Criteria:
- Catalog/setup/init/upgrade support Grok and preserve existing project files.
- Activation rejects unsafe paths/conflicts and is idempotent and recoverable.
- Existing native settings, identity, and unrelated assets remain byte-identical.
- Installed CLI discovers the packaged policy, eight agents, and workflow skills.
- No model request, authentication change, or dependency installation occurs.

Result:
Initial RED ran 24 tests against the absent implementation. Focused final
verification passed 29 tests, including meaningful FIFO, fsync, staging-cleanup,
conflict, preservation, idempotence, and concurrent-edit rollback checks.
The final full suite ran 435 tests: 434 passed and one existing environment test
was skipped. New activator statement coverage is 89%; Python/Bash/TOML syntax
and diff checks passed. Code and security reviewers returned PASS after a
post-link cleanup blocker was reproduced and fixed.
Temporary real CLI inspection verified four coexisting project variants. Native
activation created 42 private assets, preserved all 3,745 pre-existing files or
links and 1,470 directory modes, and recorded a private recovery manifest.
Grok 0.2.39 inspection discovered the native policy, eight roles, and four
workflow skills from their expected sources. Reinstallation created zero files
and no backup. No model call, login, dependency installation, or model/provider
change was performed.

Decision:
ACCEPT

Notes:
The user approved the disclosed plan and chain. This experiment is triggered by
new runtime governance and unresolved native-discovery evidence, not by the
expected absence of a new feature. Existing records are preserved in full;
terminal transition triggers record-archive. Inspection lists an additional
existing ECC plugin tdd-workflow entry; validation matches name and source
without collapsing duplicate names. Vendor compatibility assets were preserved.
Runtime skill selection and tool-permission enforcement remain unverified and
are outside the approved no-model-call validation scope.

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

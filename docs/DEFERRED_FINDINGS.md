# Deferred Findings

## Pending

- ID: DEFERRED-NET-L2-001
  Type: NETWORK_ISOLATION
  Discovered At: 2026-08-28
  Source Task: Almila Farma AD rollout Phase 7E/7F
  Location: Office/Lab upstream physical Layer-2 path
  Summary: ESXi uplink captures proved that Office and Lab currently share an upstream physical broadcast domain even though their ESXi vSwitches, port groups, and uplinks are separate. The user explicitly deferred permanent physical isolation so the scoped AD rollout can continue through ALM-MGMT01 with exact DC host rules and default-deny transit.
  Recommended Fix: In a separately approved maintenance window, make vmnic0/LAN1 exclusive to the Lab network and vmnic1/LAN2 exclusive to the Office network, then repeat the pinned ARP and ESXi uplink-capture isolation tests.

- ID: DF-20260828-0000-001
  Type: SECURITY_HARDENING
  Discovered At: 2026-08-28
  Source Task: ALM-LAB-DC01 activation reconciliation and Phase 7B IPv6 host control
  Location: Lab network 192.168.50.0/24 IPv6 RA/SLAAC path
  Summary: SEC-NET-IPv6-001 / LAB-IPV6-EGRESS-001 - ALM-LAB-DC01 receives global IPv6 prefix 2a00:1d34:35db:9a00::/64 and default route fe80::1 from upstream RA. Phase 7B added a host-level persistent outbound block for 2000::/3 and proved that global IPv6 ICMP/TCP egress is blocked while IPv4 Lab access, RDP, link-local IPv6, and the IPv6 binding remain healthy. Upstream VLAN 50 IPv6 isolation is still absent, so this host control does not protect other Lab devices and does not cover a future NAT64 path such as 64:ff9b::/96.
  Recommended Fix: Deploy the planned dedicated physical stateful firewall/router with default-deny IPv4 and IPv6 policy, block upstream IPv6 internet forwarding and transition mechanisms including NAT64 for VLAN 50, and permit only the separately approved DC-to-DC traffic. Retain and revalidate the host rule until upstream enforcement is proven.

- ID: DF-20260827-0000-002
  Type: OPERATIONAL_DEPENDENCY
  Discovered At: 2026-08-27
  Source Task: Almila Farma DC preparation Phase 3
  Location: VM_DATASTORE/ISOs
  Summary: DEFERRED-MEDIA-001 - No verified non-Evaluation Windows Server 2022 x64 production ISO is available. A manually attached SERVER_EVAL_x64FRE_en-us.iso backing was detected on both Powered Off DC VM shells and safely returned to empty client backing without changing the ISO file; it is no longer attached.
  Recommended Fix: Upload an authorized, licensed Windows Server 2022 x64 Standard or Datacenter installation ISO, record its source and checksum, and verify its bootability and edition metadata before attaching it to the Powered Off DC VMs.

- ID: DF-20260827-0000-001
  Type: OPERATIONAL_HARDENING
  Discovered At: 2026-08-27
  Source Task: Almila Farma ESXi Office network Phase 1
  Location: vmnic1 / vSwitch-OFFICE
  Summary: DEFERRED-NET-001 - vmnic1 negotiated at 100 Mbps Full; the accepted target remains 1 Gbps Full. The Phase 1 topology is operational, but the physical link may constrain future Office DC traffic.
  Recommended Fix: During an approved maintenance window, inspect the cable, RJ45 termination, patch panel, physical switch or modem port, and auto-negotiation; then verify 1 Gbps Full without changing the Lab uplink.

- ID: DF-20260818-0000-001
  Type: OPERATIONAL_HARDENING
  Discovered At: 2026-08-18
  Source Task: Blockmanpro codex-tools live repair
  Location: /root/.local/share/cma-rollbacks/codex-tools-pre-*
  Summary: Owner-only UV-tool rollback copies were created and their expected top-level contents were inspected, but a full recursive integrity manifest and isolated restore rehearsal were not performed against the live package environment.
  Recommended Fix: Add an isolated rollout harness that records a recursive manifest and rehearses restoration outside the active UV tool path before using the backup in a real rollback.

- ID: DF-20260817-0000-001
  Type: SECURITY_HARDENING
  Discovered At: 2026-08-17
  Source Task: Independent codex-tools CMA integration
  Location: tools/codex-tool-installer/src/codex_tool_installer/config.py
  Summary: Config transactions reject lexical symlink components, and rollback now rejects unexpected content or inode changes, but a concurrently replaceable ancestor or same-user change could still occur between validation and path-based backup/replace operations. Normal private native Codex homes limit exploitability; custom CMA homes are rejected.
  Recommended Fix: Anchor transaction reads, backups, replacement, and rollback to validated directory descriptors with no-follow/openat-style operations and inode identity checks.

## Completed

- ID: DF-20260716-0535-001
  Type: RISK
  Discovered At: 2026-07-16 05:35
  Fixed At: 2026-07-16 05:37
  Source Task: Update user-global custom subagent models to gpt-5.6-sol
  Location: variants/codex/home/agents/*.toml
  Summary: The portable Codex variant still pins eight custom agents to gpt-5.5.
  Fix Summary: Updated all eight Codex variant agent model overrides to gpt-5.6-sol and retained Dolphin-specific model settings.
  Evidence: Python 3.13 TOML validation and temporary Codex variant installation confirmed all eight packaged agents use gpt-5.6-sol.

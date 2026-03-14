# VM Network Outage Root Cause Analysis

Date: 2026-03-13

## Scope Clarification

This report distinguishes three separate layers that must not be mixed:

1. Host script layer
   `休息断网` is a Windows host-side script.

2. Host stability layer
   The host itself showed abnormal shutdown and hardware or driver instability signals.

3. VM symptom layer
   The Kali VM later appeared "offline" or unstable because it depended on a host that had already entered an unstable state.

The host script was not a VM script.

## Bottom Line

The essential cause was not "the VM needed to connect to the host IP."

The stronger root-cause chain was:

1. The Windows host had a serious instability event around `2026-03-13 02:59:16`.
2. The more suspicious signals pointed to host-side `Realtek PCIe` or upstream `PCIe Root Port` instability.
3. The VM network failure was a downstream symptom after the host entered an unstable state.

So the VM outage should be described as a host-originated problem reflected into the VM, not as a VM-side script problem and not as a simple "cannot access host IP" problem.

## What The Host Script Actually Did

The `休息断网` shortcut on the host executed a host-side PowerShell script.

That script only changed Windows Firewall policy to block inbound and outbound traffic.

It did not:

- sleep the machine
- shut down the machine
- disable the NIC
- change power plans
- modify the VM
- change the VM network adapter
- touch the NIC driver directly

So even though it was a host script, its logic still does not match a direct `Kernel-Power 41` style crash trigger.

## Why The Host Script Was Still Not The Direct Root Cause

The time relationship inspected in the earlier analysis was:

- abnormal shutdown time: `2026-03-13 02:59:16`
- `休息断网.lnk` creation time inspected that day: `2026-03-13 03:10:34`
- inspected script write time: `2026-03-13 03:10:45`

That means the inspected version could not have directly caused the crash at `02:59:16`.

So the correct statement is:

- it was a host script
- but the inspected script version was still not the direct cause of the host crash

## Stronger Host-Side Evidence

The earlier event-log review produced host-side crash and hardware-related clues:

- abnormal shutdown centered near `2026-03-13 02:59:16`
- multiple `BlueScreen` and `LiveKernelEvent` records in the inspected time window
- a `LiveKernelEvent 141` watchdog-class record
- later summary explicitly called out:
  - a `Realtek PCIe GbE` hardware I/O related error
  - a corrected `PCI Express Root Port` hardware error

That evidence is much more consistent with:

- unstable host NIC driver state
- unstable PCIe link state
- host power-transition or resume instability

than with:

- a VM-side cause
- a VM script
- a simple proxy configuration mistake
- a pure DNS issue

## Correct Causality

The cleaner causality is:

1. Host entered an abnormal state.
2. Host NIC or PCIe path likely became unstable.
3. VM networking then became unreliable because the VM runs on top of that host state.
4. Later proxy failures inside the VM were symptom noise on top of the deeper host problem.

## What Should Not Be Claimed

These are weaker claims and should not be treated as the root cause:

- "The VM broke because it could not reach the host IP."
- "The host firewall script itself directly crashed the VM."
- "This was mainly a VM network mode problem."

## Most Defensible Root-Cause Statement

The VM outage was most likely a secondary effect of host-side instability on the Windows machine, especially around the `Realtek PCIe` networking path or its upstream `PCIe Root Port`, during or around a power-state transition.

The host `休息断网` action was a host-side firewall operation, not a VM script, but the evidence still did not support it as the direct crash cause.

## Confidence And Limit

This is a host-first interpretation based on the earlier event-log and WER evidence.

It is stronger than the earlier shallow proxy summary, but it is still not a full crash-dump diagnosis.

The next step for a harder conclusion would be direct analysis of the referenced minidump or LiveKernel dump records from that date.

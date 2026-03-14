# VM Network Outage Root Cause Analysis

Date: 2026-03-13

## Bottom Line

The core issue was not "the VM needed to reach the host IP."

The stronger root-cause chain from the 2026-03-13 analysis was:

1. The host itself had a serious instability event around `2026-03-13 02:59:16`.
2. The evidence pointed more at host-side hardware or driver instability on the `Realtek PCIe` network path or upstream `PCIe Root Port`, not at the VM network mode itself.
3. Once the host hit that instability, the VM's networking and proxy behavior became secondary symptoms.

In short: the VM looked "offline", but the deeper problem was most likely host-side NIC or PCIe instability, not the VM depending on `192.168.1.x`.

## What Was Ruled Out

### 1. The "rest/offline" shortcut was not the direct trigger

The `休息断网` shortcut only switched Windows Firewall policy to block inbound and outbound traffic.

It did not:

- sleep the machine
- shut down the machine
- disable the NIC
- modify power plans
- touch the NIC driver

It also could not be the direct cause of the `02:59:16` abnormal shutdown, because the version inspected that day was written later:

- abnormal shutdown time: `2026-03-13 02:59:16`
- `休息断网.lnk` creation time: `2026-03-13 03:10:34`
- `Enable-Rest-Network-Lock.ps1` write time: `2026-03-13 03:10:45`

So the script was not the root cause of that crash.

### 2. This was not primarily a "VM cannot reach host IP" problem

That was a later proxy-path symptom in one specific setup.

You were right that this was not the essential reason the VM "lost network." Even if host proxy exposure was wrong, that does not explain the host abnormal shutdown and hardware-related event chain.

## Strongest Evidence From The Earlier Analysis

The 2026-03-13 event-log review surfaced host-side crash and hardware warnings around the same time window:

- abnormal shutdown / crash timeline centered near `2026-03-13 02:59:16`
- multiple `BlueScreen` and `LiveKernelEvent` records were present in the log review
- a `LiveKernelEvent 141` watchdog-class report was present
- later analysis explicitly identified two higher-value clues:
  - a `Realtek PCIe GbE` hardware I/O related error
  - a corrected `PCI Express Root Port` hardware error

That combination is more consistent with:

- unstable host NIC driver state
- unstable PCIe link state
- host resume or power-transition related hardware instability

and much less consistent with:

- a simple VM NAT or bridge misconfiguration
- a pure DNS issue
- the "rest/offline" shortcut itself crashing the machine

## Most Likely Root Cause

The most defensible root-cause statement from the available evidence is:

The VM outage was a downstream effect of host-side instability on the Realtek PCIe networking path or its upstream PCIe link, likely exposed during a power-state transition such as closing the lid or resume timing, not because the VM inherently depended on reaching the host IP.

## Why The VM Then Looked Randomly Broken

After the host-side instability event, several different network symptoms appeared:

- host-to-VM and proxy behavior became inconsistent
- VM local proxies such as `Geph 9910` and later `V2Ray 10809` also showed unstable behavior
- some symptoms looked like proxy resets, some looked like TLS failure, and some looked like path exposure mistakes

Those were real problems, but they were not the deepest layer.

They were the noisy symptom layer after the host had already entered an unstable state.

## Practical Conclusion

If the question is "what was the essence of the outage," the answer is:

It was not "the VM could not use host IP."

It was more likely:

- host abnormal shutdown or resume instability
- `Realtek PCIe` NIC or driver instability
- `PCIe Root Port` corrected hardware errors

with the VM network failure as the visible consequence.

## Confidence And Limit

This conclusion is stronger than the earlier proxy-only writeup, but it is still an inference from event logs and WER records, not a full minidump symbol analysis.

If you want the deepest possible confirmation, the next step would be minidump or LiveKernel dump analysis for the crash records referenced on 2026-03-13.

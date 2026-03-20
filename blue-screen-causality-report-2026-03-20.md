# Blue Screen Causality Report

Generated: 2026-03-20 +08:00
Host: Windows machine inspected from local shell
Scope: Assess whether the aggressive "suspicious backdoor/background process cleanup" performed on 2026-03-13 local time plausibly caused the later BSODs.

## Bottom Line

The evidence does **not** support the claim that the 2026-03-13 cleanup was the primary root cause of the BSOD pattern.

The strongest reasons are:

- The machine was already crashing **before** the cleanup window.
- The same `0x0000001e` bugcheck pattern existed **weeks earlier**.
- There is a separate and stronger signal for **kernel/driver/hardware instability**, especially:
  - repeated `WHEA-Logger` PCIe corrected hardware errors
  - `UcmUcsiCx.sys` live-kernel-report evidence
  - persistent USB/UCSI and virtual-HID related warnings
  - active third-party kernel/network drivers such as VirtualBox drivers and `WinDivert`

The cleanup may still have been a **secondary destabilizer** in a narrow sense for OEM/background tooling, but the available evidence makes that a weak hypothesis, not the lead one.

## Assessment

### Confidence by hypothesis

- `Unlikely` that disabling `sshd`, `DiagTrack`, `WpnService`, `CDPSvc`, and deleting Baidu/QQNT/Thunder/LuDaShi caused the BSODs directly.
- `Possible but weak` that disabling `ArmouryCrateControlInterface` changed OEM control-path behavior and removed a software layer that had been masking another issue.
- `More likely` that the system has an existing kernel-mode instability involving hardware, firmware, USB/Type-C/UCSI, PCIe, virtualization, or filter drivers.
- `Most important current risk` is not the 2026-03-13 user-mode cleanup itself, but the broader kernel stack that remained active afterward.

## Timeline

### BSOD and crash history before the cleanup

- `2026-01-23 15:16:38` local: bugcheck `0x000000c8`
- `2026-01-25 00:58:38` local: bugcheck `0x00000133`
- `2026-01-31 08:29:17` local: bugcheck `0x0000001e`
- `2026-01-31 21:34:54` local: bugcheck `0x0000001e`
- `2026-02-06 10:25:20` local: bugcheck `0x00020001`
- `2026-02-08 11:50:45` local: bugcheck `0x0000001e`
- `2026-02-12 21:37:02` local: bugcheck `0x0000001e`

This alone rules out the March 13 cleanup as the origin of the bugcheck family.

### Crash history immediately before the cleanup

- `2026-03-12 15:04:28` local: unexpected shutdown / crash (`Kernel-Power 41`)
- `2026-03-12 15:04:28` local: `volmgr 161` dump creation failure

This crash happened **before** the main cleanup actions below.

### Main cleanup actions

From local session and system service logs, the main service-disabling actions landed in the following window:

- `2026-03-13 01:47:17` local: `sshd` start type changed from automatic to disabled
- `2026-03-13 01:47:18` local: `WpnService` start type changed from automatic to disabled
- `2026-03-13 01:47:18` local: `CDPSvc` start type changed from automatic to disabled
- `2026-03-13 01:47:19` local: `DiagTrack` start type changed from automatic to disabled
- `2026-03-13 01:55:49` local: `BaiduNetdiskUtility` changed from demand start to disabled
- `2026-03-13 02:59:32` local: `Armoury Crate Control Interface` changed from automatic to disabled

Other cleanup in the same session included:

- deletion of Baidu Netdisk / QQNT / Thunder / LuDaShi residual directories
- removal of related firewall allow rules
- disabling ASUS / OneDrive / Edge Update / Google Update scheduled tasks
- repeated stopping of `WpnUserService_*` and `CDPUserSvc_*`
- removal of some Chrome extensions

### Crash history after the cleanup

- `2026-03-13 08:11:02` local: unexpected shutdown / crash (`Kernel-Power 41`)
- `2026-03-14 09:33:34` local: unexpected shutdown / crash
- `2026-03-15 14:10:05` local: unexpected shutdown / crash
- `2026-03-16 08:18:06` local: unexpected shutdown / crash
- `2026-03-17 08:40:08` and `23:22:41` local: repeated crashes
- `2026-03-19 08:45:22` local: repeated crash
- `2026-03-20 15:27:13` local: bugcheck `0x0000001e`

The cleanup did not end the instability, but that does not imply it caused it; the same pattern existed earlier.

## Evidence That Weakens the "Cleanup Caused BSOD" Theory

### 1. Same bugcheck family existed before the cleanup

Repeated `0x0000001e` bugchecks were already present on:

- `2026-01-31`
- `2026-02-08`
- `2026-02-12`

The latest `0x0000001e` on `2026-03-20 15:27:13` is therefore part of an older pattern, not a new post-cleanup phenomenon.

### 2. A crash happened on 2026-03-12 before the service-hardening window

The system crashed at `2026-03-12 15:04:28` local.

The main hardening changes to `sshd`, `WpnService`, `CDPSvc`, and `DiagTrack` happened at about `2026-03-13 01:47` local, hours later.

That timing directly contradicts the idea that those disabled services started the crash cycle.

### 3. Most removed items were user-mode background software, not typical BSOD root causes

Items such as:

- Baidu Netdisk
- QQ / QQNT
- Thunder / Xunlei
- LuDaShi residuals
- OneDrive scheduled tasks
- Edge updater tasks
- Google updater task

are much more likely to affect background traffic, startup behavior, or telemetry than to cause kernel bugchecks by being stopped or deleted.

Removing those may break app behavior, but they are weak candidates for producing repeated `0x1E` kernel exceptions across multiple weeks.

## Evidence That Points More Strongly Elsewhere

### 1. Repeated WHEA corrected hardware errors

From `2026-03-01` onward, the machine logged many `WHEA-Logger` Event ID `17` warnings.

Observed component detail:

- `PCI Express Root Port`
- `Error Source: Advanced Error Reporting (PCI Express)`
- `Primary Device Name: PCI\VEN_1022&DEV_14BA&SUBSYS_14C31043&REV_00`

This is a hardware/firmware/bus-level signal. It is substantially more relevant to recurrent BSOD investigation than disabled telemetry or removed updater tasks.

### 2. USB / Type-C / UCSI evidence

Current artifacts show:

- `C:\Windows\LiveKernelReports\UcmUcsiCx.sys`
- `C:\Windows\LiveKernelReports\UcmUcsiCx.sys-20260308-0157.dmp`

Active drivers include:

- `UcmUcsiAcpiClient`
- `UcmUcsiCx0101`
- `USBXHCI`

This puts the USB-C / UCSI control path in scope. That is a much more credible BSOD source than the stopped user-mode services.

### 3. Persistent boot-time driver warnings

Repeated boot warnings were logged for:

- `Kernel-PnP 219`
- `\Driver\WUDFRd failed to load`
- devices under `HID\HID_DEVICE_SYSTEM_VHF\...`

That indicates recurring driver-stack or virtual-HID friction around boot/restart.

### 4. Third-party kernel drivers remain active

Active kernel drivers currently include:

- `VBoxNetLwf`
- `VBoxSup`
- `VBoxUSBMon`
- `WinDivert`
- `amdfendr`
- `rtwlane601`

Notes:

- VirtualBox network and USB monitor drivers are classic kernel-mode complexity multipliers.
- `WinDivert` was installed multiple times on `2026-03-12` and `2026-03-20`.
- The `WinDivert` service currently reports as `Running` even though its start mode is `Disabled`, which implies it was loaded by software demand and is part of the active kernel/network path.

Kernel networking, USB filter, virtualization, and OEM device stacks are materially more plausible BSOD vectors than disabling `DiagTrack` or removing QQNT.

### 5. VBS / Hyper-V is enabled

Boot logs report:

- `Virtualization-based security ... is enabled due to HyperV`

That matters because compatibility edges become sharper when combined with:

- VirtualBox drivers
- packet/filter drivers
- OEM device services
- USB/UCSI paths

## The One Cleanup Change That Is Not Entirely Safe to Ignore

The only 2026-03-13 action that deserves non-trivial caution is:

- disabling `ArmouryCrateControlInterface`

Reason:

- It is OEM control software with potential hooks into thermal, fan, device, and platform-control behavior.
- It changed at `2026-03-13 02:59:32` local.
- A crash followed later that morning at `2026-03-13 08:11:02`.

However, this is still weak evidence for causality because:

- the machine had already crashed on `2026-03-12 15:04:28` before this change
- bugchecks had already existed since January
- the wider WHEA / UCSI / driver evidence is stronger

So the best reading is:

- `ArmouryCrateControlInterface` could be a contributing variable
- it is not well supported as the primary cause of the BSOD pattern

## Causality Ranking

### Least likely contributors from the cleanup session

- disabling `sshd`
- disabling `DiagTrack`
- disabling `WpnService`
- disabling `CDPSvc`
- deleting Baidu Netdisk / QQNT / Thunder / LuDaShi remnants
- disabling updater scheduled tasks

### Medium-interest but still secondary

- repeated forced stopping of `WpnUserService_*` and `CDPUserSvc_*`
- aggressive removal of some background software
- disabling `ArmouryCrateControlInterface`

### Higher-priority causes to investigate

- PCIe hardware / firmware instability
- USB-C / UCSI stack (`UcmUcsiCx.sys`)
- VirtualBox kernel drivers
- packet / filter driver activity (`WinDivert`)
- wireless or chipset driver interaction (`rtwlane601`, AMD platform stack)
- BIOS / firmware / OEM platform-control issues

## Practical Conclusion

If the question is:

> "Did shutting off those suspected backdoor/background components cause the blue screens?"

The evidence-based answer is:

- `Probably not` as the main cause
- `Possibly, at most, as a minor contributing change` for OEM behavior after `ArmouryCrateControlInterface` was disabled
- `More likely` the machine already had a kernel/hardware/platform instability that continued through and beyond that cleanup

## Recommended Next Steps

To move from correlation to stronger root-cause evidence, prioritize:

1. Analyze `C:\WINDOWS\Minidump\032026-8921-01.dmp` with WinDbg.
2. Analyze `C:\Windows\LiveKernelReports\UcmUcsiCx.sys-20260308-0157.dmp`.
3. Check BIOS and chipset/USB/AMD platform driver versions.
4. Temporarily remove or disable one kernel-complexity layer at a time:
   - VirtualBox drivers
   - `WinDivert`
   - optional OEM control stack
5. Correlate future crashes against:
   - USB-C docking / charger changes
   - VirtualBox usage
   - 迷X通 / `WinDivert` usage
   - standby / resume transitions

## Source Notes

This report is based on:

- local Codex session history for the 2026-03-13 cleanup actions
- Windows System event log
- WER bugcheck records
- minidump and live-kernel-report file presence
- currently loaded driver inventory

No full dump disassembly was performed in this report because a local debugger was not available in the current shell session.

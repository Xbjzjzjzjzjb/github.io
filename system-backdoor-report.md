# System Backdoor Report

Generated: 2026-03-13 02:21:32 +08:00
Updated: 2026-03-13 03:00:00 +08:00
Host: Windows machine inspected from local shell

## Scope
This report treats the following as suspicious under the user's standard:
- unattended background network traffic
- unattended collection of system, IP, proxy, or network information
- background persistence or auto-start behavior
- residual software or firewall permissions from previously installed third-party software

## Initial Findings
- No clearly disguised random-name malware process was identified in the active process list during this session.
- Multiple background-capable components were present and were treated as backdoor candidates under the user's strict standard.
- Historical Microsoft Defender detections showed prior contact with high-risk software and installers.
- Third-party software remnants and permissive firewall rules were present for Baidu Netdisk, QQ/QQNT, Thunder, and LuDaShi.

## Actions Performed
### Service hardening
- Disabled and stopped `sshd`
- Disabled and stopped `DiagTrack`
- Disabled and stopped `WpnService`
- Disabled and stopped `CDPSvc`
- Repeatedly stopped `WpnUserService_*` and `CDPUserSvc_*` where possible
- Disabled and removed `BaiduNetdiskUtility`
- Disabled and stopped `ArmouryCrateControlInterface`

### Startup reduction
- Removed login auto-start entries for:
  - OneDrive
  - GoogleDriveFS
  - LM Studio

### Firewall containment
- Removed active firewall allow rules tied to:
  - Baidu Netdisk
  - QQ / QQNT
  - Thunder
  - LuDaShi

### Software and residue cleanup
- Removed residual directories:
  - `C:\Users\admin\AppData\Local\Temp\ThunderEv`
  - `C:\Users\admin\AppData\Local\Temp\XLLiveUD`
  - `C:\Users\admin\AppData\Local\Temp\OnlineInstall`
  - `C:\Users\admin\AppData\Local\Temp\ThunderUninstall`
  - `C:\Program Files (x86)\LuDaShi`
- Removed main program directories:
  - `C:\Users\admin\AppData\Roaming\baidu\BaiduNetdisk`
  - `C:\Program Files\Tencent\QQNT`
  - `E:\Thunder`
- Stopped OneDrive residual process `FileCoAuth.exe`

### Browser extension cleanup
Removed high-permission Chrome extensions:
- `ncennffkjdiamlpmcbajkmaiiiddgioo` (Thunder-related)
- `fcoeoabgfenejglbffodgkkbkcdhcgfn` (Claude)
- `dpoljalgoeeedhiafbfkgdomfknebheh` (ChatPDF - ChatGPT to PDF)
- `jfgfiigpkhlkbnfnbobbkinehhfdhndo`
- `npdkkcjlmhcnnaoobfdjndibfkkhhdfn`
- `hdhinadidafjejdhmfkjgnolgimiaplp`

### Scheduled task hardening
Disabled these scheduled tasks:
- `ASUS Optimization 36D18D69AFC3`
- `ASUS Update Checker 2.0`
- `AsusSystemAnalysis_754F3273-0563-4F20-B12F-826510B07474`
- `AsusSystemDiagnosis_DriverQuality`
- `OneDrive Reporting Task-S-1-5-21-835720170-2271154569-687464624-1001`
- `OneDrive Standalone Update Task-S-1-5-21-835720170-2271154569-687464624-1001`
- `OneDrive Startup Task-S-1-5-21-835720170-2271154569-687464624-1001`
- `MicrosoftEdgeUpdateTaskMachineCore`
- `MicrosoftEdgeUpdateTaskMachineUA`
- `GoogleUpdaterTaskSystem147.0.7703.0{ED27931F-2F1F-4471-8C8A-9774EC26CCA0}`

## Hidden Persistence Review
- No suspicious WMI `CommandLineEventConsumer` objects were found.
- WMI bindings observed were consistent with system event log behavior, not a hidden command execution chain.
- No suspicious PowerShell profile scripts were found.
- The user Startup folder contained only `desktop.ini`.
- No clearly malicious hidden scheduled task chain was found.

## Final State
### Cleared or heavily reduced
- Baidu Netdisk
- QQ / QQNT
- Thunder / Xunlei
- LuDaShi
- OneDrive auto-start and scheduled task activity
- Armoury Crate control interface and ASUS update tasks
- Edge updater scheduled tasks
- Google updater scheduled task
- Multiple high-permission Chrome extensions

### Still present by user choice
- Geph / `gephgui-wry.exe`
- Codex / `codex.exe`
- VirtualBox / `VirtualBoxVM.exe`

These components may still produce unattended background traffic by design.

### Still present by system design
- `WpnUserService_*`
- `CDPUserSvc_*`
- core Windows and browser networking components

The two user-level services above can be stopped temporarily but were not permanently set to `Disabled` due Windows service restrictions.

## Verification Summary
Post-cleanup checks showed:
- no active firewall rules remained for removed Baidu/QQ/Thunder/LuDaShi paths
- no scheduled tasks remained active for the disabled ASUS, OneDrive, Edge updater, and Google updater items
- no remaining service registration for `BaiduNetdiskUtility`
- deleted Chrome extension folders did not reappear during the session
- no obvious hidden WMI persistence chain was found

## Overall Assessment
- Explicit Chinese big-tech software remnants targeted in this session were largely removed.
- No strong evidence of a hidden unknown malware persistence chain was found in the areas inspected.
- Remaining background risk is now concentrated in:
  - user-retained networking tools
  - normal Windows background services
  - browser/network stack behavior
  - OEM support components that were intentionally left untouched when they risked input-device impact

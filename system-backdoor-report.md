# System Backdoor Report

Generated: 2026-03-13 02:21:32 +08:00
Host: Windows machine inspected from local shell

## Scope
This report treats the following as suspicious under the user's standard:
- unattended background network traffic
- unattended collection of system, IP, proxy, or network information
- background persistence or auto-start behavior
- residual software or firewall permissions from previously installed third-party software

## Core Findings
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
- Stopped `WpnUserService_*` and `CDPUserSvc_*` where possible
- Disabled and removed `BaiduNetdiskUtility`

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

### Browser extension cleanup
Removed high-permission Chrome extensions:
- `ncennffkjdiamlpmcbajkmaiiiddgioo` (Thunder-related)
- `fcoeoabgfenejglbffodgkkbkcdhcgfn` (Claude)
- `dpoljalgoeeedhiafbfkgdomfknebheh` (ChatPDF - ChatGPT to PDF)

## Residual Risk
The following were intentionally left in place because the user depends on them:
- Geph / `gephgui-wry.exe`
- Codex / `codex.exe`
- VirtualBox / `VirtualBoxVM.exe`

These components may still produce unattended background traffic by design.

## Verification Summary
Post-cleanup checks showed:
- no active firewall rules remained for the removed Baidu/QQ/Thunder/LuDaShi paths
- no scheduled tasks remained referencing those software names
- no remaining service registration for `BaiduNetdiskUtility`
- deleted Chrome extension folders did not reappear during the session

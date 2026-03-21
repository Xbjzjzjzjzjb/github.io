# System Blacklist Hardening Notes

Date: 2026-03-21
Host: Windows
Scope: LuDaShi and 2345 family unwanted software hardening

## 1. LuDaShi Cleanup

### 1.1 Processes terminated

- `CefView.exe` from `C:\Program Files (x86)\LuDaShi\Utils\cef69\`
- `index_service.exe` from `C:\Program Files (x86)\LuDaShi\softmgr\`
- `start_menu_pro.exe` from `C:\Program Files (x86)\LuDaShi\SuperApp\start_menu_pro\`

### 1.2 Paths removed

- `C:\Program Files (x86)\LuDaShi`
- `C:\Users\admin\AppData\Roaming\Ludashi`
- `C:\Users\admin\AppData\Local\Temp\Basic\ludashi`

### 1.3 Registry removed

- `HKCU\Software\Ludashi`

## 2. HP DeskJet 1110 Bundle Cleanup

### 2.1 Temporary payload removed

- `C:\Users\admin\Downloads\HP_DJ1110_Series_Driver.exe`
- `C:\Users\admin\AppData\Local\Temp\HP_DJ1110_Series_Driver`

### 2.2 Driver packages removed from driver store

- `oem83.inf` -> `hp1100.inf`
- `oem60.inf` -> `hpygid20.inf`
- `oem20.inf` -> `hpreststub.inf`
- `oem39.inf` -> `hpwinusbstub.inf`
- `oem73.inf` -> `mvusbews.inf`
- `oem53.inf` -> `nullprint.inf`

## 3. LuDaShi Execution Blacklist

### 3.1 IFEO execution interception

Root:

- `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options`

Applied `Debugger = C:\Windows\System32\cmd.exe /c exit 1` to:

- `LuDaShi.exe`
- `LuDaShiSvc.exe`
- `ComputerZ.exe`
- `ComputerZ_dl.exe`
- `ComputerZService.exe`
- `index_service.exe`
- `start_menu_pro.exe`
- `softmgr.exe`
- `softmgrupdate.exe`
- `LDSLive.exe`
- `LDSGameMaster.exe`
- `LDSNews.exe`

### 3.2 Blocked landing directories

Directories created or retained as blocked stubs:

- `C:\Program Files (x86)\LuDaShi`
- `C:\Users\admin\AppData\Roaming\Ludashi`

ACL strategy:

- allow full control for `Administrators`
- allow full control for `SYSTEM`
- deny `Users` execute and read-execute

## 4. 2345 Family Blacklist

### 4.1 Product families covered

- 2345 Browser
- 2345 Security / PCSafe
- 2345 Pic Viewer
- 2345 PDF / OCR
- 2345 Input
- HaoZip

### 4.2 IFEO execution interception

Applied `Debugger = C:\Windows\System32\cmd.exe /c exit 1` to:

- `2345Browser.exe`
- `2345Explorer.exe`
- `2345SoftMgr.exe`
- `2345SafeCenter.exe`
- `2345SafeGuard.exe`
- `2345Security.exe`
- `2345PicViewer.exe`
- `2345OCR.exe`
- `2345PDF.exe`
- `2345Input.exe`
- `2345InputSvc.exe`
- `2345MPCSafe.exe`
- `2345MiniBrowser.exe`
- `HaoZip.exe`
- `HaoZipC.exe`
- `HaoZipSvc.exe`
- `PicViewer.exe`
- `PCSafe.exe`
- `PCSafeSvc.exe`
- `SoftMgr.exe`
- `2345BrowserProtect.exe`

### 4.3 Blocked landing directories

- `C:\Program Files\2345`
- `C:\Program Files (x86)\2345`
- `C:\Program Files\2345Soft`
- `C:\Program Files (x86)\2345Soft`
- `C:\Program Files\HaoZip`
- `C:\Program Files (x86)\HaoZip`
- `C:\Users\admin\AppData\Roaming\2345Soft`
- `C:\Users\admin\AppData\Roaming\2345Explorer`
- `C:\Users\admin\AppData\Roaming\2345Pic`
- `C:\Users\admin\AppData\Roaming\HaoZip`

ACL strategy:

- allow full control for `Administrators`
- allow full control for `SYSTEM`
- deny `Users` execute and read-execute

### 4.4 Firewall egress blocks

Added outbound block rules for:

- `C:\Program Files\2345\*`
- `C:\Program Files (x86)\2345\*`
- `C:\Program Files\HaoZip\*`
- `C:\Program Files (x86)\HaoZip\*`
- `C:\Users\admin\AppData\Roaming\2345Soft\*`
- `C:\Users\admin\AppData\Roaming\2345Pic\*`
- `C:\Users\admin\AppData\Roaming\HaoZip\*`

Rule names:

- `Block 2345 Program Files`
- `Block 2345 Program Files x86`
- `Block HaoZip Program Files`
- `Block HaoZip Program Files x86`
- `Block 2345 Roaming 2345Soft`
- `Block 2345 Roaming 2345Pic`
- `Block 2345 Roaming HaoZip`

## 5. Verification Summary

- No active LuDaShi processes after cleanup
- No active 2345 / HaoZip / PCSafe processes detected during final verification
- LuDaShi residual directories removed, then re-created only as blocked stubs
- HP DeskJet 1110 installer payload and related driver packages removed
- IFEO interception keys confirmed present for both LuDaShi and 2345 family executables

## 6. Follow-up Options

- export all blacklist registry keys as `.reg`
- export firewall rules as a reusable script
- migrate this note into a Git repository and commit it with host/date metadata

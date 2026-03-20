# Reboot Root Cause Report

Generated: 2026-03-20 10:07:39 +08:00
Host: DESKTOP-U48SQTG

## Executive Summary

The unexpected reboot on 2026-03-20 was not a normal user-initiated or update-orchestrated restart.
The strongest available evidence points to a hardware-link failure on the PCIe/NVMe path for the secondary WD Green SN350 500GB drive on `E:`.

This is not proven down to a single replaceable part, but the failure domain is narrow:

1. `WD Green SN350 500GB 2G0C` itself
2. The M.2 slot / seating / contact for that drive
3. The motherboard PCIe root port feeding that slot

Pure application/software failure is not supported by the logs.

## Timeline

### Current incident

- `2026-03-20 09:34:53`
  - `WHEA-Logger`, Event ID `17`
  - Corrected hardware error on `PCI Express Root Port`
  - Root port device: `PCI\VEN_1022&DEV_14BA&SUBSYS_14C31043&REV_00`
  - Bus location: `PCIROOT(0)#PCI(0204)` / `ACPI(GPP8)`
- `2026-03-20 09:37:38`
  - Later recorded as the timestamp of the unexpected shutdown
- `2026-03-20 09:44:09`
  - OS boot start
- `2026-03-20 09:44:11`
  - `Kernel-Power`, Event ID `41`
  - System rebooted without clean shutdown
- `2026-03-20 09:44:19`
  - `EventLog`, Event ID `6008`
  - Previous shutdown at `2026-03-20 09:37:38` was unexpected

### Historical pattern

- Repeated `WHEA-Logger` Event ID `17` entries are present across March 2026 on the same root port:
  - `PCI\VEN_1022&DEV_14BA...`
  - `PCIROOT(0)#PCI(0204)` / `GPP8`
- Additional unexpected reboot entries also occurred on:
  - `2026-03-20 08:22:29`
  - `2026-03-19 08:45:22`

## What Was Ruled Out

- No normal restart chain for this incident:
  - No `User32 1074` around the event
  - No normal shutdown events (`6006`, kernel shutdown chain) before the reboot
- No evidence of a standard Windows Update planned restart in the event window
- No NTFS corruption was detected on `E:`
  - `Repair-Volume -DriveLetter E -Scan` returned `NoErrorsFound`
- No filesystem-level error events were found tying `E:` to NTFS damage

## Device Mapping

### Physical disks

- `Disk 0`
  - Model: `WD Green SN350 500GB 2G0C`
  - Serial: `E823_8FA6_BF53_0001_001B_444A_4142_4330.`
  - Bus: `NVMe`
  - Health: `Healthy`
  - Not system disk
  - Contains `E:`
- `Disk 1`
  - Model: `WD PC SN740 SDDPNQD-512G-1002`
  - Serial: `E823_8FA6_BF53_0001_001B_448B_47EB_2AE9.`
  - Bus: `NVMe`
  - Health: `Healthy`
  - System disk: `IsBoot=True`, `IsSystem=True`
  - Contains `C:` and `D:`

### Controller / slot mapping

- NVMe controller on the failing path:
  - `PCI\VEN_15B7&DEV_5017&SUBSYS_501715B7&REV_01`
  - Friendly name: `Standard NVM Express Controller`
  - Location: `PCIROOT(0)#PCI(0204)#PCI(0000)`
- That path is downstream of:
  - `PCI\VEN_1022&DEV_14BA&SUBSYS_14C31043&REV_00`
  - Friendly name: `PCI Express Root Port`
  - Location: `PCIROOT(0)#PCI(0204)` / `ACPI(GPP8)`

Conclusion: `DEV_5017` is the controller path for the WD Green SN350, not the system drive.

## Storage / SMART-Like Indicators Collected

Windows built-in reliability counters showed:

- `WD Green SN350 500GB 2G0C`
  - Temperature: `32C`
  - TemperatureMax: `80C`
  - No explicit media errors reported by the queried Windows counters
- `WD PC SN740 SDDPNQD-512G-1002`
  - Temperature: `29C`
  - TemperatureMax: `84C`
  - No explicit media errors reported by the queried Windows counters

Important limitation:

- Windows built-in storage counters did not expose a decisive SMART failure bit or media error total here.
- That does not clear the hardware path, because the strongest signal is the repeated PCIe root-port WHEA error tied to the SN350 path.

## Filesystem Findings

### Volumes

- `C:` = OS volume on system disk
- `D:` = data volume on system disk
- `E:` = data volume on `WD Green SN350`

### E: checks

- `Volume E: (\Device\HarddiskVolume2) is healthy` appears repeatedly in NTFS info events
- `fsutil fsinfo volumeinfo E:` showed a normal writable NTFS volume
- `Repair-Volume -DriveLetter E -Scan` returned `NoErrorsFound`

Interpretation:

- The issue is below the filesystem layer, not a simple NTFS corruption problem.

## Crash-Dump Notes

- Crash control is configured for kernel dumps / minidumps:
  - `CrashDumpEnabled = 3`
  - `AutoReboot = 1`
  - `DumpFile = C:\WINDOWS\MEMORY.DMP`
  - `MinidumpDir = C:\WINDOWS\Minidump`
- However, repeated `volmgr 161` events show dump creation failures on prior crashes
- That prevented deeper attribution for some incidents

## Confidence Assessment

### High confidence

- The reboot was abnormal, not a normal restart
- The incident involved a hardware-level PCIe error on the root port feeding the SN350 path
- The affected path belongs to the secondary `WD Green SN350` on `E:`

### Medium confidence

- The SN350 drive itself is the most likely failing component

### Still possible

- Bad seating / oxidation / mechanical contact issue in the M.2 slot
- Motherboard slot or root-port instability
- Lower-level storage/chipset driver interaction amplifying a hardware link issue

## Recommended Action Order

1. Back up any important data from `E:` immediately.
2. Power off and reseat the `WD Green SN350`.
3. If the machine has another compatible M.2 slot, swap slot positions with the other NVMe drive for isolation testing.
4. If the same WHEA root-port pattern follows the SN350, replace the SN350.
5. If the error stays with the slot/root-port instead, investigate motherboard slot or PCIe path stability.

## Replace vs Reseat Judgment

Current call:

- Do **not** trust the SN350 path as stable.
- Back up now.
- It is reasonable to try **one** reseat / slot-swap test first.
- If the same event pattern repeats after reseat or after moving the drive, the practical answer is **replace the WD Green SN350**.

## Commands / Checks Performed

- Boot and reboot event review
- System / Application event correlation around `2026-03-20 09:37` to `09:45`
- WHEA hardware error review
- Disk / partition / volume mapping
- PCIe location-path mapping for NVMe controllers and root ports
- Windows storage reliability counters
- `fsutil fsinfo volumeinfo E:`
- `Repair-Volume -DriveLetter E -Scan`

# Current Status

> Public-safe status snapshot: **15 September 2026**.

## Executive Status
DroneOS is currently an **integrated technical MVP / pre-physical-validation platform** with a canonical Solar Recon→Inspection→Report workflow, real PX4 SITL two-flight execution, a target-hardware NVIDIA Jetson Field Box validation and a redesigned operator dashboard.

The private engineering source of truth is `DroneOS-Core`. PX4 remains the flight authority. DroneOS remains the mission, workflow, data, operator and reporting layer above PX4.

The key September milestone is that the **complete canonical Solar software workflow has now been exercised end to end with DroneOS running on the Jetson Field Box**, while PX4 SITL/Gazebo runs remotely on a separate computer.

## Current Engineering Baseline

### Canonical Solar Backend
The current canonical backend flow covers:

`Start Solar`
→ Recon planning/staging
→ Flight A PX4 execution
→ Recon postflight acceptance
→ `PanelMap`
→ exact Inspection proposal
→ operator confirmation
→ Flight B staging
→ Flight B PX4 execution
→ Inspection postflight acceptance
→ evidence/findings
→ `REPORT_READY`
→ canonical report

The latest canonical Solar E2E backend milestone was validated with:

- **1,885 Python safe tests passed**
- **82 dashboard runtime checks passed** at that backend milestone
- focused canonical workflow/report validation
- real PX4/Gazebo Flight A and Flight B execution

### Field Box
Validated on **NVIDIA Jetson Orin Nano Super**:

- ARM64 runtime
- native Docker baseline and non-root execution
- authenticated API and WebSocket over LAN
- remote PX4/MAVSDK connection over LAN
- mission upload/start and live telemetry return
- complete Solar software E2E through both flights and canonical report
- explicit deterministic Recon/Inspection demo providers used for the current simulator data lane

See [Field Box Validation](fieldbox_validation.md).

### Operator Dashboard
The current dashboard redesign has been validated on Jetson and laptop with **83 dashboard runtime checks**.

Validated UI direction:

- Solar workflow is the primary operator workspace
- visual Setup→Recon→Process→Review→Inspection→Report stepper
- contextual Solar actions
- always-visible flight, recovery, command and vehicle-status controls
- dominant map/HUD workspace
- non-routine tools moved into Advanced sections
- credential-free OpenStreetMap basemap for the current MVP/demo setup

This UI work changes presentation and operator hierarchy only; it does not change PX4 command behavior, mission authority, StateService or Solar backend semantics.

See [Operator Dashboard Validation](operator_dashboard_validation.md).

## Solar Workflow Status
The software workflow is now validated end to end on the target Field Box platform:

- workflow creation and exact identity binding
- Flight A Recon staging/execution
- trusted Recon handoff/acceptance
- Recon analysis → `PanelMap`
- immutable provenance
- exact Inspection proposal
- explicit operator confirmation
- Flight B staging/execution
- trusted Inspection handoff/acceptance
- evidence/findings
- canonical report publication

Important: the current full E2E lane uses **real PX4 SITL execution** for both flights but **deterministic demo sensor/media data** for Recon and Inspection postflight inputs.

## Readiness Assessment

| Component | Status | Notes |
|---|---|---|
| Core mission/safety architecture | Advanced / validated software baseline | Authority-aware lifecycle, identity and recovery boundaries |
| Solar backend E2E | **Validated** | Canonical Recon→Inspection→Report flow |
| Jetson Field Box | **Full software E2E validated** | Complete Solar flow on target edge computer with remote PX4 SITL |
| Operator dashboard | **Validated review baseline** | New mission-control UI tested on Jetson/laptop; final integration review ongoing |
| Real PX4 SITL Flight A→B | **Validated** | Both missions execute via PX4/MAVSDK AUTO |
| Trusted provenance/reporting | **Validated software baseline** | Exact workflow/mission/data lineage |
| Vehicle Agent Lite | Simulated/local | Real onboard process/network path pending |
| Real camera end-to-end capture | Pending | Next physical data boundary |
| PX4 hardware bench | Pending | No-props validation next |
| Physical flight | Pending | No real-aircraft flight claim yet |
| Real Solar site workflow | Pending | Physical Recon→Inspection evidence still required |
| Thermal defect detection | R&D | Not production-validated |
| Commercial operations | Not ready | Field/regulatory/pilot evidence still required |

## Current Limitations
- no physical-aircraft flight validation yet
- no real Vehicle Agent Lite + camera + vehicle-network pipeline validated end to end
- deterministic demo media/data is still used in the current full simulator lane
- no survey-grade PanelMap accuracy claim
- no production RGB/thermal defect detector claim
- full process-restart durability is not yet complete for every in-memory workflow artifact
- no certification or commercial-operation claim

## Current Product Position
The correct current positioning is:

> **DroneOS is an integrated technical MVP entering physical validation: the canonical Solar Recon→Inspection→Report workflow runs end to end on the NVIDIA Jetson Field Box around real PX4 SITL mission execution, with a validated operator dashboard and explicit deterministic demo sensor data. Physical UAV/camera validation, certification and commercial readiness remain pending.**

## Next Validation Boundary
The next major step is **hardware-backed physical validation**:

1. real Vehicle Agent Lite + camera/data path
2. PX4 hardware no-props bench
3. controlled first physical flight
4. physical Flight A Recon + trusted transfer
5. real PanelMap + operator-reviewed Flight B proposal
6. physical Flight B Inspection
7. real evidence/report and repeatability evaluation

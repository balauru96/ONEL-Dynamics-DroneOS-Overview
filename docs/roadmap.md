# Development Roadmap

> Updated: **15 September 2026**.

DroneOS development is organized around **validation gates**, not feature count. PX4 remains flight authority; DroneOS evolves as the mission, workflow, data and operator layer above it.

## Current Phase
**Integrated technical MVP validated on Jetson → physical hardware integration and field validation.**

The simulator/software composition problem is no longer the primary unknown. The next major unknown is whether the same architecture remains reliable across real flight-controller hardware, onboard compute, camera timing, network transfer and controlled aircraft operation.

## Completed / Validated Milestones

### Phase 1 — Core Lab/SITL Stabilization ✅
- mission lifecycle and telemetry freshness hardening
- fail-closed command gating
- mission/geofence revision identity protection
- deterministic safe-test lane and CI

### Phase 2 — Jetson Field Box Baseline ✅
- NVIDIA Jetson Orin Nano Super selected as primary Field Box
- ARM64 runtime validated
- Docker/non-root baseline validated
- authenticated local/LAN operation validated

### Phase 3 — Solar Data Contracts and Reporting ✅
- Recon capture/replay contracts
- Inspection evidence/findings contracts
- canonical Solar report
- manifest/path/checksum validation
- trusted ingestion boundaries

### Phase 4 — Solar Perception / World-Model Prototype ✅
- detector abstraction
- optional offline YOLO adapter
- image-to-ground projection support
- deterministic cross-frame fusion
- `PanelMap` generation
- Inspection proposal generation

No survey-grade mapping claim is made.

### Phase 5 — Deterministic Solar E2E ✅
Validated software composition:

Recon → trusted acceptance → analysis → PanelMap → proposal → confirmation → Inspection → evidence → findings → report

### Phase 6 — Real PX4 SITL Flight A → Flight B ✅
Validated through real PX4 SITL / Gazebo / MAVSDK AUTO:

- Flight A `SOLAR_RECON`
- completion + terminal handoff
- Recon analysis → `PanelMap`
- exact Inspection proposal
- operator confirmation
- Flight B `SOLAR_INSPECTION`
- completion + terminal handoff

### Phase 7 — Canonical A→B→Report Backend ✅
Completed and promoted into the current canonical backend baseline:

- workflow/provenance ledger
- exact workflow/read-model identity
- server-owned Recon and Inspection postflight processing
- explicit demo-data providers isolated from production/default behavior
- canonical `REPORT_READY` state
- authenticated exact-workflow report endpoint
- operator confirmation stages Flight B only; it never auto-launches Flight B
- **1,885 Python safe tests passed** on the completed milestone

### Phase 8 — Full Jetson Field Box Solar E2E ✅
Validated on the target edge computer:

- DroneOS running on NVIDIA Jetson Orin Nano Super
- PX4 SITL + Gazebo on a separate computer
- LAN MAVLink/MAVSDK mission execution
- live telemetry return
- full Solar operator flow from workflow creation through canonical report
- both PX4 missions executed through real SITL
- deterministic Recon/Inspection demo data used for the sensor/media lane

### Phase 9 — Operator Dashboard MVP ✅ / FINAL REVIEW
Validated on Jetson and laptop:

- Solar-first operator workspace
- visual workflow stepper
- clearer action hierarchy
- always-visible flight/recovery/status controls
- dominant map/HUD
- Advanced grouping for non-routine tools
- credential-free MVP basemap
- **83 dashboard runtime checks passed**

This phase is UI/UX-only; backend/flight authority is unchanged. Final integration review remains separate from the successful Jetson validation.

## Next Milestones

### Phase 10 — Vehicle Agent Lite + Real Camera Path 🔜
- run Vehicle Agent Lite on real onboard compute
- connect/calibrate the first real camera
- bind captures to exact mission execution identity
- transfer datasets over the real vehicle↔Field Box network path
- preserve manifest/checksum/authority guarantees
- validate retry, interruption and failure behavior

### Phase 11 — PX4 Hardware Bench 🔜
- integrate real PX4-compatible flight-controller hardware
- no-props validation first
- telemetry and mission upload
- power/network checks
- RC/manual recovery verification
- failsafe behavior documented before flight

### Phase 12 — First Controlled Physical Flight
- bounded waypoint mission first
- operator supervision and manual recovery path available
- capture PX4 logs and DroneOS telemetry
- compare physical behavior against SITL assumptions

### Phase 13 — Physical Solar Flight A Recon
- real Recon route
- real camera capture
- real Vehicle Agent Lite dataset finalization
- trusted transfer to Field Box
- real-data `PanelMap`

### Phase 14 — Physical Solar Flight B Inspection
- generate proposal from real Recon result
- operator review/confirmation
- real Inspection flight
- trusted Inspection transfer
- evidence/findings/report

### Phase 15 — Pilot-Quality Solar Evaluation
- repeatability across multiple runs
- panel mapping accuracy metrics
- capture completeness
- workflow reliability/failure recovery
- customer-readable report quality
- pilot/LOI/customer feedback

### Phase 16 — Thermal / Defect Detection R&D
Only after the physical RGB/data path is stable:

- thermal payload integration
- labeled defect dataset
- measured detection baseline
- confidence/calibration and human review
- edge inference optimization

### Phase 17 — Platform Expansion
Only after physical Solar proof:

- richer world-model providers
- event-driven mission proposals
- multiple sites/mission types
- optional fleet/cloud synchronization
- later verticals such as wind, infrastructure, agriculture, search and rescue, logistics and dock-based operations

These are platform directions, not current commercial claims.

## Strategic Rule for the Next Phase
The project should now resist unnecessary software scope expansion.

The highest-value sequence is:

**validated software baseline → real hardware bench → first flight → real Recon → real Inspection → real report → repeatable pilot evidence**

New platform features should not displace this validation sequence unless they fix a true safety/blocking issue.

## Validation Principles
Every milestone should continue to require:

- explicit authority ownership
- fail-closed identity handling
- deterministic tests before hardware tests
- SITL before physical flight for flight-facing changes
- documented limitations and non-claims
- operator recovery path
- auditable provenance where workflow decisions depend on prior data

## Public Positioning
Current public positioning:

- integrated technical MVP / pre-physical-validation
- canonical Solar Recon→Inspection→Report E2E validated
- full software workflow validated on NVIDIA Jetson Field Box
- real PX4 SITL two-flight execution validated
- redesigned operator dashboard validated
- physical aircraft/camera workflow, certification and commercial readiness remain pending

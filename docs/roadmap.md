# Development Roadmap

> Updated: **3 September 2026**.

DroneOS development is organized around validation gates rather than feature count. PX4 remains flight authority; DroneOS evolves as the mission, workflow, data and operator layer above it.

## Current Phase
**Integrated Solar MVP backend + real PX4 SITL validation → hardware-backed field integration.**

The earlier Lab/SITL stabilization, Jetson bootstrap and first two-flight simulator milestones have been reached. The next major boundary is physical vehicle/camera integration and controlled flight validation.

## Completed / Validated Milestones

### Phase 1 — Core Lab/SITL Stabilization ✅
- mission lifecycle and telemetry freshness hardening
- fail-closed command gating
- mission/geofence revision identity protection
- dashboard runtime verification
- deterministic safe-test lane and CI

### Phase 2 — Jetson Field Box Baseline ✅
- NVIDIA Jetson Orin Nano Super selected as primary Field Box platform
- reproducible ARM64/Python 3.12 bootstrap validated
- safe-suite parity validated on Jetson
- Docker aligned to backend/dashboard only

### Phase 3 — Solar Data Contracts and Reporting ✅
- Recon capture/replay contracts
- Inspection evidence and findings contracts
- deterministic SolarInspectionReport
- strict local manifest/media integrity validation
- SHA-256 integrity checks

### Phase 4 — Solar Vision / Mapping Prototype ✅
- detector abstraction
- optional offline YOLO adapter
- image-to-ground projection
- deterministic cross-frame panel fusion
- PanelMap generation
- InspectionPlan generation

This is an engineering prototype baseline; no survey-grade mapping claim is made.

### Phase 5 — Deterministic Solar E2E ✅
Validated offline:

Recon
→ data handoff
→ detection/projection/fusion
→ PanelMap
→ InspectionPlan
→ Inspection mission
→ evidence/findings
→ report

### Phase 6 — Real PX4 SITL Flight A → Flight B ✅
Validated through real PX4 SITL / Gazebo / MAVSDK AUTO execution:

- Flight A Solar Recon
- completion + LAND + terminal handoff
- Recon analysis → PanelMap
- exact Inspection proposal
- explicit operator confirmation
- Flight B Solar Inspection
- completion + terminal handoff

### Phase 7 — Integrated A→B→Report Workflow Backend ✅ / ACTIVE HARDENING
Implemented:

- immutable Solar workflow/provenance ledger
- accepted Recon → PanelMap → Inspection proposal workflow service
- exact operator-confirmation/staging boundary
- Inspection dataset → findings → canonical report workflow service
- workflow read model/API
- exact Recon mission/workflow identity binding
- trusted Recon ingestion wired into workflow processing
- real PX4 SITL A→B→Report integration gate

This integration line remains subject to promotion into the stable baseline after review/validation.

## Next Milestones

### Phase 8 — Vehicle Agent Lite + Real Camera Path 🔜
- run a real onboard Vehicle Agent Lite process
- bind camera captures to the exact mission execution identity
- transfer datasets over the real vehicle↔Field Box network path
- preserve checksum, manifest and authority guarantees across the physical transport boundary
- validate restart/cancellation/failure behavior

### Phase 9 — PX4 Hardware Bench 🔜
- connect real PX4 autopilot hardware
- no-props validation
- MAVLink telemetry and mission upload
- failsafe and RC/manual recovery verification
- power/network/Field Box operational checks

### Phase 10 — First Controlled Physical Flight
- simple bounded waypoint validation first
- operator supervision and manual recovery path available
- collect PX4 logs and DroneOS workflow telemetry
- compare real behavior against SITL assumptions

### Phase 11 — Physical Solar Recon → Inspection Workflow
- real Flight A capture
- Field Box Recon analysis
- operator-reviewed Inspection proposal
- real Flight B execution
- real evidence transfer
- local report generation

### Phase 12 — Pilot-Quality Solar Evaluation
- real solar-site dataset
- panel mapping accuracy metrics
- capture completeness metrics
- workflow reliability / failure recovery metrics
- customer-readable report quality
- repeatability across multiple missions/sites

### Phase 13 — Thermal / Defect Detection R&D
Only after the physical data pipeline is stable:

- thermal payload integration
- measured defect detection baseline
- labeled dataset and evaluation methodology
- confidence/calibration and human review
- edge inference optimization

No production defect-detection claim should precede measured validation.

### Phase 14 — Cloud / Fleet Platform
After local Field Box operation is dependable:

- optional report synchronization
- fleet analytics
- multi-site management
- centralized model/data lifecycle
- customer APIs and business integrations

## Strategic Product Direction
Solar inspection is the first vertical used to prove the platform architecture. The longer-term direction is a reusable mission operations platform for inspection, infrastructure, logistics and other autonomous drone workflows, while preserving a strict boundary between mission intelligence and PX4 flight control.

## Validation Principles
Every milestone should continue to require:

- explicit authority ownership
- fail-closed identity handling
- deterministic tests before hardware tests
- SITL before physical flight for changed flight-facing behavior
- documented limitations and non-claims
- operator recovery path
- immutable or auditable provenance where workflow decisions depend on prior data

## Public Claims
Current public positioning should say:

- integrated engineering prototype
- Jetson Field Box engineering baseline validated
- real PX4 SITL two-flight Solar workflow validated
- backend Recon→Inspection→Report workflow integrated
- physical flight, production camera pipeline, certification and commercial readiness are still pending

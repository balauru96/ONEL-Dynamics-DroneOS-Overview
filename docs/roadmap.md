# Development Roadmap

> Updated: **6 September 2026**.

DroneOS development is organized around validation gates rather than feature count. PX4 remains flight authority; DroneOS evolves as the mission, workflow, data and operator layer above it.

## Current Phase
**Integrated Solar MVP + real PX4 SITL + distributed Jetson Field Box validation → hardware-backed field integration.**

The earlier Lab/SITL stabilization, Jetson bootstrap and first two-flight simulator milestones have been reached. The next major boundary is physical vehicle/camera integration and controlled flight validation.

## Completed / Validated Milestones

### Phase 1 — Core Lab/SITL Stabilization ✅
- mission lifecycle and telemetry freshness hardening
- fail-closed command gating
- mission/geofence revision identity protection
- deterministic safe-test lane and CI

### Phase 2 — Jetson Field Box Baseline ✅
- NVIDIA Jetson Orin Nano Super selected as primary Field Box platform
- ARM64 runtime validated
- native Docker build validated
- non-root runtime validated
- authenticated local/LAN operation validated

### Phase 3 — Solar Data Contracts and Reporting ✅
- Recon capture/replay contracts
- Inspection evidence and findings contracts
- deterministic SolarInspectionReport
- strict manifest/media integrity validation
- SHA-256 integrity checks

### Phase 4 — Solar Vision / Mapping Prototype ✅
- detector abstraction
- optional offline YOLO adapter
- image-to-ground projection
- deterministic cross-frame panel fusion
- PanelMap generation
- InspectionPlan generation

No survey-grade mapping claim is made.

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
Implemented in the current development line:

- immutable Solar workflow/provenance ledger
- accepted Recon → PanelMap → Inspection proposal workflow service
- exact operator-confirmation/staging boundary
- Inspection dataset → findings → canonical report workflow service
- workflow read model/API
- exact Recon mission/workflow identity binding
- trusted Recon ingestion wired into workflow processing
- real PX4 SITL A→B→Report integration gate

Promotion into stable baselines remains gated by review and regression validation.

### Phase 8 — Distributed Field Box Validation ✅
Validated in September 2026:

- DroneOS running natively on NVIDIA Jetson Orin Nano / ARM64
- Docker non-root runtime
- authenticated API + WebSocket over LAN
- PX4 SITL + Gazebo on a separate computer
- remote PX4 mission upload/start over LAN
- live mission telemetry returned to the Jetson-hosted DroneOS runtime

This validates the intended separation between mission compute and flight execution in Lab/SITL. It does not replace physical hardware evidence.

## Next Milestones

### Phase 9 — Vehicle Agent Lite + Real Camera Path 🔜
- run a real onboard Vehicle Agent Lite process
- bind camera captures to exact mission execution identity
- transfer datasets over the real vehicle↔Field Box network path
- preserve checksum, manifest and authority guarantees
- validate restart/cancellation/failure behavior

### Phase 10 — PX4 Hardware Bench 🔜
- connect real PX4 autopilot hardware
- no-props validation
- MAVLink telemetry and mission upload
- failsafe and RC/manual recovery verification
- Field Box power/network operational checks

### Phase 11 — First Controlled Physical Flight
- simple bounded waypoint validation first
- operator supervision and manual recovery path available
- collect PX4 logs and DroneOS workflow telemetry
- compare real behavior against SITL assumptions

### Phase 12 — Physical Solar Recon → Inspection Workflow
- real Flight A capture
- Field Box Recon analysis
- operator-reviewed Inspection proposal
- real Flight B execution
- real evidence transfer
- local report generation

### Phase 13 — Pilot-Quality Solar Evaluation
- real solar-site dataset
- panel mapping accuracy metrics
- capture completeness metrics
- workflow reliability / failure recovery metrics
- customer-readable report quality
- repeatability across multiple missions/sites

### Phase 14 — Thermal / Defect Detection R&D
Only after the physical data pipeline is stable:

- thermal payload integration
- measured defect detection baseline
- labeled dataset and evaluation methodology
- confidence/calibration and human review
- edge inference optimization

### Phase 15 — Mission Orchestration Platform Expansion
Only after the local Solar workflow is physically proven:

- richer detection/world-model providers
- event-driven mission proposals
- multiple mission types and sites
- optional cloud synchronization and fleet analytics
- later support for other verticals such as wind, infrastructure, agriculture, search and rescue or logistics

These are platform directions, not current commercial claims.

## Strategic Product Direction
Solar inspection is the first vertical used to prove the platform architecture. The longer-term direction is a reusable mission-orchestration core built around the same controlled loop:

**observe → understand → propose → validate → execute → prove**

The platform can become more capable without moving flight-control authority out of PX4.

## Validation Principles
Every milestone should continue to require:

- explicit authority ownership
- fail-closed identity handling
- deterministic tests before hardware tests
- SITL before physical flight for changed flight-facing behavior
- documented limitations and non-claims
- operator recovery path
- auditable provenance where workflow decisions depend on prior data

## Public Claims
Current public positioning should say:

- advanced engineering prototype / pre-field-validation
- integrated Solar Recon→Inspection→Report workflow
- real PX4 SITL two-flight execution validated
- distributed NVIDIA Jetson Field Box validation completed
- physical flight, production camera pipeline, certification and commercial readiness remain pending

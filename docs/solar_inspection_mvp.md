# Solar Inspection MVP

> Updated: **3 September 2026**.

The Solar Inspection MVP is the first product workflow used to validate DroneOS as a mission operations platform above PX4.

The design deliberately uses **two separate flights** with a local post-flight processing boundary between them.

## Current Workflow

```text
Flight A — SOLAR_RECON
        ↓
landed / disarmed terminal handoff
        ↓
post-flight dataset transfer + integrity verification
        ↓
authoritative Recon dataset acceptance
        ↓
replay / detection / projection / fusion
        ↓
PanelMap
        ↓
non-executable Inspection proposal
        ↓
explicit operator confirmation
        ↓
Flight B — SOLAR_INSPECTION
        ↓
landed / disarmed terminal handoff
        ↓
Inspection dataset transfer + verification
        ↓
InspectionEvidence
        ↓
Findings
        ↓
SolarInspectionReport
```

PX4 remains the flight authority for both flights.

## What Is Implemented Today

### Flight A — Recon
- Solar Recon mission planning/staging
- mission identity/revision/geofence binding
- real PX4 SITL AUTO execution validation
- execution-qualified mission progress and completion handling
- terminal landed/disarmed handoff authorization
- simulated/local Vehicle Agent Lite capture and transfer boundary
- strict manifest, path and SHA-256 dataset verification
- authoritative dataset acceptance bound to the exact completed mission execution

### Recon Processing
- verified capture replay
- detector abstraction
- optional offline Ultralytics YOLO adapter
- external model SHA-256 verification
- altitude/FOV nadir flat-plane projection mode
- deterministic conservative cross-frame panel fusion
- authoritative `PanelMap` result

### Inspection Proposal
- deterministic InspectionPlan generation
- immutable, non-executable Solar Inspection proposal
- proposal fingerprint/provenance binding
- explicit proposal-specific operator confirmation
- authoritative Flight B staging

### Flight B — Inspection
- real PX4 SITL AUTO execution validation
- exact Flight B execution/proposal lineage preservation
- terminal handoff
- local/simulated Inspection capture and transfer
- accepted Inspection dataset bound to the completed execution

### Analysis / Report
- InspectionEvidence validation
- deterministic finding generation from an injected candidate provider
- canonical SolarInspectionReport
- deterministic report fingerprint
- immutable workflow/report provenance
- workflow read-model API

## End-to-End Validation Achieved
Two complementary E2E lanes exist:

### Deterministic offline E2E
Proves the full software/data composition from Recon through final report using deterministic fixtures.

### Real PX4 SITL A→B→Report
Proves both mission executions through real PX4 SITL/Gazebo/MAVSDK AUTO while the media/detection/evidence inputs remain deterministic local fixtures.

This distinction is important: **the mission execution is real SITL; the current camera/inspection sensor pipeline is not yet a real physical capture path.**

## Vision Model Status
An optional Solar YOLO adapter exists and has successfully loaded a verified external model artifact in an offline smoke test.

This is a prototype integration boundary, not a production mapping/defect-detection claim.

Current non-claims:

- no survey-grade geospatial panel mapping accuracy
- no validated thermal defect classification
- no production camera timing validation
- no real-flight inference authorization

## Workflow Provenance
The current workflow preserves traceability across:

- workflow identity
- Recon mission execution
- Recon dataset acceptance
- PanelMap
- Inspection proposal
- operator confirmation/staging
- Flight B execution
- Inspection dataset acceptance
- report fingerprint

The provenance ledger is not a replacement for StateService or PX4 mission authority.

## What Remains Before a Real Solar Pilot
1. real Vehicle Agent Lite process on the aircraft
2. real camera capture bound to mission identity
3. real vehicle↔Field Box transfer path
4. PX4 hardware no-props bench validation
5. first controlled physical flight
6. physical Flight A Recon processing
7. physical Flight B Inspection
8. real-site PanelMap accuracy evaluation
9. pilot-quality report evaluation
10. thermal/defect detection only after the physical data path is stable

## Product Principle
The goal is not to make DroneOS the low-level flight controller. The Solar MVP demonstrates the intended platform role:

**DroneOS decides and verifies the mission workflow and data lineage; PX4 executes the aircraft safely within its flight-control authority.**

# Solar Inspection MVP

> Updated: **15 September 2026**.

Solar Inspection is the **first product vertical** used to prove DroneOS as a reusable mission-orchestration, safety-state, trusted-data, operator and reporting platform above PX4.

The workflow is intentionally built around **two separate missions** with an authoritative post-flight processing boundary between them. The goal is not merely to fly a lawnmower route; it is to create a traceable inspection workflow where every mission, dataset, analysis result, proposal and report is tied to the exact execution that produced it.

PX4 remains flight authority. DroneOS owns the higher-level workflow, identity, safety gates, trusted data acceptance, orchestration and reporting.

![DroneOS Solar Inspection workflow](assets/solar-inspection-workflow.svg)

## Product Objective
The Solar workflow exercises the core DroneOS loop:

**discover → understand → plan → approve → execute → prove**

```text
Flight A — SOLAR_RECON
        ↓
terminal handoff
        ↓
trusted Recon transfer + validation
        ↓
authoritative Recon dataset acceptance
        ↓
detection / projection / fusion
        ↓
PanelMap
        ↓
exact non-executable Inspection proposal
        ↓
operator confirmation bound to exact proposal
        ↓
Flight B — SOLAR_INSPECTION
        ↓
terminal handoff
        ↓
trusted Inspection transfer + validation
        ↓
InspectionEvidence
        ↓
Findings
        ↓
canonical SolarInspectionReport
```

## Flight A — Recon / Mapping
Implemented engineering path:

- Solar Recon mission planning and staging
- mission identity/revision/geofence binding
- uploaded mission fingerprinting
- real PX4 SITL / Gazebo / MAVSDK AUTO execution
- mission progress observation
- terminal handoff
- manifest/path/telemetry/checksum validation
- trusted Recon dataset acceptance tied to the completed execution

A camera file is not automatically trusted evidence. DroneOS accepts a dataset only after the mission/data identity and integrity checks pass.

## Recon Analysis → PanelMap
Current architecture includes:

- detector-provider abstraction
- optional offline Ultralytics YOLO adapter behind the Solar boundary
- image-to-ground projection support
- deterministic cross-frame fusion
- authoritative `PanelMap` generation

A 2D detection is not treated as a waypoint. It must be associated with context/telemetry and projected/fused before it can become a mission-planning input.

Current limitation: the full simulator E2E path still uses deterministic demo media/data. No survey-grade mapping accuracy or production detector performance is claimed.

## Inspection Proposal — Proposal, Not Command
From the authoritative `PanelMap`, DroneOS creates an immutable, **non-executable Inspection proposal**.

The proposal is bound to:

- workflow identity
- accepted Recon result
- PanelMap provenance
- proposal identity/fingerprint
- current workflow/mission authority

The operator confirms the exact proposal. Server-side authority is revalidated before Flight B is staged.

Important invariant:

> **Confirm Inspection Route stages Flight B; it does not start AUTO.**

## Flight B — Targeted Solar Inspection
Implemented engineering path:

- authoritative Flight B staging
- proposal-to-mission lineage preservation
- real PX4 SITL / Gazebo / MAVSDK AUTO execution
- progress + terminal handoff handling
- accepted Inspection dataset bound to the exact Flight B execution

The second mission uses context derived from Flight A, preserving a deliberate review boundary between discovery and targeted inspection.

## Inspection Evidence → Findings → Report
The current backend can:

- validate InspectionEvidence
- bind evidence to Flight B execution identity
- generate deterministic findings through an injected candidate-provider boundary
- generate the canonical `SolarInspectionReport`
- compute deterministic report identity/fingerprint
- preserve immutable workflow/report provenance
- expose exact report readiness through the workflow read model
- render/open the exact canonical report associated with the loaded workflow

## End-to-End Validation Achieved

### 1. Deterministic offline Solar E2E — validated
Software composition is validated from Recon through report using deterministic local fixtures.

### 2. Real PX4 SITL A→B→Report — validated
Both Flight A and Flight B execute through real PX4 SITL/Gazebo/MAVSDK AUTO.

The canonical backend milestone was validated with **1,885 Python safe tests passed** and **82 dashboard runtime checks** at that milestone.

### 3. Full Jetson Field Box Solar E2E — validated
On 15 September 2026 DroneOS ran the complete canonical workflow on the **NVIDIA Jetson Orin Nano Super Field Box**, while PX4 SITL/Gazebo ran remotely on another computer.

Validated sequence:

**Start Solar → Prepare Recon → Recon Flight → Recon postflight → PanelMap → Inspection proposal → Confirm Inspection Route → Inspection Flight → Inspection postflight → `REPORT_READY` → canonical report**

The Recon and Inspection data sources were explicit deterministic demo providers for this lane. No silent production fallback is claimed.

### 4. Operator dashboard — validated review baseline
The redesigned operator dashboard was exercised during the Jetson E2E run and on laptop. Current review-line dashboard validation reached **83 runtime checks passed**.

## Workflow Provenance
The Solar workflow preserves traceability across:

- workflow identity
- Flight A mission identity/execution
- terminal handoff
- Recon dataset acceptance
- Recon analysis result
- `PanelMap`
- Inspection proposal
- operator confirmation
- Flight B mission identity/execution
- Inspection dataset acceptance
- InspectionEvidence/findings
- canonical report identity/fingerprint

Authority and provenance remain separate:

- **StateService / safety layer:** may this operation happen now?
- **workflow provenance:** which exact predecessor produced this result?

## Current Product Position
The Solar application is currently best described as:

> **An integrated technical Solar MVP with the full software workflow validated on the NVIDIA Jetson Field Box around real PX4 SITL execution, while physical aircraft/camera validation remains pending.**

It is **not yet a field-validated commercial Solar inspection product**.

## What Is Not Yet Claimed
- no controlled real-aircraft Solar flight validation
- no real onboard camera + Vehicle Agent Lite network path validated end to end
- no survey-grade PanelMap accuracy claim
- no validated production thermal-defect detector
- no validated production RGB defect-detection performance
- no autonomous obstacle-avoidance claim
- no certification or commercial-operation readiness claim

## What Remains Before a Real Solar Pilot
1. run Vehicle Agent Lite on real onboard compute
2. connect/calibrate the real camera
3. bind physical captures to exact mission execution identity
4. validate real vehicle↔Field Box dataset transfer
5. PX4 hardware no-props bench validation
6. first controlled physical waypoint flight
7. physical Flight A Recon
8. real Recon transfer → `PanelMap`
9. operator-reviewed Flight B proposal
10. physical Flight B Inspection
11. real Inspection transfer → findings → report
12. repeat the complete workflow reliably
13. evaluate mapping/report quality on a real solar site
14. add thermal inspection only after the physical RGB/data path is stable

## Product Principle
The product is not **“a drone with an app.”**

The goal is a reusable edge/software layer that turns autonomous flights into controlled, traceable operational workflows:

> **DroneOS orchestrates intent, state, evidence and next-action logic. PX4 remains responsible for flying the aircraft.**

# Architecture Overview

> Updated: **15 September 2026**.

## ONEL Dynamics / DroneOS Direction
ONEL Dynamics is developing DroneOS as a reusable, local-first **mission-orchestration, evidence and operator platform** for autonomous drone workflows. Solar inspection is the first vertical used to prove the architecture.

DroneOS is not intended to replace the flight controller. **PX4 remains flight authority.** DroneOS operates above PX4 as the mission, workflow, safety-state, data, operator and reporting layer.

The architectural rule remains:

> **UI and AI may propose; DroneOS validates; the operator confirms where required; PX4 executes the aircraft.**

![DroneOS-Core layers](assets/droneos-core-layers.svg)

## DroneOS-Core Layer Model
DroneOS-Core is structured as responsibility layers rather than a monolithic application.

### Layer 1 — Operator / API / Mission Control
Provides human/programmatic interaction: intent, visibility, workflow progression, confirmation, diagnostics and reports. The UI is not source of truth; server-side authority is revalidated before commit.

### Layer 2 — Mission & Workflow Orchestration
Coordinates planning, staging, start, reconciliation, terminal handoff, processing, retry, cancellation and recovery semantics.

### Layer 3 — Authority / State / Safety
`StateService` and safety logic maintain live mission/workflow authority: revisions, uploaded identity, execution/handoff identity, recovery generation, dataset acceptance and fail-closed command gates.

### Layer 4 — Flight Integration
Provides the explicit PX4/MAVLink/MAVSDK boundary for mission upload/start/progress/recovery. DroneOS does not move attitude stabilization or actuator loops into Python.

### Layer 5 — Data / Evidence / Provenance
Accepts post-flight data only after identity, schema, path, telemetry and checksum validation. Provenance binds datasets, `PanelMap`, proposals, evidence and reports to their exact predecessors.

### Layer 6 — Perception / World Model
Detector providers produce structured observations, not flight authority. Detections can be projected/fused into semantic world models such as `PanelMap`, which then feed mission proposals.

### Layer 7 — Vertical Applications
Solar is the first application layer. Future domains can reuse the same mission, authority, evidence and perception primitives without rewriting the Core.

## Current Deployment Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│ Operator Dashboard / Mission Control                         │
│ intent • workflow stepper • status • recovery • reports      │
└──────────────────────────┬───────────────────────────────────┘
                           │ HTTP / WebSocket over LAN
┌──────────────────────────▼───────────────────────────────────┐
│ DroneOS Field Box — NVIDIA Jetson Orin Nano Super            │
│ orchestration • safety-state • telemetry • provenance        │
│ trusted data • analysis • diagnostics • canonical reporting  │
└───────────────┬───────────────────────────────┬──────────────┘
                │                               │
                │ MAVLink / MAVSDK              │ physical data path
                │                               │ (next validation gate)
┌───────────────▼────────────────┐   ┌──────────▼──────────────┐
│ PX4 Flight Stack               │   │ Vehicle Agent Lite      │
│ flight authority              │   │ capture / association   │
│ stabilization • AUTO • safety │   │ finalize / transfer     │
└───────────────┬────────────────┘   └──────────┬──────────────┘
                │                               │
                └──────────────┬────────────────┘
                               ▼
                      Drone + Payload
```

## PX4 Responsibilities
PX4 owns low-level flight-control authority:

- attitude/rate stabilization
- state estimation and sensor fusion
- vehicle arming and flight modes
- AUTO mission execution
- actuator control
- core PX4 failsafes and recovery behavior

DroneOS does not run those real-time control loops.

## DroneOS Responsibilities
DroneOS owns the higher-level mission/workflow context:

- mission preparation and staging
- command safety/telemetry gating
- mission/geofence/recovery identity tracking
- mission progress and lifecycle reconciliation
- workflow progression
- trusted post-flight dataset acceptance
- analysis and semantic world-model generation
- proposal generation and operator-confirmation boundaries
- workflow provenance
- evidence/findings/report generation
- local operator visibility and diagnostics

## Field Box — Current Validation State
The primary Field Box platform is **NVIDIA Jetson Orin Nano Super**.

Validated as of 15 September 2026:

- ARM64 runtime and native Docker baseline
- non-root container execution
- authenticated API/WebSocket over LAN
- remote connection to PX4 SITL on a separate computer
- remote PX4 mission upload/start and live telemetry
- complete canonical Solar software E2E on Jetson
- both Flight A and Flight B executed through remote real PX4 SITL/Gazebo
- canonical report opened from the Jetson-hosted operator dashboard

The simulator data lane uses explicit deterministic Recon/Inspection providers; physical camera/Vehicle Agent validation is still pending.

See [Field Box Validation](fieldbox_validation.md).

## Operator Dashboard
The current operator interface is intentionally **non-authoritative**.

It exposes:

- canonical Solar workflow progression
- contextual operator actions
- flight/recovery controls
- live mission/vehicle status
- map/HUD visualization
- diagnostics and Advanced tools

The server remains responsible for authoritative validation before mission/workflow transitions. The UI redesign therefore improves operator hierarchy without changing the architecture boundary.

See [Operator Dashboard Validation](operator_dashboard_validation.md).

## Vehicle Agent Lite
Vehicle Agent Lite is intentionally narrow:

- capture
- associate sensor/media with mission execution
- finalize a verifiable dataset
- transfer it to the Field Box

It should not become a second DroneOS. Mission planning, workflow authority, trusted acceptance, analysis and reporting remain on the Field Box.

The production onboard process, real camera timing and physical network path remain the next major integration boundary.

## Mission Intelligence: What Makes DroneOS “Smart”
DroneOS intelligence is not defined as “an AI model flies the drone.” The controlled loop is:

```text
Observe
  ↓
Understand context / world model
  ↓
Propose a mission or workflow action
  ↓
Validate live authority + safety + identity
  ↓
Operator confirmation where required
  ↓
Execute through PX4
  ↓
Collect evidence
  ↓
Reconcile and advance workflow
```

Conceptually:

**smart = context + state + perception + rules + evidence**

AI/perception is one input to this loop, not the authority owner.

## Solar Workflow Architecture

```text
SOLAR_RECON
    ↓
PX4 execution identity
    ↓
terminal handoff
    ↓
Recon dataset acceptance
    ↓
detection → projection → fusion
    ↓
PanelMap
    ↓
Inspection proposal
    ↓
operator confirmation
    ↓
SOLAR_INSPECTION
    ↓
PX4 execution identity
    ↓
Inspection dataset acceptance
    ↓
InspectionEvidence → Findings
    ↓
SolarInspectionReport
```

This entire **software workflow** is now validated on the Jetson Field Box around real PX4 SITL execution. Physical sensor/aircraft validation remains the next gate.

## Safety / Authority Design Principles
1. **PX4 remains flight authority.**
2. **Fail closed on ambiguous identity/state.**
3. **Separate workflow provenance from live mission authority.**
4. **Operator confirmation remains explicit before derived Flight B staging.**
5. **Confirmation stages; it does not auto-launch Flight B.**
6. **Local-first processing.**
7. **Validate in layers: tests → SITL → Field Box → hardware bench → controlled physical flight.**
8. **No production claim from simulation alone.**

## Future Mission-Orchestration Center
After the physical Solar workflow is proven, the same Core can evolve toward:

- multiple mission types and sites
- richer perception/world-model providers
- event/detection-driven mission proposals
- fleet-level scheduling and supervision
- optional cloud synchronization/analytics
- infrastructure, wind, agriculture, search and rescue, logistics and dock-based operations

These are **future architectural directions**, not current commercial capabilities.

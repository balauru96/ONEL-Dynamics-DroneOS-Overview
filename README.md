# ONEL Dynamics – DroneOS Overview

> Public-safe project status. Snapshot: **6 September 2026**.

## What DroneOS Is
DroneOS is a **local-first, modular mission-orchestration and evidence platform above PX4**. It runs on an edge **Field Box** and coordinates mission planning, workflow state, telemetry, safety-state, trusted data handoff, analysis and reporting while **PX4 remains the flight authority**.

DroneOS is intentionally not a low-level flight controller. The platform is designed so that operator interfaces, AI/perception providers and vertical workflows can evolve without inheriting direct actuator authority.

The first product vertical is **Solar Inspection**, implemented as a two-flight workflow:

**Flight A Recon → trusted post-flight processing → PanelMap → Inspection proposal → operator confirmation → Flight B Inspection → evidence → report**

![DroneOS-Core modular layer model](docs/assets/droneos-core-layers.svg)

## Current Engineering Position
**Advanced engineering prototype / pre-field-validation.**

The private engineering source of truth is **DroneOS-Core**. The current development line has progressed beyond the earlier mission-planning PoC into an integrated mission/workflow system with real PX4 SITL execution and a distributed Jetson Field Box validation.

Current validated engineering evidence includes:

- NVIDIA **Jetson Orin Nano Super** as the primary Field Box platform
- native **ARM64** Docker build validated on Jetson
- DroneOS container validated as **non-root**
- authenticated LAN API and WebSocket access validated
- real PX4 SITL / Gazebo mission execution through MAVSDK AUTO
- **1,682 Python safe tests** passed on the latest merged `development2` milestone
- **49 dashboard runtime checks** passed on that milestone
- full deterministic Solar Recon→Inspection→Report software composition
- real PX4 SITL **Flight A Recon + Flight B Inspection** execution
- workflow provenance, mission/workflow identity binding, trusted ingestion and canonical reporting
- optional offline YOLO provider behind a Solar-specific perception boundary

## September 2026 Field Box Milestone
DroneOS has now been demonstrated in a **distributed Lab/SITL architecture**:

```text
Operator browser / Mission Control
            │
            │ HTTP / WebSocket over LAN
            ▼
NVIDIA Jetson Orin Nano
DroneOS Field Box / ARM64 Docker
            │
            │ MAVLink over LAN
            ▼
PX4 SITL + Gazebo on a separate computer
            │
            └── live mission telemetry back to DroneOS
```

The Jetson-hosted DroneOS Field Box successfully connected to remote PX4 SITL, uploaded and started a mission, observed execution, and returned live telemetry to the operator side.

![Distributed Field Box validation](docs/assets/fieldbox-distributed-validation.svg)

This materially reduces deployment risk for the pre-pilot phase, but it **does not constitute physical UAV validation or certification**.

## Solar Inspection — First Product Workflow
Solar is the first vertical because it forces DroneOS-Core to prove an entire mission/evidence loop, not just a waypoint mission.

![DroneOS Solar Inspection workflow](docs/assets/solar-inspection-workflow.svg)

The Solar workflow follows:

**discover → understand → propose → approve → inspect → prove**

### Flight A — Recon / Mapping
DroneOS prepares and stages a Solar Recon mission. PX4 executes the mission in AUTO. After landing, the Recon dataset is transferred through a trusted-ingestion boundary where identity, schema, paths, telemetry association and checksums are validated before the dataset is accepted.

The accepted Recon dataset is then processed into an authoritative `PanelMap` through the perception/world-model layer.

### PanelMap — Turning Images into Site Context
`PanelMap` is the semantic bridge between raw captures and mission planning. The intent is not to convert a 2D detection directly into a waypoint. Detections are associated with context, projected into world coordinates and fused into a structural model of the site.

### Inspection Proposal — Proposal, Not Command
From the authoritative `PanelMap`, DroneOS generates a non-executable Solar Inspection proposal. The proposal is bound to exact workflow provenance and a fingerprint.

The operator confirms the **exact proposal**. The server revalidates current authority before Flight B can be staged.

> **AI / analysis may propose; DroneOS validates; the operator confirms; PX4 executes.**

### Flight B — Targeted Inspection
PX4 then executes the derived Solar Inspection mission in AUTO. The resulting Inspection dataset is again validated and bound to the exact Flight B execution.

### Evidence, Findings and Report
The accepted Inspection dataset is transformed into `InspectionEvidence`, findings and a canonical `SolarInspectionReport` while preserving lineage back to Recon, PanelMap, proposal and both mission executions.

The product goal is not only to answer **“what was found?”**, but also **“which exact mission and dataset produced this result?”**

### Current Solar Validation Status
Validated today:

- deterministic software composition from Recon to final report
- real PX4 SITL Flight A Recon
- real PX4 SITL Flight B Inspection
- A→B workflow orchestration around real PX4 SITL execution
- trusted identity/provenance model
- distributed Jetson Field Box architecture

Still pending:

- real onboard camera + Vehicle Agent Lite end-to-end path
- physical UAV flight validation
- real-site PanelMap accuracy evaluation
- production RGB/thermal defect-detection validation

For the full product-level workflow and limitations, see [Solar Inspection MVP](docs/solar_inspection_mvp.md).

## What Has Been Proven
The current system has validated an architecture-faithful flow across software and real PX4 SITL:

1. prepare and stage a Solar Recon mission
2. ARM / TAKEOFF / AUTO through the normal PX4 path
3. observe execution-qualified mission completion
4. LAND and reach landed/disarmed terminal handoff state
5. transfer and validate Recon data locally
6. bind the accepted dataset to the exact completed mission execution
7. run Recon analysis and build an authoritative `PanelMap`
8. generate a non-executable Solar Inspection proposal
9. require explicit proposal-specific operator confirmation
10. stage the Flight B Solar Inspection mission
11. execute Flight B through real PX4 SITL/MAVSDK AUTO
12. transfer and validate Inspection evidence
13. generate deterministic findings and a canonical Solar Inspection report
14. preserve immutable workflow/report provenance

## DroneOS-Core as a Modular Core
The platform is structured around responsibility layers rather than a monolithic application:

1. **Operator / API / Mission Control** — intent, visibility, confirmation and diagnostics
2. **Mission & Workflow Orchestration** — plan, stage, execute, reconcile and advance workflow state
3. **Authority / State / Safety** — live identity, revisions, fingerprints, recovery fences and fail-closed gates
4. **Flight Integration** — PX4/MAVLink/MAVSDK mission execution boundary
5. **Data / Evidence / Provenance** — trusted ingestion, checksums, lineage and reporting
6. **Perception / World Model** — detector providers, projection, fusion and semantic site models
7. **Vertical Applications** — Solar first; future domains reuse the same orchestration primitives

The architectural principle is simple: **AI and UI may propose; DroneOS-Core validates; PX4 executes the aircraft.**

## Why the System Can Become “Smart”
DroneOS does not define intelligence as “AI directly controls the drone.” The intended model is:

**context + state + perception + rules + evidence → mission proposal → authority validation → PX4 execution → new evidence**

This creates a controlled closed loop:

**observe → understand → propose → validate → execute → prove**

That loop can support richer mission orchestration and detection workflows in the future while preserving a strict boundary around flight authority.

## Current Product Position
DroneOS is no longer only a mission-planning proof of concept. It is a **reproducible engineering prototype with an integrated Solar workflow, real two-flight PX4 SITL execution and distributed Jetson Field Box proof**.

It remains **pre-field / pre-pilot**. The next engineering boundary is physical vehicle hardware, real camera/data-transfer paths and controlled flight validation.

## Important Limitations
DroneOS is **not yet production-ready, certified, or physically flight-validated**.

Current limitations include:

- no controlled real-aircraft flight validation yet
- no real onboard camera capture pipeline validated end to end
- Vehicle Agent Lite transfer is currently simulated/local rather than a hardened onboard network service
- deterministic fixtures are still used for parts of the SITL media/detection/evidence path
- no validated production thermal-defect detector
- no claim of survey-grade panel mapping accuracy
- some workflow/mission authority remains process-local and restart recovery is still being hardened
- no commercial-operation or certification claim

## Architecture Boundary

```text
Operator / Mission Control
        │
        ▼
DroneOS Field Box
Jetson Orin Nano Super
mission orchestration • safety-state • telemetry
trusted data • provenance • analysis • reports
        │
        ├──────── future physical data path ───────► Vehicle Agent Lite / Camera
        │
        ▼
PX4 / MAVLink
flight authority • stabilization • failsafes • AUTO execution
        │
        ▼
Drone + Payload
```

PX4 owns attitude stabilization, vehicle control and core flight safety. DroneOS operates above that boundary as the mission, workflow, data and operator layer.

## Next Milestones
1. final review/hardening of the current integration line before promotion into `development`
2. real Vehicle Agent Lite + camera + network transfer path
3. PX4 hardware / no-props bench validation
4. first controlled physical flight with manual recovery path available
5. physical two-flight Solar workflow validation
6. pilot-quality mapping/report evaluation against real solar-site data
7. thermal/AI defect-detection R&D after the physical data path is proven
8. cloud/fleet services only after the local Field Box workflow is stable

## Longer-Term Platform Direction
Solar inspection is the first vertical because it exercises the reusable primitives of the Core: **discover → understand → plan → approve → execute → report**.

Once those primitives are proven on physical hardware, the same Core can evolve toward broader mission-orchestration use cases such as infrastructure inspection, wind, agriculture, search and rescue, logistics and multi-site operations. These are **platform directions, not current commercial capabilities**.

## Repository Purpose
This repository is a **public-safe overview**. The private source-of-truth development repository is **DroneOS-Core**.

It is intended for:

- grant and funding discussions
- technical partner screening
- architecture presentations
- pilot/customer conversations
- high-level progress tracking

This repository contains no DroneOS implementation source code, no operational credentials and no private DroneOS-Core code.

## Documentation
- [Current Status](docs/current_status.md)
- [Architecture Overview](docs/architecture_overview.md)
- [Field Box Validation](docs/fieldbox_validation.md)
- [Pre-Pilot Validation Scope](docs/pre_pilot_validation_scope.md)
- [Roadmap](docs/roadmap.md)
- [Solar Inspection MVP](docs/solar_inspection_mvp.md)
- [Collaboration Guidelines](docs/collaboration.md)
- [Safety Notes](docs/safety_notes.md)
- [Repository Scope](docs/repository_scope.md)

## License / Rights
No open-source license has been selected for this public overview. Unless a license is added, all rights are reserved by ONEL Dynamics / Ionuț Onel.

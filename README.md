# ONEL Dynamics – DroneOS Overview

> Public-safe project status. Snapshot: **15 September 2026**.

## What DroneOS Is
DroneOS is a **local-first, modular mission-orchestration, evidence and operator platform above PX4**. It runs on an edge **Field Box** and coordinates mission planning, workflow state, telemetry, safety-state, trusted data handoff, analysis and reporting while **PX4 remains the flight authority**.

DroneOS is intentionally not a low-level flight controller. Operator interfaces, AI/perception providers and vertical workflows can evolve without inheriting direct actuator authority.

The first product vertical is **Solar Inspection**, implemented as a two-flight workflow:

**Flight A Recon → trusted post-flight processing → PanelMap → Inspection proposal → operator confirmation → Flight B Inspection → evidence → canonical report**

![DroneOS-Core modular layer model](docs/assets/droneos-core-layers.svg)

## Current Engineering Position
**Integrated technical MVP / pre-physical-validation.**

The private engineering source of truth is **DroneOS-Core**. Since the previous public snapshot, the project has crossed two important boundaries:

1. the canonical Solar workflow now reaches `REPORT_READY` through the normal operator flow around real PX4 SITL execution; and
2. the same complete software workflow has been validated with DroneOS running on the target **NVIDIA Jetson Orin Nano Super Field Box**.

Current validated engineering evidence includes:

- NVIDIA **Jetson Orin Nano Super** as the primary Field Box platform
- native ARM64 runtime and Docker validation on Jetson
- authenticated LAN API and WebSocket access
- remote PX4 SITL / Gazebo mission execution through MAVSDK AUTO
- full canonical Solar Recon→Inspection→Report software E2E on the Jetson Field Box
- explicit deterministic Recon and Inspection demo-data providers for the current simulator lane
- **1,885 Python safe tests passed** on the canonical Solar E2E backend milestone
- **83 dashboard runtime checks passed** on the current operator-dashboard review line
- trusted ingestion, mission/workflow identity binding and immutable provenance
- canonical report publication tied to the exact Solar workflow
- redesigned operator dashboard validated on Jetson and laptop

The software is now strong enough that the next major engineering question is no longer “can the workflow be composed?” but **“does the same architecture hold on real aircraft, camera and vehicle-network hardware?”**

## September 2026 — Full Jetson Field Box E2E Milestone
DroneOS has now been demonstrated in a distributed Lab/SITL architecture with the **complete Solar operator workflow running on Jetson**:

```text
Operator browser
      │
      │ HTTP / WebSocket over LAN
      ▼
NVIDIA Jetson Orin Nano Super
DroneOS Field Box
workflow • safety-state • telemetry • analysis • report
      │
      │ MAVLink / MAVSDK over LAN
      ▼
PX4 SITL + Gazebo on a separate computer
      │
      └── real SITL mission execution + live telemetry
```

The validated sequence was:

**Start Solar Inspection → Prepare Recon → Flight A Recon → Recon postflight → PanelMap → Inspection proposal → operator confirmation → Flight B Inspection → Inspection postflight → `REPORT_READY` → canonical report**

Both missions were executed through real PX4 SITL/Gazebo. The sensor/media side remained explicit deterministic demo data for this validation lane.

![Distributed Field Box validation](docs/assets/fieldbox-distributed-validation.svg)

This materially reduces deployment and integration risk, but it **does not constitute physical UAV, camera or certification validation**.

## Operator Dashboard Milestone
The operator interface has been redesigned around the canonical Solar workflow while preserving the backend-authoritative architecture.

Current validated UI characteristics include:

- canonical Solar workflow shown first
- visual workflow stepper from Setup to Report
- contextual actions for Prepare Recon, Start Flight, Confirm Inspection Route and Open Report
- always-visible flight/recovery controls and vehicle status
- dominant mission map with flight-status HUD
- non-routine tools moved into Advanced sections
- credential-free OpenStreetMap basemap for the current MVP/demo setup
- no change to PX4 command authority, mission lifecycle, StateService or Solar backend semantics

The redesign has been validated on the Jetson Field Box and laptop and remains under final integration review at this snapshot.

See [Operator Dashboard Validation](docs/operator_dashboard_validation.md).

## Solar Inspection — First Product Workflow
Solar is the first vertical because it forces DroneOS-Core to prove an entire mission/evidence loop, not just waypoint upload.

![DroneOS Solar Inspection workflow](docs/assets/solar-inspection-workflow.svg)

The Solar workflow follows:

**discover → understand → propose → approve → inspect → prove**

### Flight A — Recon / Mapping
DroneOS prepares and stages a Solar Recon mission. PX4 executes the mission in AUTO. After landing, the Recon dataset crosses a trusted-ingestion boundary where identity, schema, paths, telemetry association and checksums are validated before acceptance.

### PanelMap — Turning Captures into Site Context
Accepted Recon data is processed into an authoritative `PanelMap`. Detections are treated as observations, not waypoints: context and telemetry are used to project/fuse them into a structural site model.

### Inspection Proposal — Proposal, Not Command
DroneOS generates a non-executable Inspection proposal from the accepted `PanelMap`. The operator confirms the **exact proposal**; confirmation stages Flight B but does not launch it.

> **AI / analysis may propose; DroneOS validates; the operator confirms; PX4 executes.**

### Flight B — Targeted Inspection
PX4 executes the staged Solar Inspection mission in AUTO. Inspection data is accepted only after the same identity/provenance checks.

### Evidence, Findings and Report
Accepted Inspection data is transformed into `InspectionEvidence`, findings and the canonical `SolarInspectionReport`, preserving lineage back through both mission executions.

For the full workflow and current limitations, see [Solar Inspection MVP](docs/solar_inspection_mvp.md).

## What Has Been Proven
The current system has validated an architecture-faithful software flow across the target Field Box and real PX4 SITL:

1. create and bind a Solar workflow
2. prepare and stage Flight A Recon
3. ARM / TAKEOFF / AUTO through the normal PX4 path
4. observe execution-qualified completion and terminal handoff
5. accept and validate Recon data
6. run Recon analysis and build `PanelMap`
7. generate an exact non-executable Inspection proposal
8. require proposal-specific operator confirmation
9. stage Flight B without auto-launching it
10. execute Flight B through PX4 SITL/MAVSDK AUTO
11. accept Inspection data bound to that exact execution
12. generate evidence, findings and canonical report
13. expose `REPORT_READY` and open the exact workflow report
14. preserve workflow/report provenance throughout

## Important Distinction: Software E2E vs Physical E2E
The **software/Field Box E2E is validated**. The **physical UAV E2E is not yet validated**.

Still pending:

- real PX4 flight-controller hardware bench validation
- real onboard Vehicle Agent Lite process
- real camera capture and mission association
- real vehicle→Field Box network transfer
- first controlled physical flight
- physical Flight A Recon and Flight B Inspection
- real-site PanelMap accuracy evaluation
- production RGB/thermal defect-detection validation
- regulatory/pilot evidence

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
The project is now moving from **software integration to hardware-backed validation**:

1. freeze the validated Solar software baseline except for true blockers
2. finalize Field Box deployment/startup reproducibility
3. integrate real PX4-compatible vehicle hardware on the bench with no props
4. integrate Vehicle Agent Lite + real camera/data path
5. perform the first controlled physical waypoint flight
6. execute physical Solar Flight A Recon
7. generate a real PanelMap and operator-reviewed Flight B proposal
8. execute physical Flight B Inspection
9. produce a real evidence-backed report
10. repeat the workflow for pilot-quality reliability and customer evaluation

See [Development Roadmap](docs/roadmap.md) and [Pre-Pilot Validation Scope](docs/pre_pilot_validation_scope.md).

## Longer-Term Platform Direction
Solar inspection is the first vertical because it exercises the reusable Core primitives: **discover → understand → plan → approve → execute → report**.

After the physical Solar workflow is proven, the same Core can evolve toward infrastructure inspection, wind, agriculture, search and rescue, logistics, dock-based operations and multi-site/fleet orchestration. These remain **platform directions, not current commercial capabilities**.

## Repository Purpose
This repository is a **public-safe overview**. The private source-of-truth development repository is **DroneOS-Core**.

It is intended for:

- grant and funding discussions
- technical partner screening
- architecture presentations
- pilot/customer conversations
- high-level progress tracking

This repository contains no DroneOS implementation source code, operational credentials or private DroneOS-Core code.

## Documentation
- [Current Status](docs/current_status.md)
- [Architecture Overview](docs/architecture_overview.md)
- [Field Box Validation](docs/fieldbox_validation.md)
- [Operator Dashboard Validation](docs/operator_dashboard_validation.md)
- [Solar Inspection MVP](docs/solar_inspection_mvp.md)
- [Pre-Pilot Validation Scope](docs/pre_pilot_validation_scope.md)
- [Roadmap](docs/roadmap.md)
- [Collaboration Guidelines](docs/collaboration.md)
- [Safety Notes](docs/safety_notes.md)
- [Repository Scope](docs/repository_scope.md)

## License / Rights
No open-source license has been selected for this public overview. Unless a license is added, all rights are reserved by ONEL Dynamics / Ionuț Onel.

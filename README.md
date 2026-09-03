# ONEL Dynamics – DroneOS Overview

> Public-safe project status. Snapshot: **3 September 2026**.

## What DroneOS Is
DroneOS is a local-first mission operations and inspection workflow platform for PX4-based drones. It runs on an edge **Field Box**, coordinates mission planning, telemetry, workflow state, data handoff, analysis and reporting, while **PX4 remains the flight authority**.

The initial product focus is a two-flight solar inspection workflow:

**Flight A Recon → post-flight processing → PanelMap → Inspection proposal → Flight B Inspection → evidence → report**

## Current Engineering Status
**Integrated Solar MVP backend + real PX4 SITL validation.**

The active private development repository is now **DroneOS-Core**. The current integration baseline has progressed well beyond the earlier single-waypoint SITL demo.

Current validated engineering baseline:

- NVIDIA **Jetson Orin Nano Super** validated as the primary Field Box platform
- reproducible ARM64 / Python 3.12 Field Box bootstrap validated
- Docker baseline aligned for DroneOS backend/dashboard only; PX4 and Gazebo remain outside the container
- PX4 SITL baseline validated with real MAVSDK mission upload/start/progress handling
- **1,682 Python safe tests passed** on the latest integration milestone
- **49 dashboard runtime checks passed**
- deterministic Solar offline E2E workflow validated
- real PX4 SITL **Flight A Recon + Flight B Inspection** validated end to end
- full current backend A→B→Report integration validated using deterministic local media/detection fixtures
- workflow provenance ledger, workflow read model, exact mission/workflow identity binding and trusted Recon ingestion are implemented
- optional offline YOLO adapter exists behind a Solar-specific detector boundary and has loaded a verified external model artifact in a smoke test

## What Has Been Proven
The current system has validated this architecture-faithful flow in simulator/integration infrastructure:

1. prepare and stage a Solar Recon mission
2. ARM / TAKEOFF / AUTO through the normal PX4 path
3. observe execution-qualified mission completion
4. LAND and reach landed/disarmed terminal handoff state
5. transfer and validate Recon capture data locally
6. bind the accepted dataset to the exact completed mission execution
7. run Recon analysis and build an authoritative `PanelMap`
8. generate a non-executable Solar Inspection proposal
9. require explicit proposal-specific operator confirmation
10. stage the Flight B Solar Inspection mission
11. execute Flight B through real PX4 SITL/MAVSDK AUTO
12. transfer and validate Inspection evidence
13. generate deterministic findings and a canonical Solar Inspection report
14. preserve immutable workflow/report provenance

## Current Product Position
DroneOS is no longer just a mission-planning proof of concept. It is now a **reproducible engineering prototype with an integrated Solar workflow and real two-flight SITL execution proof**.

It is still **pre-field / pre-pilot**. The next engineering boundary is to move the validated software workflow onto physical vehicle hardware and real sensor/data-transfer paths.

## Important Limitations
DroneOS is **not yet production-ready, certified, or physically flight-validated**.

Current limitations include:

- no controlled real-aircraft flight validation yet
- no real onboard camera capture pipeline validated end to end
- Vehicle Agent Lite transfer is currently simulated/local rather than a production onboard network service
- deterministic fixtures are still used for parts of the SITL inspection data path
- no validated production thermal-defect detector
- no claim of survey-grade panel mapping accuracy
- some workflow/mission authority remains process-local and full restart recovery is still being hardened
- operator-facing workflow controls and broader Mission Control UX are still being integrated

## Architecture Boundary

```text
Operator / Dashboard
        │
        ▼
DroneOS Field Box
Jetson Orin Nano Super
mission workflow • telemetry • provenance • analysis • reports
        │
        ├──────── future/physical data path ────────► Vehicle Agent Lite / Camera
        │
        ▼
PX4 / MAVLink
flight authority • stabilization • failsafes • AUTO execution
        │
        ▼
Drone + Payload
```

DroneOS intentionally does not replace PX4 flight-control loops. PX4 owns attitude stabilization, vehicle control and core flight safety. DroneOS operates above that boundary as the mission, workflow, data and operator layer.

## Solar Inspection MVP
The current Solar MVP is built around two separate flights rather than one monolithic autonomous mission:

**Flight A – Recon / Mapping**
- capture site imagery
- post-flight transfer to Field Box
- dataset integrity and mission-identity validation
- panel detection/projection/fusion
- `PanelMap` generation

**Operator boundary**
- generate the exact Inspection proposal
- require explicit proposal-specific confirmation before Flight B staging

**Flight B – Inspection**
- execute the derived inspection mission
- collect inspection evidence
- post-flight transfer and validation
- findings and canonical report generation

## Next Milestones
1. complete trusted production wiring for the remaining workflow ingestion/operator seams
2. validate a real Vehicle Agent Lite + camera + network transfer path
3. PX4 hardware / no-props bench validation
4. first controlled physical flight with manual recovery path available
5. physical two-flight Solar workflow validation
6. pilot-quality mapping/report evaluation against real solar-site data
7. thermal/AI defect-detection R&D after the data pipeline is proven
8. cloud/fleet services only after the local Field Box workflow is stable

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
- [Roadmap](docs/roadmap.md)
- [Solar Inspection MVP](docs/solar_inspection_mvp.md)
- [Collaboration Guidelines](docs/collaboration.md)
- [Safety Notes](docs/safety_notes.md)
- [Repository Scope](docs/repository_scope.md)

## License / Rights
No open-source license has been selected yet. Unless a license is added, all rights are reserved by ONEL Dynamics / Ionuț Onel.

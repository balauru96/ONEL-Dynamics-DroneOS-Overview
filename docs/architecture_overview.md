# Architecture Overview

> Updated: **3 September 2026**.

## ONEL Dynamics / DroneOS Direction
ONEL Dynamics is developing DroneOS as a reusable mission operations platform for autonomous drone workflows. Solar inspection is the first vertical used to prove the architecture.

DroneOS is not intended to replace the flight controller. **PX4 remains flight authority.** DroneOS operates above PX4 as the mission, workflow, data, operator and reporting layer.

## Current Deployment Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│ Operator / Dashboard                                         │
│ mission review • status • workflow visibility • reports      │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│ DroneOS Field Box — NVIDIA Jetson Orin Nano Super            │
│ mission workflow • telemetry • identity/provenance           │
│ analysis • local data processing • report generation         │
└───────────────┬───────────────────────────────┬──────────────┘
                │                               │
                │ MAVLink / MAVSDK              │ data path
                │                               │
┌───────────────▼────────────────┐   ┌──────────▼──────────────┐
│ PX4 Flight Stack               │   │ Vehicle Agent Lite      │
│ flight authority              │   │ onboard capture/relay   │
│ stabilization • AUTO • safety │   │ physical path pending   │
└───────────────┬────────────────┘   └──────────┬──────────────┘
                │                               │
                └──────────────┬────────────────┘
                               ▼
                      Drone + Payload
```

## PX4 Responsibilities
PX4 owns the low-level flight-control authority:

- attitude and rate stabilization
- state estimation and sensor fusion
- vehicle arming and flight modes
- AUTO mission execution
- actuator control
- core PX4 failsafes and recovery behavior

DroneOS does not run those real-time control loops.

## DroneOS Responsibilities
DroneOS owns the higher-level mission/workflow context:

- mission preparation and staging
- command safety/telemetry gating around operator actions
- mission/geofence/recovery identity tracking
- mission progress and lifecycle reconciliation
- local operator dashboard
- Solar workflow composition
- post-flight dataset acceptance and integrity verification
- analysis and PanelMap generation
- Inspection proposal generation and operator-confirmation boundary
- workflow provenance
- evidence/findings/report generation

## Field Box
The primary Field Box engineering platform is now **NVIDIA Jetson Orin Nano Super**.

Validated direction:

- ARM64 / Python 3.12 runtime
- local-first operation
- backend and dashboard on the Field Box
- Docker for DroneOS backend/dashboard only
- PX4 and Gazebo remain outside the DroneOS container

The Field Box is intended to remain useful without a permanent cloud connection. Cloud services are a later extension, not the primary flight/runtime dependency.

## Vehicle Agent Lite
Vehicle Agent Lite represents the onboard capture/data-relay boundary.

Current status:

- its Recon/Inspection transfer semantics are represented in the integration architecture
- local/simulated data-transfer paths are validated
- the production physical onboard process, camera timing and network path are still pending validation

The intended role is narrow: bind captured media/sensor data to the exact mission execution and transfer it safely to the Field Box. It does not replace PX4 flight authority.

## Solar Workflow Architecture

```text
SOLAR_RECON
    ↓
PX4 execution identity
    ↓
terminal landed/disarmed handoff
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

A persistent workflow/provenance layer binds the important semantic artifacts together, but it does **not** become a parallel flight authority or replace StateService/PX4 lifecycle authority.

## Safety / Authority Design Principles

1. **PX4 remains flight authority.**
2. **Fail closed on ambiguous identity.** A stale/foreign mission, workflow, dataset or execution must not be silently accepted.
3. **Separate workflow provenance from live mission authority.**
4. **Operator confirmation remains explicit before the derived Flight B mission.**
5. **Local-first processing.** Sensor/media processing and reporting can occur at the Field Box without requiring cloud availability.
6. **Validate in layers.** Deterministic tests → SITL → hardware bench → controlled physical flight.
7. **No production claim from simulation alone.** Real SITL execution is meaningful engineering evidence but is not physical-flight certification.

## Current vs Future

### Current engineering prototype
- single-vehicle PX4 integration
- Jetson Field Box
- mission lifecycle/safety gates
- two-flight Solar workflow
- local post-flight processing
- workflow provenance/reporting
- optional offline Solar YOLO adapter

### Future platform direction
- real Vehicle Agent/camera pipeline
- thermal inspection
- physical field pilots
- richer Mission Control UX
- multiple vehicles/sites
- optional cloud/fleet analytics
- additional verticals beyond Solar

These future capabilities should be introduced only after the current local mission/data workflow proves reliable on physical hardware.

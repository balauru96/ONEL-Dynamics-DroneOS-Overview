# Current Status

> Public-safe status snapshot: **6 September 2026**.

## Executive Status
DroneOS is currently an **advanced engineering prototype / pre-field-validation platform** with an integrated Solar inspection workflow, real PX4 SITL two-flight execution and a distributed NVIDIA Jetson Field Box validation.

The private engineering source of truth is `DroneOS-Core`. Active integration work is reviewed and hardened before promotion into the `development` baseline and later into stable `main` releases.

PX4 remains the flight authority. DroneOS remains the mission, workflow, data, operator and reporting layer above PX4.

## Current Engineering Baseline

### Field Box
- NVIDIA Jetson Orin Nano Super validated as the primary Field Box platform
- native ARM64 Docker build validated on Jetson
- DroneOS runtime validated as non-root
- authenticated API and LAN/WebSocket access validated
- Jetson-hosted DroneOS connected to PX4 SITL on a separate computer over LAN
- remote mission upload/start validated through the normal PX4/MAVSDK mission path
- live telemetry returned to the Jetson-hosted DroneOS runtime
- Docker remains scoped to DroneOS backend/dashboard; PX4 and Gazebo remain outside the container

See [Field Box Validation](fieldbox_validation.md).

### Test / Quality Baseline
Latest merged `development2` Solar workflow milestone:

- **1,682 Python safe tests passed**
- **49 dashboard runtime checks passed**
- deterministic safe-test lane and GitHub CI are part of the engineering workflow

The safe test lane is strong software evidence but does not replace hardware validation.

### PX4 / SITL Validation
Validated with real PX4 SITL + Gazebo + MAVSDK:

- Flight A `SOLAR_RECON`
- mission upload/start/progress observation
- completion reconciliation
- LAND and landed/disarmed terminal handoff
- Recon processing into `PanelMap`
- exact Inspection proposal generation and operator-confirmed staging
- Flight B `SOLAR_INSPECTION`
- second real AUTO mission execution
- terminal handoff
- Inspection dataset processing
- canonical Solar Inspection report generation

The current A→B→Report SITL integration uses real PX4 mission execution for both flights. Deterministic local fixtures are still used for parts of the camera/media/detection/evidence path.

## Solar Workflow Status
The current backend workflow covers:

`Flight A Recon`
→ trusted post-flight dataset acceptance
→ Recon analysis
→ `PanelMap`
→ immutable provenance
→ exact Inspection proposal
→ explicit operator confirmation
→ Flight B staging
→ real SITL Flight B execution
→ Inspection dataset acceptance
→ evidence/findings
→ canonical report

Recent workflow work also includes:

- immutable workflow/provenance ledger
- workflow read-model API
- workflow-aware Recon mission identity binding
- trusted Recon ingestion wired into workflow runtime
- fail-closed identity mismatch/recovery behavior
- real PX4/Gazebo Solar A→B observability work under review

## DroneOS-Core Position
DroneOS-Core is designed as a modular mission-intelligence core rather than one monolithic application.

Its logical responsibilities are separated into:

1. Operator / API / Mission Control
2. Mission & Workflow Orchestration
3. Authority / State / Safety
4. Flight Integration
5. Data / Evidence / Provenance
6. Perception / World Model
7. Vertical Applications

The architectural rule is that UI or AI does not automatically become authority. Operator and perception layers may propose; DroneOS validates current identity/state/safety; PX4 executes the aircraft.

## Vision / AI Status
- optional offline Ultralytics YOLO adapter exists behind the Solar detector boundary
- verified external model loading has been demonstrated in a smoke test
- perception output is non-authoritative and feeds structured world-modeling / proposal generation
- current real-SITL A→B workflow does **not** claim production camera inference
- no validated thermal defect detector is claimed
- no survey-grade mapping accuracy is claimed

## Readiness Assessment

| Component | Status | Notes |
|---|---|---|
| Core mission/safety architecture | Advanced prototype | Authority-aware lifecycle, identity and recovery boundaries |
| Jetson Field Box | **Distributed validated** | ARM64, Docker, auth, LAN, remote PX4 and telemetry return |
| Docker Field Box | Validated baseline | DroneOS backend/dashboard only |
| Solar offline E2E | Validated | Deterministic Recon→Report composition |
| Real PX4 SITL Flight A→B | Validated | Both missions execute through real PX4 SITL/MAVSDK AUTO |
| Backend A→B→Report workflow | Integrated | Provenance/read model/ingestion present in current development line |
| Vehicle Agent Lite | Simulated/local | Physical onboard network/camera path not yet validated |
| PX4 hardware bench | Pending | Next hardware boundary |
| Real camera end-to-end capture | Pending | Required before field pilot |
| Physical flight | Pending | First controlled real-aircraft flight remains ahead |
| Thermal defect detection | R&D | Not validated |
| Commercial operations | Not ready | Requires field validation, regulatory work and pilot evidence |

## Known Limitations
- no physical-aircraft flight validation yet
- no real Vehicle Agent/camera/network pipeline validated end to end
- parts of the SITL media/detection/evidence path still use deterministic fixtures
- workflow/mission authority is not fully restart-durable in every path
- no production-grade thermal/defect detector
- no certification or commercial-operation validation

## Next Validation Boundary
The next major step is **hardware-backed field integration**:

1. Vehicle Agent Lite + real camera/data path
2. PX4 hardware no-props bench validation
3. controlled first physical flight
4. physical Recon→Inspection two-flight workflow
5. pilot-quality Solar mapping/report evaluation

## Public Claim
The correct current public claim is:

> **DroneOS is an advanced, safety-oriented engineering prototype for PX4-based mission operations, with an integrated Solar Recon→Inspection→Report workflow, real PX4 SITL execution and a distributed NVIDIA Jetson Field Box validation. Physical UAV validation, certification and commercial readiness remain pending.**

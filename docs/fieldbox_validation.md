# Field Box Validation

> Public-safe validation snapshot: **15 September 2026**.

## Purpose
The DroneOS Field Box is the edge-compute node for mission orchestration, telemetry/state handling, trusted data processing, diagnostics and reporting. The current engineering platform is **NVIDIA Jetson Orin Nano Super**.

## Validation Stage 1 — Distributed Mission Execution
The first distributed milestone demonstrated DroneOS running on the Jetson while PX4 SITL and Gazebo ran on a separate computer.

```text
Operator browser
      │
      │ HTTP / WebSocket over LAN
      ▼
Jetson Orin Nano Super
DroneOS Field Box
      │
      │ MAVLink / MAVSDK over LAN
      ▼
PX4 SITL + Gazebo
separate computer
      │
      └── live telemetry back to DroneOS
```

Validated evidence included:

- native ARM64 runtime
- Docker/non-root baseline
- authenticated API access
- LAN dashboard/API reachability
- WebSocket connection over LAN
- remote PX4 connection
- mission upload/start through PX4Bridge/MAVSDK
- PX4 mission execution in Gazebo
- live telemetry returned to the Jetson-hosted runtime

## Validation Stage 2 — Full Solar Software E2E on Jetson
On 15 September 2026 the validation was extended from a single distributed mission to the **complete canonical Solar workflow** with DroneOS running on the Jetson Field Box.

Validated operator sequence:

1. Start Solar Inspection
2. Prepare Recon Mission
3. Flight A `SOLAR_RECON`
4. terminal handoff
5. Recon postflight processing
6. `PanelMap`
7. Inspection proposal
8. operator confirmation
9. Flight B `SOLAR_INSPECTION`
10. Inspection postflight processing
11. `REPORT_READY`
12. open canonical Inspection report

Both flights executed through real PX4 SITL/Gazebo on the remote computer. The Recon and Inspection sensor/media inputs were provided by **explicit deterministic demo providers** for this simulator lane.

The redesigned operator dashboard was also exercised on the Jetson during this validation.

![Distributed validation diagram](assets/fieldbox-distributed-validation.svg)

## What This Proves
This demonstrates that the intended Field Box deployment boundary is viable for the full software workflow:

> **DroneOS can run the canonical Solar mission/workflow loop on the target ARM64 edge computer, communicate with remote PX4 over LAN, execute both mission phases through the normal PX4 mission path, process trusted demo datasets and publish the exact canonical report back to the operator.**

This is substantially stronger than a same-machine simulator demo because it exercises the target edge computer and real network boundary between mission compute and flight execution.

## What This Does Not Prove
This validation is **not physical-aircraft, physical-camera, certification or commercial readiness evidence**.

It does not yet prove:

- real flight-controller hardware behavior
- aircraft power/network reliability
- real camera timing and capture association
- real Vehicle Agent Lite network behavior
- RF/LTE/5G field behavior
- vibration/GPS/environmental effects
- real solar-site mapping accuracy
- production RGB/thermal defect-detection performance
- regulatory or certification compliance

## Current Deployment Baseline
For the current Field Box validation lane:

- DroneOS server/dashboard runs on Jetson
- browser access is local/LAN
- PX4 SITL/Gazebo runs remotely
- PX4 remains flight authority
- deterministic demo data is explicitly enabled only for the simulator validation lane
- default/production behavior must not silently fabricate trusted datasets

## Next Validation Boundary
The evidence ladder now moves to physical hardware:

1. real Vehicle Agent Lite + camera/data transfer
2. PX4 hardware no-props bench
3. controlled physical waypoint flight
4. physical Recon capture and trusted transfer
5. real-data `PanelMap`
6. physical Flight B Inspection
7. repeatable Solar pilot-quality workflow

## Public Positioning
The correct public claim is:

> **The DroneOS Field Box has been validated on NVIDIA Jetson Orin Nano Super with the complete canonical Solar software workflow around real remote PX4 SITL mission execution. Physical UAV/camera validation remains pending.**

# Current Status

DroneOS-Lab is in **Lab/SITL Stabilization** phase. This document provides a conservative readiness assessment, the current engineering baseline, validated flows, and known limitations.

## Current Engineering Baseline
- 413 Python safety/backend tests
- 12 dashboard JavaScript runtime tests
- 425 combined deterministic safe tests
- Dashboard runtime harness executes real production JavaScript extracted from `dashboard.html`
- Node runtime preferred, with GJS fallback as an alternate runtime

## Current Status
- Advanced Lab/SITL + Field Box stabilization
- Docker deployment is intended for DroneOS backend/dashboard only, not PX4 or Gazebo
- PX4 remains the flight authority and is responsible for flight safety
- Jetson Field Box hardware validation is pending
- No real aircraft flight validation yet
- No commercial operations validation yet

## Validated Lab / SITL Flow
The following flow has been validated in the lab and simulator infrastructure:

- dashboard mission plan upload
- external ARM accepted by PX4
- TAKEOFF accepted by PX4
- AUTO mission execution started
- PX4 SITL executed a waypoint mission
- dashboard displayed FLYING / MISSION / MISSION_EXECUTING / PX4 ACK TRUE

## Field Box and Dashboard Features Validated in Lab
- token-authenticated local dashboard access exists
- telemetry and state monitoring
- stale telemetry and last-known state handling
- command safety gating for ARM, TAKEOFF, LAND, RTL, AUTO, STOP, CANCEL
- mission upload and start validation
- full mission revalidation after upload
- Field Box health check and diagnostic direction
- debug and reporting direction
- Docker deployment baseline
- ARM64 container validation direction

## Known Limitations
- Battery telemetry can be unavailable in SITL; automatic RTL is disabled when battery telemetry is unavailable
- Production-grade identity and security hardening is not complete
- Hardware validation is pending: Jetson Field Box, PX4 bench testing, and real flight
- Real flight and commercial operations are not validated
- AI/thermal defect detection is future research and not yet validated

## Readiness Assessment
| Component | Status | Notes |
|-----------|--------|-------|
| Lab/SITL Framework | In Progress | PX4 SITL connection, dashboard flow, and mission execution in simulator validated |
| Docker Field Box Flow | In Progress | Backend/dashboard containerization validated; hardware deployment pending |
| Jetson Field Box | Pending | ARM64 and field hardware validation pending |
| PX4 Hardware Bench | Pending | Real autopilot bench validation pending |
| Real Flight | Not Started | No real flight validation yet |
| Commercial Operation | Not Started | Early prototype stage |

## What This Repository Represents
This repository is a public-facing overview repository, not the private DroneOS-Lab source repository. It contains high-level status descriptions, architecture summaries, and a safe public presentation of the project direction.

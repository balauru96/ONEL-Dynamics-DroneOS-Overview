# ONEL Dynamics – DroneOS Overview

## What DroneOS Is
DroneOS is a local-first operator/backend/dashboard layer above PX4. It runs on a Field Box edge node and coordinates mission planning, telemetry, reporting, and operator monitoring while PX4 remains the flight authority.

## What Problem DroneOS Solves
DroneOS provides a local mission coordination layer for PX4-based drones, including:

- mission planning and execution monitoring
- local telemetry and vehicle state visibility
- guided mission report generation
- field-deployable edge dashboard access
- a practical path toward solar inspection workflows

## Current Engineering Baseline
- 413 Python safety/backend tests
- 12 dashboard JavaScript runtime tests
- 425 combined deterministic safe tests
- Dashboard runtime harness executes real production JavaScript extracted from `dashboard.html`
- Node runtime is preferred, with GJS fallback as an alternate runtime
- Validated PX4 SITL mission execution through dashboard flow
- Docker/local Field Box direction only
- Jetson Field Box hardware validation is pending

## Current Status
**Advanced Lab/SITL + Field Box stabilization.**

- Lab/SITL validation completed for dashboard mission upload and PX4 workflow
- PX4 remains the flight authority; DroneOS is the mission/operator layer
- DroneOS Field Box runs backend and dashboard locally and connects to PX4
- Docker should deploy only DroneOS backend/dashboard, not PX4 or Gazebo
- Jetson Field Box deployment is the next major validation milestone
- Not production-ready, not certified, not real-flight validated

## Validated Flow
- mission plan upload via dashboard
- external ARM accepted by PX4
- TAKEOFF accepted by PX4
- AUTO mission execution started
- PX4 SITL executed a waypoint mission
- dashboard displayed FLYING / MISSION / MISSION_EXECUTING / PX4 ACK TRUE

## Known Limitation
- Battery telemetry can be unavailable in SITL; automatic RTL is disabled when battery telemetry is unavailable

## Field Box Direction
A DroneOS Field Box is intended to:

- host the backend and operator dashboard locally
- connect to PX4 via MAVLink
- provide local mission supervision, telemetry, and reporting
- support token-authenticated local dashboard access
- provide health checks, stale telemetry handling, and safety gating
- keep PX4 as the flight control authority

## Solar Inspection MVP Direction
Initial product direction is solar inspection, with a two-stage workflow:

1. Recon / mapping mission
2. Post-flight local data transfer to Jetson Field Box
3. Panel layout detection/mapping as a future baseline goal
4. Inspection route generation
5. Inspection mission execution
6. Local report generation

AI/thermal defect detection is future research and development, not yet validated.

## Repository Purpose
This repository is a public-safe overview, not the private DroneOS-Lab development repository. It is intended for presentations, architecture summaries, partner discussions, and demonstration of high-level status.

## Repository Scope
This repository is not:

- the source-of-truth development repository
- a production deployment bundle
- a validated real flight system
- a security-certified product
- a platform for operationally commanding real aircraft

## Documentation
- [Current Status](docs/current_status.md)
- [Architecture Overview](docs/architecture_overview.md)
- [Roadmap](docs/roadmap.md)
- [Solar Inspection MVP](docs/solar_inspection_mvp.md)
- [Collaboration Guidelines](docs/collaboration.md)
- [Safety Notes](docs/safety_notes.md)
- [Repository Scope](docs/repository_scope.md)

## Repository Structure
ONEL-Dynamics-DroneOS-Overview/
├── README.md
└── docs/
    ├── architecture_overview.md
    ├── collaboration.md
    ├── current_status.md
    ├── roadmap.md
    ├── repository_scope.md
    ├── safety_notes.md
    └── solar_inspection_mvp.md

## Public-Safe Notes
This repository contains no DroneOS implementation source code, no production flight logic, no operational credentials, and no private DroneOS-Lab source code.
It is intended for public-safe communication, grant reviewers, collaboration screening, and partner discussions.

## License / Rights
No open-source license has been selected yet. Unless a license is added, all rights are reserved by ONEL Dynamics / Ionuț Onel.

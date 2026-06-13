# ONEL Dynamics – DroneOS Overview

## Project Overview

**ONEL Dynamics** develops **DroneOS**, a local-first mission/operator layer for PX4-based drones, focused on Field Box deployment, mission workflows, telemetry, reporting, and future solar inspection support.

### What is DroneOS?

DroneOS is a software mission and operator layer that sits above PX4 (the flight stack). It provides:

- **Mission Coordination**: Mission planning, execution, and cancellation
- **Telemetry & State Monitoring**: Real-time vehicle state visibility and monitoring
- **Operator Dashboard**: Local-first operator interface for mission supervision
- **Structured Reporting**: Flight history, mission outcomes, and diagnostic reporting
- **Field Box Deployment**: Docker-based edge compute platform for autonomous operations
- **Future Extensions**: Solar inspection workflows, Vehicle Agent (onboard communication), and AI vision capabilities

### Important Note

**This is an overview/presentation repository**, not the private development repository. It is designed to be safe for presentations, collaboration discussions, grant conversations, and future technical partnerships.

## Current Status

**Lab/SITL Stabilization Phase** – DroneOS-Lab is actively being developed as a prototype and field box stabilization system.

### What Has Been Validated

- Backend and dashboard flow in Docker containers
- PX4 SITL connection and telemetry/state monitoring
- Mission workflow execution in simulator
- Report generation and flight history tracking
- Field Box health check and diagnostic direction
- **Recovery principle**: If DroneOS or the backend is unavailable, PX4 remains capable of safe recovery and landing through PX4/operator control

### What Is Not Ready

- **Not production-ready**: Lab/SITL testing only
- **Not certified**: No regulatory validation or approval
- **Real flight**: Not yet validated with real hardware or aircraft
- **Commercial**: Early-stage development

## Public-Safe Roadmap

| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Lab/SITL stabilization | In progress |
| 2 | Docker Field Box flow | In progress |
| 3 | Jetson Field Box validation | Pending |
| 4 | PX4 hardware/no-props bench testing | Pending |
| 5 | First controlled real flight | Not started |
| 6 | Video/image capture and solar inspection MVP | Not started |
| 7 | Vehicle Agent prototype | Future |
| 8 | AI vision baseline | Future |
| 9 | Cloud/analytics integration | Future |

## Getting Started

- **[Current Status](docs/current_status.md)** – Detailed readiness assessment and what has been validated
- **[Architecture Overview](docs/architecture_overview.md)** – System design, layers, and future roadmap
- **[Roadmap](docs/roadmap.md)** – Stage-by-stage development plan
- **[Collaboration Guidelines](docs/collaboration.md)** – How to work with this repository
- **[Safety Notes](docs/safety_notes.md)** – Critical safety and operational considerations

## ⚠️ Safety Warning

DroneOS is **not a flight-critical system** and is **not a replacement for PX4**. PX4 remains the flight authority. Real drone flight requires hardware validation, no-props bench testing, failsafe configuration, operator supervision, and legal/regulatory compliance. See [Safety Notes](docs/safety_notes.md) for details.


## Questions?

For collaboration inquiries, technical questions, or partnership discussions, please refer to [Collaboration Guidelines](docs/collaboration.md).

## Repository Structure

ONEL-Dynamics-DroneOS-Overview/
├── README.md
└── docs/
    ├── current_status.md
    ├── architecture_overview.md
    ├── roadmap.md
    ├── collaboration.md
    └── safety_notes.md

## Usage / Purpose

This repository is intended for public-safe project communication, presentations, grant discussions, collaboration planning, and partner conversations.

It does not contain the private DroneOS-Lab development source code, operational secrets, internal deployment details, or production flight logic.

## License / Usage

No open-source license has been selected yet. Unless a license is added, all rights are reserved by ONEL Dynamics / Ionuț Onel. Do not reuse, redistribute, or treat this repository as open-source software without written permission.

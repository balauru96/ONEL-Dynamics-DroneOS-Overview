# Repository Scope

> Updated: **15 September 2026**.

This repository is a **public-safe documentation and presentation repository** for ONEL Dynamics / DroneOS.

It contains no DroneOS implementation source code, production flight logic, operational credentials/secrets or private `DroneOS-Core` code.

## What This Repository Contains
- high-level project status and architecture descriptions
- public-safe engineering milestones and validation results
- current roadmap/readiness information
- safety notes and collaboration guidelines
- Solar Inspection MVP documentation
- Field Box and operator-dashboard validation summaries
- public-safe diagrams

It contains no runnable backend, PX4 bridge, planner, detector, workflow runtime or Vehicle Agent implementation.

## Private Source of Truth
The active private engineering repository is **DroneOS-Core**.

This Overview repository may describe validated capabilities from DroneOS-Core at a high level, but it does not mirror or publish its implementation.

## Current Public Snapshot
As of 15 September 2026 this repository may accurately state that:

- the canonical Solar software workflow reaches `REPORT_READY`
- both Solar flights execute through real PX4 SITL/Gazebo
- the complete software workflow has been validated with DroneOS running on NVIDIA Jetson Orin Nano Super
- deterministic demo sensor/media providers are used in the current simulator lane
- the redesigned operator dashboard is validated on Jetson/laptop
- physical aircraft/camera validation remains pending

## What This Repository Does Not Contain
- DroneOS implementation source code
- executable flight code
- PX4 mission-execution implementation
- authentication/security implementation details
- private `.env` files, credentials or operational logs
- private model artifacts or datasets
- code synchronized from private DroneOS-Core

## Public-Safe Use
This repository is intended for:
- grant/funding reviewers
- technical collaborators and partners
- architecture/status presentations
- early pilot/customer discussions
- public progress communication

It is not intended for operational deployment and cannot be used by itself as a flight system.

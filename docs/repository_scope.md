# Repository Scope

This repository is a **public-safe documentation and presentation repository** for ONEL Dynamics / DroneOS.

It contains no DroneOS implementation source code, no production flight logic, no operational credentials or secrets, and no private `DroneOS-Core` source code.

## What This Repository Contains
- high-level project status and architecture descriptions
- public-safe engineering milestones and validation results
- roadmap and readiness information
- safety notes and collaboration guidelines
- public-safe Solar Inspection MVP documentation
- no runnable backend, PX4 bridge, planner, detector, workflow runtime or Vehicle Agent implementation

## Private Source of Truth
The active private engineering repository is **DroneOS-Core**.

This Overview repository may describe validated capabilities from DroneOS-Core at a high level, but it does not mirror or publish its implementation.

## What This Repository Does Not Contain
- DroneOS implementation source code
- executable prototype/production flight code
- PX4 mission execution implementation
- authentication/security implementation details
- private `.env` files, credentials or operational logs
- private model artifacts or datasets
- code synchronized from the private DroneOS-Core repository

## Public-Safe Use
This repository is intended for:
- grant and funding reviewers
- technical collaborators and partners
- architecture/status presentations
- early pilot and customer discussions
- public progress communication

It is not intended for operational deployment and cannot be used by itself as a flight system.

# Pre-Pilot Validation Scope

> Public-safe project scope · September 2026

## Objective
Move DroneOS from an advanced engineering prototype with distributed Field Box / PX4 SITL validation into a **hardware-backed Solar pre-pilot MVP**.

## Current Evidence
Already demonstrated:

- modular DroneOS mission/workflow core
- real PX4 SITL mission execution
- Solar Recon→Inspection→Report software workflow
- NVIDIA Jetson Orin Nano / ARM64 Field Box runtime
- distributed Jetson↔PX4 communication over LAN
- remote mission upload/start and live telemetry return
- authenticated local-first operator access

## Funding Target
**Planned pre-pilot funding need: approximately €25,000.**

The funding is intended to reduce the remaining **hardware, perception and field-validation risk**, not to rebuild the already demonstrated mission core.

## Intended Use of the Next Phase
Typical cost areas include:

- UAV / PX4-compatible validation hardware
- camera and sensor integration
- Vehicle Agent Lite physical data path
- Field Box storage/deployment hardening
- hardware bench tests
- controlled physical flight validation
- real Solar Recon data collection
- mapping/report evaluation
- pilot preparation and technical documentation

Final cost eligibility depends on the selected funding instrument and must be confirmed before project start.

## Measurable Technical Outcomes
The pre-pilot phase should aim to demonstrate:

1. real camera captures bound to exact mission execution identity
2. verified vehicle→Field Box dataset transfer
3. PX4 hardware bench validation with recovery paths
4. controlled physical Recon mission
5. real PanelMap generation from physical data
6. operator-confirmed physical Inspection mission
7. trusted Inspection evidence ingestion
8. canonical customer-readable report with full provenance
9. repeatable workflow across multiple controlled runs

## Non-Claims
The current project is not yet certified, production-ready or commercially flight-proven. The pre-pilot phase exists specifically to generate the physical evidence required before those claims can be considered.

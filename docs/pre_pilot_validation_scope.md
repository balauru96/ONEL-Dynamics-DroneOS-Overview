# Pre-Pilot Validation Scope

> Public-safe project scope · **15 September 2026**

## Objective
Move DroneOS from an **integrated technical MVP with full Jetson Field Box software E2E** into a **hardware-backed Solar pre-pilot MVP**.

The next phase should reduce physical integration risk rather than expand software scope for its own sake.

## Current Evidence
Already demonstrated:

- modular DroneOS mission/workflow core
- canonical Solar Recon→Inspection→Report backend
- real PX4 SITL Flight A and Flight B execution
- NVIDIA Jetson Orin Nano Super Field Box runtime
- full Solar software E2E on Jetson with remote PX4 SITL/Gazebo
- authenticated local/LAN operator access
- trusted data/provenance/report pipeline
- redesigned operator dashboard validated on Jetson/laptop
- **1,885 Python safe tests passed** on the canonical Solar backend milestone
- **83 dashboard runtime checks passed** on the current UI review line

## Funding Objective
A practical near-term objective is to secure **approximately €25,000 of external support** toward the hardware-backed validation phase.

This should not be read as a claim that the total eligible R&D project cost is exactly €25,000. Depending on the selected funding instrument and funding rate, the total project volume may need to be materially higher.

The funding case should be framed as a bounded R&D/validation project, not simply as a hardware purchase.

## Intended Use of the Next Phase
Typical cost/work areas:

- PX4-compatible development UAV / validation hardware
- flight controller, power and telemetry integration
- camera and onboard compute integration
- Vehicle Agent Lite physical data path
- Field Box storage/deployment hardening
- no-props hardware bench validation
- controlled first-flight program
- real Solar Recon data collection
- real-data PanelMap evaluation
- physical Flight B inspection validation
- report/pilot evaluation and technical documentation

Final cost eligibility must be confirmed against the selected funding program before project start or purchase commitments.

## Proposed Technical Work Packages

### WP1 — Physical Platform Integration
- PX4-compatible vehicle hardware
- flight-controller communication
- power/network integration
- bench safety/recovery checks

### WP2 — Real Sensor / Vehicle Agent Path
- onboard compute
- real camera
- mission-bound capture identity
- dataset finalization/transfer to Field Box

### WP3 — Controlled Flight Validation
- first bounded waypoint mission
- physical Flight A Recon
- operational logs/recovery evidence

### WP4 — Physical Solar E2E
- real Recon → PanelMap
- operator-reviewed Inspection proposal
- physical Flight B
- evidence/findings/report

### WP5 — Repeatability / Pilot Readiness
- repeat runs
- mapping/capture quality metrics
- failure/recovery analysis
- customer-readable report quality
- pilot/LOI preparation

## Measurable Technical Outcomes
The pre-pilot phase should aim to demonstrate:

1. real camera captures bound to exact mission execution identity
2. verified vehicle→Field Box dataset transfer
3. PX4 hardware bench validation with recovery paths
4. controlled physical Recon mission
5. real-data `PanelMap`
6. operator-confirmed physical Inspection mission
7. trusted Inspection evidence ingestion
8. canonical customer-readable report with full provenance
9. repeatable workflow across multiple controlled runs

## Non-Claims
The current project is not yet certified, production-ready or commercially flight-proven. The pre-pilot phase exists specifically to generate the physical evidence required before those claims can be considered.

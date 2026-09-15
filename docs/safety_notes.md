# Safety and Validation Notes

> Updated: **15 September 2026**.
>
> Public-safe overview. This is not an operational flight manual, certification package or regulatory approval.

## Safety Boundary
**PX4 remains flight authority.** DroneOS-Core operates above PX4 as the mission/workflow, safety-state, data and operator layer.

DroneOS may:

- prepare and stage missions
- validate mission identity, state and telemetry conditions
- request high-level mission execution and recovery actions
- observe mission progress and terminal state
- process trusted post-flight evidence

DroneOS does not:

- replace PX4 stabilization or actuator-control loops
- bypass PX4 native failsafes
- treat UI, network input or AI output as authority by default
- claim dynamic obstacle avoidance

## Fail-Closed Normal Operations
Normal commands require demonstrable current state. Stale, missing or divergent identity/telemetry must block normal progression rather than be treated optimistically.

Protected context includes:

- mission/geofence revisions
- uploaded mission identity/fingerprint
- execution and terminal-handoff identity
- recovery generation
- dataset acceptance
- proposal/workflow identity
- telemetry freshness and validity

The principle is simple: **unknown state does not authorize a normal command.**

## Recovery Remains Separate
Fail-closed normal logic must not make recovery impossible.

LAND / RTL and manual recovery paths are treated separately from normal mission progression. The current operator dashboard keeps recovery/interrupt controls visible while the backend remains authoritative.

## Geofence, No-Fly and Obstacle Avoidance Are Different
- DroneOS route/no-fly validation checks planned geometry and can provide runtime warnings.
- PX4 geofence/failsafe behavior belongs to the flight-controller layer.
- Dynamic obstacle avoidance/replanning is a separate future capability.

DroneOS currently makes **no dynamic obstacle-avoidance claim**.

## Current Validated Safety-Relevant Evidence
As of 15 September 2026:

- fail-closed mission/workflow identity gates are implemented and covered by deterministic tests
- canonical Solar E2E backend validation reached **1,885 Python safe tests passed**
- real PX4 SITL Flight A → Flight B execution has been demonstrated
- full canonical Solar software E2E has been demonstrated with DroneOS running on Jetson
- authenticated API/WebSocket access is validated in the local/LAN deployment model
- redesigned operator UI preserves backend authority and keeps recovery controls visible
- PX4 remains flight authority throughout

These results are meaningful software/Lab/SITL evidence, but they are **not physical-flight validation or certification**.

## Solar-Specific Safety Boundary
For the Solar workflow:

1. Flight A discovers the site.
2. trusted Recon ingestion verifies/accepts the dataset.
3. analysis produces the authoritative `PanelMap`.
4. DroneOS generates a **non-executable** Inspection proposal.
5. the operator confirms the exact proposal.
6. DroneOS revalidates current authority.
7. Flight B is staged.
8. a separate operator action starts Flight B through the normal PX4 path.

The intended boundary is:

> **AI / analysis may propose; DroneOS validates; the operator confirms; PX4 executes.**

AI/perception does not directly start Flight B and does not receive actuator authority.

## Demo Data Isolation
The current full simulator/Jetson E2E uses explicit deterministic demo providers for Recon and Inspection data.

This distinction is intentional:

- demo providers are enabled explicitly for validation
- production/default behavior must not silently fabricate trusted sensor data
- successful software E2E does not imply real sensor validation

## Current Security Position
The local/LAN baseline includes authentication and protected API/WebSocket access.

Production hardening still requires:

- secret management
- secure transport/tunneling where appropriate
- audit logging
- least privilege
- update policy
- separation/rotation of field credentials

No production-security certification is claimed.

## Physical Validation Still Required
Before pilot-quality autonomous operation can be claimed, the project still needs:

1. real PX4 hardware no-props bench validation
2. real Vehicle Agent Lite + camera/data path
3. controlled physical flight
4. physical Recon capture/trusted transfer
5. physical Flight B Inspection
6. repeatability/recovery evidence across multiple runs
7. site-specific operational and regulatory assessment

## Validation Ladder
DroneOS follows an evidence ladder:

**deterministic tests → real PX4 SITL → full Jetson Field Box E2E → PX4 hardware bench → controlled physical flight → Solar site pilot**

Passing one stage does not replace the next.

## Public Claim
> **DroneOS is an integrated technical MVP with safety-oriented authority boundaries validated in software, real PX4 SITL and full Jetson Field Box E2E. Physical UAV/camera validation, certification and commercial operational readiness remain pending.**

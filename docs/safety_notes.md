# Safety and Validation Notes

> Updated: **6 September 2026**.
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

- mission and geofence revisions
- uploaded mission fingerprint
- execution and terminal-handoff identity
- recovery generation
- dataset acceptance
- proposal and workflow identity
- telemetry freshness and validity

The principle is simple: **unknown state does not authorize a normal command.**

## Recovery Remains Separate
Fail-closed normal logic must not make recovery impossible.

LAND / RTL and manual recovery paths are treated separately from normal mission progression so that a rejected normal command does not become a reason to block a safe exit path. Recovery is still constrained by explicit recovery semantics; it is not a generic bypass around mission authority.

## Geofence, No-Fly and Obstacle Avoidance Are Different
These concepts must not be conflated:

- DroneOS route/no-fly validation checks planned geometry and can provide runtime warnings.
- PX4 geofence/failsafe behavior belongs to the flight-controller safety layer.
- Dynamic obstacle avoidance or automatic replanning around obstacles is a separate future capability.

DroneOS currently makes **no dynamic obstacle-avoidance claim**.

## Current Validated Safety-Relevant Evidence
As of 6 September 2026:

- fail-closed mission/workflow identity gates are implemented and covered by deterministic tests
- real PX4 SITL Flight A → Flight B mission execution has been demonstrated
- distributed NVIDIA Jetson Field Box ↔ PX4 SITL communication has been validated over LAN
- authenticated API and WebSocket access have been validated in the local/LAN deployment model
- remote PX4 mission upload/start and live telemetry return have been demonstrated
- PX4 remains flight authority throughout the architecture

These results are meaningful software/Lab/SITL evidence, but they are **not physical-flight validation or certification**.

## Current Security Position
The current local/LAN deployment baseline includes authentication and protected API/WebSocket access.

Production deployment hardening still requires items such as:

- secret management
- secure transport or tunneling where appropriate
- audit logging
- least privilege
- update policy
- separation of development and field credentials
- operational key/credential rotation procedures

No production-security certification is claimed.

## Physical Validation Still Required
Before pilot-quality autonomous operation can be claimed, the project still needs:

1. real PX4 hardware / no-props bench validation
2. real Vehicle Agent Lite + camera/data path
3. controlled physical flight
4. physical Recon capture and trusted transfer
5. physical Flight B inspection
6. repeatability and recovery evidence across multiple runs
7. site-specific operational and regulatory assessment

## Solar-Specific Safety Boundary
For the Solar workflow:

1. Flight A discovers the site.
2. Trusted Recon ingestion verifies and accepts the dataset.
3. Analysis produces the authoritative `PanelMap`.
4. DroneOS generates a **non-executable** Inspection proposal.
5. The operator confirms the exact proposal fingerprint.
6. DroneOS revalidates current workflow/mission authority.
7. Only then can Flight B be staged for PX4 execution.

The intended boundary is:

> **AI / analysis may propose; DroneOS validates; the operator confirms; PX4 executes.**

AI/perception does not directly start Flight B and does not receive actuator authority.

## Validation Ladder
DroneOS follows an evidence ladder rather than treating one test class as proof of every layer:

**deterministic tests → real PX4 SITL → distributed Field Box validation → PX4 hardware bench → controlled physical flight → Solar site pilot**

Each stage answers a different engineering question. Passing one stage does not replace the next.

## Public Claim
> **DroneOS is an advanced engineering prototype with safety-oriented authority boundaries validated in software, real PX4 SITL and distributed Jetson Lab/SITL. Physical UAV validation, certification and commercial operational readiness remain pending.**

## Related Documentation
- [Current Status](current_status.md)
- [Architecture Overview](architecture_overview.md)
- [Field Box Validation](fieldbox_validation.md)
- [Solar Inspection MVP](solar_inspection_mvp.md)
- [Roadmap](roadmap.md)

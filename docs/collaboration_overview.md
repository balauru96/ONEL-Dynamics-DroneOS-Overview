# DroneOS-Lab – Public Collaboration Overview

## Project Description

DroneOS is being developed by ONEL Dynamics as a local-first mission and
operator layer for PX4-based drones. Its intended role is to support mission
workflows, telemetry, operator monitoring, diagnostics, structured reporting,
and future Field Box deployment, including a solar-inspection workflow.

This repository is an early collaboration and path-planning prototype within
that wider direction. It should not be presented as a complete DroneOS product
or as a flight-ready system.

## Current Status

The current repository supports a **lab-stage prototype** description. The code
provides a FastAPI backend prototype, in-memory vehicle state, telemetry and
WebSocket flows, example mission endpoints, flight-history logging, basic
no-fly-zone checks, experimental path-planning modules, and an asynchronous PX4
bridge stub.

The following distinctions are important for public discussions:

- **Lab/SITL prototype:** The repository is suitable for software exploration
  and future simulator integration. No complete SITL setup or validation record
  is included in this checkout.
- **PX4 integration:** A PX4-facing API boundary and development stub exist.
  Real MAVSDK/MAVLink transport and validated PX4 integration are not present.
- **Operator interface:** Backend routes reference a dashboard, but the
  dashboard asset is absent from this repository. A complete operator
  interface cannot be verified here.
- **Telemetry and state monitoring:** In-memory state, telemetry snapshots,
  WebSocket broadcasting, status reporting, and local flight-history output
  are represented in the backend.
- **Mission workflow:** Example mission generation, preview, upload, start,
  cancel, land, and return-to-launch API concepts are represented. End-to-end
  simulator execution is not verified by repository tests or configuration.
- **Field Box and Docker flow:** These are intended deployment directions.
  Docker files, Jetson setup, Field Box scripts, and deployment validation are
  not included in this checkout.
- **Solar inspection and reporting:** Solar inspection is a target use case.
  Image capture, inspection analysis, and solar report generation are not
  implemented here.
- **Authentication:** No token or authentication baseline is present in the
  current repository.
- **Field Box health checks:** No dedicated Field Box health or check flow is
  present. A small API status endpoint exists, but it is not a device health
  management system.
- **Recovery:** PX4 must remain the flight authority. DroneOS must not become
  the only recovery mechanism for a vehicle.

## Architecture Summary

PX4 remains responsible for flight control and validated vehicle safety
behavior. DroneOS does not replace PX4.

DroneOS is intended to coordinate higher-level concerns:

- Mission planning and operator workflows
- Telemetry and vehicle-state presentation
- Mission monitoring and diagnostics
- Data collection and structured reporting
- Future Field Box deployment and local processing

The prospective architecture may later include a Jetson-based Field Box,
Vehicle Agent, AI vision services, cloud synchronization, and analytics. These
are roadmap components, not completed features demonstrated by this
repository.

```text
Operator and Mission Workflows
              |
DroneOS monitoring, planning, diagnostics, and reporting
              |
Future Field Box / Vehicle Agent integration boundary
              |
PX4 autopilot and vehicle safety mechanisms
```

## What Is Implemented

The current repository contains:

- A FastAPI backend prototype with state and command endpoints
- In-memory telemetry and vehicle-state handling
- WebSocket state broadcasting
- Local JSON flight-history logging
- Example mission-shape generation for survey, patrol, inspection, and
  agriculture scenarios
- Basic circular no-fly-zone checks for selected targets and waypoints
- A simple circular-zone detour prototype
- An experimental grid-based A* planner with smoothing
- A PX4 bridge stub for interface development
- Basic command cooldown and flight-state checks in parts of the API

The repository does not currently include a working dashboard asset, automated
tests, Docker helpers, deployment scripts, report templates, an authentication
layer, or production security configuration.

## Experimental or Incomplete

- The project is not production-ready.
- It has not been validated for real drone flight.
- Hardware integration and hardware safety validation remain pending.
- The PX4 bridge is a stub and does not provide real MAVLink or MAVSDK
  communication.
- The API and bridge interfaces do not fully agree on all methods and telemetry
  fields.
- Mission and path-planning behavior has no automated test coverage here.
- The experimental planners are not wired into the FastAPI mission flow.
- No-fly-zone and geofence handling is simplified and requires further backend,
  PX4, and operational validation.
- The referenced dashboard file is missing from this checkout.
- Video, image capture, and AI inspection pipelines are future work.
- Solar inspection report generation is future work.
- The Vehicle Agent is future work.
- Jetson Field Box and Docker deployment flows are future work in the context
  of this repository.

## Safety Notes

- Treat this repository as SITL/lab-only unless a capability has been
  explicitly validated and documented elsewhere.
- Do not use it for real drone missions without controlled hardware validation,
  regulatory review, and an approved operating procedure.
- Real hardware work requires properly configured PX4 failsafes and an
  independently validated operator intervention path, including RC override
  where appropriate.
- DroneOS must not be treated as the only recovery path.
- A generated geometric path is not proof that a mission is safe or flyable.
- Flight validation must consider airspace, terrain, obstacles, weather,
  battery reserve, navigation quality, communications loss, and vehicle
  performance.
- Never bypass PX4 arming checks, geofences, failsafes, flight modes, or
  return-to-launch behavior.
- Never commit secrets, credentials, tokens, private connection details, or
  sensitive operational logs.

## Collaboration Rules

- Work on a separate branch for each focused change.
- Do not push directly to stable branches.
- Keep pull requests small enough to review confidently.
- Include automated test results or clear manual validation notes.
- Do not modify flight-critical, mission, or safety logic without review.
- Discuss scope before adding large features or changing architecture.
- Document assumptions, limitations, and safety impact.
- Do not commit `.env` files, tokens, credentials, private files, or logs that
  contain secrets or sensitive data.

## Recommended Contributor Workflow

```bash
# Confirm the starting state
git status

# Create a focused branch
git checkout -b feature/name

# Make changes, then review them
git diff
git diff --check

# Run available safe tests or checks
python3 -m compileall -q drone_api drone_core tasks

# Confirm the final scope
git status

# Commit and publish the branch
git add <changed-files>
git commit -m "Describe the focused change"
git push -u origin feature/name

# Open a pull request in the Git hosting platform
```

Each pull request should explain what changed, why it changed, what was tested,
what remains untested, and whether the change can affect PX4 integration,
missions, vehicle commands, safety behavior, or public interfaces.

## Presentation Summary

> DroneOS-Lab is a working lab-stage prototype of a local-first mission control
> layer for PX4-based drones. The current focus is validating a Jetson-based
> Field Box workflow and preparing a solar inspection MVP with mission
> planning, telemetry, video/image capture, and structured reporting.

This statement describes the program direction. In the current repository,
backend and planning prototypes are represented; Jetson deployment,
video/image capture, and solar reporting remain roadmap work.

## Roadmap

The following stages are proposed and should be gated by documented acceptance
criteria and safety review:

1. **Jetson Field Box validation:** Package and validate the local deployment,
   startup, diagnostics, update, and recovery workflow.
2. **PX4 hardware/no-props bench:** Validate communication, state mapping,
   command handling, failsafes, and operator recovery without propellers.
3. **First controlled flight:** Proceed only after bench results, risk review,
   legal compliance, checklists, and independent recovery controls are in
   place.
4. **Video and image capture:** Add timestamped, mission-linked media capture
   with storage and privacy controls.
5. **Solar inspection support report:** Produce a structured, reviewable report
   that links mission, telemetry, and captured evidence without overstating
   automated findings.
6. **Vehicle Agent:** Define and validate a narrow vehicle-side interface with
   clear ownership, health reporting, and failure behavior.
7. **AI vision baseline:** Establish datasets, measurable evaluation criteria,
   human review, and traceable model outputs.
8. **Cloud and analytics:** Add optional synchronization and fleet analytics
   only after local workflows, security, ownership, and data governance are
   mature.

## Public-Safe Use

This document intentionally excludes secrets, credentials, private network
details, personal contact information, legal or financial details, and
operational vehicle configuration. Public presentations should preserve the
same boundary and clearly separate implemented repository evidence from
planned capabilities.

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

## Repository Structure

```
ONEL-Dynamics-DroneOS-Overview/
├── README.md                          # This file
├── docs/
│   ├── current_status.md             # Readiness assessment
│   ├── architecture_overview.md       # System design and vision
│   ├── roadmap.md                    # Development stages
│   ├── collaboration.md              # Collaboration guidelines
│   └── safety_notes.md               # Safety and operational requirements
├── drone_api/                        # Backend API implementation
├── drone_core/                       # Core mission and planning modules
└── tasks/                            # Utilities and development tasks
```

## Questions?

For collaboration inquiries, technical questions, or partnership discussions, please refer to [Collaboration Guidelines](docs/collaboration.md).

## Repository Layout

```text
.
├── drone_api/
│   └── server.py              # FastAPI prototype and in-memory state
├── drone_core/
│   ├── path_service.py        # Simple circular-zone detour prototype
│   └── planner.py             # Experimental grid/A* mission planner
├── droneos-collab-path        # Unconfigured gitlink entry
├── tasks/
│   └── px4_bridge_stub.py     # Async development stub, not real PX4 I/O
├── .gitignore
└── README.md
```

There are no additional README files in the current repository.

## DroneOS Architecture Context

DroneOS is intended to operate as a mission and operator layer above PX4:

```text
Operator UI / Mission Tools
            |
DroneOS mission, telemetry, reporting, and coordination services
            |
Vehicle integration boundary (future Vehicle Agent / Field Box)
            |
PX4 autopilot and its validated flight-safety mechanisms
```

PX4 remains the flight authority. DroneOS should plan missions, present
telemetry, support operator workflows, and coordinate higher-level services;
it must not bypass PX4 arming checks, flight modes, failsafes, geofencing, or
other safety controls.

The wider ONEL Dynamics direction may include a Field Box, Vehicle Agent, AI
vision, solar-inspection reporting, and cloud or analytics services. Those
systems are future architecture context, not implemented capabilities of this
repository. Changes here should remain focused on collaboration and
path-planning experiments unless a broader scope is agreed first.

## Local Setup

Python 3.9 or newer is recommended. The repository does not currently declare
or pin its dependencies; the API source directly requires FastAPI, and Uvicorn
is useful for local serving.

```bash
git clone <repository-url>
cd DroneOS-collab-path

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn
```

For local inspection only, start the API from the repository root:

```bash
uvicorn drone_api.server:app --reload
```

Useful endpoints include:

- `http://127.0.0.1:8000/docs` for generated API documentation.
- `http://127.0.0.1:8000/api/status` for a small status snapshot.
- `http://127.0.0.1:8000/state` for the current in-memory state.

Do not treat a successful server start or stub connection as proof of PX4
connectivity or flight readiness. The dashboard routes currently reference a
missing file.

## Basic Checks

There is no automated test suite at present. The available repository-level
checks are limited to Python syntax compilation and Git whitespace checks:

```bash
python3 -m compileall -q drone_api drone_core tasks
git diff --check
git status --short
```

Any planner, mission, safety, or vehicle-integration change should add focused
tests before it is considered ready to merge. Simulation and manual validation
notes should be included in the pull request.

## PX4 / MAVLink Notes

- `tasks/px4_bridge_stub.py` simulates delays and a small amount of state; it
  does not use MAVSDK, MAVLink, a serial link, UDP, or a real PX4 vehicle.
- API labels such as `PX4`, connection state, arm, takeoff, land, and RTL do not
  demonstrate a validated end-to-end autopilot integration.
- The server and bridge currently disagree on some method names and telemetry
  fields. This boundary must be defined and tested before integration work.
- New vehicle commands must preserve PX4 as the final flight authority and
  must be tested in PX4 SITL before any hardware consideration.
- Never disable or work around PX4 pre-arm checks, failsafes, geofences, RTL,
  or operator control requirements from this layer.

## Safety Notes

Path generation in this repository is advisory prototype logic. A geometrically
valid path is not necessarily a safe or flyable path. Validation must account
for altitude, terrain, structures, weather, vehicle performance, GPS quality,
link loss, battery reserve, local airspace, regulations, emergency procedures,
and PX4 configuration.

No-fly-zone handling is currently simplified and must not be treated as a
certified geofence or collision-avoidance system.

## Known Limitations

- Early-stage collaboration repository with incomplete integration boundaries.
- Not validated for real hardware flight.
- Safety, geofence, path, and mission validation may be incomplete or
  internally inconsistent.
- Planner prototypes are not wired into the API and have no automated coverage.
- No production security guarantees, authentication, authorization, hardened
  configuration, or secrets-management design.
- In-memory state and permissive CORS are development conveniences, not
  production architecture.
- Flight-history files are local development logs and are not a complete audit
  or reporting system.
- Future integration into the main DroneOS codebase requires careful interface,
  safety, security, and ownership review.

## Collaboration Rules

- Work on a separate branch for every change.
- Do not push directly to `main`.
- Do not modify mission or flight-safety logic without review.
- Do not add large features without discussing and agreeing on scope.
- Keep commits focused, understandable, and documented.
- Open a pull request with a clear description of behavior and risk.
- Include automated test results or explicit manual validation notes.
- Do not commit secrets, tokens, `.env` files, private logs, credentials, keys,
  or vehicle connection details.

## Recommended Contributor Workflow

```bash
# Check the starting state
git status

# Create a focused branch
git switch -c feature/short-description

# Make and review changes
git diff

# Run the available checks
python3 -m compileall -q drone_api drone_core tasks
git diff --check

# Commit the focused change
git add <changed-files>
git commit -m "Describe the change"

# Push the branch
git push -u origin feature/short-description

# Open a pull request through the Git hosting interface or CLI
gh pr create --fill
```

Before requesting review, explain what changed, why it changed, what was tested,
what was not tested, and whether mission, PX4, MAVLink, safety, or API behavior
could be affected.

## Do Not

- Do not run real drone missions from this repository.
- Do not commit credentials or private operational data.
- Do not bypass PX4 safety mechanisms or flight authority.
- Do not merge untested mission or vehicle-command code.
- Do not change core architecture or safety assumptions without documenting and
  reviewing them.
- Do not interpret prototype API responses, generated paths, or stub telemetry
  as evidence that a vehicle is safe to arm or fly.

## License

The previous project documentation described the repository as private and
proprietary. No standalone license file is currently present. Confirm usage,
distribution, and contribution terms with ONEL Dynamics before reusing this
code outside the authorized collaboration context.

# Development Roadmap

DroneOS development is organized into realistic, staged milestones. Each stage builds on the previous, with clear validation criteria and public-safe readiness claims.

## Timeline Overview

| Stage | Timeline | Status | Key Validation |
|-------|----------|--------|-----------------|
| 1 | Current | **In Progress** | Lab/SITL stabilization |
| 2 | 1–2 weeks | **In Progress** | Docker Field Box flow |
| 3 | 2–4 weeks | Pending | Jetson hardware validation |
| 4 | 4–6 weeks | Pending | PX4 bench testing |
| 5 | 6–8 weeks | Not Started | First controlled real flight |
| 6 | 2–3 months | Not Started | Solar inspection MVP |
| 7 | 3–4 months | Not Started | Vehicle Agent prototype |
| 8 | 4–6 months | Not Started | AI vision baseline |
| 9 | 6–9 months | Future | Cloud/analytics integration |

---

## Stage 1: Lab/SITL Stabilization

**Status:** 🔄 **In Progress**

**Goal:** Stabilize DroneOS architecture and core mission engine in simulator.

### Objectives

- ✅ FastAPI backend operational with mission endpoints
- ✅ PX4 SITL connection and MAVLink communication verified
- ✅ Telemetry streaming and state management working
- ✅ Mission workflow (create, upload, execute, cancel) demonstrated
- ✅ Basic report generation and flight history
- ⏳ Comprehensive test coverage and API documentation
- ⏳ Error handling and edge case resilience

### Validation Criteria

- Backend can handle 30+ mission endpoints without crashes
- PX4 SITL connection stable for 1+ hour of continuous operation
- Telemetry updates at ≥10 Hz without data loss
- Mission execution completes without operator intervention
- Reports generated within 5 seconds of mission end

### Deliverables

- Documented API endpoints and data schemas
- SITL test scenario library (5+ representative missions)
- Architecture diagrams and interface specifications
- Operational runbook for developers

**Readiness Claim:** Lab/SITL framework ~80% ready; suitable for early collaborators and architectural review.

---

## Stage 2: Docker Field Box Flow

**Status:** 🔄 **In Progress**

**Goal:** Containerize DroneOS backend and dashboard for portable Field Box deployment.

### Objectives

- ✅ Docker Compose configuration for backend, dashboard, database
- ✅ Environment configuration and secrets management skeleton
- ✅ Container health checks and graceful shutdown
- ✅ Volume mounts for persistent logs and mission history
- ⏳ Docker networking and PX4 SITL container coordination
- ⏳ Performance and resource optimization

### Validation Criteria

- Full stack starts and stabilizes in <30 seconds
- Dashboard accessible within 1 minute of container startup
- Mission execution works end-to-end in containerized environment
- No data loss on graceful shutdown
- CPU and memory usage within reasonable limits (TBD)

### Deliverables

- `docker-compose.yml` with all services
- `.env.example` with configuration template
- Deployment guide for Linux machines
- Health check and logging configuration

**Readiness Claim:** Docker Field Box flow ~75% ready; deployment flow validated; pending hardware-specific testing.

---

## Stage 3: Jetson Field Box Validation

**Status:** ⏸️ **Pending Hardware**

**Goal:** Deploy and validate DroneOS on Jetson developer kit.

### Objectives

- ⏳ Jetson ARM64 architecture compatibility verified
- ⏳ Docker deployment on Jetson successful
- ⏳ PX4 SITL connection via Jetson maintained
- ⏳ Performance benchmarks (CPU, memory, network latency)
- ⏳ Video I/O and sensor integration tested
- ⏳ Power consumption and thermal profiling

### Validation Criteria

- DroneOS backend runs stably on Jetson for 24+ hours
- Telemetry latency acceptable (<100ms over UDP)
- Video streaming from Jetson to dashboard at ≥15 FPS
- Thermal throttling does not occur under typical load
- Power draw within safety margins for UAV operation

### Deliverables

- Jetson deployment guide with setup steps
- Performance baseline report
- ARM64 compatibility issues documented and resolved
- Power and thermal analysis

**Readiness Claim:** After completion: Jetson Field Box ready for field testing with no-props bench drones.

---

## Stage 4: PX4 Hardware / No-Props Bench Testing

**Status:** ⏸️ **Pending**

**Goal:** Validate PX4 autopilot communication and safety mechanisms with real hardware (no propellers).

### Objectives

- ⏳ PX4 autopilot (e.g., Pixhawk 4) connected to Jetson Field Box
- ⏳ MAVLink communication and telemetry verified
- ⏳ Failsafe and RC override tested and confirmed
- ⏳ Mission upload and execution on real autopilot tested
- ⏳ Sensor fusion and state estimation accuracy verified
- ⏳ Emergency landing and recovery procedures validated

### Validation Criteria

- Telemetry from real PX4 matches SITL behavior
- RC override responds correctly in <1 second
- Failsafe mechanisms engage as configured
- Mission execution on real autopilot is repeatable
- No unexpected vehicle behavior or loss of control

### Deliverables

- Bench test checklist and procedures
- Safety configuration guide for PX4
- Hardware compatibility matrix
- Failure mode analysis and mitigation
- Go/no-go decision criteria for first flight

**Readiness Claim:** After completion: Ready to proceed to first controlled real flight.

---

## Stage 5: First Controlled Real Flight

**Status:** ⏸️ **Not Started**

**Goal:** Execute first autonomous flight with DroneOS and Jetson Field Box.

### Prerequisites

- ✅ Stage 4 validation complete
- ✅ Safety and failsafe procedures tested on bench
- ✅ Operator training and certification
- ✅ Airspace clearance and regulatory approval (if required)
- ✅ Recovery procedures and abort plan documented

### Objectives

- ⏳ Simple waypoint mission in open, empty area
- ⏳ Manual RC override remains operator control
- ⏳ Continuous telemetry streaming and monitoring
- ⏳ Post-flight analysis and data review

### Validation Criteria

- Autonomous takeoff, navigation, and landing completed
- No loss of control events
- Operator can assume manual control at any time
- Vehicle returns safely after mission
- All telemetry and logs available for analysis

### Deliverables

- Flight test report with video and telemetry logs
- Lessons learned and issues identified
- Updated safety and operational procedures

**Readiness Claim:** Real flight validated; operational constraints identified for next missions.

---

## Stage 6: Solar Inspection MVP with Video/Images and Report

**Status:** ⏸️ **Not Started**

**Goal:** Deliver minimum viable product for solar panel inspection with video capture, image storage, and structured reporting.

### Objectives

- ⏳ Video stream capture and storage during mission
- ⏳ Image extraction and timestamping
- ⏳ Geolocation tagging for captured images
- ⏳ Automated report generation (mission summary + image gallery)
- ⏳ Integration with solar inspection workflow
- ⏳ Payload integration (e.g., USB camera, thermal camera)

### Validation Criteria

- Video captured at ≥15 FPS, stored without corruption
- Image extraction produces usable frames every 1–2 seconds
- Geolocation accuracy within ±2 meters
- Report generated within 5 minutes of mission end
- Customer can review images and results in report

### Deliverables

- Video and image capture pipeline code
- Report template and generation logic
- Integration guide for camera payloads
- Solar inspection workflow documentation
- Example mission and report output

**Readiness Claim:** Solar inspection MVP ready for limited operational trials.

---

## Stage 7: Vehicle Agent Prototype

**Status:** ⏸️ **Not Started**

**Goal:** Develop onboard communication and diagnostic node for advanced telemetry and video relay.

### Objectives

- ⏳ Embedded compute node architecture design
- ⏳ MAVLink relay and command forwarding
- ⏳ Video stream capture and transcoding
- ⏳ Health monitoring and diagnostics
- ⏳ Real-time communication protocol (e.g., UDP, MAVLink)
- ⏳ Integration with Jetson Field Box

### Validation Criteria

- Vehicle Agent communicates with Field Box reliably
- Video stream quality and latency acceptable
- Diagnostics provide actionable health information
- Failsafe: if Vehicle Agent fails, PX4 and Field Box continue normal operation

### Deliverables

- Vehicle Agent firmware/software
- Communication protocol specification
- Integration guide with Field Box
- Troubleshooting and diagnostic procedures

**Readiness Claim:** After completion: Advanced telemetry and video available for inspection workflows.

---

## Stage 8: AI Vision Baseline

**Status:** ⏸️ **Not Started**

**Goal:** Implement AI vision for fault detection, anomaly identification, and automated reporting.

### Objectives

- ⏳ Object detection model baseline (e.g., YOLOv8 or equivalent)
- ⏳ Solar panel defect/fault detection trained on representative dataset
- ⏳ Model quantization for edge deployment
- ⏳ Real-time inference pipeline on Vehicle Agent or Field Box
- ⏳ Integration with solar inspection report generation
- ⏳ Performance benchmarking (accuracy, latency, compute cost)

### Validation Criteria

- Defect detection accuracy ≥85% on test dataset
- Inference latency <1 second per image
- False positive rate acceptable for user review workflow
- Model successfully deployed on Jetson hardware

### Deliverables

- Trained AI models and training code
- Edge inference pipeline
- Model performance report
- Integration guide for inspection reports

**Readiness Claim:** After completion: AI vision assists inspection workflows; human review remains required.

---

## Stage 9: Cloud Integration and Enterprise Features

**Status:** ⏸️ **Future**

**Goal:** Extend DroneOS with cloud connectivity, fleet management, and business intelligence.

### Objectives

- ⏳ Cloud API design and authentication
- ⏳ Async report and data upload from Field Box
- ⏳ Fleet management dashboard and multi-site oversight
- ⏳ Historical data storage and analytics
- ⏳ Predictive maintenance and health trends
- ⏳ Customer API and SaaS platform
- ⏳ Compliance and audit trail management

### Validation Criteria

- Data upload is reliable and encrypted
- Fleet dashboard provides useful operational insights
- Analytics enable predictive maintenance decisions
- Cloud services are cost-effective and scalable

### Deliverables

- Cloud backend architecture and API
- Fleet management UI
- Analytics dashboards
- SaaS documentation and terms

**Readiness Claim:** After completion: Enterprise-grade DroneOS platform ready for commercial deployment.

---

## Go/No-Go Criteria Between Stages

Before proceeding to the next stage, the following must be true:

1. **Previous stage objectives met**: All planned deliverables complete and tested
2. **Validation criteria satisfied**: Measurable success indicators achieved
3. **No critical blockers**: Known issues do not prevent progress
4. **Safety review passed**: Safety officer/advisor approves next phase
5. **Operator readiness**: Training and procedures in place for new capabilities
6. **Documentation updated**: Clear runbooks and procedures for new functionality

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Jetson hardware delays | Delays Stage 3+ | Procure early; use developer kits first |
| Regulatory delays | Delays real flight | Begin airspace coordination early |
| PX4 integration issues | Delays Stage 4+ | Maintain test matrix with multiple PX4 versions |
| Video/AI performance | Delays Stages 6–8 | Prototype on Jetson early; profile throughput |
| Third-party API changes | Delays Stages 6+ | Abstract external dependencies; test regularly |
| Personnel/resource constraints | Delays all stages | Plan sprints; prioritize critical paths |

---

## Communication and Public Claims

- **During Stages 1–4**: "Lab/SITL prototype, under active development"
- **During Stages 5–6**: "Real flight validated, inspection MVP operational"
- **During Stages 7–8**: "Advanced telemetry and AI vision available"
- **During Stage 9**: "Enterprise-grade platform ready for commercial operations"

**Always include:** "Not production-ready, not certified, requires operator supervision and regulatory approval for real operations."

---

**See [Current Status](current_status.md) for weekly progress updates.**

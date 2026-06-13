# Architecture Overview

## ONEL Dynamics Vision

**ONEL Dynamics** is envisioned as an enterprise IT and R&D company focused on autonomous drone operations, inspection services, and AI-driven analytics. DroneOS is the software foundation that enables this vision.

## DroneOS: The Mission Operating System

DroneOS is a **mission/operator layer** for PX4-based drones. It abstracts mission coordination, telemetry aggregation, reporting, and diagnostics from the flight control layer, allowing:

- Autonomous mission workflows and multi-vehicle supervision
- Structured telemetry and operator monitoring
- Integration with specialized services (inspection, analytics, AI vision)
- Edge deployment via Field Box for local-first operations
- Future cloud integration for fleet analytics and business intelligence

## System Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                   Operator Dashboard                             │
│            (Web UI, Mission Planning, Fleet Monitoring)          │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   DroneOS Field Box                              │
│         (Mission Coordination, Telemetry, Reporting,             │
│          Health Checks, Diagnostics, Service Orchestration)     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                   MAVLink/UDP
                    Boundary
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    Vehicle Agent                                 │
│         (Onboard Communication, Diagnostic Relay,                │
│          Video/Sensor Aggregation, Local Computing)             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                   MAVLink/Serial
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    PX4 Flight Stack                              │
│         (Flight Control, Sensor Fusion, Failsafe,                │
│          RC Override, Autopilot Mode Management)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                    Hardware/Sensors
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Drone + Payload                                │
│      (Airframe, Actuators, Sensors, Cameras, Batteries)         │
└─────────────────────────────────────────────────────────────────┘
```

## Core Boundaries and Responsibilities

### PX4 (Flight Authority)

**PX4 owns flight safety and control:**

- Attitude stabilization and flight mode management
- Sensor fusion and state estimation
- RC receiver override and failsafe logic
- Motor safety and propeller kill switches
- Geofencing (hardware-based confidence layer)

**PX4 does NOT:**

- Plan or optimize missions beyond simple waypoint navigation
- Aggregate telemetry from multiple vehicles or sensors
- Generate mission reports or analytics
- Coordinate with ground operators or dashboards

### DroneOS (Mission and Operations)

**DroneOS owns mission coordination and reporting:**

- Mission planning, conflict detection, and execution sequencing
- Telemetry collection, aggregation, and real-time streaming
- Operator dashboard and mission supervision
- Structured flight reporting and audit trails
- Health diagnostics and recovery coordination
- Integration with specialized services (inspection, analytics, vision)

**DroneOS does NOT:**

- Command attitude, rate, or directly control actuators (PX4 does)
- Claim to be safer or more reliable than PX4 (it is not)
- Replace operator decision-making or RC override
- Handle safety-critical real-time control loops

### Vehicle Agent (Future)

**Vehicle Agent owns onboard intelligence and relay:**

- Video/sensor streaming to Field Box
- Local diagnostics and telemetry relay to DroneOS
- Onboard computing for time-sensitive workloads (e.g., obstacle detection)
- Battery management and health monitoring
- Payload coordination

### Operator Dashboard

**Dashboard owns operator situational awareness:**

- Real-time vehicle tracking and state visualization
- Mission planning and upload interface
- Flight history review and reporting
- Alerts and health monitoring
- Manual RC control fallback interface

## Future Enterprise Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      Cloud Services                               │
│  (Fleet Analytics, Business Intelligence, AI Model Training,      │
│   Compliance Reporting, Historical Analysis)                     │
└───────┬────────────────┬────────────────────┬─────────────────┬──┘
        │                │                    │                 │
   Analytics         AI Vision          Solar Inspection    Compliance
   Pipeline          Services           Services           & Audit
        │                │                    │                 │
        └────────────────┼────────────────────┼─────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │   ONEL Control & Analytics    │
         │  (Multi-Field Box Oversight)  │
         └───────────────┬───────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
  ┌─────▼──────┐                 ┌──────▼──────┐
  │ Field Box  │                 │ Field Box   │
  │  Site A    │    ...          │  Site B     │
  └──────┬──────┘                 └──────┬──────┘
         │                               │
      Drones                          Drones
```

## Deployment Model: Field Box

A **Field Box** is an edge compute node (currently Docker-based, future Jetson-based) that:

1. **Hosts DroneOS**: Mission engine, telemetry aggregation, reporting
2. **Hosts Operator Dashboard**: Local or remote web interface
3. **Manages Vehicle Agents**: Communicates with onboard systems
4. **Manages PX4 Connections**: MAVLink gateway to autopilots
5. **Coordinates Services**: Inspection workflows, video capture, AI analysis
6. **Logs and Reports**: Flight history, mission outcomes, diagnostics
7. **Operates Autonomously**: Can function offline; syncs to cloud when available

### Benefits

- **Local-first**: Low-latency mission execution and telemetry
- **Reliability**: Operates without cloud if necessary
- **Privacy**: Sensor data and flight plans stay local unless explicitly synced
- **Scalability**: Multiple Field Boxes can be managed from central cloud
- **Flexibility**: Can be deployed as containerized (Docker) or embedded (Jetson)

## Future Services and Departments

### AI Vision Department

- Object and anomaly detection
- Solar panel fault identification
- Crop and field health analysis
- Model training and optimization
- On-device and cloud inference

### Inspection Services

- Solar panel inspection workflows
- Thermal imaging analysis
- Structural inspection protocols
- Automated defect reporting
- Integration with solar energy companies

### Cloud and Analytics

- Fleet-wide performance dashboards
- Predictive maintenance and health trends
- Compliance and audit trail management
- Historical data analysis and ML training
- Integration with customer business systems

### Field Operations

- Operator training and certification
- Hardware maintenance and logistics
- Site management and compliance
- Customer support and issue resolution

## Design Principles

1. **Clear Separation of Concerns**: Each layer has defined responsibilities; no layer bypasses another
2. **Recovery Independence**: If any layer fails, the layer below remains operational
3. **Local-First**: Edge compute is primary; cloud is asynchronous enhancement
4. **Operator Centrality**: Humans remain in decision-making loop; automation assists, not replaces
5. **Open Standards**: PX4/MAVLink are industry standards; DroneOS is not proprietary
6. **Security Through Isolation**: Flight control and mission control are distinct attack surfaces
7. **Testability**: Each layer can be validated independently before integration

## Integration Points

| Interface | Protocol | Direction | Purpose |
|-----------|----------|-----------|---------|
| Operator ↔ Dashboard | HTTP/WebSocket | Bidirectional | Mission planning, monitoring, manual control |
| Dashboard ↔ DroneOS | HTTP/REST, WebSocket | Bidirectional | Mission upload, telemetry streaming, diagnostics |
| DroneOS ↔ Vehicle Agent | HTTP, MAVLink | Bidirectional | Command relay, telemetry aggregation, health checks |
| DroneOS ↔ PX4 | MAVLink/UDP | Bidirectional | Mission waypoints, telemetry, mode commands |
| DroneOS ↔ Cloud | HTTPS/Sync API | Asynchronous | Report upload, analytics sync, model updates |

## Future Enhancements

- **Multi-Vehicle Coordination**: Swarm mission planning and collision avoidance
- **Advanced Autonomy**: AI-driven mission adaptation and obstacle avoidance
- **Hardened Security**: Public-key cryptography, secure boot, firmware integrity
- **Hardware Redundancy**: Dual autopilots, hot standby, recovery automation
- **Regulatory Integration**: Compliance workflows, airspace coordination, certification
- **Commercial Platform**: SaaS dashboards, customer API, billing integration

---

**For safety and operational details, see [Safety Notes](safety_notes.md).**

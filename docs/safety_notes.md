# Safety and Operational Requirements

**⚠️ CRITICAL:** DroneOS is not a replacement for PX4, and this overview is not a safety document. Real drone flight requires comprehensive safety engineering, regulatory compliance, and operational oversight. This document outlines key principles and requirements for safe operation.

## Core Safety Principles

### 1. PX4 is Flight Authority

**Non-negotiable principle:** PX4 remains the flight control authority at all times. DroneOS:

- ✓ Coordinates missions and telemetry
- ✓ Commands high-level behaviors (waypoint navigation, RTH)
- ✓ Monitors vehicle state and diagnostics

DroneOS does NOT:

- ✗ Override PX4 safety mechanisms
- ✗ Directly command actuators, rates, or attitudes
- ✗ Replace RC override or failsafe logic
- ✗ Substitute for human operator oversight

### 2. Recovery Independence

**If DroneOS is unavailable, PX4 must still land safely.**

- PX4 must be configured with independent failsafe mechanisms (e.g., RTH on signal loss)
- RC receiver must be able to assume control at any time
- Mission abort must not require communication with DroneOS backend
- Operator must retain ability to land manually via RC transmitter

### 3. Operator Oversight

**Humans remain in the decision-making loop.**

- Every autonomous mission must have operator supervision
- Operator must be trained and certified for the specific operation
- Manual RC override must be immediately available
- Operator must understand limitations and can abort at any time

### 4. Validation Precedes Deployment

**Lab/SITL success does not equal real flight readiness.**

- Hardware validation required before first flight
- Failsafe and RC override tested on real autopilot
- No-props bench testing completed
- Weather, airspace, and site-specific hazards assessed

## Pre-Flight Checklist

Before flying any autonomous mission with DroneOS:

### Hardware Validation

- [ ] PX4 autopilot powered on and armed successfully in SITL
- [ ] Real PX4 autopilot (if applicable) communicates with Field Box
- [ ] MAVLink connection established and telemetry received
- [ ] RC receiver functional and responds to transmitter commands
- [ ] Failsafe mode (e.g., RTH) confirmed on real PX4
- [ ] Propellers removed (if ground testing)
- [ ] Battery fully charged and voltage within safe range
- [ ] All sensors calibrated (compass, accelerometer, gyro)
- [ ] Vehicle weight within specified limits

### Software Configuration

- [ ] DroneOS backend running and dashboard accessible
- [ ] Telemetry streaming at ≥10 Hz
- [ ] Mission file verified in SITL first
- [ ] Geofence (if applicable) properly configured in PX4
- [ ] Failsafe behavior set to RTH with reasonable altitude
- [ ] RC failsafe configured to activate on signal loss
- [ ] Flight mode switcher tested (manual ↔ auto)

### Environmental/Operational

- [ ] Weather conditions suitable (wind, rain, visibility)
- [ ] Airspace checked for other aircraft or obstructions
- [ ] Regulatory approval obtained (if required)
- [ ] Safety perimeter established and cleared
- [ ] Operator trained on emergency procedures
- [ ] Second person available for safety spotting
- [ ] Emergency landing zone identified
- [ ] Medical and emergency services contacted (if required)

### Pre-Arm Actions

- [ ] All checklist items above signed off
- [ ] Vehicle in clear, level area away from people/obstacles
- [ ] Motor/propeller safety checked
- [ ] RC transmitter on and communication confirmed
- [ ] Operator briefing complete; abort plan understood
- [ ] Final visual inspection of vehicle

## Flight Testing Phases

### Phase 1: No-Props Bench Testing

**Objective:** Validate autopilot, sensors, and failsafe without flight risk.

- PX4 connected to Field Box
- Motors disabled or propellers removed
- Failsafe triggers (signal loss, low battery, geofence) tested
- Manual and auto mode switching verified
- Telemetry and logging confirmed
- Expected duration: 30–60 minutes

**Go/No-Go:** If all systems respond correctly, proceed to Phase 2.

### Phase 2: First Controlled Flight

**Objective:** Validate autonomous flight with continuous operator supervision.

- Simple waypoint mission in open area (no obstacles)
- Mission duration <15 minutes
- Operator ready to assume manual control at any time
- Continuous telemetry monitoring
- Ground chase vehicle for line-of-sight (if required)

**Success Criteria:**
- Autonomous takeoff and navigation completed
- All waypoints reached within ±5 meters
- Autonomous landing completed safely
- No loss of control events
- All telemetry logged successfully

**Go/No-Go:** If all criteria met and analysis shows no anomalies, clear for routine missions.

### Phase 3: Expanded Missions

**Objective:** Gradually increase mission complexity and duration.

- Longer missions (up to planned operational duration)
- More waypoints and turns
- Video/image capture (if applicable)
- Operator supervision and log analysis

**Proceed when:** Each previous phase successful; no anomalies in logs.

## Known Limitations and Constraints

### Software Maturity

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| No redundant telemetry | Loss of visibility if connection drops | Always maintain line-of-sight |
| No certified geofence | Software geofence not a safety barrier | Physical perimeter + operator supervision |
| No automatic collision avoidance | Cannot sense obstacles | Fly in open areas; pre-plan trajectories |
| Limited failsafe sophistication | May not handle all failure modes | Comprehensive pre-flight checklist |
| No production security | Potential for unauthorized access/control | Operate on isolated networks; use VPN if needed |

### Hardware Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| PX4 SITL only (current) | Real flight not yet validated | Complete hardware and flight testing before operations |
| No Jetson Field Box yet | Deployment pending | Use docker on standard Linux for initial testing |
| Battery endurance TBD | Mission duration unknown | Conservative estimates; always have reserve power |
| Weather capability unknown | May not fly in rain/wind | Start in calm conditions; characterize limits |

### Operational Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| Single operator required | Limited scalability | Add observer; plan for multiple vehicles later |
| No beyond-visual-line-of-sight (BVLOS) | Local area operations only | Obtain BVLOS waiver if needed (regulatory process) |
| No night operations | Daylight only | Equip with lighting for extended operation (if approved) |
| No communication relay | Range limited by radio | Stay within communication range; use range extender if needed |

## Regulatory Compliance

**DroneOS is not regulatory advice.** Depending on your jurisdiction, real drone operations may require:

- Operator certification or licensing
- Remote ID and airspace registration
- Visual line-of-sight (VLOS) or specific airspace approval
- Insurance and liability coverage
- Environmental impact assessment
- Airspace coordination (Class B/C airports, etc.)
- Safety approvals from aviation authority

**Before flying, consult:**

- FAA regulations (Part 107 in USA)
- Local aviation authority rules
- Your organization's legal and safety teams

## Incident and Failure Response

### If Communication is Lost

1. PX4 failsafe activates automatically (e.g., RTH)
2. Operator assumes manual RC control
3. Land vehicle safely in clear area
4. Do not attempt to regain autonomous control mid-flight
5. Power down and investigate after landing

### If Telemetry Stops

1. Operator immediately switches to manual (RC) control
2. Land vehicle safely
3. Check Field Box and network connectivity
4. Review logs for root cause
5. Do not fly again until issue resolved

### If Vehicle Behaves Unexpectedly

1. Immediately assume manual RC control
2. Land vehicle in safe area
3. Do not attempt to resume autonomous operation
4. Power down and investigate
5. Review telemetry logs and sensor data
6. Correct root cause before next flight

### If Propeller Damage or Motor Issue Detected

1. Land immediately
2. Power down all systems
3. Inspect for damage
4. Do not fly until replaced/repaired
5. Test on bench with no-props before next flight

## Post-Flight Analysis

After every flight:

1. **Download and review logs**: Telemetry, PX4 logs, video
2. **Check for anomalies**: Unexpected behavior, sensor errors, communication dropouts
3. **Verify telemetry completeness**: All data points recorded
4. **Document observations**: What went well, what needs improvement
5. **Update procedures**: If new issues found, adjust checklists or configuration
6. **Archive records**: Long-term storage for compliance and troubleshooting

## Safety Culture

**Implement a safety-first culture:**

- Encourage reporting of issues without blame
- Prioritize safety over schedule or cost
- Ask "Why?" multiple times to find root causes
- Learn from near-misses, not just accidents
- Regularly review and update procedures
- Maintain clear communication between team and operators
- Celebrate safe operations; take failures seriously

## Training and Certification

Operators must be trained in:

1. **DroneOS basics**: Dashboard, mission planning, telemetry interpretation
2. **PX4 concepts**: Flight modes, failsafe behavior, RC override
3. **Vehicle-specific**: Payload, battery, weather limits
4. **Emergency procedures**: Loss of comms, manual recovery, abort protocols
5. **Regulatory**: Local rules and operational constraints
6. **First aid**: Basic medical response for field operations

**Maintain training records and recertify regularly.**

## Questions or Concerns?

If you identify a safety issue or have questions about safe operation:

1. **Document the issue**: What happened, when, and why it's a concern
2. **Contact the team privately**: Do not post safety issues publicly
3. **Collaborate on mitigation**: Work together to understand and resolve
4. **Update procedures**: Ensure others learn from the issue

## Additional Resources

- **[Architecture Overview](architecture_overview.md)** – Understand system design and boundaries
- **[Current Status](current_status.md)** – What has been validated and what is pending
- **[Roadmap](roadmap.md)** – Development stages and validation requirements
- **PX4 Safety Documentation**: https://docs.px4.io/main/en/safety/
- **FAA Part 107 (USA)**: https://www.faa.gov/uas/commercial_operators/part_107/
- **ASTM F3269** (Standard for Operations of Small UAS): Industry standard for safe UAS operations

---

**Remember: Safe operations require continuous attention to detail, honest communication about limitations, and respect for the power and risks of autonomous systems.**

# Development Roadmap

DroneOS development is organized into conservative milestones. Each phase is intended to be gated by validation criteria, hardware readiness, and safety review.

## Current Phase
**Advanced Lab/SITL + Field Box stabilization**

Jetson Field Box hardware validation is the next major milestone.

## Phases

1. **Phase 1: Lab/SITL stabilization**
   - Stabilize DroneOS architecture in simulation
   - Validate mission upload, telemetry, and PX4 SITL execution
   - Refine the dashboard runtime harness and local mission flow

2. **Phase 2: Field Box Docker/local deployment**
   - Containerize DroneOS backend and dashboard for edge deployment
   - Validate local Field Box startup, health checks, and mission flow
   - Clarify that Docker deploys DroneOS backend/dashboard only, not PX4 or Gazebo

3. **Phase 3: Jetson Field Box validation**
   - Validate ARM64 deployment and Jetson compatibility
   - Confirm Docker/local Field Box stability on Jetson hardware
   - Run PX4 SITL mission flow on Jetson as a preparation step

4. **Phase 4: PX4 hardware / no-props bench validation**
   - Validate real PX4 autopilot communication on bench hardware
   - Verify MAVLink telemetry, failsafes, and RC override behavior
   - Ensure hardware safety practices before first flight

5. **Phase 5: First controlled real flight**
   - Execute a controlled, simple waypoint mission
   - Keep manual RC override and operator supervision as the primary safety path
   - Collect telemetry, logs, and post-flight analysis

6. **Phase 6: Solar inspection MVP / pilot**
   - Deliver an inspection workflow with video/image capture and reporting
   - Use local Field Box processing to support inspection mission planning
   - Keep AI/thermal defect detection as future R&D unless validated

7. **Phase 7: Vehicle Agent Lite / onboard node**
   - Define optional onboard communication and relay node
   - Support sensor telemetry, local diagnostics, and video/sensor relay
   - Keep Vehicle Agent future/optional for Field Box v0.1 architecture

8. **Phase 8: AI vision baseline**
   - Add a measured AI vision baseline for future inspection workflows
   - Focus on dataset, evaluation criteria, and human-reviewed outcomes
   - Do not claim validated defect detection before it is proven

9. **Phase 9: Cloud / analytics future**
   - Explore optional cloud synchronization, fleet analytics, and reporting
   - Keep cloud as an extension after local Field Box workflows are stable

## Validation Criteria
Each phase should be gated by clear acceptance criteria, including:

- validated functionality in the intended environment
- documented safety and hardware assumptions
- operator supervision and recovery procedures
- regression testing and functional verification
- clear limits on what is not yet validated

## Public Claims
- Emphasize the current stage: lab/SITL and Field Box stabilization
- Do not claim production readiness or certification
- Do not claim real flight validation
- Do not claim AI/thermal defect detection as implemented
- Clarify that PX4 remains the flight authority and that DroneOS is the mission/operator layer

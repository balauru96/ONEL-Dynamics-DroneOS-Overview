# Collaboration Guidelines

This repository is the public-safe documentation and presentation surface for ONEL Dynamics / DroneOS.

The active private engineering source of truth is **DroneOS-Core**. Do not copy private implementation details from DroneOS-Core into this repository.

## This Repository Is For
- project status and roadmap updates
- public-safe architecture explanations
- grant and partner discussions
- validation summaries
- safety and operational documentation
- pilot/customer-facing technical context

## Do Not Publish Here
- private DroneOS-Core source code
- mission/safety implementation details that expose operational logic
- authentication/token implementation details
- private credentials, `.env` files, IP addresses or deployment secrets
- private logs or internal incident reports
- proprietary datasets or model artifacts
- claims of physical-flight, certification or production readiness without validation

## Current Collaboration Areas
Useful public-safe collaboration areas include:

- Jetson Field Box deployment and operational documentation
- PX4 hardware bench-validation procedures
- Vehicle Agent Lite / camera integration planning
- Solar inspection workflow and report UX
- dataset/evaluation methodology for panel mapping and future thermal analysis
- Mission Control / dashboard UX
- regulatory and pilot-readiness research
- grant and customer-discovery preparation

## Engineering Validation Principle
Flight-facing changes should continue to follow the project validation ladder:

**deterministic tests → SITL → hardware bench → controlled physical flight**

PX4 remains the flight authority. DroneOS remains the mission/workflow/operator layer.

## Public Status Discipline
When describing the project externally:

- say that Jetson Field Box engineering validation exists
- say that the Solar two-flight workflow has been validated through real PX4 SITL
- distinguish real SITL mission execution from deterministic camera/media fixtures
- do not claim physical-aircraft validation yet
- do not claim certified/commercial readiness
- do not claim production thermal defect detection

## Contact
For collaboration, partner or grant discussions, contact the project maintainer privately.

# Collaboration Guidelines

> Updated: **15 September 2026**.

This repository is the public-safe documentation and presentation surface for ONEL Dynamics / DroneOS.

The active private engineering source of truth is **DroneOS-Core**. Do not copy private implementation details from DroneOS-Core into this repository.

## This Repository Is For
- project status and roadmap updates
- public-safe architecture explanations
- grant/funding and partner discussions
- validation summaries
- safety/operational documentation
- pilot/customer-facing technical context

## Do Not Publish Here
- private DroneOS-Core source code
- flight/safety implementation details that expose sensitive operational logic
- authentication/token implementation details
- credentials, `.env` files, private IP/deployment secrets
- private logs or internal incident reports
- proprietary datasets/model artifacts
- claims of physical-flight, certification or production readiness without evidence

## Current Collaboration Areas
Useful public-safe collaboration areas now include:

- physical PX4 hardware bench planning
- Vehicle Agent Lite + real camera integration
- vehicle↔Field Box network/data-transfer validation
- controlled first-flight test planning
- Solar mapping/evaluation methodology
- future RGB/thermal defect-analysis evaluation
- operator dashboard / report UX
- regulatory/pilot-readiness research
- grant and customer-discovery preparation

The software/Jetson simulator composition is already strong enough that collaboration should now prioritize **physical validation and measurable pilot evidence** over broad new feature scope.

## Engineering Validation Principle
Flight-facing changes should continue to follow:

**deterministic tests → SITL → Jetson Field Box E2E → hardware bench → controlled physical flight → pilot**

PX4 remains flight authority. DroneOS remains the mission/workflow/operator/data layer.

## Public Status Discipline
When describing the project externally:

- say that the canonical Solar software workflow is E2E validated
- say that full software E2E has run on the NVIDIA Jetson Field Box
- say that both missions execute through real PX4 SITL/Gazebo
- distinguish real PX4 execution from deterministic demo camera/media data
- say that the redesigned operator dashboard has been validated
- do not claim physical-aircraft validation yet
- do not claim certified/commercial readiness
- do not claim production thermal/RGB defect detection

## Contact
For collaboration, partner, pilot or grant discussions, contact the project maintainer privately.

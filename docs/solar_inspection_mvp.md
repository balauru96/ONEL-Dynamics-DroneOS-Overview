# Solar Inspection MVP

The solar inspection MVP is an initial product direction for DroneOS. It focuses on local-first workflows, mission planning, and structured reporting for solar array inspection.

## Two-Stage Workflow

1. **Recon / mapping mission**
   - Fly an initial mission to capture imagery and sensor data
   - Map the inspection area and gather site context
   - Collect data in a format suitable for post-flight processing

2. **Post-flight local processing on the Field Box**
   - Transfer captured data to the local Field Box
   - Perform panel layout detection and mapping as a future baseline goal
   - Generate an inspection route based on the mapped layout
   - Execute a follow-up inspection mission
   - Produce a local report summarizing mission outcomes and captured evidence

## What This MVP Includes
- local mission planning for recon and inspection
- dashboard-driven mission upload and monitoring
- local processing direction on the Field Box
- report generation for mission summary and media evidence
- clear separation between mission coordination and PX4 flight authority

## What This MVP Does Not Include Yet
- AI/thermal defect detection is future research and not yet validated
- fully automated panel inspections with defect scoring
- certified commercial inspection operations
- real flight validation with production aircraft

## Future Baseline Goals
- panel layout detection and mapping on the Field Box
- inspection route generation from mapped panel layouts
- local report generation linked to mission telemetry
- optional onboard sensor relay via Vehicle Agent Lite
- measured AI vision support after validation

# Operator Dashboard Validation

> Public-safe snapshot: **15 September 2026**.

## Objective
The dashboard redesign turns the original engineering-heavy interface into a clearer **operator mission-control surface** without moving authority into the browser.

The dashboard remains a presentation and operator-intent layer. Backend state, mission identity, workflow authority and safety checks remain server-side; PX4 remains flight authority.

## Validated UI Direction
The current dashboard has been validated on both the **NVIDIA Jetson Orin Nano Super Field Box** and the development laptop.

Key changes:

- canonical Solar workflow moved to the primary operator position
- visual workflow stepper: `SETUP → RECON → PROCESS → REVIEW → INSPECTION → REPORT`
- contextual actions for:
  - Start Solar Inspection
  - Prepare Recon Mission
  - Start Flight
  - Confirm Inspection Route
  - Open Inspection Report
- all critical top-toolbar controls and status remain visible
- LAND / RTL / STOP / CANCEL remain visibly separated as recovery/interrupt actions
- map remains the dominant mission workspace
- Flight Status HUD remains visible over the map
- technical/non-routine tools moved into collapsed Advanced sections
- credential-free OpenStreetMap basemap used for the current MVP/demo baseline

## Validation Evidence
Current review-line validation includes:

- **83 dashboard runtime checks passed**
- `git diff --check` clean on the basemap regression fix
- dashboard exercised during full Solar E2E on Jetson
- dashboard exercised on laptop
- canonical Solar workflow remains functionally unchanged

## Authority / Safety Boundary
The redesign does **not** change:

- PX4 command behavior
- mission lifecycle semantics
- StateService authority
- safety/geofence authority
- Solar Recon/Inspection backend processing
- trusted ingestion/provenance/reporting
- API contracts

The browser still submits operator intent; the server must revalidate current state/identity before authoritative transitions.

## Basemap Regression Fix
During visual validation, legacy map providers could return authentication-watermark tiles. The current default unauthenticated basemap was narrowed to the canonical OpenStreetMap tile endpoint with visible attribution.

This is an MVP/demo choice, not a final commercial mapping-infrastructure decision. Production deployment will require a map provider or self-hosted strategy appropriate to expected traffic, availability and licensing requirements.

## Current Status
The redesign is **validated as a technical-MVP operator interface** and remains under final integration review at this snapshot.

It should be treated as the visual baseline for physical-validation demos, while additional UI work should remain secondary to the next major engineering milestone: real hardware/camera validation.

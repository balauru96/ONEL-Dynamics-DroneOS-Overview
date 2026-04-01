🚁 DroneOS

DroneOS is a modular software platform for autonomous drone missions, designed for real-time control, mission planning, and edge-based data processing.

Built with a focus on reliability, modularity, and local-first operation, DroneOS enables drones to execute missions safely—even under unstable connection conditions.

---

✨ Key Features

🧭 Mission Planning

- Waypoint-based missions (survey, patrol, inspection, agriculture)
- Dynamic mission generation
- Real-time path preview

🛰 PX4 Integration (MAVSDK)

- Full mission upload and execution
- Takeoff, land, RTL (Return-To-Launch)
- Live telemetry synchronization

🔁 Connection Resilience

- Automatic reconnect to PX4
- No UI freeze or backend crash on disconnect
- Safe state recovery

🗺 Interactive Dashboard

- Real-time map visualization
- Live telemetry (position, battery, altitude, mode)
- Mission execution tracking

🚫 Geofencing / No-Fly Zones

- Define restricted areas
- Prevent invalid mission planning

📡 Live Telemetry Streaming

- WebSocket-based real-time updates
- Flight history logging

---

🧱 Architecture

DroneOS is built as a modular system:

UI (Dashboard)
   ↓
FastAPI Backend (Mission, State, Control)
   ↓
PX4 Bridge (MAVSDK)
   ↓
PX4 Autopilot (Simulation / Real Drone)

---

🚀 Getting Started

1. Start PX4 (SITL)

cd PX4-Autopilot
make px4_sitl gazebo

2. Start Backend

cd ONEL_DYNAMICS_PROJECT
uvicorn server:app --reload

3. Open Dashboard

http://127.0.0.1:8000/dashboard

---

🎬 Demo Capabilities

DroneOS currently supports:

- Autonomous mission execution
- Real-time control via dashboard
- Automatic reconnect during mission (fault tolerance)
- Live telemetry visualization
- Return-to-launch (RTL) behavior

---

⚙️ Tech Stack

- Backend: FastAPI (Python)
- Drone Communication: MAVSDK / MAVLink
- Autopilot: PX4
- Frontend: HTML / JavaScript dashboard
- Simulation: Gazebo

---

🧠 Design Principles

- Local-first processing (no dependency on cloud)
- Modular architecture (UI, backend, bridge separation)
- Fault tolerance (reconnect & recovery mechanisms)
- Real-time responsiveness

---

📍 Current Status

- ✅ PX4 integration complete
- ✅ Mission planning & execution
- ✅ Telemetry synchronization
- ✅ Reconnect handling
- 🔧 Ongoing: stabilization & real-world deployment

---

🎯 Vision

DroneOS aims to become a sovereign European platform for autonomous drone operations, enabling:

- Secure local data processing (Edge AI)
- Industrial inspection workflows
- Scalable fleet management (future cloud layer)
- Modular hardware integration

---

👤 Author

Onel Ionut
Founder, ONEL Dynamics

---

📄 License

Private / Proprietary (for now)
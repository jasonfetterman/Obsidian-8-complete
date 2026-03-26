# OBSIDIAN-8 System Architecture Diagram

This document describes the high‑level architecture of the OBSIDIAN‑8 robotics platform and how all major subsystems interact.

Reference documents:

- 00_System_Definition/OBSIDIAN8_MASTER_BOM_REV_B.md
- 02_Electrical/POWER_DISTRIBUTION_DIAGRAM.md
- 03_Control_Architecture/LEG_KINEMATICS_SPEC.md
- 04_Autonomy/SWARM_CONTROL_ARCHITECTURE.md
- 05_Perception/HEAD_MODULE_V1.md

---

## System Overview

Sensors → Jetson AI → Mission Control → Motion Control → Servos

External communication flows through the swarm network layer.

---

## Major Subsystems

### Perception Layer
Runs on the Jetson Orin NX.

Sensors:
- Intel RealSense D455
- Luxonis OAK‑D Pro
- Slamtec RPLidar S2
- VectorNav VN‑100 IMU
- 6 × IMX477 cameras

Responsibilities:
- SLAM mapping
- terrain analysis
- object detection
- localization

---

### Mission Control Layer
Runs on Raspberry Pi 5.

Responsibilities:
- mission planning
- swarm coordination
- task allocation
- network communication

---

### Motion Control Layer
Runs on Teensy 4.1.

Responsibilities:
- gait generation
- stabilization
- joint control

---

### Actuation Layer

24 × AGFRC A86BHMW brushless servos.

Each leg contains:

- Coxa joint
- Femur joint
- Tibia joint

---

### Power Layer

Battery:
24V 30Ah LiFePO4

Power rails:

- 8V servo rail
- 12V sensor rail
- 5V logic rail

Conversion handled by MeanWell RSD‑500 DC‑DC converters.

---

### Swarm Network

Communication:

WiFi 6 mesh network using Ubiquiti UniFi U6 Mesh hardware.

Software:

ROS2 DDS messaging layer.
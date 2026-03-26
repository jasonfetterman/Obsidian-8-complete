# OBSIDIAN-8 Swarm System

Reference:
04_Autonomy/SWARM_CONTROL_ARCHITECTURE.md

---

## Command Robot

Platform:

OBSIDIAN-8 (45 inch octopod)

Responsibilities:

- global SLAM mapping
- task allocation
- navigation planning
- swarm coordination
- communications hub

Compute:

Jetson Orin NX + Raspberry Pi 5

---

## Worker Robots

Approximate size:

22 inch platforms

Typical hardware:

- Raspberry Pi 4/5
- depth camera
- IMU
- WiFi communication

Worker responsibilities:

- area exploration
- environment scanning
- data relay

---

## Network Architecture

Communication Model:

Workers → Command Node → Workers

Hardware:

Ubiquiti U6 Mesh

Software:

ROS2 DDS

---

## Mission Control

The command robot assigns:

- exploration sectors
- mapping tasks
- inspection tasks
- return‑to‑dock commands
# OBSIDIAN-8 Build Guide

---

## Phase 1 — Mechanical Assembly

Reference:
01_Mechanical/OBSIDIAN8_MECHANICAL_LAYOUT.md

Steps:

1. Assemble 3030 chassis ring
2. Install cross‑bracing
3. Mount battery tray
4. Install leg mounting brackets

---

## Phase 2 — Leg Assembly

Reference:
03_Control_Architecture/LEG_KINEMATICS_SPEC.md

Steps:

1. Install coxa servo
2. Install femur assembly
3. Install tibia segment
4. Attach TPU foot pad

Repeat for all 8 legs.

---

## Phase 3 — Electrical System

Reference:
02_Electrical/POWER_DISTRIBUTION_DIAGRAM.md

Steps:

1. Install battery
2. Install DC‑DC converters
3. Wire servo power rails
4. Install fuses and contactors

---

## Phase 4 — Sensor Installation

Reference:
05_Perception/HEAD_MODULE_V1.md

Steps:

1. Install head mast
2. Mount cameras
3. Install lidar
4. Install IMU

---

## Phase 5 — Software Deployment

1. Install OS on Jetson and Pi
2. Configure ROS2
3. Deploy motion control stack
4. Deploy swarm communication
# OBSIDIAN-8 Hardware Overview

Reference BOM:
00_System_Definition/OBSIDIAN8_MASTER_BOM_REV_B.md

---

## Actuation

Servos:

24 × AGFRC A86BHMW HV Brushless Servo

Specifications:

- 400 kg·cm torque
- steel gear train
- dual ball bearings
- CNC aluminum case

---

## Frame System

Primary structure:

- 3030 aluminum extrusion ring
- 2020 aluminum bracing
- 3 mm aluminum mounting plates

Printed components:

- coxa housings
- femur beams
- tibia beams

Material:

PA6‑CF or PA12‑CF carbon‑fiber nylon

---

## Power System

Battery:

LiTime 24V 30Ah LiFePO4

Power Conversion:

2 × MeanWell RSD‑500

Protection:

- 150A ANL fuse
- contactors
- E‑stop system

---

## Sensors

Navigation:

- Intel RealSense D455
- RPLidar S2
- VectorNav VN‑100 IMU

Vision:

- Luxonis OAK‑D Pro
- 6 × Arducam IMX477 cameras

---

## Networking

Swarm Communication:

Ubiquiti UniFi U6 Mesh

Protocol:

ROS2 DDS
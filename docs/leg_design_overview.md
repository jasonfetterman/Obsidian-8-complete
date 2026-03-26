# OBSIDIAN-8 Leg Design Overview

Reference:
03_Control_Architecture/LEG_KINEMATICS_SPEC.md

The OBSIDIAN‑8 robot uses an 8‑leg octopod configuration optimized for stability and terrain traversal.

---

## Leg Structure

Each leg contains three degrees of freedom.

Joints:

1. Coxa (horizontal rotation)
2. Femur (upper leg pitch)
3. Tibia (lower leg extension)

Total actuators:

24

---

## Geometry

Coxa length: 70 mm  
Femur length: 210 mm  
Tibia length: 260 mm  

Neutral stance radius:

~550 mm from robot center.

---

## Mechanical Design

Frame materials:

- aluminum extrusion chassis
- carbon‑fiber reinforced nylon printed components

Printed components:

- coxa housings
- femur beams
- tibia beams

---

## Stability Model

The robot maintains a support polygon using at least four legs in contact with the ground.

Primary gait:

Tripod gait.

Secondary gait:

Wave gait for rough terrain.
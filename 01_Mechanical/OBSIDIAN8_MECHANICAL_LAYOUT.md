# OBSIDIAN-8 MECHANICAL LAYOUT (V3.3)

## Overview

This document defines the physical mechanical layout of the OBSIDIAN‑8
octopod platform (hybrid extrusion + 3D printed design). It establishes the
core geometry and modular assembly references used when building the robot in CAD.

Target Platform Size: 45 inch footprint (1143 mm)

Target Mass: 24--25 kg (hybrid design with printed limbs and modules)

Primary Structure: 3030 aluminum extrusion backbone with 2020 cross braces

------------------------------------------------------------------------

# Chassis Geometry

Outer Diameter: ~700 mm

Coxa Mount Radius: ~350 mm from chassis center

Foot Radius (neutral stance): ~550 mm from chassis center

Leg Mount Positions: 8 equally spaced positions at 45° intervals:

Front Leg1 -- 0°  
Front‑Right Leg2 -- 45°  
Right Leg3 -- 90°  
Rear‑Right Leg4 -- 135°  
Rear Leg5 -- 180°  
Rear‑Left Leg6 -- 225°  
Left Leg7 -- 270°  
Front‑Left Leg8 -- 315°

Notes: 3D printed leg brackets attach to 3030 backbone at these positions.

------------------------------------------------------------------------

# Structural Frame

Primary Load Ring: 3030 aluminum extrusion backbone

Cross Bracing: 2020 aluminum extrusion

Top Plate: 3 mm aluminum sheet (mounts battery and compute modules)

Battery Tray: 3D printed or aluminum tray mounted centrally

Purpose: Maintain low CG and structural rigidity while keeping modularity

Notes: Printed gussets reinforce high-torque leg mounts

------------------------------------------------------------------------

# Servo Orientation

Each leg uses:

- **Coxa Servo:** Mounted horizontally in 3D printed coxa bracket  
- **Femur Servo:** Mounted vertically in 3D printed femur beam  
- **Tibia Servo:** Mounted inline with printed tibia segment  

Servo Access: Printed service openings allow horn access without full disassembly

------------------------------------------------------------------------

# Center of Gravity

Major mass components:

- Battery  
- Compute hardware  
- Power electronics  

Placement:

- Central along X and Y axes  
- Low as practical along Z axis (approx. 0.42 m from chassis base)  

Target CG position: Within 50 mm of chassis center

Low CG improves stability during walking and stair climbing

------------------------------------------------------------------------

# Battery Placement

Battery: 24V 30Ah LiFePO4  

Recommended Location: Directly under top chassis plate in central battery tray  

Mounting: Shock-isolated, removable tray

------------------------------------------------------------------------

# Head Mast Mount

Location: Center of robot body  

Height: 300–400 mm above chassis  

Mounting Method:

- 3D printed mast bracket or aluminum mast column  
- Bolted to central 3030 frame plate  

Vibration Isolation: Rubber bushings recommended

------------------------------------------------------------------------

# Electronics Bay

Location: Central interior chassis area

Components:

- Jetson Orin NX  
- Raspberry Pi 5  
- Teensy 4.1  
- Duet 3 6HC  
- DC‑DC converters  

Recommended Mounting:

- Stacked electronics plates (3D printed or aluminum)  
- Ensure airflow between layers

------------------------------------------------------------------------

# Cooling System

Active Cooling:

- 2 × 80 mm fans (e.g., Noctua)  

Airflow Path:

- Bottom intake → Top exhaust vents  

Purpose:

- Prevent heat buildup from servos, DC‑DC converters, and compute modules

------------------------------------------------------------------------

# Cable Routing

Main Power Harness:

- Battery → DC‑DC converters → servo rails  

Recommended cable gauges:

- 6 AWG main battery trunk  
- 8 AWG converter feeds  
- 10–12 AWG servo leads  

Leg Cable Routing:

- Wires routed through printed coxa housing  
- Strain relief at rotating joints  
- High-flex silicone robotics cable recommended

------------------------------------------------------------------------

# CAD Assembly Notes

Recommended model order:

1. 3030 chassis backbone ring  
2. 2020 cross braces  
3. 3D printed leg mount brackets  
4. Coxa assemblies  
5. Femur assemblies  
6. Tibia assemblies  
7. Battery tray (printed or aluminum)  
8. Electronics stack  
9. Head mast  

Notes: Following this order minimizes interference errors during assembly.  
Printed modules can be iterated or replaced without altering the main chassis.

------------------------------------------------------------------------

# Design Notes (V3.3)

- Hybrid frame reduces overall mass while maintaining stiffness  
- 3D printed modules modular and replaceable for rapid upgrades  
- All high-load points reinforced with gussets and brackets  
- Neutral stance and CG verified for tripod gait and stair climbing stability  
- Supports FMEA, CM, and simulation testing

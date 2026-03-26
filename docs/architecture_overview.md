# OBSIDIAN-8 Architecture Overview

OBSIDIAN-8 is a 45-inch autonomous octopod robotics platform designed to function as the command node for a distributed swarm of smaller robotic agents.

## Mechanical Platform

Reference:
01_Mechanical/OBSIDIAN8_MECHANICAL_LAYOUT.md  
03_Control_Architecture/LEG_KINEMATICS_SPEC.md

Key parameters:

- 8 legs
- 3 DOF per leg
- Coxa length: 70 mm
- Femur length: 210 mm
- Tibia length: 260 mm
- Foot radius: ~550 mm

Chassis structure:

- 3030 aluminum extrusion load ring
- 2020 aluminum cross bracing
- Central electronics bay
- Under‑mounted LiFePO4 battery

---

## Compute Stack

Primary AI Compute:
NVIDIA Jetson Orin NX 16GB

Mission Controller:
Raspberry Pi 5

Realtime Motion Controller:
Teensy 4.1

Safety / IO Supervisor:
Duet 3 6HC

Responsibilities:

Jetson → perception + SLAM  
Pi → mission control + swarm coordination  
Teensy → gait control  
Duet → safety monitoring

---

## Sensor Suite

Reference:
05_Perception/HEAD_MODULE_V1.md

Sensors:

- Intel RealSense D455 depth camera
- Luxonis OAK‑D Pro AI camera
- Slamtec RPLidar S2
- VectorNav VN‑100 IMU
- 6 × Sony IMX477 cameras

---

## Power System

Reference:
02_Electrical/POWER_DISTRIBUTION_DIAGRAM.md  
02_Electrical/Power_Budget_Analysis.txt

Battery:
24V 30Ah LiFePO4

Power rails:

- 8V servo rail
- 12V sensor rail
- 5V logic rail

DC‑DC Converters:

2 × MeanWell RSD‑500

---

## Swarm Network

Reference:
04_Autonomy/SWARM_CONTROL_ARCHITECTURE.md

Communication:

- WiFi 6 Mesh
- Ubiquiti UniFi U6 Mesh hardware
- ROS2 DDS messaging
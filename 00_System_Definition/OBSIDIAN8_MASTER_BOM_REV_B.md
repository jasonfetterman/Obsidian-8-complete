# OBSIDIAN-8 MASTER BOM --- REV B (UPDATED)

45" AUTONOMOUS OCTOPOD SWARM COMMAND PLATFORM

## TARGET SPECIFICATIONS

Footprint: 45 inches (1143 mm) Target Mass: \~27--30 kg Actuation Class:
400 kg·cm brushless HV servos Battery: 24V 30Ah LiFePO4 Primary Compute:
NVIDIA Jetson Orin NX 16GB Mission Computer: Raspberry Pi 5 Realtime
Motion: Teensy 4.1 Safety & IO Supervisor: Duet 3 6HC

------------------------------------------------------------------------

# 1. ACTUATION SYSTEM

24 × AGFRC A86BHMW 400 kg·cm Brushless HV Servo\
2 × Spare Units

Specs: - 400 kg·cm @ 8.4V - CNC aluminum case - Steel gears - Dual ball
bearings - 25T spline

Estimated Cost: \~\$6,240

------------------------------------------------------------------------

# 2. FRAME SYSTEM

Extrusion: - 4m 3030 Aluminum Extrusion (Primary Load Ring) - 4m 2020
Aluminum Extrusion (Bracing)

Structural Hardware: - M6 Grade 10.9 bolts - Steel corner brackets -
Sliding T-nuts

Reinforcement Plates: - 3mm Aluminum (Top plate, battery tray, servo
backing plates)

Estimated Cost: \~\$920

------------------------------------------------------------------------

# 3. JOINT & SHAFT SYSTEM

Bearings: 56 × 6001-2RS Bearings

Shafting: 12 mm Hardened Steel Precision Rod

Retention: 12 mm Shaft Collars

Estimated Cost: \~\$404

------------------------------------------------------------------------

# 4. PRINTED STRUCTURE

Material: PA6-CF or PA12-CF Carbon Fiber Nylon

Components: - 8 Coxa housings - 8 Femur box beams - 8 Tibia box beams -
Reinforced servo mounts - TPU replaceable foot pads

Estimated Cost: \~\$320

------------------------------------------------------------------------

# 5. BATTERY SYSTEM

Battery: LiTime 24V 30Ah LiFePO4

Charger: 24V 15A LiFePO4 Charger

Estimated Cost: \~\$680

------------------------------------------------------------------------

# 6. SERVO POWER SYSTEM

DC-DC Regulation: 2 × MeanWell RSD-500 (24V → 8V)

Protection: - 150A ANL Fuse - 2 × 80A MIDI Fuses - 2 × 150A DC
Contactors

Distribution: Copper bus bars 6 AWG main trunk 10--12 AWG servo
distribution

Estimated Cost: \~\$1,040

------------------------------------------------------------------------

# 7. CONTROL SYSTEM

High-Level Compute: Raspberry Pi 5

AI Compute: NVIDIA Jetson Orin NX 16GB Carrier: Seeed Studio J4012

Motion Controller: Teensy 4.1

Safety Controller: Duet 3 6HC

Logic Power: Isolated 5V DC-DC

Estimated Cost: \~\$1,200

------------------------------------------------------------------------

# 8. PERCEPTION & NAVIGATION SYSTEM

Depth Camera: Intel RealSense D455

AI Vision Camera: Luxonis OAK-D Pro

Lidar: Slamtec RPLidar S2

IMU: VectorNav VN-100 (or BNO085 as budget option)

Swarm Cameras: 6 × Arducam IMX477 USB Cameras

Estimated Cost: \~\$1,400

------------------------------------------------------------------------

# 9. NETWORKING SYSTEM

Swarm Communications: Ubiquiti UniFi U6 Mesh

Estimated Cost: \~\$180

------------------------------------------------------------------------

# 10. MONITORING & SAFETY

Current Sensors: 2 × ACS758-100B

Thermal Sensors: 100k NTC Thermistors

Emergency Controls: Industrial E-stop Marine battery disconnect

Estimated Cost: \~\$220

------------------------------------------------------------------------

# 11. AUTONOMOUS DOCK SYSTEM

Connector: Anderson SB120

Dock Structure: Steel base UHMW alignment rails

Estimated Cost: \~\$400

------------------------------------------------------------------------

# PROJECT COST SUMMARY

Actuation: \~\$6,240\
Frame: \~\$920\
Joint Hardware: \~\$404\
Printed Structure: \~\$320\
Battery: \~\$680\
Power System: \~\$1,040\
Compute System: \~\$1,200\
Perception System: \~\$1,400\
Networking: \~\$180\
Safety: \~\$220\
Dock: \~\$400

Estimated Total: \~\$13,000

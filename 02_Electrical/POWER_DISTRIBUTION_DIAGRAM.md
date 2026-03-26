# OBSIDIAN-8 POWER DISTRIBUTION DIAGRAM

## System Overview

The OBSIDIAN-8 power system is built around a 24V LiFePO4 battery pack
with multiple regulated rails for servos, compute systems, and sensors.

Primary Battery: 24V 30Ah LiFePO4

Maximum Continuous Current: 100A

Main Fuse: 150A ANL

Emergency Disconnect: Marine 150A Battery Switch

------------------------------------------------------------------------

## Power Architecture

24V Battery Bus \| \|---- DC-DC Converter Bank A → Servo Rail A (8V) \|
\|---- DC-DC Converter Bank B → Servo Rail B (8V) \| \|---- 24V → 12V
Converter → Sensors & Head Module \| \|---- 24V → 5V Converter → Logic
Electronics

------------------------------------------------------------------------

## Servo Power System

DC-DC Units: 2 × MeanWell RSD-500

Input: 24V

Output: 8V adjustable

Distribution: Copper bus bars

Wiring: 6 AWG main trunk 8 AWG DC-DC feed 10--12 AWG servo lines

Total Servos: 24 × HV brushless servos

Peak Current Consideration: \~120A burst possible during gait
transitions.

------------------------------------------------------------------------

## Logic Power Rail

5V Rail supplies:

-   Raspberry Pi 5
-   Jetson carrier logic
-   IMU
-   cameras
-   network hardware

Converter: Isolated 24V → 5V DC-DC converter

------------------------------------------------------------------------

## Sensor Power Rail

12V rail supplies:

-   RealSense depth camera
-   OAK-D camera
-   Lidar
-   cooling fans

Converter: 24V → 12V DC-DC converter

------------------------------------------------------------------------

## Safety Monitoring

Current Sensors: 2 × ACS758-100B Hall sensors

Thermal Monitoring: 100k NTC thermistors

Emergency Stop: Industrial E-stop cuts servo rail contactors while
keeping logic power active.

------------------------------------------------------------------------

## Dock Charging

Dock Connector: Anderson SB120

Charger: 24V 15A LiFePO4 CC/CV charger

Charging occurs through docking station while robot remains powered
down.

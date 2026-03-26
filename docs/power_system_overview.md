# OBSIDIAN-8 Power System Overview

Reference:

02_Electrical/POWER_DISTRIBUTION_DIAGRAM.md  
02_Electrical/Power_Budget_Analysis.txt

---

## Battery

Primary power source:

LiTime 24V 30Ah LiFePO4 battery.

Energy capacity:

~720 Wh.

---

## Power Conversion

Two MeanWell RSD‑500 converters generate the servo rail.

Input:
24V

Output:
8V

---

## Power Rails

Servo Rail:
8V for 24 brushless servos.

Sensor Rail:
12V for cameras, lidar, and cooling.

Logic Rail:
5V for compute hardware.

---

## Protection Systems

Electrical protection:

- 150A ANL fuse
- DC contactors
- emergency stop

Monitoring:

- current sensors
- thermal sensors
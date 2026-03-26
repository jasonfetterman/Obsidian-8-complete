# OBSIDIAN-8 SWARM CONTROL ARCHITECTURE

## Overview

OBSIDIAN-8 functions as the command platform for a swarm of smaller
half-scale robots. The command robot maintains the master map, assigns
tasks, and coordinates swarm activity.

## System Roles

### Command Unit

Robot: OBSIDIAN-8 (45" platform)

Responsibilities: - Global SLAM mapping - Task assignment - Navigation
planning - Communication relay - Docking management - System health
monitoring

Primary compute: - NVIDIA Jetson Orin NX (perception & mapping) -
Raspberry Pi 5 (mission logic) - Teensy 4.1 (gait control)

------------------------------------------------------------------------

## Worker Robots

Recommended Worker Size: \~22 inch footprint

Worker Robot Hardware: - Raspberry Pi 4 or Pi 5 - Forward depth camera
(Intel RealSense D435 or D455) - IMU (BNO085) - WiFi 6 communication
module

Worker tasks: - Area scanning - Environmental sampling - Relay
communications - Local obstacle avoidance

Workers report telemetry to the command robot.

------------------------------------------------------------------------

## Network Topology

Communication Model:

Workers → Command → Workers

All swarm units communicate with the OBSIDIAN‑8 command node. The
command node distributes navigation instructions and task assignments.

Primary Network: WiFi 6 Mesh

Recommended Hardware: Ubiquiti UniFi U6 Mesh

------------------------------------------------------------------------

## Software Stack

Middleware: ROS2 (DDS communication)

Major subsystems:

Perception Layer: Runs on Jetson (vision, SLAM, object detection)

Mission Layer: Runs on Raspberry Pi (task assignment, swarm
coordination)

Control Layer: Runs on Teensy (gait & stabilization)

------------------------------------------------------------------------

## Task Allocation Model

The command robot dynamically assigns tasks to swarm units.

Example tasks:

-   Explore Sector A
-   Map Corridor B
-   Inspect Object
-   Return to Dock
-   Assist Unit

Command robot maintains task queue and assigns based on:

-   robot battery level
-   robot position
-   mission priority

------------------------------------------------------------------------

## Docking & Charging

The OBSIDIAN‑8 base station manages recharge cycles.

Dock System: Anderson SB120 connector

Command robot monitors battery levels and schedules dock returns.

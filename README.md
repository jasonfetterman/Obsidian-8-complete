# OBSIDIAN-8

<div align="center">

# 🌐 OBSIDIAN-8 Autonomous Search & Rescue Ecosystem

**Multi-domain autonomous response platform integrating aerial systems, ground assets, infrastructure nodes, and swarm command architecture**

![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-air%20%7C%20ground%20%7C%20infrastructure-blue)
![Architecture](https://img.shields.io/badge/architecture-swarm-black)
![License](https://img.shields.io/badge/license-TBD-lightgrey)

---

**One network. Many platforms. Coordinated response.**

</div>

---

# Overview

OBSIDIAN-8 is a modular autonomous search-and-rescue ecosystem designed around coordinated multi-domain operations.

The project combines:

- Autonomous aerial platforms
- Ground rescue systems
- Infrastructure assets
- Mesh communications
- Command & control nodes
- Distributed swarm behavior
- Manufacturing data
- CAD / printable components
- Field deployment systems

The architecture allows independent assets to function as a coordinated response network under a unified command layer.

---

# System Architecture

```text
OBSIDIAN-8 QUEEN
│
├── AIR DOMAIN
│   ├── OBS-AIR-SAR-01
│   ├── OBS-AIR-RECON-01
│   ├── OBS-AIR-RELAY-01
│   └── OBS-AIR-LIGHTDEL-01
│
├── GROUND DOMAIN
│   ├── OBS-GROUND-SAR-01
│   ├── OBS-GROUND-CARGO-01
│   ├── OBS-GROUND-SCAN-01
│   └── OBS-GROUND-EOD-01
│
├── INFRASTRUCTURE DOMAIN
│   ├── OBS-INFRA-DOCK-001
│   ├── OBS-INFRA-FAB-001
│   ├── OBS-INFRA-SOLAR-001
│   └── OBS-INFRA-HANGAR-001
│
└── NETWORK LAYER
    ├── Mesh
    ├── LTE
    ├── Telemetry
    └── SATCOM
```

---

# Fleet Components

## AIR SYSTEMS

### OBS-AIR-SAR-01
Search & Rescue aerial platform

Capabilities:

- Thermal search
- Victim detection
- Emergency supply delivery
- Forward scouting
- Mesh relay support

---

### OBS-AIR-RECON-01

Long-range mapping and reconnaissance platform

Capabilities:

- Area mapping
- Terrain analysis
- Mission planning support
- RTK navigation

---

### OBS-AIR-RELAY-01

Network extension platform

Capabilities:

- Mesh extension
- Signal backbone
- Emergency communications
- Telemetry relay

---

### OBS-AIR-LIGHTDEL-01

Logistics support drone

Capabilities:

- Payload transport
- Medical delivery
- Supply drops

---

## GROUND SYSTEMS

### OBS-GROUND-SAR-01

Tracked casualty extraction platform

Capabilities:

- Patient transport
- Rescue support
- Medical telemetry
- Swarm extraction operations

---

### OBS-GROUND-CARGO-01

Logistics rover

Capabilities:

- Equipment movement
- Supply transport
- Payload delivery

---

### OBS-GROUND-SCAN-01

Ground mapping unit

Capabilities:

- LiDAR mapping
- Terrain analysis
- Sensor fusion

---

### OBS-GROUND-EOD-01

Hazard inspection platform

Capabilities:

- Remote inspection
- Dangerous area assessment
- Sensor deployment

---

## INFRASTRUCTURE

### OBS-INFRA-DOCK-001

Autonomous support station

Functions:

- Charging
- Docking
- Maintenance
- Fleet servicing

---

### OBS-INFRA-FAB-001

Field fabrication unit

Functions:

- Component production
- Spare parts
- Repair support

---

### OBS-INFRA-SOLAR-001

Energy support node

Functions:

- Solar charging
- Battery buffering
- Auxiliary power

---

### OBS-INFRA-HANGAR-001

Deployable shelter

Functions:

- Staging
- Protection
- Launch operations

---

# Repository Structure

```text
OBSIDIAN-8/
│
├── docs/
├── fleet/
│   ├── AIR/
│   ├── GROUND/
│   └── INFRA/
│
├── command/
├── swarm/
├── electronics/
├── infrastructure/
├── tests/
└── assets/
```

---

# Technology Stack

## Flight Systems

- PX4
- ArduPilot
- ROS2
- MAVLink

---

## Compute

- NVIDIA Jetson Orin
- Cube Orange+
- STM32 controllers

---

## Navigation

- RTK GPS
- Optical flow
- IMU fusion
- Terrain sensing

---

## Communications

- RFD900 telemetry
- Mesh networking
- LTE fallback
- SATCOM integration

---

# Current Platforms

| Platform | Status |
|----------|--------|
| OBS-AIR-SAR-01 | Development |
| OBS-GROUND-SAR-01 | Development |
| QUEEN Node | Architecture |
| Dock Infrastructure | Planning |

---

# Objectives

- Autonomous SAR operations
- Distributed fleet coordination
- Modular manufacturing
- Open architecture
- Deployable infrastructure
- Multi-domain interoperability

---

# Development Roadmap

## Phase 1

Core systems

- Air SAR platform
- Ground SAR platform
- Initial mesh networking

---

## Phase 2

Command systems

- QUEEN integration
- Mission allocation
- Fleet coordination

---

## Phase 3

Infrastructure

- Dock
- Hangar
- Fabrication
- Energy nodes

---

## Phase 4

Swarm deployment

- Coordinated missions
- Distributed autonomy
- Multi-unit operations

---

# Documentation

Primary documents:

- System Architecture
- Fleet Tree
- Specifications
- Procurement
- Build Manuals
- CAD
- Electronics
- Firmware

---

# Contribution

Project structure is organized by platform.

Each asset contains:

```text
SPECIFICATION
PROCUREMENT
BUILD
CAD
STL
FIRMWARE
OPERATIONS
```

Contributors should maintain platform isolation and documentation completeness.

---

# Disclaimer

OBSIDIAN-8 is an engineering and research project focused on autonomous systems, disaster response concepts, robotics integration, and multi-domain coordination architecture.

Deployment, testing, and operation should comply with all applicable laws, aviation regulations, safety requirements, and local operating rules.

---

<div align="center">

**OBSIDIAN-8**

Autonomous Systems • Search & Rescue • Swarm Coordination

</div>

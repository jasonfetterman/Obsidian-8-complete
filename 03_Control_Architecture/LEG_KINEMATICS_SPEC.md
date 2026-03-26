# OBSIDIAN-8 LEG KINEMATICS SPEC

## Overview

This document defines the geometric layout, joint limits, and motion
assumptions for the OBSIDIAN-8 octopod leg system. The robot uses 8 legs
with 3 degrees of freedom per leg (24 actuators total).

## Joint Structure

Each leg contains three joints:

1.  Coxa (Yaw) -- rotates the leg horizontally from the body
2.  Femur (Pitch) -- raises and lowers the upper leg
3.  Tibia (Pitch) -- extends the lower leg to control reach and ground
    contact

Actuator Type: AGFRC A86BHMW 400 kg·cm Brushless HV Servo

Total Actuators: 24

## Geometric Dimensions

Recommended nominal geometry for stability and stride efficiency:

Coxa Length: 70 mm

Femur Length: 210 mm

Tibia Length: 260 mm

Body Radius (center → coxa axis): \~350 mm

Foot Radius (center → neutral foot position): \~550 mm

These values produce a stable support polygon and allow sufficient
stride.

## Joint Motion Limits

Coxa (Yaw): -60° to +60°

Femur (Pitch): -30° to +75°

Tibia (Pitch): -100° to +20°

Limits should be enforced in firmware to prevent mechanical damage.

## Neutral Standing Pose

Recommended neutral pose:

Coxa: 0°

Femur: 45°

Tibia: -60°

This pose keeps the robot center of gravity inside the support polygon
while maintaining actuator efficiency.

## Gait Models

Primary Gait: Tripod gait (fast locomotion)

Secondary Gait: Wave gait (maximum stability for rough terrain)

Tripod Gait Pattern Example:

Group A: Legs 1, 3, 5, 7

Group B: Legs 2, 4, 6, 8

One group lifts while the other provides support.

## Stability Model

The robot must maintain its center of gravity within the support polygon
formed by the legs in ground contact.

Minimum recommended ground contact: 4 legs at all times during slow
movement.

## Foot Design

Material: TPU 95A

Diameter: 55--70 mm

Recommended Features: Replaceable traction pads Slight concave bottom
for grip

## CAD Modeling Notes

Key design constraints for modeling:

-   Maintain consistent joint axis alignment
-   Ensure servo horns remain accessible for maintenance
-   Provide clearance for wiring through coxa joint
-   Include strain relief for servo wiring

# OBSIDIAN-8 PERCEPTION & SENSOR ARCHITECTURE

## HEAD MODULE (6-CAMERA SYSTEM)

Layout:

Front Stereo Pair: 2 × Arducam IMX477

Side Cameras: 2 × Arducam IMX477

Rear Cameras: 2 × Arducam IMX477

Purpose: 360° environmental awareness and swarm monitoring.

------------------------------------------------------------------------

## PRIMARY NAVIGATION SENSORS

Depth Camera: Intel RealSense D455

Used for: - Terrain mapping - Obstacle detection - SLAM support

------------------------------------------------------------------------

## AI VISION

Camera: Luxonis OAK-D Pro

Capabilities: - Neural inference - Object detection - Person
recognition - Swarm robot tracking

------------------------------------------------------------------------

## LIDAR SYSTEM

Model: RPLidar S2

Specifications: - 360° scan - 30m range - SLAM support

------------------------------------------------------------------------

## IMU SYSTEM

Preferred: VectorNav VN-100

Alternative: BNO085

Purpose: - Orientation - Balance control - Motion stabilization

------------------------------------------------------------------------

## SENSOR PROCESSING PIPELINE

Jetson Orin NX: AI inference sensor fusion SLAM

Raspberry Pi 5: Mission logic swarm coordination

Teensy 4.1: Realtime gait stabilization

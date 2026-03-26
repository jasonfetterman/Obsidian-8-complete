# OBSIDIAN-8 HEAD MODULE V1

## Purpose

Central sensor mast providing 360° perception, AI vision processing, and
swarm monitoring.

## Sensor Layout

Front Stereo Pair: - 2 × Arducam IMX477 USB Cameras

Side Vision: - 2 × Arducam IMX477 USB Cameras

Rear Vision: - 2 × Arducam IMX477 USB Cameras

Depth Camera: - Intel RealSense D455

AI Vision Camera: - Luxonis OAK-D Pro

Lidar: - Slamtec RPLidar S2

IMU: - VectorNav VN-100 (BNO085 acceptable alternative)

## Compute

Primary AI Compute: - NVIDIA Jetson Orin NX 16GB

Carrier Board: - Seeed Studio J4012

Responsibilities: - SLAM - Terrain mapping - Object detection - Swarm
tracking - Sensor fusion

## Mechanical Design

Recommended Mast Height: 300--400 mm above chassis

Mounting Method: - Aluminum mast structure - Rubber vibration isolation
bushings

Protection: - Polycarbonate dome - Aluminum sensor frame

Cooling: - 2 × Noctua NF‑A8 80mm PWM fans

## Estimated Power Budget

Jetson Orin NX: \~25W Camera array: \~10W Lidar: \~8W Cooling + sensors:
\~5W

Total Head Unit Budget: \~45--50W

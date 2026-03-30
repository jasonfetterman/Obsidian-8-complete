//
// servo_driver.cpp
// OBSIDIAN-8 V3 — REV D
// Converts leg target positions into servo angles and drives servos
//

#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include <chrono>

// Include your hardware interface here, e.g., serial or PWM lib
#include "servo_interface.h"

struct LegCommand {
    double x;     // meters
    double y;     // meters
    double z;     // meters
    std::string phase;  // "swing" or "stance"
};

// Kinematic constants (example lengths in meters)
const double COXA = 0.05;
const double FEMUR = 0.15;
const double TIBIA = 0.15;

// Forward declaration
std::vector<double> inverse_kinematics(double x, double y, double z);

// Send servo angles to hardware
void send_servo_angles(const std::vector<double>& angles) {
    // Replace with actual servo interface code
    for (size_t i = 0; i < angles.size(); i++) {
        ServoInterface::setAngle(i, angles[i]);
    }
}

void drive_legs(const std::vector<LegCommand>& leg_commands) {
    for (size_t i = 0; i < leg_commands.size(); i++) {
        LegCommand cmd = leg_commands[i];
        std::vector<double> angles = inverse_kinematics(cmd.x, cmd.y, cmd.z);
        send_servo_angles(angles);
    }
}

// Simple inverse kinematics for 3-DOF leg (Coxa, Femur, Tibia)
std::vector<double> inverse_kinematics(double x, double y, double z) {
    std::vector<double> angles(3, 0.0);

    // Coxa rotation (horizontal)
    angles[0] = atan2(y, x);

    // Distance in horizontal plane minus coxa
    double r = sqrt(x*x + y*y) - COXA;
    double s = z;

    double D = (r*r + s*s - FEMUR*FEMUR - TIBIA*TIBIA) / (2 * FEMUR * TIBIA);
    if (D > 1.0) D = 1.0;      // clamp
    if (D < -1.0) D = -1.0;

    // Knee angle (Tibia)
    angles[2] = acos(D);

    // Hip angle (Femur)
    angles[1] = atan2(s, r) - atan2(TIBIA*sin(angles[2]), FEMUR + TIBIA*cos(angles[2]));

    return angles;  // radians
}

// -------------------- TEST LOOP --------------------
int main() {
    // Initialize servo interface
    ServoInterface::init();

    // Example: 8 legs
    std::vector<LegCommand> test_legs(8);
    for (int i = 0; i < 8; i++) {
        test_legs[i] = {0.2, (i%2==0?0.15:-0.15), -0.2, "stance"};
    }

    while (true) {
        drive_legs(test_legs);
        std::this_thread::sleep_for(std::chrono::milliseconds(20));  // 50 Hz
    }

    return 0;
}

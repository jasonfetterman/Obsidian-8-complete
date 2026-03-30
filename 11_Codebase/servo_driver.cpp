// servo_driver.cpp
// OBSIDIAN-8 V3 — REV D
// Low-level driver for AGFRC 400 kg·cm HV servos
// Sends joint commands via PWM / CAN / serial depending on servo configuration

#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include <chrono>
#include "pid_controller.h"

#define NUM_LEGS 8
#define JOINTS_PER_LEG 3

// Simulated servo interface (replace with actual hardware API)
class ServoInterface {
public:
    void send_angle(int servo_id, double angle_deg) {
        // Hardware-specific command to set servo angle
        std::cout << "[ServoInterface] Servo " << servo_id
                  << " -> " << angle_deg << " deg" << std::endl;
    }
};

// -------------------- GLOBALS --------------------
ServoInterface servo_bus;
PIDController pid_controllers[NUM_LEGS][JOINTS_PER_LEG]; // PID per joint
double current_joint_angles[NUM_LEGS][JOINTS_PER_LEG] = {0};

// -------------------- FUNCTIONS --------------------
double apply_limits(double angle, double min_deg, double max_deg) {
    if (angle < min_deg) return min_deg;
    if (angle > max_deg) return max_deg;
    return angle;
}

// -------------------- CLASS --------------------
class ServoDriver {
public:
    ServoDriver() {
        // Initialize PID controllers for each joint
        for(int leg=0; leg<NUM_LEGS; leg++) {
            for(int joint=0; joint<JOINTS_PER_LEG; joint++) {
                pid_controllers[leg][joint] = PIDController(1.0, 0.01, 0.05);
            }
        }
    }

    void send_joint_targets(std::vector<std::vector<double>> joint_targets) {
        for(int leg=0; leg<NUM_LEGS; leg++) {
            for(int joint=0; joint<JOINTS_PER_LEG; joint++) {
                double target = joint_targets[leg][joint];
                // Apply joint limits (example values, replace as needed)
                double limited = apply_limits(target, -90.0, 90.0);
                // PID computation
                double pid_out = pid_controllers[leg][joint].compute(limited, current_joint_angles[leg][joint]);
                current_joint_angles[leg][joint] = pid_out;
                // Send to hardware
                int servo_id = leg * JOINTS_PER_LEG + joint;
                servo_bus.send_angle(servo_id, pid_out);
            }
        }
    }

    void halt_motion() {
        std::cout << "[ServoDriver] Halting all servos." << std::endl;
        for(int leg=0; leg<NUM_LEGS; leg++) {
            for(int joint=0; joint<JOINTS_PER_LEG; joint++) {
                int servo_id = leg * JOINTS_PER_LEG + joint;
                servo_bus.send_angle(servo_id, current_joint_angles[leg][joint]);
            }
        }
    }
};

// -------------------- TEST LOOP --------------------
#ifdef TEST_SERVO_DRIVER
int main() {
    ServoDriver driver;
    std::vector<std::vector<double>> test_targets(NUM_LEGS, std::vector<double>(JOINTS_PER_LEG, 30.0));
    driver.send_joint_targets(test_targets);
    std::this_thread::sleep_for(std::chrono::seconds(1));
    driver.halt_motion();
    return 0;
}
#endif

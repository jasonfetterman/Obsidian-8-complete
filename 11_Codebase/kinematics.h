#pragma once
// kinematics.h
// OBSIDIAN-8 V3 — REV D
// Forward and inverse kinematics for 3-DOF leg (coxa, femur, tibia)

#include <cmath>
#include <array>
#include <stdexcept>

struct JointAngles {
    double coxa;  // degrees
    double femur; // degrees
    double tibia; // degrees
};

struct FootPosition {
    double x;  // meters
    double y;  // meters
    double z;  // meters
};

class Kinematics {
private:
    double l_coxa;  // length from hip to femur pivot
    double l_femur; // femur length
    double l_tibia; // tibia length

public:
    Kinematics(double coxa_len, double femur_len, double tibia_len)
        : l_coxa(coxa_len), l_femur(femur_len), l_tibia(tibia_len) {}

    JointAngles inverse(const FootPosition& foot) {
        JointAngles angles;

        // Coxa rotation in XY plane
        angles.coxa = atan2(foot.y, foot.x) * 180.0 / M_PI;

        // Distance from coxa joint to foot in horizontal plane
        double horizontal_dist = sqrt(foot.x*foot.x + foot.y*foot.y) - l_coxa;
        double z = -foot.z; // convention: downward positive

        double L = sqrt(horizontal_dist*horizontal_dist + z*z);

        // Law of cosines for femur and tibia
        double cos_theta2 = (l_femur*l_femur + L*L - l_tibia*l_tibia) / (2 * l_femur * L);
        if(cos_theta2 < -1.0 || cos_theta2 > 1.0) throw std::domain_error("Inverse kinematics unreachable");
        double theta2 = acos(cos_theta2);

        double cos_theta3 = (l_femur*l_femur + l_tibia*l_tibia - L*L) / (2 * l_femur * l_tibia);
        if(cos_theta3 < -1.0 || cos_theta3 > 1.0) throw std::domain_error("Inverse kinematics unreachable");
        double theta3 = acos(cos_theta3);

        double alpha = atan2(z, horizontal_dist);

        angles.femur = (theta2 + alpha) * 180.0 / M_PI;   // degrees
        angles.tibia = (theta3 - M_PI) * 180.0 / M_PI;    // degrees, downward bend

        return angles;
    }

    FootPosition forward(const JointAngles& angles) {
        FootPosition foot;

        double coxa_rad = angles.coxa * M_PI / 180.0;
        double femur_rad = angles.femur * M_PI / 180.0;
        double tibia_rad = angles.tibia * M_PI / 180.0;

        double L = l_femur * cos(femur_rad) + l_tibia * cos(femur_rad + tibia_rad);
        foot.z = -(l_femur * sin(femur_rad) + l_tibia * sin(femur_rad + tibia_rad));

        foot.x = (l_coxa + L) * cos(coxa_rad);
        foot.y = (l_coxa + L) * sin(coxa_rad);

        return foot;
    }
};

// imu_reader.cpp
// OBSIDIAN-8 V3 — REV D
// Reads BNO085 IMU data and provides orientation & angular velocity

#include <iostream>
#include <cmath>
#include <thread>
#include <chrono>
#include "bno085_driver.h" // Assume low-level I2C/SPI interface library

struct IMUData {
    double roll;   // degrees
    double pitch;  // degrees
    double yaw;    // degrees
    double gx;     // deg/s
    double gy;     // deg/s
    double gz;     // deg/s
};

// -------------------- CLASS --------------------
class IMUReader {
private:
    BNO085Driver imu;
    IMUData last_data;

public:
    IMUReader() {
        if(!imu.begin()) {
            std::cerr << "[IMUReader] Failed to initialize BNO085" << std::endl;
            throw std::runtime_error("IMU initialization failed");
        }
        last_data = {0,0,0,0,0,0};
    }

    IMUData read() {
        double quat[4];
        if(imu.getQuaternion(quat)) {
            // Convert quaternion to Euler angles (roll, pitch, yaw)
            double w = quat[0], x = quat[1], y = quat[2], z = quat[3];

            last_data.roll  = atan2(2*(w*x + y*z), 1 - 2*(x*x + y*y)) * 180.0/M_PI;
            last_data.pitch = asin(2*(w*y - z*x)) * 180.0/M_PI;
            last_data.yaw   = atan2(2*(w*z + x*y), 1 - 2*(y*y + z*z)) * 180.0/M_PI;
        }

        double gyro[3];
        if(imu.getGyro(gyro)) {
            last_data.gx = gyro[0];
            last_data.gy = gyro[1];
            last_data.gz = gyro[2];
        }

        return last_data;
    }
};

// -------------------- TEST LOOP --------------------
#ifdef TEST_IMU
int main() {
    IMUReader imu;
    while(true) {
        IMUData data = imu.read();
        std::cout << "Roll: " << data.roll << " Pitch: " << data.pitch
                  << " Yaw: " << data.yaw
                  << " GX: " << data.gx << " GY: " << data.gy << " GZ: " << data.gz
                  << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    return 0;
}
#endif

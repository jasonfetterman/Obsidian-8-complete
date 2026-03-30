//
// imu_reader.cpp
// OBSIDIAN-8 V3 — REV D
// Reads BNO085 IMU for orientation and motion sensing
//

#include <iostream>
#include <thread>
#include <chrono>
#include "bno085.h"  // Include your IMU library / driver header

class IMUReader {
public:
    IMUReader(int i2c_bus = 1, int address = 0x4A) {
        imu = new BNO085(i2c_bus, address);
        if (!imu->begin()) {
            std::cerr << "[IMUReader] Failed to initialize BNO085" << std::endl;
        }
        else {
            std::cout << "[IMUReader] BNO085 initialized" << std::endl;
        }
    }

    ~IMUReader() {
        delete imu;
    }

    void update() {
        if (imu->dataAvailable()) {
            imu->readSensor();  // reads accel, gyro, mag, quaternions

            quaternion[0] = imu->getQuaternionW();
            quaternion[1] = imu->getQuaternionX();
            quaternion[2] = imu->getQuaternionY();
            quaternion[3] = imu->getQuaternionZ();

            accel[0] = imu->getAccelX();
            accel[1] = imu->getAccelY();
            accel[2] = imu->getAccelZ();

            gyro[0] = imu->getGyroX();
            gyro[1] = imu->getGyroY();
            gyro[2] = imu->getGyroZ();
        }
    }

    std::vector<double> getQuaternion() { return quaternion; }
    std::vector<double> getAccel() { return accel; }
    std::vector<double> getGyro() { return gyro; }

private:
    BNO085* imu;
    std::vector<double> quaternion{0, 0, 0, 0};
    std::vector<double> accel{0, 0, 0};
    std::vector<double> gyro{0, 0, 0};
};

// -------------------- TEST LOOP --------------------
int main() {
    IMUReader imu;
    while (true) {
        imu.update();
        auto q = imu.getQuaternion();
        auto a = imu.getAccel();
        auto g = imu.getGyro();

        std::cout << "[IMU] Quaternion: "
                  << q[0] << ", " << q[1] << ", " << q[2] << ", " << q[3]
                  << " | Accel: " << a[0] << ", " << a[1] << ", " << a[2]
                  << " | Gyro: " << g[0] << ", " << g[1] << ", " << g[2]
                  << std::endl;

        std::this_thread::sleep_for(std::chrono::milliseconds(50));  // 20 Hz
    }
    return 0;
}

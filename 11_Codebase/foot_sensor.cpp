//
// foot_sensor.cpp
// OBSIDIAN-8 V3 — REV D
// Reads 8 foot contact switches for gait and balance
//

#include <iostream>
#include <array>
#include <thread>
#include <chrono>
#include <mutex>
#include "gpio_interface.h"  // Replace with your GPIO library

class FootSensor {
public:
    FootSensor() {
        // Initialize GPIO pins for 8 foot sensors
        // Example GPIO pins: 2-9
        sensor_pins = {2, 3, 4, 5, 6, 7, 8, 9};
        for (auto pin : sensor_pins) {
            GPIO::setup(pin, GPIO::IN);
        }
    }

    // Reads all 8 sensors and returns array of bools
    std::array<bool,8> read() {
        std::lock_guard<std::mutex> lock(mtx);
        for (size_t i = 0; i < 8; i++) {
            sensor_state[i] = GPIO::read(sensor_pins[i]);
        }
        return sensor_state;
    }

    void update_loop() {
        while (running) {
            read();
            std::this_thread::sleep_for(std::chrono::milliseconds(20));  // 50 Hz
        }
    }

    void start() {
        running = true;
        sensor_thread = std::thread(&FootSensor::update_loop, this);
    }

    void stop() {
        running = false;
        if (sensor_thread.joinable())
            sensor_thread.join();
    }

private:
    std::array<int,8> sensor_pins;
    std::array<bool,8> sensor_state{false};
    std::thread sensor_thread;
    bool running = false;
    std::mutex mtx;
};

// -------------------- TEST LOOP --------------------
int main() {
    FootSensor foot;
    foot.start();

    while (true) {
        auto state = foot.read();
        std::cout << "[FootSensor] ";
        for (bool s : state) {
            std::cout << s << " ";
        }
        std::cout << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    foot.stop();
    return 0;
}

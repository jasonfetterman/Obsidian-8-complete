// foot_sensor.cpp
// OBSIDIAN-8 V3 — REV D
// Reads foot contact sensors and provides debounced contact states

#include <iostream>
#include <array>
#include <chrono>
#include <thread>

#define NUM_FEET 8
#define DEBOUNCE_MS 20  // debounce time in milliseconds

class FootSensor {
private:
    std::array<bool, NUM_FEET> last_state;
    std::array<std::chrono::steady_clock::time_point, NUM_FEET> last_change;

public:
    FootSensor() {
        last_state.fill(false);
        auto now = std::chrono::steady_clock::now();
        last_change.fill(now);
    }

    /**
     * Read raw digital input from sensors
     * Replace this function with actual GPIO/I2C reads
     */
    std::array<bool, NUM_FEET> read_raw() {
        std::array<bool, NUM_FEET> raw;
        for(int i=0; i<NUM_FEET; i++) {
            // Simulate sensor (replace with GPIO read)
            raw[i] = false;
        }
        return raw;
    }

    /**
     * Return debounced foot contact states
     */
    std::array<bool, NUM_FEET> read() {
        auto raw = read_raw();
        auto now = std::chrono::steady_clock::now();

        for(int i=0; i<NUM_FEET; i++) {
            if(raw[i] != last_state[i]) {
                auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(now - last_change[i]).count();
                if(duration >= DEBOUNCE_MS) {
                    last_state[i] = raw[i];
                    last_change[i] = now;
                }
            }
        }
        return last_state;
    }
};

// -------------------- TEST LOOP --------------------
#ifdef TEST_FOOT_SENSOR
int main() {
    FootSensor fs;
    while(true) {
        auto states = fs.read();
        std::cout << "Foot contacts: ";
        for(auto s : states) std::cout << s << " ";
        std::cout << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    return 0;
}
#endif

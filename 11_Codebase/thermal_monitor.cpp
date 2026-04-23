// thermal_monitor.cpp — REV C (Thermal → Hardware Kill Integration)

#include <Arduino.h>

// ---------------- CONFIG ----------------

// Analog temp sensors (LM35 or equivalent)
#define TEMP_SERVO_PIN A0
#define TEMP_BATTERY_PIN A1
#define TEMP_BUCK_PIN A2

// Kill line output pin (wired to relay / MOSFET control)
#define KILL_PIN 22

// Thresholds (°C)
#define TEMP_WARNING 60.0
#define TEMP_CRITICAL 70.0
#define TEMP_RESET 55.0   // hysteresis reset point

// Filtering
#define FILTER_ALPHA 0.2

// Timing
#define UPDATE_INTERVAL_MS 100

// ---------------- STATE ----------------

float filteredServo = 25.0;
float filteredBattery = 25.0;
float filteredBuck = 25.0;

bool thermalShutdownActive = false;

// ---------------- UTIL ----------------

float readTemperature(int pin) {
    int raw = analogRead(pin);
    float voltage = (raw / 1023.0) * 3.3;
    return voltage * 100.0; // LM35
}

float filterTemp(float prev, float current) {
    return prev + FILTER_ALPHA * (current - prev);
}

// ---------------- KILL CONTROL ----------------

void enableServos() {
    digitalWrite(KILL_PIN, HIGH);  // ACTIVE HIGH = power ON
}

void disableServos() {
    digitalWrite(KILL_PIN, LOW);   // cut power
}

// ---------------- ACTIONS ----------------

void thermalThrottle() {
    // Signal to Pi via serial (you already have comms)
    Serial.println("THERMAL_WARNING");
}

void thermalShutdown() {
    disableServos();  // HARD CUT
    thermalShutdownActive = true;
    Serial.println("THERMAL_SHUTDOWN");
}

// ---------------- CORE ----------------

void updateThermal() {
    float tServo = readTemperature(TEMP_SERVO_PIN);
    float tBattery = readTemperature(TEMP_BATTERY_PIN);
    float tBuck = readTemperature(TEMP_BUCK_PIN);

    filteredServo = filterTemp(filteredServo, tServo);
    filteredBattery = filterTemp(filteredBattery, tBattery);
    filteredBuck = filterTemp(filteredBuck, tBuck);

    float maxTemp = filteredServo;
    if (filteredBattery > maxTemp) maxTemp = filteredBattery;
    if (filteredBuck > maxTemp) maxTemp = filteredBuck;

    // --- CRITICAL SHUTDOWN ---
    if (maxTemp >= TEMP_CRITICAL) {
        if (!thermalShutdownActive) {
            thermalShutdown();
        }
        return;
    }

    // --- HYSTERESIS RESET ---
    if (thermalShutdownActive && maxTemp < TEMP_RESET) {
        thermalShutdownActive = false;
        enableServos();
        Serial.println("THERMAL_RECOVERY");
    }

    // --- WARNING ---
    if (maxTemp >= TEMP_WARNING && !thermalShutdownActive) {
        thermalThrottle();
    }

    // Debug
    Serial.print("TEMP | S:");
    Serial.print(filteredServo);
    Serial.print(" B:");
    Serial.print(filteredBattery);
    Serial.print(" C:");
    Serial.print(filteredBuck);
    Serial.print(" MAX:");
    Serial.println(maxTemp);
}

// ---------------- SETUP ----------------

void setupThermal() {
    analogReadResolution(10);

    pinMode(KILL_PIN, OUTPUT);

    // Default SAFE behavior
    disableServos();
}

// ---------------- LOOP ----------------

void loopThermal() {
    static unsigned long lastUpdate = 0;

    if (millis() - lastUpdate >= UPDATE_INTERVAL_MS) {
        lastUpdate = millis();
        updateThermal();
    }
}

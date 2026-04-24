// thermal_monitor.cpp — REV E (Structured Temp Output + Latched Safety)

#include <Arduino.h>

// ---------------- CONFIG ----------------

#define TEMP_SERVO_PIN A0
#define TEMP_BATTERY_PIN A1
#define TEMP_BUCK_PIN A2

#define KILL_PIN 22
#define RESET_BUTTON_PIN 23

#define TEMP_WARNING 60.0
#define TEMP_CRITICAL 70.0

#define FILTER_ALPHA 0.2
#define UPDATE_INTERVAL_MS 100

// ---------------- STATE ----------------

float filteredServo = 25.0;
float filteredBattery = 25.0;
float filteredBuck = 25.0;

bool thermalShutdownLatched = false;

// ---------------- UTIL ----------------

float readTemperature(int pin) {
    int raw = analogRead(pin);
    float voltage = (raw / 1023.0) * 3.3;
    return voltage * 100.0;
}

float filterTemp(float prev, float current) {
    return prev + FILTER_ALPHA * (current - prev);
}

// ---------------- CONTROL ----------------

void enableServos() {
    digitalWrite(KILL_PIN, HIGH);
}

void disableServos() {
    digitalWrite(KILL_PIN, LOW);
}

// ---------------- ACTIONS ----------------

void thermalThrottle() {
    Serial.println("THERMAL_WARNING");
}

void triggerThermalShutdown() {
    disableServos();
    thermalShutdownLatched = true;
    Serial.println("THERMAL_SHUTDOWN_LATCHED");
}

// ---------------- RESET ----------------

void checkManualReset() {
    if (thermalShutdownLatched) {
        if (digitalRead(RESET_BUTTON_PIN) == HIGH) {
            thermalShutdownLatched = false;
            enableServos();
            Serial.println("THERMAL_MANUAL_RESET");
            delay(500);
        }
    }
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

    // --- ALWAYS SEND TEMP DATA ---
    Serial.print("TEMP:");
    Serial.print(filteredServo); Serial.print(",");
    Serial.print(filteredBattery); Serial.print(",");
    Serial.println(filteredBuck);

    if (thermalShutdownLatched) {
        checkManualReset();
        return;
    }

    if (maxTemp >= TEMP_CRITICAL) {
        triggerThermalShutdown();
        return;
    }

    if (maxTemp >= TEMP_WARNING) {
        thermalThrottle();
    }
}

// ---------------- SETUP ----------------

void setupThermal() {
    analogReadResolution(10);
    pinMode(KILL_PIN, OUTPUT);
    pinMode(RESET_BUTTON_PIN, INPUT);
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

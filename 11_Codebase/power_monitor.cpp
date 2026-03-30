// power_monitor.cpp
// OBSIDIAN-8 V3 — REV D
// Monitors all high-current rails and triggers safety mechanisms

#include <Arduino.h>

// -------------------- HARDWARE CONFIG --------------------
// ACS758 current sensors connected to Teensy analog pins
const int CURRENT_SENSOR_BANK_A = A0;  // Servos bank A
const int CURRENT_SENSOR_BANK_B = A1;  // Servos bank B

// Battery voltage monitor
const int VOLTAGE_PIN = A2; // Voltage divider to ADC pin

// Contactors for servo banks
const int CONTACTOR_BANK_A = 5; // Digital output pin
const int CONTACTOR_BANK_B = 6;

// Fuses / status LEDs (optional)
const int LED_FAULT = 13;

// -------------------- SENSOR CALIBRATION --------------------
const float ACS_OFFSET = 2.5;      // ACS758 zero-current output (V)
const float ACS_SENSITIVITY = 0.040; // 40 mV/A
const float VOLTAGE_DIVIDER_RATIO = 11.0; // Battery voltage divider R1+R2 / R2

// Safety limits
const float MAX_CURRENT = 80.0;    // Maximum safe servo current (A)
const float MAX_VOLTAGE = 28.0;    // Maximum battery voltage
const float MIN_VOLTAGE = 20.0;    // Minimum battery voltage

// -------------------- GLOBAL VARIABLES --------------------
float currentA = 0.0;
float currentB = 0.0;
float batteryVoltage = 0.0;

// -------------------- HELPER FUNCTIONS --------------------

// Read current from ACS758 sensor (bank A/B)
float readCurrent(int pin) {
    int adc = analogRead(pin);
    float voltage = (adc / 1023.0) * 5.0; // Teensy ADC is 0-5V
    float current = (voltage - ACS_OFFSET) / ACS_SENSITIVITY;
    return current;
}

// Read battery voltage via voltage divider
float readVoltage(int pin) {
    int adc = analogRead(pin);
    float voltage = (adc / 1023.0) * 5.0 * VOLTAGE_DIVIDER_RATIO;
    return voltage;
}

// Trigger emergency shutdown
void triggerEmergencyShutdown() {
    digitalWrite(CONTACTOR_BANK_A, LOW);
    digitalWrite(CONTACTOR_BANK_B, LOW);
    digitalWrite(LED_FAULT, HIGH);
    Serial.println("EMERGENCY SHUTDOWN ACTIVATED!");
}

// Check all sensors against safety limits
void checkSafety() {
    bool faultDetected = false;

    // Current checks
    if (abs(currentA) > MAX_CURRENT) {
        Serial.print("FAULT: Bank A overcurrent! ");
        Serial.print(currentA);
        Serial.println(" A");
        faultDetected = true;
    }
    if (abs(currentB) > MAX_CURRENT) {
        Serial.print("FAULT: Bank B overcurrent! ");
        Serial.print(currentB);
        Serial.println(" A");
        faultDetected = true;
    }

    // Voltage checks
    if (batteryVoltage > MAX_VOLTAGE) {
        Serial.print("FAULT: Overvoltage! ");
        Serial.print(batteryVoltage);
        Serial.println(" V");
        faultDetected = true;
    }
    if (batteryVoltage < MIN_VOLTAGE) {
        Serial.print("FAULT: Undervoltage! ");
        Serial.print(batteryVoltage);
        Serial.println(" V");
        faultDetected = true;
    }

    // Trigger shutdown if any fault
    if (faultDetected) {
        triggerEmergencyShutdown();
    } else {
        digitalWrite(LED_FAULT, LOW);
    }
}

// -------------------- SETUP --------------------
void setup() {
    Serial.begin(115200);

    pinMode(CONTACTOR_BANK_A, OUTPUT);
    pinMode(CONTACTOR_BANK_B, OUTPUT);
    pinMode(LED_FAULT, OUTPUT);

    // Enable servo banks
    digitalWrite(CONTACTOR_BANK_A, HIGH);
    digitalWrite(CONTACTOR_BANK_B, HIGH);

    Serial.println("Power Monitor Initialized — OBSIDIAN-8 V3");
}

// -------------------- LOOP --------------------
void loop() {
    // Read sensors
    currentA = readCurrent(CURRENT_SENSOR_BANK_A);
    currentB = readCurrent(CURRENT_SENSOR_BANK_B);
    batteryVoltage = readVoltage(VOLTAGE_PIN);

    // Check for safety faults
    checkSafety();

    // Debug output
    Serial.print("Voltage: ");
    Serial.print(batteryVoltage);
    Serial.print(" V | Current A: ");
    Serial.print(currentA);
    Serial.print(" A | Current B: ");
    Serial.println(currentB);

    delay(200); // 5 Hz update rate
}

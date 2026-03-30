// thermal_monitor.cpp
// OBSIDIAN-8 V3 — REV D
// Monitors servo, controller, and battery temperatures and triggers safety shutdown

#include <Arduino.h>
#include <math.h> // For log() in thermistor calculations

// -------------------- HARDWARE CONFIG --------------------
// NTC thermistors analog pins
const int SERVO_TEMP_BANK_A = A3;  // Example: bank A servo temp
const int SERVO_TEMP_BANK_B = A4;  // Example: bank B servo temp
const int BOARD_TEMP = A5;         // Teensy/Duet board temp
const int BATTERY_TEMP = A6;       // LiFePO4 battery temp

// Contactors for servo banks
const int CONTACTOR_BANK_A = 5;
const int CONTACTOR_BANK_B = 6;

// Fault LED
const int LED_FAULT = 13;

// -------------------- THERMISTOR CONFIG --------------------
// 100k NTC thermistor
const float THERMISTOR_NOMINAL = 100000.0; // 100k ohm at 25°C
const float TEMPERATURE_NOMINAL = 25.0;    // 25°C reference
const float B_COEFFICIENT = 3950.0;        // Beta coefficient
const float SERIES_RESISTOR = 10000.0;     // Series resistor in voltage divider

// Safety temperature limits (°C)
const float MAX_SERVO_TEMP = 80.0;
const float MAX_BOARD_TEMP = 75.0;
const float MAX_BATTERY_TEMP = 60.0;

// -------------------- GLOBAL VARIABLES --------------------
float tempServoA = 0.0;
float tempServoB = 0.0;
float tempBoard = 0.0;
float tempBattery = 0.0;

// -------------------- HELPER FUNCTIONS --------------------

// Convert analog reading to temperature (°C) using Beta formula
float readNTCTemperature(int pin) {
    int adc = analogRead(pin);
    float voltage = (adc / 1023.0) * 5.0;
    float resistance = (5.0 - voltage) * SERIES_RESISTOR / voltage;
    float steinhart;
    steinhart = resistance / THERMISTOR_NOMINAL;      // (R/Ro)
    steinhart = log(steinhart);                       // ln(R/Ro)
    steinhart /= B_COEFFICIENT;                       // 1/B * ln(R/Ro)
    steinhart += 1.0 / (TEMPERATURE_NOMINAL + 273.15); // + (1/To)
    steinhart = 1.0 / steinhart;                      // Invert
    steinhart -= 273.15;                              // Convert to °C
    return steinhart;
}

// Trigger emergency shutdown
void triggerEmergencyShutdown() {
    digitalWrite(CONTACTOR_BANK_A, LOW);
    digitalWrite(CONTACTOR_BANK_B, LOW);
    digitalWrite(LED_FAULT, HIGH);
    Serial.println("EMERGENCY SHUTDOWN DUE TO OVERHEAT!");
}

// -------------------- SAFETY CHECK --------------------
void checkThermalSafety() {
    bool faultDetected = false;

    // Servo temperatures
    if (tempServoA > MAX_SERVO_TEMP) {
        Serial.print("FAULT: Bank A servo overtemperature: ");
        Serial.print(tempServoA);
        Serial.println(" °C");
        faultDetected = true;
    }
    if (tempServoB > MAX_SERVO_TEMP) {
        Serial.print("FAULT: Bank B servo overtemperature: ");
        Serial.print(tempServoB);
        Serial.println(" °C");
        faultDetected = true;
    }

    // Board temperature
    if (tempBoard > MAX_BOARD_TEMP) {
        Serial.print("FAULT: Board overtemperature: ");
        Serial.print(tempBoard);
        Serial.println(" °C");
        faultDetected = true;
    }

    // Battery temperature
    if (tempBattery > MAX_BATTERY_TEMP) {
        Serial.print("FAULT: Battery overtemperature: ");
        Serial.print(tempBattery);
        Serial.println(" °C");
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

    Serial.println("Thermal Monitor Initialized — OBSIDIAN-8 V3");
}

// -------------------- LOOP --------------------
void loop() {
    // Read temperatures
    tempServoA = readNTCTemperature(SERVO_TEMP_BANK_A);
    tempServoB = readNTCTemperature(SERVO_TEMP_BANK_B);
    tempBoard  = readNTCTemperature(BOARD_TEMP);
    tempBattery= readNTCTemperature(BATTERY_TEMP);

    // Check safety
    checkThermalSafety();

    // Debug output
    Serial.print("Servo A: "); Serial.print(tempServoA); Serial.print(" °C | ");
    Serial.print("Servo B: "); Serial.print(tempServoB); Serial.print(" °C | ");
    Serial.print("Board: "); Serial.print(tempBoard); Serial.print(" °C | ");
    Serial.print("Battery: "); Serial.println(tempBattery); Serial.println(" °C");

    delay(500); // 2 Hz update rate
}

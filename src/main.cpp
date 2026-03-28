#include <Arduino.h>
#include <Wire.h>
#include <Mouse.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

float sensitivity = 2.0;
float damper = 0.15;
int pressure_threshold = 600;

const int PRESSURE_PIN = A0;
const int PUFF_WINDOW_MS = 400;
const int LONG_PUFF_MS = 1200;

Adafruit_MPU6050 mpu;
float smoothed_X = 0;
float smoothed_Y = 0;

unsigned long puffStartTime = 0;
unsigned long lastPuffTime = 0;
int puffCount = 0;
bool isPuffing = false;
bool actionFired = false;

void executeHomeSequence() {
    for(int i = 0; i < 50; i++) { Mouse.move(-100, -100, 0); }
    delay(50);
    for(int i = 0; i < 15; i++) { Mouse.move(100, 50, 0); } 
}

void parseSerial() {
    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n');
        if (cmd.startsWith("SENS:")) sensitivity = cmd.substring(5).toFloat();
        if (cmd.startsWith("DAMP:")) damper = cmd.substring(5).toFloat();
        if (cmd.startsWith("THRE:")) pressure_threshold = cmd.substring(5).toInt();
    }
}

void setup() {
    Serial.begin(115200);
    Wire.begin();
    if (!mpu.begin()) while (1) delay(10);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    Mouse.begin();
}

void loop() {
    parseSerial();
    sensors_event_t a, g, temp; 
    mpu.getEvent(&a, &g, &temp);

    smoothed_X = (damper * g.gyro.z) + ((1.0 - damper) * smoothed_X);
    smoothed_Y = (damper * g.gyro.y) + ((1.0 - damper) * smoothed_Y);
    
    Mouse.move(-(int)(smoothed_X * sensitivity * 10), (int)(smoothed_Y * sensitivity * 10), 0);
    
    int currentPressure = analogRead(PRESSURE_PIN);
    bool currentlyPuffing = (currentPressure > pressure_threshold);
    unsigned long currentTime = millis();

    if (currentlyPuffing && !isPuffing) {
        isPuffing = true;
        puffStartTime = currentTime;
        actionFired = false;
    } else if (!currentlyPuffing && isPuffing) {
        isPuffing = false;
        if ((currentTime - puffStartTime) < LONG_PUFF_MS) {
            puffCount++;
            lastPuffTime = currentTime;
        }
    } else if (currentlyPuffing && isPuffing && (currentTime - puffStartTime) >= LONG_PUFF_MS && !actionFired) {
        executeHomeSequence();
        actionFired = true;
        puffCount = 0;
    }

    if (!isPuffing && puffCount > 0 && (currentTime - lastPuffTime) > PUFF_WINDOW_MS) {
        if (puffCount == 1) Mouse.click(MOUSE_LEFT);
        else if (puffCount >= 2) Mouse.click(MOUSE_RIGHT);
        puffCount = 0;
    }
    delay(10);
}

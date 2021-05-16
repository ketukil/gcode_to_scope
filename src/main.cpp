/**
 * @file main.cpp
 * @author ketukil (cat2kill@gmial.com)
 * @brief Some oscilloscope vector magic done for Zoki's birthday
 * @version 1.0
 * @date 2021-05-08
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#include <Arduino.h>
#include <stdint.h>
#include <avr/pgmspace.h>
#include "graphic.h"

const int X_pin = 5;
const int Y_pin = 6;
const int voltage_measurement_pin = A0

const char *const messages[] = {
    ".\n",
    " * System online . . . . . . . . . . . . . . [ok] \n",
    " * Optimizing neural network . . . . . . . . [failed]\n",
    " * Multiply 7 * 4 = ?? . . . . . . . . . . . [error]\n",
    " * Measure external voltage . . . . . . . . .[",
    " units]\n",
    " * Set PWM to 62500.00 Hz . . . . . . . . . .[ok]\n",
    " * Adjust RC constat . . . . . . . . . . . . [manually]\n",
    " * Connect to external oscilloscope . . . .  [manually]\n",
    "\n\n",
    " * HAVE A GREAT FUCKING BIRTHDAY DUDE ! . .  [ok]\n"
};

void setup()
{
    Serial.begin(9600);

    delay(500);

    pinMode(13, OUTPUT);

    pinMode(X_pin, OUTPUT);
    pinMode(Y_pin, OUTPUT);
    pinMode(voltage_measurement_pin, INPUT);

    int voltage = analogRead(voltage_measurement_pin);

    for (int i = 0; i < sizeof(messages)/sizeof(messages[0]); i++)
    {   
        Serial.print(messages[i]);
        if (i == 4) Serial.print(voltage);
        delay(400);
        digitalWrite(13, 1);
        delay(100);
        digitalWrite(13, 0);
    }

    digitalWrite(13, 1);
    TCCR0B = (TCCR0B & B11111000) | B00000001;
}

void loop()
{
    unsigned long n;
    uint8_t x, y;

    for (n = 0; n < DOT_ARRAY_SIZE; n++)
    {
        x = pgm_read_byte(&dot[n][0]);
        y = pgm_read_byte(&dot[n][1]);
        analogWrite(X_pin, x);
        analogWrite(Y_pin, y);
        delay(50);
    }
    digitalWrite(13, 0);
    delay(50);
    digitalWrite(13, 1);
}

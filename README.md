# Embedded-Motion-Classification-System
## Project overview

This project implements a real-time motion classification system on an STM32 microcontroller using a pretrained and quantized machine learning model generated with Edge Impulse (https://www.edgeimpulse.com/)

The system captures motion data from a sensor (accelerometer), performs preprocessing, and runs on-device inference to classify motion patterns.

## Machine Learning Pipeline
1. Data collection using motion sensor
2. Dataset labeling
3. Model training in Edge Impulse
4. Model quantization (int8)
5. Deployment to STM32
6. Real-time inference on-device

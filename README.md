# Devices used
*	Arduino Uno with a water sensor attached
*	Nucleo F303RE with a LM35 temperature sensor attached
*	Raspberry Pi 3
# Description
Arduino and Nucleo send sensor data to Raspberry Pi via USB interface. Raspberry observes the data and sends user an alarm message through PushBullet if water is detected. Raspberry also has a web server with a simple website where the temperature data is updated.

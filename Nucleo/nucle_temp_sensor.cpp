#include "mbed.h"
 
AnalogIn analog_value(A0);

Serial raspberry(USBTX, USBRX); // tx, rx

//Ticker so device can low power sleep between readings
LowPowerTicker ticker;

double delay = 10;

float meas = 0.0f;
float cal = 666;
int measAmount = 100;

void getTemp()
{
	// get average of 100 samples to avoid bad readings
    for (int i = 0; i < measAmount; i++) {
        meas = meas + analog_value.read()*cal; // Converts and read the analog input value to celsius
        wait_ms(20); // 200 ms
    }
    raspberry.printf("%f\r\n", meas/measAmount);
    meas = 0;
    sleep();
}

int main() 
{
    ticker.attach(&getTemp, delay); 
}
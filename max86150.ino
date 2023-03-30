#include <Wire.h>
#include "max86150.h"
#include <FIR.h>

MAX86150 max86150Sensor;

#define debug Serial

int16_t ecgsigned16;
uint16_t redunsigned16;

FIR<long, 13> fir;

long coef[13] = {
  -364,
  -103,
  -42,
  60,
  173,
  262,
  295,
  262,
  173,
  60,
  -42,
  -103,
  -364};

void setup()
{
  debug.begin(115200);
  //debug.println("MAX86150 Basic Readings Example");

  // Setarea coeficienților
  fir.setFilterCoeffs(coef);

  // Initializarea senzorului
  if (max86150Sensor.begin(Wire, I2C_SPEED_FAST) == false)
  {

    while (1)
  }
  max86150Sensor.setup(); // Configurarea senzorului
}

void loop()
{
  if (max86150Sensor.check() > 0)
  {
    ecgsigned16 = (int16_t)(max86150Sensor.getECG() >> 2);
    redunsigned16 = (uint16_t) (max86150Sensor.getFIFORed()>>2);
    debug.print(millis());
    debug.print('\t');
    //debug.print(',');
    debug.print(fir.processReading(ecgsigned16));
    debug.print('\t');
    debug.println(redunsigned16);
  }
}

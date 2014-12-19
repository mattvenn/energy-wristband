#include <RFduinoBLE.h>

// default serial RX & TX are on pins 0 & 1 
int button = 0;
int batt_level = 1;

const int num_leds = 4;
int leds[num_leds] = {2, 3, 4, 5};
int motor = 6;

// timings
int motor_on = 50;
int motor_off = 300;

int last_reading = 0;

// struct to send messages back
typedef struct Msg
{
    int batt;
    int uptime;
};

Msg msg;

// message buffer
char txBuf[32];

// #define SERIAL_DEBUG

void setup() 
{
    //keep this small because total is 15 bytes for this and advertisement data
    RFduinoBLE.deviceName = "e-wb";

    // advertisement interval makes a big difference to power consumption
    RFduinoBLE.advertisementInterval = 2000; 

    // initialise pins
    pinMode(button, INPUT_PULLUP);
    pinMode(batt_level, OUTPUT);

    pinMode(motor, OUTPUT);
    digitalWrite(motor, LOW);

    // analog reference
    analogReference(VBG);
    // no prescaling (defaults to 1/3?)
    analogSelection(AIN_NO_PS);

    // leds
    for( int i = 0 ; i<num_leds; i ++)
    {
        pinMode(leds[i], OUTPUT);
    }

    // check power consumption on this
    digitalWrite(batt_level, LOW);
    RFduino_pinWake(button, LOW);

    #ifdef SERIAL_DEBUG
        Serial.begin(9600);
    #endif

    // start the BLE stack
    RFduinoBLE.begin();

    // show that we've started
    for(int i = 0; i < 4 ; i ++)
    {
        bar_graph(4);
        delay(100);
        bar_graph(0);
        delay(100);
    }

    // initialise watchdog
    NRF_WDT->CRV = 10 * 32768; // Timeout period of 10 s
    NRF_WDT->TASKS_START = 1; // Watchdog start
}


// reading the dac makes a 300uA difference to power consumption, which
// stays high after a read. So this turns it off after use
int readDAC()
{
  NRF_ADC->TASKS_START = 1;

  pinMode(batt_level, INPUT);

  delay(10);

  int batt = analogRead(batt_level); 

  NRF_ADC->TASKS_STOP = 1;

  pinMode(batt_level, OUTPUT);
//  digitalWrite(batt_level, LOW); //with this in, seems slightly larger energy usage

  return batt;
}

void loop()
{
    // sleep 5 seconds or till we're woken by BLE or button press
    RFduino_ULPDelay(5000);

    // reset watchdog
    NRF_WDT->RR[0] = WDT_RR_RR_Reload;

    // if button pressed, show last reading
    if(RFduino_pinWoke(button))
    {
        RFduino_resetPinWake(button);
        bar_graph(last_reading);
        delay(1000);
        bar_graph(0);
    }
}


// when a radio connection is made
void RFduinoBLE_onConnect()
{
    // send back battery and uptime
    // would be good to know how send() works
    // I think it puts the data in a buffer which can then be read if the
    // client makes a connection & does a read
    msg.batt = readDAC();
    msg.uptime = millis() / 1000;
    memcpy(&txBuf, &msg, sizeof(msg));
    RFduinoBLE.send(txBuf, sizeof(msg));
}

// when we receive data
void RFduinoBLE_onReceive(char *data, int len)
{
    if(len == 1) 
    {
        // then just set the last_reading, so wristband can be silently updated
        last_reading = data[0];
    }
    else if(len == 2)
    {
        // flash & vibe
        #ifdef SERIAL_DEBUG
        Serial.println(data[0], DEC);
        Serial.println(data[1], DEC);
        #endif
        last_reading = data[1];
        indicate(data[0], data[1]);
    }  
}

// show the energy change with lights and motor pulses
void indicate(int start, int end)
{
    if( start < end )
    {
        for(int i = start; i <= end; i ++)
        {
            bar_graph(i);
            vibe();
        }
    }
    else
    {
        for(int i = start; i >= end; i --)
        {
            bar_graph(i);
            vibe();
        }
    }

    // lights off
    bar_graph(0);
}

// can we do this with PWM?
void vibe()
{
    digitalWrite(motor, HIGH);
    delay(motor_on);
    digitalWrite(motor, LOW);
    delay(motor_off);
}

void bar_graph(int level)
{
  // all off
  for(int i=0; i < num_leds; i ++)
        digitalWrite(leds[i], LOW); 

  // turn on what we need
  for(int i=0; i < level; i ++)
    digitalWrite(leds[i], HIGH); 
}

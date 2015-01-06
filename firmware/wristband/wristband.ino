#include <RFduinoBLE.h>

// default serial RX & TX are on pins 0 & 1 
int button = 0;
int batt_level = 1;

const int num_leds = 4;
int leds[num_leds] = {2, 3, 4, 5};
int motor = 6;

// UI constants
const int bar_delay = 400;  // time between changing leds on the bargraph
const int bar_end_delay = 400; // time between showing multiple bar graphs
const int min_motor = 40;   // min motor pwm
const int max_motor = 200;  // max motor pwm
// how long before last update becomes 'old', needs to be more than the update
// of the daemon process - which is 10mins for now
const double comm_timeout = 1000 * 60 * 15; // 15 minutes

int last_reading = 0;
// each update message has as sequence number to avoid repeated warnings
int last_seq = -1; 
double last_comms = 0;

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
    NRF_WDT->CRV = 20 * 32768; // Timeout period of 10 s
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
        if(millis() > last_comms + comm_timeout)
        {
            for(int i=0; i<3; i++)
            {
                bar_graph(last_reading);
                delay(250);
                bar_graph(0);
                delay(250);
            }
        }
        else
        {
            bar_graph(last_reading);
            delay(1000);
            bar_graph(0);
        }
        RFduino_resetPinWake(button);
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
    last_comms = millis();
    if(len == 1) 
    {
        // then just set the last_reading, so wristband can be silently updated
        last_reading = data[0];
    }
    else if(len == 3)
    {
        // flash & vibe
        #ifdef SERIAL_DEBUG
        Serial.println(data[0], DEC);
        Serial.println(data[1], DEC);
        Serial.println(data[2], DEC);
        #endif
        last_reading = data[1];
        int seq = data[2];
        if(seq != last_seq)
        {
            indicate(data[0], data[1]);
            last_seq = seq;
        }
    }  
}

// show the energy change with lights and motor pulses
void indicate(int start, int end)
{
    // vibe to start with
    vibe(start,end);

    // repeat the light show 3 times
    for(int i=0; i<3; i++)
    {
        if( start < end )
        {
            for(int i = start; i <= end; i ++)
            {
                bar_graph(i);
                delay(bar_delay);
            }
        }
        else
        {
            for(int i = start; i >= end; i --)
            {
                bar_graph(i);
                delay(bar_delay);
            }
        }
        delay(bar_end_delay);
    }

    // lights off
    bar_graph(0);
}

void vibe(int start, int end)
{

    int start_m = map(start,1,4,min_motor,max_motor);
    int end_m = map(end,1,4,min_motor,max_motor);
    int step = 1;
    int d = 10;

    if(end>start)
    {
        for(int i=start_m; i<end_m; i+=step)
        {
            analogWrite(motor,i);
            delay(d);
        }
    }
    else
    {
        for(int i=start_m; i>end_m; i-=step)
        {
            analogWrite(motor,i);
            delay(d);
        }
    }
    analogWrite(motor,0);
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

/*
    FlagBot Firmware
    Author: David Estevez Fernandez
    Licence: GPLv3 
    
*/

//-- Dependencies
#include <Servo.h>

//-- Definitions of configuration parameters
#define FLAG_PIN 8
#define FLAG_INITIAL_POS 90
#define BAUD_RATE 9600

#define LED_PIN 13

//-- Create global objects:
#define BUFFER_SIZE 16

Servo servo;
char buffer[BUFFER_SIZE];

//-- Hardware setup
void setup()
{
    //-- Setup the signal LED
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);
    
    //-- Initialize the servo:
    servo.attach(FLAG_PIN);
    servo.write(FLAG_INITIAL_POS);
    
    //-- Setup the serial port:
    Serial.begin(BAUD_RATE);
    Serial.flush();
    Serial.println("[Debug] Ok!");
    
    //-- Clear the buffer:
    erase(buffer);
}

void loop()
{
	if ( Serial.available() > 0 )
	{
		//-- Recieve the command:
		delay(20); //-- Waits for the buffer to be filled

		int data = Serial.available(); //-- Number of bytes recieved
		
		if (data > BUFFER_SIZE) //--Avoid overflow
			data = BUFFER_SIZE;

		for ( int i = 0; i < data; i++) //-- Write the data on the buffer
			buffer[i] = Serial.read(); 

		//-- Decrypt the command:
		if ( buffer[0] == 'M')
		{
		  //-- Manage 'move' commands
  		  move_cmd(buffer);
		}
                else if (buffer[0] == 'L')
                {
                  //-- Toggle LED
                  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
                }
		else if (buffer[0] == 'P' && buffer[1] == 'I'
				&& buffer[2] == 'N' && buffer[3] == 'G')
		{	
			//-- PING: checks the connection
			Serial.println("Ok");
		}

		//-- If it doesn't recognize the command, or has received it correctly
		//-- prepare for a new command:
		Serial.flush();
		erase(buffer);
	}
}

void move_cmd(char * buffer)
{
   int end_pos = strcspn(buffer, "\n");
   int angle = strtol(buffer+1, NULL, 10);;
   Serial.println(angle);
   servo.write(angle); 
}

void erase( char *buffer)
{
  //-- Clear the buffer:
  memset(buffer, 0, BUFFER_SIZE * sizeof(char));
}

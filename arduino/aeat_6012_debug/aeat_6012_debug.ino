// Read in 12-bits Magnetic Encoder AEAT-6012-A06
// RobinL modified by linarism and bstadlbauer
// Script for debugging. Returns a continous stream of angle measurements as soon as started

// Declarate

const int CSn = 4; // Chip select
const int CLK = 7; // Clock signal
const int DO = 8; // Digital Output from the encoder which delivers me a 0 or 1, depending on the bar angle..

unsigned int sensorWaarde = 0;

void setup(){

  Serial.begin(115200);
  Serial.println("Hello World!"); //send sample text to monitor for debug

  pinMode(CSn, OUTPUT);
  pinMode(CLK, OUTPUT);
  pinMode(DO, INPUT);

  digitalWrite(CLK, HIGH);
  digitalWrite(CSn, HIGH);
}

void loop() {
  sensorWaarde = readSensor();
  delayMicroseconds(1); //Tcs waiting for another read in
}

unsigned int readSensor(){
  unsigned int dataOut = 0;

  digitalWrite(CSn, LOW);
  delayMicroseconds(1); //Waiting for Tclkfe

  //Passing 12 times, from 0 to 11
  for(int x=0; x<12; x++){
    digitalWrite(CLK, LOW);
    delayMicroseconds(1); //Tclk/2
    digitalWrite(CLK, HIGH);
    delayMicroseconds(1); //Tdo valid, like Tclk/2
    dataOut = (dataOut << 1) | digitalRead(DO); //shift all the entering data to the left and past the pin state to it. 1e bit is MSB
  }

  digitalWrite(CSn, HIGH); //deselects the encoder from reading
  Serial.println(dataOut);
  return dataOut;
}


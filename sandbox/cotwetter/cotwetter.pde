char sbit = 's';
char fbit = 'x';

int RED = 0;
int GREEN = 1;
int BLUE = 2;
//led assignments
// long is GND
// RxBG

void setup() {
  establishSerialContact();
  setupPins(); 
}

void loop() {
  waitForInput();
  getAndWriteLED();
}

void getAndWriteLED() {
  int sflag = Serial.read();
  int city = Serial.read(); 
  int color = Serial.read();
  int fflag = Serial.read();
  Serial.write(sflag);Serial.write(city);Serial.write(color);Serial.write(fflag);
  if ( sflag == sbit && fflag == fbit ) {
    writeLED(city, color);  
  }
}

void establishSerialContact() {
  Serial.begin(9600);
  if (Serial.available() <= 0) {
    Serial.write('A');Serial.write('t');Serial.write('W');
  }
}

// makes pins 22-52 Digital Out
void setupPins() {
  int pinSet;
  for (pinSet=22; pinSet<53; ++pinSet) {
    pinMode(pinSet, OUTPUT);
  } 
}

void turnAllOff(int city) {
  digitalWrite(city + RED, LOW);
  digitalWrite(city + GREEN, LOW);
  digitalWrite(city + BLUE, LOW);
}

void writeLED(int city, int color) {
  turnAllOff(city);
  switch (color) {
    case 0: //off
      break;
    case 1: //red
      digitalWrite(city + RED, HIGH);
      break;
    case 2: //green
      digitalWrite(city + GREEN, HIGH);
      break;
    case 3: //blue
      digitalWrite(city + BLUE, HIGH);
      break;
    case 4: //cyan
      digitalWrite(city + GREEN, HIGH);
      digitalWrite(city + BLUE, HIGH);
      break;
    case 5: //yellow
      digitalWrite(city + GREEN, HIGH);
      digitalWrite(city + RED, HIGH);
      break;
    case 6: //purple
      digitalWrite(city + RED, HIGH);
      digitalWrite(city + BLUE, HIGH);
      break;
    case 7: //white
      digitalWrite(city + RED, HIGH);
      digitalWrite(city + GREEN, HIGH);
      digitalWrite(city + BLUE, HIGH);
      break;
  }   
}

void waitForInput() {
  while(Serial.available() <= 3) {
    delay(100); //nop while nothing on line
  }
}

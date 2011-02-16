int inByte = 0;         // incoming serial byte
int count = 0;
//led assignments
// long is GND
// RXGB
int red = 42;
int blue = 43;
int green = 41;

void setup() {
  Serial.begin(9600);
  establishContact();
  setupPins(); 
}

void loop() {
  if (Serial.available() > 0) {
    count++;
    inByte = Serial.read();
    toggleBoardLED();
    turnAllOff();
    rotateColor();  
  }
}

void establishContact() {
  if (Serial.available() <= 0) {
    Serial.write('X');
  }
}

void setupPins() {
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
}

void turnAllOff() {
  digitalWrite(red, LOW);
  digitalWrite(green, LOW);
  digitalWrite(blue, LOW);
}

void rotateColor() {
  switch (count%3) {
    case 0:
      digitalWrite(red, HIGH);
      break;
    case 1:
      digitalWrite(green, HIGH);
      break;
    case 2: 
      digitalWrite(blue, HIGH);
      break;
  }   
}

void toggleBoardLED() {
  if (count%2 == 0) {
    digitalWrite(inByte, HIGH);
  }
  else {
    digitalWrite(inByte, LOW);
  }
}

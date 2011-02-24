int inByte = 0;         // incoming serial byte
int count = 0;
//led assignments
// long is GND
// RxBG
int red = 41;
int blue = 43;
int green = 42;

void setup() {
  establishSerialContact();
  setupPins(); 
}

void loop() {
  //digitalWrite(red, HIGH);
  //digitalWrite(green, HIGH);
  //digitalWrite(blue, HIGH);
  waitForInput();
  count++;
  inByte = Serial.read();
  toggleBoardLED();
  rotateColor();  
}

void establishSerialContact() {
  Serial.begin(9600);
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
  turnAllOff();
  switch (count%8) {
    case 0:
      digitalWrite(red, HIGH);
      break;
    case 1:
      digitalWrite(green, HIGH);
      break;
    case 2: 
      digitalWrite(blue, HIGH);
      break;
    case 3: 
      digitalWrite(blue, HIGH);
      digitalWrite(green, HIGH);
      break;
    case 4: 
      digitalWrite(green, HIGH);
      digitalWrite(red, HIGH);
      break;
    case 5: 
      digitalWrite(blue, HIGH);
      digitalWrite(red, HIGH);
      break;
    case 6: 
      //digitalWrite(blue, HIGH);
      break;
    case 7: 
      digitalWrite(blue, HIGH);
      digitalWrite(red, HIGH);
      digitalWrite(green, HIGH);
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

void waitForInput() {
  while(Serial.available() <= 0) {
    delay(100); //nop while nothing on line
  }
}

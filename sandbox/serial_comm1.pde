int inByte = 0;         // incoming serial byte

void setup()
{
  // start serial port at 9600 bps:
  Serial.begin(9600);
  establishContact();  // send a byte to establish contact until receiver responds 
}

void loop()
{
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    digitalWrite(inByte, HIGH);
    delay(500);
    digitalWrite(inByte, LOW);
          
  }
}

void establishContact() {
  if (Serial.available() <= 0) {
    Serial.write('X');
    delay(300);
  }
}

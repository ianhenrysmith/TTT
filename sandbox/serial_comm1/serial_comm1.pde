int inByte = 0;         // incoming serial byte
int count = 0;
void setup()
{
  // start serial port at 9600 bps:
  Serial.begin(9600);
  establishContact();  // send a byte to establish contact until receiver responds 
}

void loop()
{
  if (Serial.available() > 0) {
    count++;
    inByte = Serial.read();
    if (count%2 == 0) {
      digitalWrite(inByte, HIGH);
      switch (count%3) {
        case 0:
          digitalWrite(52, HIGH);
          break;
        case 1:
          digitalWrite(42, HIGH);
          break;
        case 2: 
          digitalWrite(43, HIGH);
          break;
      }
    }
    else {
      digitalWrite(inByte, LOW);
      switch (count%3) {
        case 0:
          digitalWrite(52, LOW);
          break;
        case 1:
          digitalWrite(42, LOW);
          break;
        case 2: 
          digitalWrite(43, LOW);
          break;
      }
    }     
  }
}

void establishContact() {
  if (Serial.available() <= 0) {
    Serial.write('X');
  }
}

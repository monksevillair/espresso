
const int buttonPin = 2;
const int ledPin = 13;

int hallState = 0;

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
}


void loop() {
  hallState = !digitalRead(buttonPin);
  Serial.println(hallState);
  digitalWrite(LED_BUILTIN, hallState);
  delay(10);
}

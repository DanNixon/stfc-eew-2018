const int led_pin = 13;

void setup()
{
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);
}

void loop()
{
  digitalWrite(led_pin, !digitalRead(led_pin));
  delay(100);
}

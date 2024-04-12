int const X_PIN = 15; //X = PIN D15      
int const Y_PIN = 2;  //Y = PIN D2
int const Z_PIN = 4;  //Z = PIN D4

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  unsigned int X = analogRead(X_PIN);
  unsigned int Y = analogRead(Y_PIN);
  unsigned int Z = analogRead(Z_PIN);

  Serial.print("X = ");
  Serial.println(X);
  Serial.print("Y = ");
  Serial.println(Y);
  Serial.print("Z = ");
  Serial.println(Z);
  Serial.println("-------");
  delay(200);
}
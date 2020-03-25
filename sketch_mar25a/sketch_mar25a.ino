void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, LOW);
  if (Serial.available() == 0) return;
  
  String command = Serial.readString();
  command.trim();
  
  if (command.startsWith("ra")) {
    digitalWrite(13, HIGH);
    
    int port = 0;
    if (sscanf(command.c_str(), "%*3c%d", &port) == 1) {  
      int val = analogRead(A0);
      Serial.print("analog ");
      Serial.print(port);
      Serial.print(" ");
      Serial.println(val);
      return;
    }
  }
  Serial.println("ERR: Unknown command: \"" + command + "\"");
}

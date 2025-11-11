#include <SoftwareSerial.h>
SoftwareSerial BT(2, 3); // RX, TX

// Motor driver pins
int IN1 = 8, IN2 = 9, IN3 = 10, IN4 = 11;
int ENA = 5, ENB = 6;

// Ultrasonic sensor pins
int TRIG = 13, ECHO = 12;

String inputString = "";
bool newData = false;
long duration;
int distance;

// ==================== Setup ====================
void setup() {
  BT.begin(9600);
  Serial.begin(9600);
  
  pinMode(IN1, OUTPUT); 
  pinMode(IN2, OUTPUT); 
  pinMode(IN3, OUTPUT); 
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  stopCar();
}

// ==================== Motor Functions ====================
void forward() { 
  digitalWrite(IN1, HIGH); 
  digitalWrite(IN2, LOW); 
  digitalWrite(IN3, HIGH); 
  digitalWrite(IN4, LOW);
}

void backward() { 
  digitalWrite(IN1, LOW);  
  digitalWrite(IN2, HIGH); 
  digitalWrite(IN3, LOW);  
  digitalWrite(IN4, HIGH);
}

void right() {
  // Right turn — left motor forward, right motor backward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void left() {
  // Left turn — left motor backward, right motor forward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void stopCar()  { 
  digitalWrite(IN1, LOW);  
  digitalWrite(IN2, LOW); 
  digitalWrite(IN3, LOW);  
  digitalWrite(IN4, LOW);
}

// ==================== Ultrasonic Function ====================
int getDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  duration = pulseIn(ECHO, HIGH);
  int distance = duration * 0.034 / 2; // convert to cm
  return distance;
}

// ==================== Main Loop ====================
void loop() {
  // Read characters until newline
  while (BT.available()) {
    char c = BT.read();
    if (c == '\n') {
      newData = true;
      break;
    } else {
      inputString += c;
    }
  }

  if (newData) {
    newData = false;
    int obstacleDist = getDistance();

    if (inputString.length() >= 2) {
      char cmd = inputString.charAt(0);
      int speedVal = inputString.substring(1).toInt();
      speedVal = constrain(speedVal, 0, 255);

      Serial.print("Cmd: "); Serial.print(cmd);
      Serial.print("  Speed: "); Serial.print(speedVal);
      Serial.print("  Distance: "); Serial.println(obstacleDist);

      analogWrite(ENA, speedVal);
      analogWrite(ENB, speedVal);

      // ===== Obstacle Handling =====
      if (obstacleDist < 15 && cmd == 'F') {
        Serial.println("Obstacle Detected! Stopping...");
        stopCar();
        delay(200);
        backward();        // move back for a bit
        delay(400);
        stopCar();
      }
      else {
        if (cmd == 'F' && obstacleDist >= 15) forward();
        else if (cmd == 'B') backward();
        else if (cmd == 'R') right();
        else if (cmd == 'L') left();
        else stopCar();
      }
    }

    inputString = ""; // clear buffer
  }
}

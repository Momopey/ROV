#include <Servo.h>

Servo Motor[4];
int Pos[4]={3,5,6,9};
int Light[4]={7,8,10,11};
int Mot[4]={1100,1100,1100};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=0;i<4;i++){
    Motor[i].attach(Pos[i]);
  }
  for(int i=0;i<4;i++){
    Motor[i].writeMicroseconds(1500);
  }
  delay(2000);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.setTimeout(50);
}

void setMotor(){
  for(int i=0;i<4;i++){
    Motor[i].writeMicroseconds(Mot[i]);
    if(Mot[i]>1520){
      digitalWrite(Light[i],HIGH);
    }else{
      digitalWrite(Light[i],LOW);
    }
  }
}
void stopAll(){
  for(int i=0;i<4;i++){
    Motor[i].writeMicroseconds(1100);
  }
}
float rate=5;
void loop() {
  while(Serial.available()){
    String prnt=Serial.readStringUntil('/n');
    String thisStr="";
    int ind=0;
    for(int i=0;i<prnt.length();i++){
      if(prnt.charAt(i)==':'){
        Mot[ind]=thisStr.toInt();
        thisStr="";
        ind++;
      }else{
        thisStr.concat(prnt.charAt(i));
      }
    }
    setMotor();
    //delay(1000/rate);
    Serial.flush();
  }
  //dimAll();
}



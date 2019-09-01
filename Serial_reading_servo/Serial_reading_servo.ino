#include <Servo.h>

Servo MotorOuts[20]={};
char TypeOuts[20]={};  // 'm','l'
int PosOuts[20]={};// UPDATE WITH ACTUAL POSITIONS
int DataOuts[20]={};
int numOuts=0;

char TypeSens[20]={};  // 'u'
int PosSens[20][2]={};// UPDATE WITH ACTUAL POSITIONS
int numSens=0;

boolean verb=true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=0;i<1;i++){
    MotorOuts[i].attach(PosOuts[i]);
  }
  for(int i=0;i<1;i++){
    MotorOuts[i].writeMicroseconds(1500);
  }
  delay(2000);
//  pinMode(10, OUTPUT);
//  pinMode(11, OUTPUT);
//  pinMode(7, OUTPUT);
//  pinMode(8, OUTPUT);
  Serial.setTimeout(50);
}
void setupOuts(String set){
  String sep[20]={"","","","","","","","","","","","","","","","","","","",""};
  int index=0;
  for(int i=0;i<set.length();i++){
    if(set.charAt(i)==':'){
      PosOuts[index]=sep[index].substring(1).toInt();
      TypeOuts[index]=sep[index].charAt(0);
      if(verb){
        Serial.println("out"+String(index)+":"+sep[index]);
      }
      index++;
    }else{
      sep[index]+=set.charAt(i);
    }
  }
  numOuts=index;
  for(int i=0;i<numOuts;i++){
    if(TypeOuts[i]=='m'){
      MotorOuts[i].attach(PosOuts[i]);
    }else{
      pinMode(PosOuts[i], OUTPUT);
    }
  }
}
void setupSens(String set){
  String sep[20]={"","","","","","","","","","","","","","","","","","","",""};
  int index=0;
  for(int i=0;i<set.length();i++){
    if(set.charAt(i)==':'){
      TypeSens[index]=sep[index].charAt(0);
      String posit=sep[index].substring(1);
      if(verb){
        Serial.println("ses"+String(index)+":"+sep[index]);
        Serial.println("ses"+String(index)+":"+posit);
      }
      int count=0;
      String locPos[2]={"",""};
      for(int j=0; j<posit.length();j++){
        if(posit.charAt(j)==','){
          PosSens[index][count]=locPos[count].toInt();
          if(verb){
            Serial.println("sen"+String(index)+":"+String(count)+":"+locPos[count]);
          }
          count++;
        }else{
          locPos[count]+=posit.charAt(j); 
        }
      }
      index++;
    }else{
      sep[index]+=set.charAt(i);
    }
  }
  numSens=index;
  for(int i=0;i<numOuts;i++){
    pinMode(PosSens[i][0], OUTPUT);
    pinMode(PosSens[i][1], INPUT);
  }
}

void setOuts(){
  for(int i=0;i<numOuts;i++){
    //Motor[i].writeMicroseconds(Mot[i]);
    if(TypeOuts[i]=='m'){
      MotorOuts[i].write(DataOuts[i]);
    }else{
      analogWrite(PosOuts[i],DataOuts[i]);
    }
  }
}
void stopAll(){
  for(int i=0;i<6;i++){
    MotorOuts[i].writeMicroseconds(1100);
  }
}
float rate=5;

///sesu5,6,:nsetm3:l9:l10:l11:n40:255:255:255:nret
void loop() {
  while(Serial.available()){
    String prnt=Serial.readStringUntil('/n');
    if(verb){
      Serial.println(prnt);
    }
    if(prnt=="ret"){
      for(int i=0;i<numOuts;i++){
        Serial.println("dao"+ String(DataOuts[i]));
      }
      for(int i=0;i<numOuts;i++){
        Serial.println("tyo"+String(TypeOuts[i]));
      }
      for(int i=0;i<numOuts;i++){
        Serial.println("poo"+ String(PosOuts[i]));
      }
      for(int i=0;i<numSens;i++){
        Serial.println("tys"+String(TypeSens[i]));
      }
      for(int i=0;i<numSens;i++){
        Serial.println("pos"+ String(PosSens[i][0])+":"+ String(PosSens[i][1]));
      }
    }else if(prnt.substring(0,3)=="set"){
      setupOuts(prnt.substring(3));
    }else if(prnt.substring(0,3)=="ses"){
      setupSens(prnt.substring(3));
    }else if(prnt=="req"){
      //Serial.println("Requesting sensor info");
      String ret="";
      for(int i=0;i<numSens;i++){
        int trigPin=5;//PosSens[i][0];
        int echoPin=6;//PosSens[i][1];
        //Clears the trigPin
        digitalWrite(trigPin, LOW);
        delayMicroseconds(2);
        // Sets the trigPin on HIGH state for 10 micro seconds
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);
        float duration = pulseIn(echoPin, HIGH);
        if(verb){
          Serial.println("dur"+String(duration));
        }
        // Calculating the distance
        int distance= duration*0.034/2;
        //Serial.println("distance: "+String(distance));
        ret+=String(distance);
        ret+=":";
      }
      Serial.println("ret"+ret);
    }else{
      String thisStr="";
      int ind=0;
      for(int i=0;i<prnt.length();i++){
        if(prnt.charAt(i)==':'){
          if(thisStr!=""){
            DataOuts[ind]=thisStr.toInt();
          }
          if(verb){
            Serial.println("rec"+thisStr+":"+ind);
          }
          thisStr="";
          ind++;
          
        }else{
          thisStr.concat(prnt.charAt(i));
        }
      }
      setOuts();
      //delay(1000/rate);
      //Serial.flush();
    }
  }
  //dimAll();
}



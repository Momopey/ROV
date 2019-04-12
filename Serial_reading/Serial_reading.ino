void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.setTimeout(50);
}
int Pos[4]={7,8,10,11};
int Light[4]={255,255,255,255};
void setLight(){  
  for(int i=0;i<=4;i++){
   if(Light[i]>124){
    digitalWrite(Pos[i],HIGH);
   }else{
    digitalWrite(Pos[i],LOW);
   }
  }
}
void dimAll(){
  for(int i=0;i<=4;i++){
    digitalWrite(Pos[i],LOW);
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
        Light[ind]=thisStr.toInt();
        thisStr="";
        ind++;
      }else{
        thisStr.concat(prnt.charAt(i));
      }
    }
    setLight();
//    digitalWrite(10,HIGH);
//    delay(1000/rate);
    Serial.flush();
  }
}



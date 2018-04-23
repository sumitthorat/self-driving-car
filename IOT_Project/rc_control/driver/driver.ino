int forward_pin = 6;
int back_pin = 7;
int left_pin = 10;
int right_pin = 12;

int command =0;
int time1 = 50;
int time2 = 9;

void setup() {
  pinMode(forward_pin,OUTPUT);
  pinMode(back_pin,OUTPUT);
  pinMode(left_pin,OUTPUT);
  pinMode(right_pin,OUTPUT);
  Serial.begin(9600);
}

void loop() {
//forward(time1, time2);
  

  if(Serial.available() > 0){
    command = Serial.read();  
  }
  else{
    reset();  
  }

  drive(command,time1,time2);
}

void reset(){
  digitalWrite(forward_pin,LOW);
  digitalWrite(back_pin,LOW);
  digitalWrite(left_pin,LOW);
  digitalWrite(right_pin,LOW);  
}

void forward(int time1, int time2){
  digitalWrite(forward_pin,HIGH);
  delay(time1);
  reset();
  //delay(time2);
}

void back(int time1, int time2){
  digitalWrite(back_pin,HIGH);
  delay(time1);
  reset();
  delay(time2);
}

void left(int time1, int time2){
  digitalWrite(left_pin,HIGH);
  delay(time1);
  reset();
  delay(time2);
}

void forward_left(int time1, int time2){
  digitalWrite(left_pin,HIGH);
  digitalWrite(forward_pin,HIGH);
  delay(time1);
  reset();
 // delay(time2);
  
}

void back_left(int time1, int time2){
  digitalWrite(back_pin,HIGH);
  digitalWrite(left_pin,HIGH);
  delay(time1);
  reset();
  delay(time2);
}

void right(int time1, int time2){
  digitalWrite(right_pin,HIGH);
  delay(time1);
  reset();
  delay(time2);
}

void forward_right(int time1, int time2) {
  digitalWrite(right_pin, HIGH);
  digitalWrite(forward_pin, HIGH);
  delay(time1);
  reset();
  //delay(time2);
}

void back_right(int time1, int time2){
  digitalWrite(back_pin,HIGH);
  digitalWrite(right_pin,HIGH);
  delay(time1);
  reset();
  delay(time2);
}

void drive(int command, int time1, int time2){
  switch(command){
    case 0:reset(); break;
    case 1:forward(time1,time2); break;
    case 2:back(time1,time2); break;
    case 3:right(time1,time2); break;
    case 4:left(time1,time2); break;
    
    case 6:forward_right(time1,time2); break;
    case 7:forward_left(time1,time2); break;
    case 8:back_right(time1,time2); break;
    case 9:back_left(time1,time2); break;  
    default: Serial.print("Inalid Command\n");
  }  
}

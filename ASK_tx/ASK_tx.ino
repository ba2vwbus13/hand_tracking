void setup() 
{
    Serial.begin(115200);
    pinMode(3,OUTPUT);
}


void loop() 
{
  byte HS;
  
  for(int i=0;i<8;i++){ //HS選び
    switch (i){
      case 0:
        HS = B00000000;
        break;
      case 1:
        HS = B00000001;
        break;
      case 2:
        HS = B00000010;
        break;
      case 3:
        HS = B00000011;
        break;
      case 4:
        HS = B00000100;
        break;
      case 5:
        HS = B00000101;
        break;
      case 6:
        HS = B00000110;
        break;
      case 7:
        HS = B00000111;
        break;
    }
    tone(3,40000);  //ストップビット
    delay(10);
    noTone(4);  //スタートビット
    
    for(int pos=0;pos<3;pos++){ //信号送信
      boolean b;
      b = bitRead(HS,2-pos);
      if(b) {
        tone(3,40000);
        delay(2);
      }
      else{
        noTone(3);
        delay(2);
      }
    }
  }
}

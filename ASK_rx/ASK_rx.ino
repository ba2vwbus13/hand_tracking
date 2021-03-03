void setup() 
{
   Serial.begin(115200);
   pinMode(5,INPUT_PULLUP);
}

void loop() 
{
  boolean capture = false;
  byte HS = B00000000;
   
  if(digitalRead(5)){
      unsigned long onTime = millis();
      
      while(digitalRead(5)){  
        while(millis()-onTime >= 9){       //ストップビット判定
        
          if(digitalRead(5) != 1){
            unsigned long offTime = millis();
          
            while(digitalRead(5) != 1){     //スタートビット判定
              if(millis()-offTime >= 3){
                capture = true;
                break;
              }
            }
          }
          if(capture = true) break;
        }
        break;
      }
   }

   while(capture){          //信号判定
      for(int pos=0;pos<3;pos++){
        if(digitalRead(5)){
          bitSet(HS,2-pos);
        }
        else {
          bitClear(HS,2-pos);
        }
        if(pos=0) delay(3);
        else if(pos=1) delay(2);
      }
      capture = false;
      break;
   }

   for(int pos=0;pos<3;pos++){   //受信信号表示
      int b;
      b = bitRead(HS,2-pos);
      Serial.print(b);
   }
   Serial.print("  ");

   switch (HS){         //HSの意味表示
      case B00000000:
          Serial.println("浮上する");
          break;
      case B00000001:
          Serial.println("潜行する");
          break;
      case B00000010:
          Serial.println("ちょっと待って");
          break;
      case B00000011:
          Serial.println("問題なし");
          break;
      case B00000100:
          Serial.println("問題あり");
          break;
      case B00000101:
          Serial.println("エア切れ");
          break;
      case B00000110:
          Serial.println("耳抜き");
          break;
      case B00000111:
          Serial.println("指差し");
          break;
   }
}

/* 
  Developed by:  Eduardo Zola - Zola Lab 2018 - www.zolalab.com.br - egzola@gmail.com
  Ultrasonic Data Communication
  Copyright (c) 2015 Eduardo Zola.  All right reserved.
  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.
  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.
*/

void setup() 
{
    Serial.begin(115200);
    pinMode(3,OUTPUT);
}

void loop() 
{
   send("Ultrasonic communication by Zola Lab\n");
   send("Hello World\n\n");
}

void send(String msg)
{
   byte ch;
   unsigned int pos = 0;
   unsigned int sz = msg.length();
   while(pos<sz)
   {
      ch = msg.charAt(pos);
      Serial.print((char)ch);
      //tone(3,40000);
      tone(3,40000);
      delay(10);
      noTone(3);
      for(int i=0;i<8;i++)
      {
         boolean b;
         b = bitRead(ch,7-i);
         if(b) 
         {
            //tone(3,40000);
            tone(3,40000);
            delay(2);
         }
         else
         {
            //tone(3,40000);
            tone(3,40000);
            delay(4);
         }
         noTone(3);
         delay(11);
      }
      pos++;
   }
}

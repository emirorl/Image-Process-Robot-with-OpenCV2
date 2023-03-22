#include <FastLED.h> //Kütüphane import
#define LED_GROUP_SIZE 10 //LED sayısı
#define LED_GROUP_PINS1 2
#define LED_GROUP_PINS2 3
#define LED_GROUP_PINS3 4
#define LED_GROUP_PINS4 5
#define LED_GROUP_PINS5 6

CRGB leds1[LED_GROUP_SIZE];
CRGB leds2[LED_GROUP_SIZE];
CRGB leds3[LED_GROUP_SIZE];
CRGB leds4[LED_GROUP_SIZE];
CRGB leds5[LED_GROUP_SIZE];
 int i;
 int l1;
 int l2;
 int sutun1;
 int sutun2; 
 int length1;
 int length2;
 int color1;
 int color2; 
 int k;
 int a;
 int ledmatris[10][5]={ 0 };

void setup() {
FastLED.addLeds<WS2812B, LED_GROUP_PINS1, GRB>(leds1, LED_GROUP_SIZE);
  FastLED.addLeds<WS2812B, LED_GROUP_PINS2, GRB>(leds2, LED_GROUP_SIZE);
  FastLED.addLeds<WS2812B, LED_GROUP_PINS3, GRB>(leds3, LED_GROUP_SIZE);
  FastLED.addLeds<WS2812B, LED_GROUP_PINS4, GRB>(leds4, LED_GROUP_SIZE);
  FastLED.addLeds<WS2812B, LED_GROUP_PINS5, GRB>(leds5, LED_GROUP_SIZE);
  FastLED.setBrightness(255);
  FastLED.show();
  i = 0;
  l1 = 0;
  l2 = 0;
  sutun1 = 0;
  sutun2 = 0;
  length1 = 0;
  length2 = 0;
  color1 = 0;
  color2 = 0;
  k = 0;
  a = 0;
}

void loop() {
   
  if((i%3)==0){
      
      if((i%2==0)){      
      length1 = (random()%4)+1;
      l1=0;
      color1 = random(2)+1;
      sutun1 = random()%5;

      }else if(!(i%2==0)){
       length2 = (random()%4)+1;
       l2=0; 
       color2 = random(2)+1;
       sutun2 = random()%5;         
      }                     
  }
  for(k=0; k<9;k++){
    for(a=0; a<5; a++){
      ledmatris[9-k][a]=ledmatris[8-k][a];    
    }            
  }
    ledmatris[0][0]={0};
    ledmatris[0][1]={0};
    ledmatris[0][2]={0};
    ledmatris[0][3]={0};
    ledmatris[0][4]={0};
    if((l1<length1)){
      ledmatris[0][sutun1]=color1;
      l1++;
    } 
    if((l2<length2)){
      ledmatris[0][sutun2]=color2;
      l2++;
    }    
    for(k=0;k<10;k++){
      if((ledmatris[k][0]==0)){
        leds1[k].setRGB(0,0,0);
      }else if((ledmatris[k][0]==1)){
        leds1[k].setRGB(50,0,0);
      }else if((ledmatris[k][0]==2)){
        leds1[k].setRGB(0,150,0);
      }
      if((ledmatris[k][1]==0)){
        leds2[k].setRGB(0,0,0);
      }else if((ledmatris[k][1]==1)){
        leds2[k].setRGB(50,0,0);
      }else if((ledmatris[k][1]==2)){
        leds2[k].setRGB(0,150,0);
      }
      if((ledmatris[k][2]==0)){
        leds3[k].setRGB(0,0,0);
      }else if((ledmatris[k][2]==1)){
        leds3[k].setRGB(50,0,0);
      }else if((ledmatris[k][2]==2)){
        leds3[k].setRGB(0,150,0);
      }
      if((ledmatris[k][3]= =0)){
        leds4[k].setRGB(0,0,0);
      }else if((ledmatris[k][3]==1)){
        leds4[k].setRGB(50,0,0);
      }else if((ledmatris[k][3]==2)){
        leds4[k].setRGB(0,150,0);
      }
      if((ledmatris[k][4]==0)){
        leds5[k].setRGB(0,0,0);
      }else if((ledmatris[k][4]==1)){
        leds5[k].setRGB(50,0,0);
      }else if((ledmatris[k][4]==2)){
        leds5[k].setRGB(0,150,0);
      }
      
    }
  i++;
  FastLED.show();
  delay(1000);
}

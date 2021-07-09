//const uint8_t gu8ListPin[]={0,1,2,3,4,5,6,7,8,9,10};
//#define PIN_LED_A  (2)
//#define PIN_LED_B  (3)

#define PIN_PHTR_A  (7)
#define PIN_PHTR_B  (8)

#define PIN_TRIGGER_PULSE  (9)
#define PIN_LED_SEND_PULSE  (10)

uint8_t gu8FlagOffLeft=0;
uint8_t gu8FlagOffRight=0;
uint8_t gu8StatePrev=0;
float gfSumTrigger = 0;
uint8_t gu8FlagTriggerOn = 0;
uint64_t gulTimeMilliPrev;

void setup() {
  Serial.begin(115200);

//  pinMode(PIN_LED_A,OUTPUT);
//  pinMode(PIN_LED_B,OUTPUT);

  pinMode(PIN_PHTR_A,INPUT);
  pinMode(PIN_PHTR_B,INPUT);

  pinMode(PIN_TRIGGER_PULSE,OUTPUT);

  gu8FlagOffLeft = 0;
  gu8FlagOffRight = 0;
  gu8StatePrev = 0;
  gulTimeMilliPrev =millis();
  gu8FlagTriggerOn =0;

}

#define VAL_THRESH_LEFT_A (600)
#define VAL_THRESH_RIGHT_B (600)

void loop() {

//  digitalWrite(PIN_LED_A,HIGH);
//  delay(1);
  uint16_t uiphtrA=analogRead(PIN_PHTR_A);
//  digitalWrite(PIN_LED_A,LOW);


//  digitalWrite(PIN_LED_B,HIGH);
//  delay(1);
  uint16_t uiphtrB=analogRead(PIN_PHTR_B);
//  digitalWrite(PIN_LED_B,LOW);

  gu8FlagOffLeft = uiphtrA < VAL_THRESH_LEFT_A;
  gu8FlagOffRight = uiphtrB < VAL_THRESH_RIGHT_B;
  
  uint8_t u8StateCurr ;
  u8StateCurr = gu8FlagOffLeft*gu8FlagOffRight;  // 1: standing
  u8StateCurr += gu8FlagOffLeft*((~gu8FlagOffRight)&1)*2; // 2: right knee up
  u8StateCurr += ((~gu8FlagOffLeft)&1)*gu8FlagOffRight*3; // 3: left knee up 
  u8StateCurr += ((~gu8FlagOffLeft)&1)*((~gu8FlagOffRight)&1)*4; //4: jump

  if(gu8StatePrev != u8StateCurr){
    gfSumTrigger += (u8StateCurr==2)*0.5;
    gfSumTrigger += (u8StateCurr==3)*0.5;

    gu8StatePrev = u8StateCurr;
  }

  
  if(gfSumTrigger >= 1.0 )
  {
    digitalWrite(PIN_LED_SEND_PULSE,1);
    digitalWrite(PIN_TRIGGER_PULSE,1);
    gu8FlagTriggerOn = 1;
    gulTimeMilliPrev =millis();
    gfSumTrigger =0;
  }

  Serial.print("uiphtrA= ");
  Serial.print(uiphtrA);
  Serial.print("\tuiphtrB= ");
  Serial.print(uiphtrB);

  Serial.print("\tu8StateCurr= ");
  Serial.print(u8StateCurr);
  Serial.print("\tgfSumTrigger= ");
  Serial.print(gfSumTrigger);
  Serial.print("\tgfSumTrigger= ");
  Serial.print(gfSumTrigger);

  Serial.println("");

  if(gu8FlagTriggerOn&&((millis()-gulTimeMilliPrev)> 2)){
    digitalWrite(PIN_LED_SEND_PULSE,0);
    digitalWrite(PIN_TRIGGER_PULSE,0);
    gu8FlagTriggerOn=0;
  }


  //delay(500);
  //digitalWrite(PIN_LED_A,LOW);
  //digitalWrite(PIN_LED_B,LOW);
  //delay(500);

}

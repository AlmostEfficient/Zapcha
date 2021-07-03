int pinOne = 8;
int pinTwo = 9;
int LEDpin = 13;

void setup(){
    Serial.begin(9600);
}

void loop(){
    // data = analogRead(analogPin); 
    // Serial.println(data);

    if(Serial.available()> 0){
        userInput = Serial.read();
        if (userInput == 'g'){
            data = analogRead(analogPin);
            Serial.println(data);
        }
    }
}

String r;

void setup(){
    Serial.begin(9600);
}

void loop(){
    if(Serial.available()){         
        r = (Serial.readString());
        Serial.println(r);
        if (r.startsWith("CMD"))
        {
            Serial.print("Received command: ");
            Serial.println(r);
            String pin = getValue(r, ' ', 1);
            String val = getValue(r, ' ', 2);

            int pinint = pin.toInt();
            int valint = val.toInt();

            pinMode(pinint, OUTPUT);
            digitalWrite(pinint, valint);
        } else {
          Serial.print("Commande inconnue: ");
            Serial.println(r);      
        }
    }
}

// https://arduino.stackexchange.com/a/1237s
String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}


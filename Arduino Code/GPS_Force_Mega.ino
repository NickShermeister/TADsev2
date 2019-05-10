#include <gSoftSerial.h>
#include <SD.h>

#define RX_PIN    14
#define TX_PIN    15
#define SD_CHIP_SELECT 10

#define SYNC_PERIOD    .1L*60L*1000L    // 5 minutes between calls to flush()
#define ss Serial3
File logfile;
#include "HX711.h"


// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 22;
const int LOADCELL_SCK_PIN = 23;


HX711 scale;




String readString; //main captured String 
String speed1;
String type;
String fix;

int ind; // , locations
int ind1;
int ind2;
int ind3;
int ind4;
int date_ind;
int date_ind1;

long ms;

void setup()
{
  Serial.begin(115200);
  Serial3.begin(9600);   // serial port 3
  Serial.print(F("\nHello\n"));
  Serial3.println(F("$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28"));     // RMC and GGA
  //ss.listen();
  
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(2280.f);                      // this value is obtained by calibrating the scale with known weights; see the README for details
  scale.tare();
  
  
  Serial.println(F("Type any char to start logging."));
  Serial.println(F("\nEchoing to screen in the meantime:"));
  delay(1000);
//  while (!Serial.available()) {
//    if (ss.available()) {
//      char c = ss.read();
//      if (c == '\r') {                  // end of line detected
//      Serial.write(", millis = ");      // add something before the CRLF
//      Serial.print(millis());
//      Serial.println();                 // CRLF
//    } else if (c == '\n') {
//      // ignore the newline since it's printed after receiving CR
//    } else
//      Serial.write(c);
//    }
//  }
  Serial.read();    // flush input buffer

  Serial.print(F("\n\nInitializing SD card..."));
  if (!SD.begin(10, 11, 12, 13)) {
    Serial.println(F("Card init. failed!"));
    while (true) {}
  }
  Serial.println(F("done."));
  
  Serial.print(F("Opening file..."));
  char filename[15];
  strcpy(filename, "GPSLOG00.CSV");
  for (uint8_t i = 0; i < 100; i++) {
    filename[6] = '0' + i/10;
    filename[7] = '0' + i%10;
    if (!SD.exists(filename)) {
      break;
    }
  }

  logfile = SD.open(filename, FILE_WRITE);
  if(!logfile) {
    Serial.print(F("Couldnt create ")); 
    Serial.println(filename);
    while (true) {}
  }
  Serial.print(F(" Writing to ")); 
  Serial.println(filename);
  logfile.print("Time,");
  logfile.print("Pace,");
  logfile.println("Pull");
  logfile.flush();
  Serial.println(F("Type any character to close the file."));
  ms = SYNC_PERIOD;
}

bool name_flag = false;

void loop()
{



  if (ss.available()) {
    char c = ss.read();
      if (c == '\r') {                  // end of line detected
      ind1 = readString.indexOf(',');  //finds location of first ,
      type = readString.substring(0, ind1);   //captures first data String
      

      
      if (type.equals("$GPRMC")){
      if (name_flag == false){
        date_ind = 
      }
      ind = readString.indexOf(',',15);
      ind1 = readString.indexOf(',',ind + 1);
      fix = readString.substring(ind + 1, ind1);
          if (fix.equals("A")){
              logfile.print(millis());
              logfile.print(",");
              ind2 = readString.indexOf(',', 44);   //finds location of second ,
              //Serial.print(ind2);
              ind3 = readString.indexOf(',', 47);   //finds location of second ,
              //Serial.print(ind3);
              speed1 = readString.substring(ind2+1, ind3+1);   //captures second data String
              //Serial.println(speed1);
              logfile.print(speed1);
        //      logfile.write(", millis = ");     // add something before the CRLF
        //      logfile.print(millis());
               //Serial.print(scale_avg);
              logfile.println(scale.get_units(),1);
        
    
          }
         else{
            //Serial.println("No Fix");
            //logfile.println(",");
          }
       
      }
      readString=""; //clears variable for new input
      speed1="";
      }else if (c == '\n') {
      // ignore the newline since it's printed after receiving '\r'
    } else{
      readString += c; //makes the string readString
      //logfile.write(c); 
       }
       


  }
  if (millis() > ms) {
    logfile.flush();
    ms += SYNC_PERIOD;  // 5 minutes;
  }
  
  if (Serial.available()) {
    logfile.close();
    Serial.println(F("\nFile closed."));
    while (1) {}
  }
}

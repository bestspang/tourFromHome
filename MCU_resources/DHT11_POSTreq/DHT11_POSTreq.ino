#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Wire.h>
#include <DHT.h>
#include <DHT_U.h>



#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

// SSID & Password
//const char* ssid = "Abbok Design2.4G";
//const char* password = "INDA2019"; 
const char* ssid = "TP-LINK_F5BC40";
const char* password = "22278456"; 

const char* ssid2 = "Abbok Design2.4G";
const char* password2 = "INDA2019"; 

//Webapp Name 'bplinebot.herokuapp.com/weather'
const char* serverName = "https://www.idayx.com/api";
const char* sha = "26:9D:4B:6C:EC:24:88:E0:0F:D9:75:8D:BF:88:35:AA:7B:F4:FB:5C";


String apiKeyValue = "kndOFSoiVnSvOEfef7sEFV78s65";
String deviceModel = "A01";
String sensorName = "DHT11";
String sensorLocation = "Abbok";

// DHT Sensor
uint8_t DHTPin = D2; 
               
// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);                

float TempCstat;
float TempFstat;
float HumidityStat;
int wifi2 = 0;
 
void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(DHTPin, INPUT);
  dht.begin();              

  Serial.println("Connecting to ");
  Serial.println(ssid);

  
  WiFi.begin(ssid, password);
  //check wi-fi is connected to wi-fi network
  int var = 0;
  while (WiFi.status() != WL_CONNECTED && var <= 10) {
  if (var == 10) {
    wifi2 = 1;
  }
  delay(1000);
  Serial.print(".");
  var++;
  }
  
  if (wifi2 == 1) {
    Serial.print("Try connecting 2nd wifi!");
    //connect to your local wi-fi network
    WiFi.begin(ssid2, password2);
    //check wi-fi is connected to wi-fi network
    while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    }
  }

  
  
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

  /*
  bool status = dht.begin(0x76);
  if (!status) {
    Serial.println("Could not find a valid DHT11 sensor, check wiring or change I2C address!");
    while (1);
  }*/

}
void loop() {
  //Check WiFi connection status
  if(WiFi.status() == WL_CONNECTED){
    //HTTPClient http;
    HTTPClient http;
    
    http.begin(serverName, sha);
    
    //content-type header
    //http.addHeader("Content-Type", "text/plain");
    http.addHeader("Content-Type", "application/json"); //JSON
    //http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    // Prepare your HTTP POST request data
    String httpRequestData = handle_requestJson(apiKeyValue, sensorName, sensorLocation);
    Serial.print("httpRequestData: ");
    Serial.println(httpRequestData);

    // Send HTTP POST request
    //int httpResponseCode = http.POST("Hello, World!");
    //int httpResponseCode = http.POST(httpRequestData);
    int httpResponseCode = http.POST(httpRequestData);
        
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  //Send an HTTP POST request every 2 seconds
  delay(2000);  
}

String handle_request(String apiKeyValue, String sensorName,String sensorLocation) {
  String RequestData = "";
  TempCstat = dht.readTemperature(); // Gets the values of the temperature
  TempFstat = (TempCstat * 9/5) + 32; // Gets the values of the temperature 
  HumidityStat = dht.readHumidity(); // Gets the values of the humidity
  RequestData += "api_key=" + apiKeyValue + "&sensor=" + sensorName
                          + "&location=" + sensorLocation + "&value1=" + (float)TempCstat
                          + "&value2=" + (float)HumidityStat + "";
  return RequestData;
}

String handle_requestJson(String apiKeyValue, String sensorName,String sensorLocation) {
  String RequestData = "";
  TempCstat = dht.readTemperature(); // Gets the values of the temperature
  TempFstat = (TempCstat * 9/5) + 32; // Gets the values of the temperature 
  HumidityStat = dht.readHumidity(); // Gets the values of the humidity
  RequestData += "{\"name\":\"" + sensorName +
                 "\",\"model\":\"" + deviceModel + 
                 "\",\"temp\":\"" + (float)TempCstat + 
                 "\",\"humid\":\"" + (float)HumidityStat + 
                 "\",\"api\":\"" + apiKeyValue + 
                 "\"}";
  return RequestData;
}

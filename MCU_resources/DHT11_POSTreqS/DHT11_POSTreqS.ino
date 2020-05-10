#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h> 
#include <Wire.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTTYPE DHT11
 
/* WIFI */
const char *ssid = "TP-LINK_F5BC40";
const char *password = "22278456";
String apiKeyValue = "kndOFSoiVnSvOEfef7sEFV78s65";
String sensorName = "DHT11";
String sensorLocation = "Abbok";

// DHT Sensor
uint8_t DHTPin = D2; 

// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);

float TempCstat;
float TempFstat;
float HumidityStat;

// plantly-restful.herokuapp.com/api
const char *host = "plantly-restful.herokuapp.com/api";
const char *endpoint = "/post";
const int httpsPort = 80;  //HTTPS= 443 and HTTP = 80
 
//SHA1 finger print
const char fingerprint[] PROGMEM = "08 3B 71 72 02 43 6E CA ED 42 86 93 BA 7E DF 81 C4 BC 62 30";
 
void setup() {
  delay(1000);
  Serial.begin(115200);
  //DHT11
  pinMode(DHTPin, INPUT);
  dht.begin(); 
  
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  
  WiFi.begin(ssid, password); //Connect to your WiFi router
  Serial.println("");
 
  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  //If connection successful show IP address
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP
}

void loop() {
  WiFiClientSecure httpsClient;    //Declare object of class WiFiClient
 
  Serial.println(host);
 
  Serial.printf("Using fingerprint '%s'\n", fingerprint);
  httpsClient.setFingerprint(fingerprint);
  httpsClient.setTimeout(15000); // 15 Seconds
  delay(1000);
  
  Serial.print("HTTPS Connecting");
  int r=0; //retry counter
  while((!httpsClient.connect(host, httpsPort)) && (r < 30)){
      delay(100);
      Serial.print(".");
      r++;
  }
  if(r==30) {
    Serial.println("Connection failed");
  }
  else {
    Serial.println("Connected to web");
  }
  
  String getData, Link;
  // "say=Hi&to=Mom"
  String httpRequestData = handle_requestJson(apiKeyValue, sensorName, sensorLocation);
  int len = httpRequestData.length();
  //POST Data
  Link = endpoint;
  Serial.print("httpRequestData: ");
  Serial.println(httpRequestData);
  Serial.print("Lenght: ");
  Serial.println(len);
 
  Serial.print("requesting URL: ");
  Serial.println(host);
  /*
   POST /post HTTP/1.1
   Host: postman-echo.com
   Content-Type: application/x-www-form-urlencoded
   Content-Length: 13
  
   say=Hi&to=Mom
    
   */
 
  httpsClient.print(String("POST ") + Link + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Content-Type: application/json"+ "\r\n" +
               "Content-Length: "+ len + "\r\n\r\n" +
               httpRequestData + "\r\n" +
               "Connection: close\r\n\r\n");
 
  Serial.println("request sent");
                  
  while (httpsClient.connected()) {
    String line = httpsClient.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
 
  Serial.println("reply was:");
  Serial.println("==========");
  String line;
  while(httpsClient.available()){        
    line = httpsClient.readStringUntil('\n');  //Read Line by Line
    Serial.println(line); //Print response
  }
  Serial.println("==========");
  Serial.println("closing connection");
    
  delay(5000);  //POST Data at every 5 seconds
}

String handle_requestJson(String apiKeyValue, String sensorName,String sensorLocation) {
  String RequestData = "";
  TempCstat = dht.readTemperature(); // Gets the values of the temperature
  TempFstat = (TempCstat * 9/5) + 32; // Gets the values of the temperature 
  HumidityStat = dht.readHumidity(); // Gets the values of the humidity
  RequestData += "{\"api_key\":\"" + apiKeyValue + "\",\"sensorName\":\"" + sensorName + "\",\"sensorLocation\":\"" +
                sensorLocation+"\",\"temp\":\"" + (float)TempCstat + "\",\"Humidity\":\"" + (float)HumidityStat + "\"}";
  return RequestData;
}

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

WiFiUDP udp;

#define LED_PIN 2

int connectionAttempts = 0;
const int maxConnectionAttempts = 100;

bool has_been_connected = false;

void wifi_setup() {
  Serial.print("\nConnecting to ");
  Serial.println(config.ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(config.ssid, config.password);
  pinMode(LED_PIN,OUTPUT);
  digitalWrite(LED_PIN,HIGH);
  wifi_check_and_connect();
  
}


void wifi_check_and_connect() {

  while (WiFi.status() != WL_CONNECTED) {

//    Serial.println(WiFi.status());
    
    if (connectionAttempts <= maxConnectionAttempts) {
        Serial.print(".");
//        Serial.println(connectionAttempts);
        connectionAttempts++;
        delay(200);
        
    }
    else {
      digitalWrite(LED_PIN,HIGH);
      WiFi.disconnect();
      Serial.print("\nConnecting to ");
      Serial.println(config.ssid);
      WiFi.mode(WIFI_STA);
      WiFi.begin(config.ssid, config.password);
      connectionAttempts = 0;
      has_been_connected = false;
    }
  }

  if (!has_been_connected){

      digitalWrite(LED_PIN,LOW);
      
      Serial.println("");
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
  
      has_been_connected = true;
  }
}

void wifi_send_UDP_packet(String packet) {
  // Check Wi-Fi connection and reconnect if necessary
  wifi_check_and_connect();

  // Send UDP packet
  int udpServerPort = atoi(config.serverPort);
  udp.beginPacket(config.serverIP, udpServerPort);

  udp.print(millis());
  udp.print(":");
  udp.print(packet);
  
  udp.endPacket();
}

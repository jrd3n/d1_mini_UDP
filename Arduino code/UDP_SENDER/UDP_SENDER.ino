
struct Config {
  char ssid[32];
  char password[32];
  char serverIP[16];
  char serverPort[16];
};

Config config;

void setup(){
  
  Serial.begin(9600);

  config_setup();
  
  wifi_setup();
  
}

void loop(){


//  Serial.println("here");
//  
  wifi_send_UDP_packet("Hello");
  
//  delay(1000);/
  
}

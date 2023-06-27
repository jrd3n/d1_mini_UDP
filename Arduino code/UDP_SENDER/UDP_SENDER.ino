
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

  ADC_setup();

//  pinMode(ANALOG_PIN,INPUT);/
  
}

void loop(){

//  Serial.println("here");

  wifi_send_UDP_packet(String(ADC_Reading()));
  
  delay(3);// a delay is needed because the cashe gets saturated going too fast
  
}

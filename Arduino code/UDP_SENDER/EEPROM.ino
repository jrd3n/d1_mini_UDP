#include <FS.h>
#include <ArduinoJson.h>

#define CONFIG_FILE "/config.json"

#define CONFIG_PIN 14 // this is pin 5

String user_input;

void config_setup() {
  SPIFFS.begin();
  loadConfig();

  pinMode(CONFIG_PIN, INPUT_PULLUP);

  unsigned long startTime = millis(); // Store the current time

  while (!Serial && millis() - startTime < 5000) {
    // Wait for serial connection or timeout
  }
  
  if (!digitalRead(CONFIG_PIN)) {
    Serial.println("");
    print_header();
    while (true) {

      if (Serial.available()) {
        user_input = Serial.readString(); // Read the input as a string
        user_input.trim(); // Remove leading and trailing whitespaces
  
        update_parameter("ssid", config.ssid, sizeof(config.ssid));
        update_parameter("pass", config.password, sizeof(config.password));
        update_parameter("ip", config.serverIP, sizeof(config.serverIP));
        update_parameter("port", config.serverPort, sizeof(config.serverPort));
  
        if (user_input == "q" || user_input == "exit") {
          return;
        }
      }
    }
  }
}

void print_header() {
  loadConfig();

  Serial.println("Please type one of the following phases to change one of the parameters:");
  Serial.print("\tssid\tto change SSID \t\t\t("); Serial.print(config.ssid); Serial.println(")");
  Serial.print("\tpass\tto change Wifi password \t("); Serial.print(config.password); Serial.println(")");
  Serial.print("\tip\tto change serverIP\t\t("); Serial.print(config.serverIP); Serial.println(")");
  Serial.print("\tport\tto change serverPort\t\t("); Serial.print(config.serverPort); Serial.println(")");
  Serial.println("\texit\tto continue");
}

void update_parameter(String activation_phase, char* parameter, size_t parameterSize) {
  if (user_input.equals(activation_phase)) {
    Serial.print("Enter new value for ");
    Serial.print(activation_phase);
    Serial.println(": ");
  
    while (!Serial.available()) {
      // Wait until new input is available
    }
  
    String newValue = Serial.readString(); // Read the new value as a string
    newValue.trim(); // Remove leading and trailing whitespaces
  
    // Truncate the new value if it exceeds the maximum length
    newValue = newValue.substring(0, parameterSize - 1);
  
    // Copy the new value to the respective array
    newValue.toCharArray(parameter, parameterSize);
  
    Serial.print(activation_phase);
    Serial.print(" updated with : ");
    Serial.println(parameter);
  
    saveConfig();
    print_header();
    
  }
}


void loadConfig() {
  File configFile = SPIFFS.open(CONFIG_FILE, "r");
  if (configFile) {
    size_t size = configFile.size();
    std::unique_ptr<char[]> buf(new char[size]);
    configFile.readBytes(buf.get(), size);

    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, buf.get());
    if (!error) {
      strlcpy(config.ssid, doc["ssid"] | "", sizeof(config.ssid));
      strlcpy(config.password, doc["password"] | "", sizeof(config.password));
      strlcpy(config.serverIP, doc["serverIP"] | "", sizeof(config.serverIP));
      strlcpy(config.serverPort, doc["serverPort"] | "", sizeof(config.serverPort));  
    }
    configFile.close();
  }
}

void saveConfig() {
  File configFile = SPIFFS.open(CONFIG_FILE, "w");
  if (configFile) {
    StaticJsonDocument<256> doc;
    Serial.println("here");
    Serial.println(config.ssid);
    doc["ssid"] = config.ssid;
    doc["password"] = config.password;
    doc["serverIP"] = config.serverIP;
    doc["serverPort"] = config.serverPort;

    serializeJson(doc, configFile);
    configFile.close();
  }
}

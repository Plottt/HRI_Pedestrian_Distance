#include <Adafruit_NeoPixel.h>

// Pin and LED configuration
#define LED_PIN    6
#define LED_COUNT 60

// NeoPixel strip object
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGB + NEO_KHZ800);

// Define Modes
enum Mode {
  MODE_OFF,
  MODE_CONSTANT_COLOR,
  MODE_BLINKING_COLOR,
  MODE_DYNAMIC_BLINKING
};

Mode currentMode = MODE_OFF;

// Predefined colors for each mode
uint32_t color1 = strip.Color(10, 30, 39);   // Constant Color: Blue
uint32_t color2 = strip.Color(255, 0, 0);   // Blinking Color: Red
uint32_t color3 = strip.Color(255, 0, 0);   // Dynamic Blinking Color: Green

// Blinking speed for MODE_BLINKING_COLOR
unsigned long blinkSpeed = 400;             // 500 ms

// Dynamic Blinking parameters for MODE_DYNAMIC_BLINKING
uint8_t blinkRate = 5;                      // Default blinking rate (1-10)
unsigned long minSpeed = 100;               // Minimum blink speed in ms
unsigned long maxSpeed = 1000;              // Maximum blink speed in ms
unsigned long currentBlinkSpeed = 400;      // Initial blink speed

// Blinking control variables
bool isBlinkOn = false;
unsigned long previousMillis = 0;

// Function prototypes
void setModeOff();
void setModeConstantColor();
void setModeBlinkingColor();
void setModeDynamicBlinking();
void setAllPixels(uint32_t color);
void handleBlinkingColor();
void handleDynamicBlinking();

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.show();
  strip.setBrightness(255);

  Serial.println("NeoPixel Controller Initialized with predefined modes.");
  Serial.println("Available commands:");
  Serial.println("a - Turn off LEDs");
  Serial.println("b - Constant color mode (blue)");
  Serial.println("c - Blinking color mode (red)");
  Serial.println("d - Dynamic blinking mode (red)");
  Serial.println("dX - Set blink rate for mode 'd' (X from 1 to 10)");
}

void loop() {
  // Check for mode change or blink rate adjustment command
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() > 0) {
      char mode = input.charAt(0);

      if (mode == 'd' && input.length() > 1) {
        // Set blink rate for Dynamic Blinking Mode
        int rate = input.substring(1).toInt();
        if (rate >= 1 && rate <= 10) {
          blinkRate = rate;
          Serial.print("Dynamic Blinking Rate set to: ");
          Serial.println(blinkRate);
        } else {
          Serial.println("Invalid rate. Please enter a rate between 1 and 10.");
        }
      } else {
        // Change mode based on single-character input
        switch (mode) {
          case 'a': currentMode = MODE_OFF; Serial.println("Mode 'a' - LEDs OFF"); break;
          case 'b': currentMode = MODE_CONSTANT_COLOR; Serial.println("Mode 'b' - Constant Blue"); break;
          case 'c': currentMode = MODE_BLINKING_COLOR; Serial.println("Mode 'c' - Blinking Red"); break;
          case 'd': currentMode = MODE_DYNAMIC_BLINKING; Serial.println("Mode 'd' - Dynamic Blinking Green"); break;
          default: Serial.println("Unknown command. Use 'a', 'b', 'c', or 'dX' where X is blink rate 1-10."); break;
        }
      }
    }
  }

  // Execute the current mode
  switch (currentMode) {
    case MODE_OFF: setModeOff(); break;
    case MODE_CONSTANT_COLOR: setModeConstantColor(); break;
    case MODE_BLINKING_COLOR: handleBlinkingColor(); break;
    case MODE_DYNAMIC_BLINKING: handleDynamicBlinking(); break;
  }
}

// Turn off all LEDs
void setModeOff() {
  strip.clear();
  strip.show();
}

// Set all LEDs to constant blue color
void setModeConstantColor() {
  setAllPixels(color1);
}

// Blinking red color mode
void handleBlinkingColor() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= blinkSpeed) {
    previousMillis = currentMillis;
    isBlinkOn = !isBlinkOn;
    setAllPixels(isBlinkOn ? color2 : strip.Color(0, 0, 0));
  }
}

// Dynamic green blinking mode with varying speed
void handleDynamicBlinking() {
  // Calculate blink speed based on blinkRate
  currentBlinkSpeed = map(blinkRate, 1, 10, maxSpeed, minSpeed);
  unsigned long currentMillis = millis();
  Serial.println(currentBlinkSpeed);
  if (currentMillis - previousMillis >= currentBlinkSpeed) {
    previousMillis = currentMillis;
    isBlinkOn = !isBlinkOn;
    setAllPixels(isBlinkOn ? color3 : strip.Color(0, 0, 0));
  }
}

// Helper to set all pixels to a given color
void setAllPixels(uint32_t color) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

import serial
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

# Serial communication setup
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Use the appropriate serial port
time.sleep(2)  # Allow time for the connection to be established

# DHT11 sensor setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # BCM numbering

# Buzzer setup
BUZZER_PIN = 18  # BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def control_buzzer(value):
    GPIO.output(BUZZER_PIN, value)

try:
    while True:
        humidity, temperature = read_sensor_data()

        if humidity is not None and temperature is not None:
            print(f"Temperature={temperature:.2f}°C Humidity={humidity:.2f}%")

            if temperature > 25.0 and humidity > 60:
                ser.write(b'1')  # Send '1' to Arduino to turn on the buzzer
                control_buzzer(GPIO.HIGH)
            else:
                ser.write(b'0')  # Send '0' to Arduino to turn off the buzzer
                control_buzzer(GPIO.LOW)

        time.sleep(5)  # Read sensor data and update buzzer every 5 seconds

except KeyboardInterrupt:
    ser.close()
    GPIO.cleanup()

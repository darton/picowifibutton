import urequests
import network
import usocket as socket
import machine
import time
from utime import sleep_ms, sleep
import rp2

# Configuration
WIFI_SSID = "homewifi"
WIFI_PASSWORD = "homewifipasswd"

SHELLY_API_CMD = "http://192.168.1.40/relay/0?turn=toggle"

led = machine.Pin("LED", machine.Pin.OUT)
led.off()


def led_blinking(on_time, off_time, number_of_blinks):
    for n in range(number_of_blinks):
        led.toggle()
        sleep_ms(on_time)
        led.toggle()
        sleep_ms(off_time)    
    

def connect_wifi():
    rp2.country('PL')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            led_blinking(100,100,2)
    print("Connected to Wi-Fi, IP:", wlan.ifconfig()[0])



# Funkcja do wysyłania żądań HTTP
def send_http_request(url):
    try:
        response = urequests.get(url)
        print("HTTP Response:", response.status_code)
        response.close()
    except Exception as e:
        print("Error:", e)



def main():
    # 1. Turn on Wi-Fi, read data, send to Redis
    connect_wifi()
    # Główna logika
    send_http_request(SHELLY_API_CMD)

 
if __name__ == "__main__":
    main()


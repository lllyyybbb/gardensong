 main.py — gardensong sensor node (Adafruit Feather HUZZAH ESP8266)
# MicroPython runs this automatically on power-up. It joins WiFi, reads the
# DHT11, POSTs the reading to the Pi, waits, and repeats.
#Feather HUZZAH flashed with MicroPython(ESP8266) via Thonny
# Code generated with Claude
#
# LED status (onboard blue LED, next to the antenna):
#   1 blink  = reading posted OK
#   2 blinks = Pi refused the reading
#   3 blinks = sensor read failed
#   4 blinks = couldn't reach the Pi
#   5 blinks = WiFi wouldn't connect
#   6 blinks = unexpected error

import network, socket, time, dht, machine

# ---- FILL THESE IN --------------------------------------------------
SSID       = "YOUR NETWORK HERE"       # the IoT network the board joined
PASSWORD   = "YOUR NETWORK PASSWORD HERE"
PI_IP      = "YOUR PI IP HERE"            # the Pi's PINNED IP (verify: hostname -I on the Pi)
PI_PORT    = 5000 #YOUR PI PORT HERE
POST_EVERY = 600                        # seconds between readings (600 = every 10 min)
DHT_PIN    = 14
# ---------------------------------------------------------------------

led = machine.Pin(2, machine.Pin.OUT)   # onboard blue LED (active-low: 0 = on)
led.value(1)                            # start off
sensor = dht.DHT11(machine.Pin(DHT_PIN))
wlan = network.WLAN(network.STA_IF)


def blink(n=1, on=0.08, off=0.15):
    for _ in range(n):
        led.value(0); time.sleep(on)
        led.value(1); time.sleep(off)


def wifi_connect(timeout=20):
    wlan.active(True)
    if wlan.isconnected():
        return True
    wlan.connect(SSID, PASSWORD)
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            return False
        time.sleep(0.5)
    return True


def read_sensor(tries=4):
    for _ in range(tries):
        try:
            sensor.measure()
            return sensor.temperature(), sensor.humidity()
        except OSError:
            time.sleep(2)   # DHT11 flubs the first poll; retry
    return None


def post(temp, humidity):
    body = '{"temperature": %d, "humidity": %d}' % (temp, humidity)
    req = ("POST /data HTTP/1.0\r\nHost: %s\r\n"
           "Content-Type: application/json\r\n"
           "Content-Length: %d\r\nConnection: close\r\n\r\n%s"
           % (PI_IP, len(body), body))
    s = socket.socket()
    s.settimeout(10)
    try:
        s.connect((PI_IP, PI_PORT))
        s.send(bytes(req, "utf-8"))
        return b"200" in s.recv(64)
    finally:
        s.close()


def cycle():
    if not wifi_connect():
        print("wifi: failed"); blink(5); return
    reading = read_sensor()
    if reading is None:
        print("sensor: read failed"); blink(3); return
    temp, humidity = reading
    print("read:", temp, "C", humidity, "%")
    try:
        ok = post(temp, humidity)
        print("post:", "200 OK" if ok else "refused")
        blink(1 if ok else 2)
    except Exception as e:
        print("post error:", e); blink(4)


time.sleep(2)               # settle on boot
while True:
    try:
        cycle()
    except Exception as e:
        print("cycle error:", e); blink(6)
    time.sleep(POST_EVERY)

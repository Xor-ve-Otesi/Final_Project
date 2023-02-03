import socket
import network
import time
from machine import Pin, PWM, ADC

ssid = 'Galaxy A32AE20'
password = 'qgfb9519'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
ai = socket.getaddrinfo("192.168.61.141", 1234)
addr = ai[0][-1]

class Pico():

    def __init__(self) -> None:

        # TODO Pinleri degistir
        # LED
        self.green_led = [Pin(19, Pin.PULL_UP), Pin(21, Pin.PULL_UP), Pin(26, Pin.PULL_UP)]
        self.red_led = [Pin(28, Pin.PULL_UP), Pin(27, Pin.PULL_UP), Pin(20, Pin.PULL_UP)]

        # MOTOR 1
        self.ena_1 = PWM(Pin(0, Pin.OUT))
        self.ena_1.duty_u16(0)
        self.ena_1.freq(1000)
        self.in1_1 = Pin(1, Pin.OUT)
        self.in2_1 = Pin(2, Pin.OUT)

        # MOTOR 2
        self.ena_2 = PWM(Pin(5, Pin.OUT))
        self.ena_2.duty_u16(0)
        self.ena_2.freq(1000)
        self.in1_2 = Pin(3, Pin.OUT)
        self.in2_2 = Pin(4, Pin.OUT)

        #"""
        self.direction = 40
        self.speed1 = 0
        self.speed2 = 0
        self.role = 0

        self.cl = socket.socket()
        self.cl.connect(addr)
        old_data = ""

        while True:
            time.sleep(0.2)
            self.cl.send(str.encode("2"))
            data = self.cl.recv(1024).decode()

            if old_data != data:
                data = data.split(",")
                self.direction = int(data[0])
                self.speed1 = int(data[1])
                self.speed2 = int(data[2])
                self.role = int(data[3])
                if int(self.direction) == 90:
                    self.backward_1()
                    self.forward_2()
                    self.ena_1.duty_u16(int(self.speed1 / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed2 / 100 * 65536))
                    time.sleep(0.2)
                    self.stop_1()
                    self.stop_2()

                elif int(self.direction) == -90:
                    self.forward_1()
                    self.backward_2()
                    self.ena_1.duty_u16(int(self.speed1 / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed2 / 100 * 65536))
                    time.sleep(0.2)
                    self.stop_1()
                    self.stop_2()

                elif int(self.direction) == 0:
                    self.forward_1()
                    self.forward_2()
                    self.ena_1.duty_u16(int(self.speed1 / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed2 / 100 * 65536))
                    time.sleep(0.2)
                    self.stop_1()
                    self.stop_2()

                elif int(self.direction) == -1:
                    self.backward_1()
                    self.backward_2()
                    self.ena_1.duty_u16(int(self.speed1 / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed2 / 100 * 65536))
                    time.sleep(0.2)
                    self.stop_1()
                    self.stop_2()

                else:
                    self.stop_1()
                    self.stop_2()

                if self.role:
                    for led in self.green_led:
                        led.on()    
                    for led in self.green_red:
                        led.off()

                else:
                    for led in self.green_led:
                        led.off()    
                    for led in self.green_red:
                        led.on()

                old_data = data
    
        client_socket.close()
        #"""

    def stop_1(self):
        self.in1_1.value(0)
        self.in2_1.value(0)
        self.ena_1.duty_u16(0)
    
    def forward_1(self):
        self.in1_1.value(1)
        self.in2_1.value(0)

    def backward_1(self):
        self.in1_1.value(0)
        self.in2_1.value(1)

    def stop_2(self):
        self.in1_2.value(0)
        self.in2_2.value(0)
        self.ena_2.duty_u16(0)
    
    def forward_2(self):
        self.in1_2.value(1)
        self.in2_2.value(0)

    def backward_2(self):
        self.in1_2.value(0)
        self.in2_2.value(1)


if __name__ == '__main__':
    Pico()
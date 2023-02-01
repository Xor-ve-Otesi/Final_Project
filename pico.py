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
        self.green_led = Pin(1, Pin.OUT)
        self.red_led = Pin(2, Pin.OUT)

        # MOTOR 1
        self.ena_1 = PWM(Pin(2, Pin.OUT))
        self.ena_1.duty_u16(0)
        self.ena_1.freq(1000)
        self.in1_1 = Pin(4, Pin.OUT)
        self.in2_1 = Pin(5, Pin.OUT)

        # MOTOR 2
        self.ena_2 = PWM(Pin(2, Pin.OUT))
        self.ena_2.duty_u16(0)
        self.ena_2.freq(1000)
        self.in1_2 = Pin(4, Pin.OUT)
        self.in2_2 = Pin(5, Pin.OUT)

        #"""
        self.direction = 0
        self.speed = 0
        self.role = 0

        self.cl = socket.socket()
        self.cl.connect(addr)

        while True:
            time.sleep(0.2)
            self.cl.send(str.encode("2"))
            data = self.cl.recv(1024).decode()

            if old_data != data:
                data = data.split(",")
                self.direction = data[0]
                self.speed = data[1]
                self.role = data[2]

                if int(self.direction) == 90:
                    self.forward_1()
                    self.backward_2()
                    self.ena_1.duty_u16(int(self.speed / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed / 100 * 65536))

                elif int(self.direction) == -90:
                    self.backward_1()
                    self.forward_2()
                    self.ena_1.duty_u16(int(self.speed / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed / 100 * 65536))

                elif int(self.direction) == 0:
                    self.forward_1()
                    self.forward_2()
                    self.ena_1.duty_u16(int(self.speed / 100 * 65536))
                    self.ena_2.duty_u16(int(self.speed / 100 * 65536))

                if self.role:
                    self.green_led.value(1)
                    self.red_led.value(0)

                else:
                    self.green_led.value(0)
                    self.red_led.value(1)

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
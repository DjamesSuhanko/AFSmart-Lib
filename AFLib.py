from machine import I2C
from machine import Pin
from machine import ADC
from machine import reset

import onewire
import ds18x20
import time

class AFLib:
    def __init__(self):
        self.RELAY_PCF = 0x27

        self.DELAY_AN  = 20

        self.sda       = Pin(0)
        self.scl       = Pin(2)

        self.ON        = 1
        self.OFF       = 0
        self.INVERT    = 2

        self.buf       = bytearray(1)
        self.buf[0]    = 0

        self.i2cbus    = i2cbus = I2C(scl=self.scl,sda=self.sda)

        self.adc       = ADC(0)

        self.ow        = onewire.OneWire(Pin(12))
        self.ds        = ds18x20.DS18X20(self.ow)


    def relay(self,number,state):
        if number == 0 or number > 8:
            return

        """
        PCF8674
        0 1 2 3 4 5 6 7

        1 2 4 8 16 32 64
        """

        # incremental. escolhe o bit e soma
        if state == self.ON:
            self.buf[0] = int(self.buf[0])|(1<<int(number) - 1)

        #decrementa apenas o bit selecionado
        elif state == self.OFF:
            self.buf[0] = int(self.buf[0])&~(1<<int(number)-1)

        self.i2cbus.writeto(self.RELAY_PCF,self.buf)

    def status(self):
        #TODO: implement more info
        result = self.i2cbus.scan()

        print(" ")
        print('I2C addresses: ')
        addr = ""
        for address in result:
            print(hex(address))
            addr += str(hex(address)+",")
        addr = addr[:-1]

        print(" ")

        #nao funciona
        #print(self.i2cbus.readfrom(0x27, 255))

        print('Relay status : ', str(bin(self.buf[0]))[2:])

        temp = self.tempOneWire(10,20)

        return {"relays":str(bin(self.buf[0]))[2:],"i2c":addr,"temperature":temp}

    def analog(self,loop):
        means = 0
        for i in range(0,loop):
            means += self.adc.read()
            time.sleep_ms(self.DELAY_AN)

        means = means/loop
        return means

    def tempOneWire(self,loop,interval):
        roms = self.ds.scan()

        if len(roms) < 1:
            print('Devices found (yes/no): No ')
            print('Ckeck if device is connected. Aborting...')
            return

        print('Devices found (yes/no): Yes')

        temps = []
        for i in range(0,loop):
            print('temperatures: ', end='')
            self.ds.convert_temp()
            time.sleep_ms(interval)
            for rom in roms:
                print(self.ds.read_temp(rom),end='')
                temps.append(str(self.ds.read_temp(rom)))
            print()
            return temps[0] #temporario

    def uninstall(self):
        import os
        time.sleep_ms(20)
        print("Removing library...")
        os.remove('AFLib.py')
        print("Done.")

    def selfTest(self):
        print(" ")
        print(" Testing relays...")
        for i in range(1,8):
            print("relay ",i)
            self.relay(i,self.ON)
            time.sleep_ms(500)
            self.relay(i,self.OFF)

        print(" ")
        print("Reading OneWire bus...")
        self.tempOneWire(5,20)

        print(" ")
        print("Reading analog bus...")
        value = self.analog(5)
        print(value)

        print(" ")
        print("Status...")
        self.status()

    def reboot(self):
        reset()

    def led(self, state):
        if state == self.ON:
            self.buf[0] = int(self.buf[0]) | (1 << 7)

        # decrementa apenas o bit selecionado
        elif state == self.OFF:
            self.buf[0] = int(self.buf[0]) & ~(1 << 7)

        else:
            return

        self.i2cbus.writeto(self.RELAY_PCF, self.buf)
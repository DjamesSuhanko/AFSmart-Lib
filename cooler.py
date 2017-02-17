import AFLib
from time import sleep_ms
from time import ticks_ms
from time import ticks_diff

class Cooler:
    def __init__(self):
        self.af           = AFLib.AFLib()

        self.ALL          = 14
        self.COOLER_ONE   = 1
        self.COOLER_TWO   = 2
        self.FAN_TURBO    = 3
        self.PELTIER_UP   = 6
        self.PELTIER_DOWN = 5

        self.ON           = self.af.ON
        self.OFF          = self.af.OFF

    #os reles do AFSmart comecam em UP, baixar imediatamente
    def downAll(self):
        self.af.relay(1,self.af.OFF)

   #inicia um item escolhido entre as macros do init
    def start(self,choice):
        if choice == self.ALL:
            relays = [1,2,3,6,5]
            for i in relays:
                if i == 5:
                    acum = ticks_ms()
                    delta = 0
                    while delta > 10000:
                        delta = ticks_diff(time.ticks_ms(),acum)

                self.af.relay(i,self.af.ON)
                sleep_ms(10)

            self.af.relay(4,self.OFF)
            self.af.relay(7,self.OFF)
            return
        self.af.relay(choice,self.af.ON)

    #baixa um item escolhod entre as macros do init
    def stop(self, choice):
        self.af.relay(choice, self.af.OFF)

    #caso queira desligar por peltier
    def peltier_sink_side(self,state):
        self.af.relay(self.PELTIER_UP, state)

    def peltier_box_side(self, state):
        self.af.relay(self.PELTIER_DOWN, state)

    def fan_sink(self,state):
        self.af.relay(self.COOLER_ONE, state)

    def fan_box(self,state):
        self.af.relay(self.PELTIER_UP, state)

    def fan_turbo(self,state):
        self.af.relay(self.FAN_TURBO, state)

    def temperature(self,loop,interval):
        return self.af.tempOneWire(loop,interval)

    def help(self):
        print("Functions:")
        print("* downAll() - Turn off all relays")
        print("* start(choice) - turn on relay(s)")
        print("OPTIONS:\n\
        self.ALL\n\
        self.COOLER_ONE\n\
        self.COOLER_TWO\n\
        self.FAN_TURBO\n\
        self.PELTIER_UP\n\
        self.PELTIER_DOWN")
        print("* stop(choice) - same options above")
        print("* peltier_sink_side(state) - ON or OFF")
        print("* peltier_box_side(state)")
        print("* fan_sink(state)")
        print("* fan_box(state)")
        print("* fan_turbo(state)")
        print("* temperature(loop,interval) - times to means, delay")
        print("* uninstall() - remove the cooler library")
        print("* reboot() - reset machine, except status")

    def uninstall(self):
        import os
        os.remove("cooler.py")

    def reboot(self):
        from machine import reset
        reset()



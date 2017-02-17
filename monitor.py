import cooler
import time

cool = cooler.Cooler()

cool.start(cool.ALL)

OFF = 0
ON  = 1

system = OFF

while True:
    #pega 10 amostras com intervalo de 20ms entre cada pra fazer a media
    temp = cool.temperature(10,20)

    if temp > 26.5 and system == OFF:
        cool.start(cool.ALL)
        system = ON

    if temp < 24.5 and system == ON:
        cool.fan_box(cool.OFF)
        cool.fan_turbo(cool.OFF)
        cool.peltier_box_side(cool.OFF)

        #Agora espera dissipar o calor remanescente do peltier externo...
        acum  = time.ticks_ms()
        delta = 0
        #espera 20 segundos para desligar o segundo peltier
        while delta < 20000:
            delta = time.ticks_diff(time.ticks_ms(),acum)
        cool.peltier_sink_side(cool.OFF)

        #agora espera dissipar o calor do ultimo peltier antes de desligar a fan externa
        acum = time.ticks_ms()
        delta = 0
        while delta < 20000:
            delta = time.ticks_diff(time.ticks_ms(),acum)
        cool.fan_sink(cool.OFF)
        system = OFF
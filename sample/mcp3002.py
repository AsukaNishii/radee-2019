#!usr/bin/env python3
# -*- coding: utf-8 -*-

# mcp3002.py
# - wait_for_edge方式でSPI読み出しをするプログラム
#     ADCとして`MCP3002`を使用
#     データシート : http://akizukidenshi.com/download/ds/microchip/mcp3002.pdf
# - 使用するピン(BCM)
#     GPIO18 : 入力 割り込み(receiver)
#     GPIO17 : 出力 センサーのリセット(resetter)
#     GPIO27 : 出力 処理フラグ(flag)

import RPi.GPIO as GPIO
import spidev
import datetime

class Radee:
    def __init__(self, receiver_bcm=18, resetter_bcm=17, flag_bcm=27, \
                 ch_spi=0, timing_const=0.00002):
        self.receiver_bcm = receiver_bcm
        self.resetter_bcm = resetter_bcm
        self.flag_bcm     = flag_bcm
        self.ch_spi       = ch_spi
        self.timing_const = timing_const
        self.spi          = spidev.SpiDev()
        self.t            = time.time()
        self.voltage      = 0

    def gpio_setup(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(receiver_bcm, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(resetter_bcm, GPIO.OUT)
        GPIO.output(resetter_bcm, GPIO.LOW)

        GPIO.setup(flag_bcm, GPIO.OUT)
        GPIO.output(flag_bcm, GPIO.LOW)

    def spi_setup(self):
        spi.open(0, 0)
        spi.max_speed_hz = 1000000

    # 参考 : https://qiita.com/Zensa55/items/1a2779c24de20ee35af8
    def spi_read_qiita(self):
        command1 = 0xd | (ch_spi<<1)
        command1 <<= 3
        ret = spi.xfer2([command1,0,0])
        adcout = (ret[0]&0x3)<<8 | ret[1]
        return adcout

    def spi_read(self):
        tmp = spi.xfer2([0x68, 0x00])
        val = ((tmp[0] << 8) + tmp[1]) & 0x3ff
        return val

    def measure(self):
        GPIO.wait_for_edge(receiver_bcm, GPIO.RISING)
        time.sleep(timing_const)
        GPIO.output(flag_bcm, GPIO.HIGH)
        t = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        voltage = spi_read()
        GPIO.output(flag_bcm, GPIO.LOW)
        time.sleep(0.0003)
        GPIO.output(resetter_bcm, GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(resetter_bcm, GPIO.LOW)

    def print_data(self):
        print(f"time = {t}, voltage = {voltage}")

    def cleanup(self):
        spi.close()
        GPIO.cleanup()

if __name__ = "__main__":
    radee = Radee()

    radee.gpio_setup()
    radee.spi_setup()

    try:
        while True:
            radee.measure()
            radee.print_data()
    except KeyboardInterrupt:
        pass
    finally:
        radee.cleanup()

#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
radee2019/sample/demo_test_mcp3002.py

@2019, Kazuki IWANAGA

- wait_for_edge方式でSPI読み出しをするプログラム
    ADコンバータは`MCP3002`を想定
    データシート : http://akizukidenshi.com/download/ds/microchip/mcp3002.pdf
- 使用するピン(BCM)
    GPIO18 : 入力(receiver) 信号が来たことを知らせる割り込み信号を受信する
    GPIO17 : 出力(resetter) 読み出し終了後にセンサーのリセット信号を出力する
    GPIO27 : 出力(holder)     電圧を読み出しの間ホールドする信号を出力する
"""

# import RPi.GPIO as GPIO
# import spidev # https://pypi.org/project/spidev/
import datetime
import time
import random
import csv

class MCP3002:
    """
    MCP3002関連をまとめたクラス

    Attributes
    ----------
    spi_ch : int
        RaspberryPiのSPIのチャンネル番号(0か1のどちらか)
    spi : object
        spidevで提供されているオブジェクト
    """
    def __init__(self, spi_ch):
        """
        Constructor

        Parameters
        ----------
        spi_ch : int
            RaspberryPiのSPIのチャンネル番号(0か1のどちらか)
        """
        self.spi_ch       = spi_ch
        # self.spi          = spidev.SpiDev()

    def spi_setup(self):
        """
        SPIの初期化
        """
        print("RUN : spi_setup")
        # self.spi.open(0, 0)
        # self.spi.max_speed_hz = 1000000 # 10 MHz

    def spi_read(self):
        """
        SPIでADコンバータの出力を読み出す

        MCP3002の分解能は10bitだが, 8bitずつ送られてくるため結合が必要である
        これはxfer2で取得した2つの8bitのうち最初のものを8bit左へシフトすることで実現できる
        また, 最初の余分な6bitは0x3ff(2進数で0b1111111111)とのANDによって0にする

        参考 : http://tekitoh-memdhoi.info/views/745

        Returns
        -------
        val : int
            ADコンバータの出力値, すなわち測定電圧値[V]
        """
        print("RUN : spi_read")
        # tmp = self.spi.xfer2([0x68, 0x00]) # ch0なら0x68, ch1なら0x78
        # val = ((tmp[0] << 8) + tmp[1]) & 0x3ff
        return random.randint(1, 1023)

    # def spi_read_qiita(self):
    #     """
    #     SPI読み出しの予備(Qiitaで拾った)
    #     spi_readが動かない時に切り替える

    #     参考 : https://qiita.com/Zensa55/items/1a2779c24de20ee35af8

    #     Returns
    #     -------
    #     adcout : int
    #         ADコンバータの出力値, すなわち測定電圧値[V]
    #     """
    #     command1 = 0xd | (spi_ch<<1)
    #     command1 <<= 3
    #     ret = self.spi.xfer2([command1,0,0])
    #     adcout = (ret[0]&0x3)<<8 | ret[1]
    #     return adcout

    def spi_cleanup(self):
        """
        SPIの終了処理を行う
        """
        print("RUN : spi_cleanup")
        # self.spi.close()

class Radee(MCP3002):
    """
    Main Class
    MCP3002を継承

    Attributes
    ----------
    receiver_bcm : int, default 18
        割り込み信号を受信するGPIOピンのBCM番号
    resetter_bcm : int, default 17
        半導体センサーのリセット信号を出力するGPIOピンのBCM番号
    holder_bcm : int, default 27
        ホールド信号を出力するGPIOピンのBCM番号
    spi_ch : int
        RaspberryPiのSPIのチャンネル番号(0か1のどちらか)
    timing_const : float
        信号を受信してからガウシアンのピークに達するまでにかかる秒数[s]
    spi : object
        spidevで提供されているオブジェクト
    data : dict
        測定データ  (time, voltage)
            time : datetime
                測定時刻(%y-%m-%d %H:%M:%S)
            voltage : int
                測定電圧[V]

    See Also
    --------
    MCP3002 : MCP3002関連のクラス   
    """
    def __init__(self, receiver_bcm=18, resetter_bcm=17, holder_bcm=27, \
                 timing_const=0.00002, spi_ch=0):
        """
        Constructor

        Parameters
        ----------
        receiver_bcm : int, default 17
            割り込み信号を受信するGPIOピンのBCM番号
        resetter_bcm : int, default 18
            半導体センサーのリセット信号を出力するGPIOピンのBCM番号
        holder_bcm : int, default 27
            ホールド信号を出力するGPIOピンのBCM番号
        spi_ch : int
            RaspberryPiのSPIのチャンネル番号(0か1のどちらか)
        timing_const : float
            信号を受信してからガウシアンのピークに達するまでにかかる秒数[s]

        See Also
        --------
        MCP3002.__init__ : super().__init__で呼び出される
        """
        super().__init__(spi_ch)
        self.receiver_bcm = receiver_bcm
        self.resetter_bcm = resetter_bcm
        self.holder_bcm   = holder_bcm
        self.timing_const = timing_const
        self.data         = {"time": time.time(), "voltage": 0}

    def gpio_setup(self):
        """
        GPIOを初期化する
        """
        print("RUN : gpio_setup")
        # GPIO.setmode(GPIO.BCM)

        # GPIO.setup(self.receiver_bcm, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # GPIO.setup(self.resetter_bcm, GPIO.OUT)
        # GPIO.output(self.resetter_bcm, GPIO.LOW)

        # GPIO.setup(self.holder_bcm, GPIO.OUT)
        # GPIO.output(self.holder_bcm, GPIO.LOW)

    def measure(self):
        """
        測定を行う

        1. 割り込み信号を受信(GPIO.RISING)
        2. ガウシアン信号がピークになるまで待ってからホールド信号を出力(GPIO.HIGH)
        3. 時間の測定
        4. 電圧値の読み出し(self.spi_read)
        5. ホールド信号を止める(GPIO.LOW)
        6. リセット信号を出力(GPIO.HIGH)
        7. リセット信号を止める(GPIO.LOW)

        See Also
        --------
        MCP3002.spi_read : SPIでADコンバータの出力を取得する
        """
        time.sleep(1)
        print("RUN : measure")
        # GPIO.wait_for_edge(self.receiver_bcm, GPIO.RISING)
        # time.sleep(self.timing_const)

        # GPIO.output(self.holder_bcm, GPIO.HIGH)
        self.data["time"] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        self.data["voltage"] = self.spi_read()
        # GPIO.output(self.holder_bcm, GPIO.LOW)

        # time.sleep(0.0003) # 本当に必要か分からないので要検証
        # GPIO.output(self.resetter_bcm, GPIO.HIGH)
        # time.sleep(0.0005) # リセット信号を認識するのにかかる時間
        # GPIO.output(self.resetter_bcm, GPIO.LOW)

    def print_data(self):
        """
        現在保持している測定時刻と測定電圧を表示する
        """
        print("RUN : print_data")
        print("{time}, {voltage}".format(**self.data))

    def data2csv(self, filename):
        """
        現在保持している測定時刻と測定電圧をCSVファイルに書き込む

        Parameters
        ----------
        filename : string
            CSVファイル名
        """
        print("RUN : data2csv")
        with open(filename, 'a') as f:
            writer = csv.DictWriter(f, ["time", "voltage"])
            writer.writerow(self.data)

    def gpio_cleanup(self):
        """
        GPIOの終了処理を行う
        """
        print("RUN : gpio_cleanup")
        # GPIO.cleanup()

if __name__ == "__main__":
    radee = Radee() # インスタンス作成

    radee.gpio_setup()
    radee.spi_setup()

    try:
        while True: # Ctrl + Cで止めるまで無限ループ
            radee.measure()
            radee.print_data()
            radee.data2csv("sample.csv")
            print("-----------------------")
    except KeyboardInterrupt:
        pass
    finally:
        radee.spi_cleanup()
        radee.gpio_cleanup()

from __future__ import print_function
import RPi.GPIO as IO
import time

PIN_D0=16
PIN_D1=17
PIN_D2=18
PIN_D3=19
PIN_D4=20
PIN_D5=21
PIN_D6=22
PIN_D7=23

DATAPINS = [PIN_D0, PIN_D1, PIN_D2, PIN_D3, PIN_D4, PIN_D5, PIN_D6, PIN_D7]
RDATAPINS = [z for z in reversed(DATAPINS)]

PIN_INT=12
PIN_READY=13

PIN_MUTE=4
PIN_RS=24
PIN_WS=25
PIN_BDIR=26
PIN_BEN=27

ROMADDR=0x0F

class TMS5220:
    def __init__(self, verbosity):
        self.verbosity = verbosity

        IO.setmode(IO.BCM)
        IO.setwarnings(False) # turn off warnings about reusing the pins

        IO.setup(PIN_BEN, IO.OUT)
        IO.setup(PIN_BDIR, IO.OUT)
        IO.output(PIN_BEN, 1)
        IO.output(PIN_BDIR, 1)
    
        self.setDataInput()

        IO.setup(PIN_MUTE, IO.OUT)
        IO.setup(PIN_RS, IO.OUT)
        IO.setup(PIN_WS, IO.OUT)

        IO.setup(PIN_INT, IO.IN)
        IO.setup(PIN_READY, IO.IN)

        IO.output(PIN_MUTE, 0)
        IO.output(PIN_RS, 1)
        IO.output(PIN_WS, 1)

        self.reset()
        
    def cleanup(self):
        # make sure pigpio is cleaned up
        pass

    def shortDelay(self):
        for i in range(0,100):
            pass

    def tinyDelay(self):
        pass
        
    def setDataInput(self):
        for datapin in DATAPINS:
            IO.setup(datapin, IO.IN)
        IO.output(PIN_BDIR, 0)

    def setDataOutput(self):
        for datapin in DATAPINS:
            IO.setup(datapin, IO.OUT)
        IO.output(PIN_BDIR, 1)

    def readInput(self):
        d = 0
        for pin in RDATAPINS:
            d = d << 1
            if IO.input(pin)==1:
                d = d | 1
        return d & 0xFF
    
    def writeOutput(self, d):
        d = (d & 0xFF)
        for pin in DATAPINS:
            IO.output(pin, (d & 1))
            d = d >> 1

    def read(self):
        while IO.input(PIN_READY)!=0:
            pass
        self.setDataInput()
        IO.output(PIN_BEN, 0)
        IO.output(PIN_RS, 0)
        self.tinyDelay()
        while IO.input(PIN_READY)!=0:
            pass
        d = self.readInput()
        IO.output(PIN_RS, 1)
        IO.output(PIN_BEN, 1)
        return d
    
    def write(self, d):
        while IO.input(PIN_READY)!=0:
            pass
        self.setDataOutput()
        self.writeOutput(d)
        IO.output(PIN_BEN, 0)
        self.tinyDelay()
        IO.output(PIN_WS, 0)
        self.tinyDelay()                # When setting ADDR, it seems important that WS goes high before ready goes low
        IO.output(PIN_WS, 1)
        while IO.input(PIN_READY)!=0:
            pass
        IO.output(PIN_BEN, 1)

    def mute(self, d):
        if d:
            IO.output(PIN_MUTE, 1)
        else:
            IO.output(PIN_MUTE, 0)

    def wait(self):
        while True:
            d = self.read()
            if (d & 0x80)==0:
                return

    def setAddr(self, d):
        d = d | (ROMADDR << 14)
        self.write((d & 0x0F) | 0x40)
        self.write(((d>>4) & 0x0F) | 0x40)
        self.write(((d>>8) & 0x0F) | 0x40)
        self.write(((d>>12) & 0x0F) | 0x40)
        self.write(((d>>16) & 0x0F) | 0x40)

    def sayWord(self, d):
        self.wait()
        self.setAddr(d)
        self.write(0x50)

    def sayWords(self, words):
        for word in words:
            #self.dump(word)
            self.sayWord(word)

    def sayExternal(self, data):
        # Wait for not speaking
        self.wait()

        # Send the first command
        self.write(0x60)

        # Get the length of the data
        length = len(data)

        if length < 16:
            raise Exception("Too damn short")

        remaining = length - 16

        # Send the first 16 bytes
        for i in range(16):
            self.write(data[i])

        index = 16

        # Send the remaining data in chunks
        while remaining > 0:
            # Wait for buffer less than half full
            while (self.read() & 0x40) == 0:
                pass

            if remaining < 8:
                # Send the remaining bytes if less than 8
                for i in range(remaining):
                    self.write(data[index + i])
                break
            else:
                # Send the next 8 bytes
                for i in range(8):
                    self.write(data[index + i])
                index += 8
                remaining -= 8

    def reset(self):
        for i in range(0,9):
            self.write(0xFF)
            self.shortDelay()
        self.write(0x70)
        self.shortDelay()

    def dump(self, d):
        for i in range(0, 10):
            self.setAddr(d)
            self.write(0x10)
            print("Reading %04X:%02X" % (d, self.read()))
            d+=1




        


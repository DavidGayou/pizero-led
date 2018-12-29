
import time
from flask import Flask
from flask_cors import CORS
from neopixel import *


# LED strip configuration:
LED_COUNT = 300      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#LED Dress specific values
LED_PER_RIBBON = 30
RIBBON_COUNT = 10



def setDressPixel(strip, ribbon_pos, pos_in_ribbon, color):
    """Color a specific led in the dress by providing the riboon and the pos in ribbon"""
    strip.setPixelColor(ribbon_pos*LED_PER_RIBBON + pos_in_ribbon, color)

def fillDressDown(strip, color, wait_ms=50):
    """Color the dress row by row from up to bottom"""
    for lpos in range(0, LED_PER_RIBBON):
        for rpos in range(0, RIBBON_COUNT):
            setDressPixel(strip, rpos, lpos, color)
            strip.show()
        time.sleep(wait_ms/1000.0)

def fillDressUp(strip, color, wait_ms=50):
    """Color the dress row by row from up to bottom"""
    for lpos in range(0, LED_PER_RIBBON):
        for rpos in range(0, RIBBON_COUNT):
            setDressPixel(strip, rpos, LED_PER_RIBBON - 1 - lpos, color)
            strip.show()
        time.sleep(wait_ms/1000.0)

def dressSpiralDown(strip, color, iter=10, step=3, wait_ms=50):
    prevpos =0
    litLed=dict()

    for it in range(0, iter):
        for rpos in range(0, RIBBON_COUNT):
            if rpos not in litLed:
                litLed[rpos]=[] 
            
            #Clean the leds 
            for i in litLed[rpos]:
                setDressPixel(strip, rpos, i, Color(0,0,0))
            strip.show()

            for i in range(0,step):
                p = (prevpos+i) % LED_PER_RIBBON
                setDressPixel(strip, rpos, p, color)
                litLed[rpos]=litLed[rpos].append(p)
            prevpos = (prevpos + step) %LED_PER_RIBBON

            strip.show()
            time.sleep(wait_ms/1000.0)

def dressSpiralUp(strip, color, iter=10, step=3, wait_ms=50):
    prevpos =0
    litLed=dict()

    for it in range(0, iter):
        for rpos in range(0, RIBBON_COUNT):
            if rpos not in litLed:
                litLed[rpos]=[] 
            
            #Clean the leds 
            for i in litLed[rpos]:
                setDressPixel(strip, rpos, i, Color(0,0,0))
            strip.show()

            for i in range(0,step):
                p = (prevpos+i) % LED_PER_RIBBON
                setDressPixel(strip, rpos, p, color)
                litLed[rpos]=litLed[rpos].append(p)
            prevpos = (prevpos + step) %LED_PER_RIBBON

            strip.show()
            time.sleep(wait_ms/1000.0)



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def shootingStarAtPos(strip, pos, queue_length):
    headColor = Color(255,255,255)
    strip.setPixelColor(pos, headColor)
    
    for i in range(0,queue_length):
        if (pos-i) > 0:
            queuePosColor=155-(10*i)
            strip.setPixel(pos-i, Color(queuePosColor, queuePosColor, queuePosColor) )

    

def shootingStar(strip, queue_length=5, wait_ms=10):
    """shooting star accross the ribbon"""

    for i in range(0,LED_COUNT):
        shootingStarAtPos(strip, i, queue_length)
        strip.show()
        time.sleep(wait_ms/1000.0)


app = Flask(__name__)
CORS(app)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/rainbow')
def runRainbow():
    rainbow(strip)
    return "Rainbow"

@app.route('/ColorWipeRed')
def runColorWipeRed():
    colorWipe(strip,Color(0, 255, 0))
    return "ColorWipeRed"

@app.route('/ColorWipeBlue')
def runColorWipeBlue():
    colorWipe(strip,Color(0, 0, 255))
    return "ColorWipeBlue"

@app.route('/ColorWipeGreen')
def runColorWipeGreen():
    colorWipe(strip,Color(255, 0, 0))
    return "ColorWipeGreen"

@app.route('/ColorWipePurple')
def runColorWipePurple():
    colorWipe (strip, Color(157, 18, 255))
    return "ColorWipePurple"

@app.route('/RainbowCycle')
def runRainbowCycle():
    rainbowCycle(strip)
    return "RainbowCycle"

@app.route('/theaterChaseRed')
def runTheaterChase():
    theaterChase(strip,Color(0,255,0))
    return "theaterChaseRainbow"

@app.route('/debug')
def debug():
    theaterChase(strip,Color(0,255,0),iterations=1000)
    return "theaterChaseRainbow"

@app.route('/theaterChaseRainbow')
def runTheaterChaseRainbow():
    theaterChaseRainbow(strip)
    return "theaterChaseRainbow"

#############
#FILL DRESS

@app.route('/fillDressDownWhite')
def runfillDressDownWhite():
    fillDressDown (strip,Color(255, 255, 255))
    return "fillDressDownWhite"

@app.route('/fillDressDownYellow')
def runfillDressDownYellow():
    fillDressDown (strip, Color(255,255,0))
    return "fillDressDownYellow"

@app.route('/fillDressDownRed')
def runfillDressDownRed():
    fillDressDown (strip, Color(0,255,0))
    return "fillDressDownRed"

@app.route('/fillDressDownGreen')
def runfillDressDownGreen():
    fillDressDown (strip, Color(255,0,0))
    return "fillDressDownGreen"

@app.route('/fillDressDownBlue')
def runfillDressDownBlue():
    fillDressDown (strip, Color(0,0,255))
    return "fillDressDownblue"

@app.route('/fillDressDownRed')
def runFillDownRed():
    fillDressDown(strip, Color(0,255,0))
    return "FillDressDownRed"

#######
# Shooting Star

@app.route('/shootingStar')
def runShootingStar():
    shootingStar(strip, 10)
    return "Shooting Star"

@app.route('/clear')
def runClear():
    colorWipe(strip, Color(0,0,0), 10)
    return "clear"

@app.route('/SpiralDownWhite')
def runSpiralDownWhite():
    dressSpiralDown(strip, Color(255,255,255))
    return "SpiralDownWhite"

    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
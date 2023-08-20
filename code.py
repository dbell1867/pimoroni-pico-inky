import time
import busio
import board
import displayio
from displayio import Bitmap
import terminalio
from adafruit_display_text import label
import adafruit_uc8151d
from adafruit_bitmap_font import bitmap_font
import digitalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon
import math


displayio.release_displays()

#Define buttons
button_a = digitalio.DigitalInOut(board.GP12)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.GP13)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

button_c = digitalio.DigitalInOut(board.GP14)
button_c.direction = digitalio.Direction.INPUT
button_c.pull = digitalio.Pull.UP

# This pinout works on the Raspberry Pi Pico and Pico W and may need to be altered if these pins are being used by other packs or bases.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)  # Uses SCK and MOSI
epd_cs = board.GP17
epd_dc = board.GP20
epd_reset = board.GP21
epd_busy = None

# Make a bus to communicate with the screen.
display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=400000
)
time.sleep(1)

# Setting parameters for the display.
display = adafruit_uc8151d.UC8151D(
    display_bus,
    width=296,#296
    height=128,#128
    rotation=270,
    black_bits_inverted=True, #This is the background(False = Black True = White)
    color_bits_inverted=True,  #This is the font(False = White)
    grayscale=True,
    refresh_time=1,
    seconds_per_frame = 3,
)

font = terminalio.FONT

# Make a group to write to.
splash = displayio.Group()
one = displayio.Group(scale=1 , x=0, y=0)
two = displayio.Group(scale =1, x=128, y=0)
web_time = displayio.Group(scale=1, x=5, y=4)
board_time = displayio.Group(scale=1, x=5, y=33)
elapsed_time_web = displayio.Group(scale=1, x=5, y= 62)
elapsed_time_board = displayio.Group(scale=1, x=5, y= 91)

#color_bitmap = displayio.Bitmap(128, 128, 1)
# color_palette = displayio.Palette(1)
# color_palette[0] = 0xFFFFFF
# bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
# splash.append(bg_sprite)
##########################################################################
rect_b = Rect(x=0, y=0, width=129, height=128, outline=0xFFFFFF, fill=0xFFFFFF)
splash.append(rect_b)
rect_a = Rect(4, 4, 121, 121, outline=0x000000, stroke=2)
splash.append(rect_a)

# Clock Face
circ = Circle(x0=64, y0=64, r=56, outline= 0x000000, fill=0x000000)
splash.append(circ)

# Hour Markers
hour_ticks = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
outer_radius = 56
inner_radius = 46
for x in hour_ticks:
    hour_tick = Line(x0 = math.floor(64+outer_radius*math.cos(math.radians(x))),
        y0= math.floor(64+outer_radius*math.sin(math.radians(x))),
        x1= math.floor(64+inner_radius*math.cos(math.radians(x))),
        y1= math.floor(64+inner_radius*math.sin(math.radians(x))),
        color = 0xFFFFFF)
    splash.append(hour_tick)

# Minute Markers
inner_radius2 = 54
for i in range(60):
    if i in hour_ticks:
        pass
    else:
        deg = i*6
        min_tick = Line(x0 = math.floor(64+outer_radius*math.cos(math.radians(deg))),
            y0= math.floor(64+outer_radius*math.sin(math.radians(deg))),
            x1= math.floor(64+inner_radius2*math.cos(math.radians(deg))),
            y1= math.floor(64+inner_radius2*math.sin(math.radians(deg))),
            color = 0xFFFFFF)
        splash.append(min_tick)

# small button circle at ceter of clock face
circa = Circle(x0=64, y0=64, r=5, fill=0xFFFFFF)
one.append(circa)

rr = RoundRect(x=3 ,y=4 ,width=163 ,height=122, r=10, outline=0xFFFFFF ,stroke=2 )
two.append(rr)

r_web_time = RoundRect(x=5, y=5, width=150, height= 25, r= 5, outline=0xFFFFFF, stroke=2)
web_time.append(r_web_time)
text_label1b = label.Label(
    font=font, text='web time:', color=0xFFFFFF
)  # yTop label
text_label1b.anchor_point = (0,0)
text_label1b.anchored_position = (
    10,
    12,
)
web_time.append(text_label1b)

r_board_time = RoundRect(x=5, y=5, width=150, height= 25, r= 5, outline=0xFFFFFF, stroke=2)
board_time.append(r_board_time)
text_label1a = label.Label(
    font=font, text='board time:', color=0xFFFFFF
)  # yTop label
text_label1a.anchor_point = (0,0)
text_label1a.anchored_position = (
    10,
    12,
)
board_time.append(text_label1a)


r_elapsed_web = RoundRect(x=5, y=5, width=150, height= 25, r= 5, outline=0xFFFFFF, stroke=2)
elapsed_time_web.append(r_elapsed_web)
text_label1c = label.Label(
    font=font, text='elapsed time:', color=0xFFFFFF
)  # yTop label
text_label1c.anchor_point = (0,0)
text_label1c.anchored_position = (
    10,
    12,
)
elapsed_time_web.append(text_label1c)

r_elapsed_board = RoundRect(x=5, y=5, width=150, height= 25, r= 5, outline=0xFFFFFF, stroke=2)
elapsed_time_board.append(r_elapsed_board)
text_label1d = label.Label(
    font=font, text='elapsed board:', color=0xFFFFFF
)  # yTop label
text_label1d.anchor_point = (0,0)
text_label1d.anchored_position = (
    10,
    12,
)
elapsed_time_board.append(text_label1d)


splash.append(one)
splash.append(two)
two.append(web_time)
two.append(board_time)
two.append(elapsed_time_web)
two.append(elapsed_time_board)



display.show(splash)
display.refresh()

while True:
    pass


#!/usr/bin/python

from PIL import Image, ImageOps, ImageDraw,ImageStat,ImageEnhance
import math
import os
import time
from easyprocess import Proc

class Meter_Exception(Exception):
    def __init__(self, message):
        super(Meter_Exception, self).__init__(message)
        self.message = message

# map of energy for meter's bar graph
e_map = [ 10, 50, 100, 150, 200, 250, 350, 450, 550, 650, 750, 950, 1150, 1350, 1550, 2000, 2500, 3000, 3500, 4000, 4500, 5500, 6500, 7500, 8500, 10000, 12000, 14000, 16000, 18000, ]

def take_photo(timeout,logger):
    cmd = '/usr/bin/fswebcam -q -d /dev/video0  -r 800x600 --no-banner  --set "Exposure, Auto"="Manual Mode" --set "Exposure (Absolute)"=200 --set brightness=50% --set "Exposure, Auto Priority"="False" meter.jpg'
    proc=Proc(cmd).call(timeout=timeout)
    #print proc.stdout
    if proc.stderr:
        logger.warning(proc.stderr)
    return proc.return_code

def adjust(im):
    im=im.convert('L')
    w = 500
    h = 350
    box = (80,60,w,h)
    region = im.crop(box)
    contr = ImageEnhance.Contrast(region)
    region = contr.enhance(2.0)
    return region


#function that returns the average value of a region of pixels
def avg_region(image,box):
    region = image.crop(box)
    stat = ImageStat.Stat(region)
    return stat.mean[0]

def read_energy(img,logger):
    draw = ImageDraw.Draw(img)
    img_width = img.size[0]
    img_height = img.size[1]
    sample_w = 7
    cent_x = img_width / 2
    cent_y = img_height * 0.71
    length = img_width / 2.8 # radius of bar graph
    sens = 20

    # arc legnth of bar graph
    arc_l = 104
    max_energy = 4500.0
    segment = 1
    arc_step = 2
    energy_div = (max_energy * arc_step ) / (2 * arc_l)
    d = -arc_l
    segs = 0
    last_bright = 255
    fill = 0
    change = False
    while d < arc_l:
        segs += 1
        d += arc_step
        # bars are not placed linearly:
        arc_step += 0.37
        deg = d - 90
        x = cent_x + length * math.cos(math.radians(deg))
        y = cent_y + length * math.sin(math.radians(deg))
        x = int(x)
        y = int(y)
        box = (x, y, x+sample_w, y+sample_w)
        bright = avg_region(img,box)
        # detect end of bar graph by change in brightness of pixel
        if change == False and (bright - last_bright )> sens:
            fill = 255
            segment = segs
            change = False
        draw.rectangle(box,fill=fill)
        last_bright = bright

    segment -= 1 # because list is 0 indexed
    logger.debug("found seg change at %d, energy = %dW" % (segment, e_map[segment])) 
    img.save("read.jpg")
    return(e_map[segment])


def read_meter(meter_port, logger, timeout=10):
    try:
        os.remove('meter.jpg')
    except OSError:
        pass
    logger.debug("taking photo with timeout = %d", timeout)
    ret = take_photo(timeout,logger)
    if ret == -15:
        raise Meter_Exception("photo timed out")
    logger.debub("took photo")

    image_file = "meter.jpg"
    try:
        img = Image.open(image_file)
    except IOError:
        raise Meter_Exception("no photo taken")
        

    img = adjust(img)

    energy = read_energy(img,logger)
    temp = 20  # fake
    #img.show()
    return temp, energy

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    print(read_meter(None,logging))

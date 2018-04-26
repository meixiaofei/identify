#!/usr/local/bin/python
# encoding=utf8
import sys
from pytesseract import *
import sys,os
from PIL import Image,ImageDraw
import numpy as np
from collections import Counter
import re

def depoint(img):
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            #print "x: " + str(x) + " y: " + str(y) + " value: " + str(pixdata[x,y])
            if pixdata[x,y-1] < 1:#上
                count = count + 1
            if pixdata[x,y+1] < 1:#下
                count = count + 1
            if pixdata[x-1,y] < 1:#左
                count = count + 1
            if pixdata[x+1,y] < 1:#右
                count = count + 1
            if pixdata[x-1,y-1] < 1:#左上
                count = count + 1
            if pixdata[x-1,y+1] < 1:#左下
                count = count + 1
            if pixdata[x+1,y-1] < 1:#右上
                count = count + 1
            if pixdata[x+1,y+1] < 1:#右下
                count = count + 1
            if count > 4:
                pixdata[x,y] = 0
    return img.crop((1, 1, w - 1, h - 1))

def initTable(threshold=140):
 table = []
 for i in range(256):
     if i < threshold:
         table.append(0)
     else:
         table.append(1)

 return table

#im = Image.open(os.getcwd() + '/1.jpg')
#im = Image.open(os.getcwd() + '/2.jpeg')

reload(sys)
sys.setdefaultencoding('utf8')
for i in range(50):
    file_path = os.getcwd() + '/img/' + str(i) + '.jpg'
    im = Image.open(file_path)
    im = im.convert('L')

    im = im.point(initTable(111), '1')
    im = depoint(im)
    im.save(os.getcwd() + '/img/' + str(i) + '-bak.jpg')

    identified = image_to_string(im, config='-psm 6')
    identified = identified.replace('‘', '-')
    identified = identified.replace('—', '-')
    identified = identified.replace('—', '-')
    identified = identified.replace('-', '-')
    identified = identified.replace('~', '-')
    identified = identified.replace('f', '+')
    identified = identified.replace(':', '=')
    identified = identified.replace('?', '=')
    identified = identified.replace('==', '=')
    identified = identified.replace('=-', '=')
    identified = identified.replace('=)', '=')
    identified = identified.replace('.)', '0')
    identified = identified.replace('y', '+')
    identified = identified.replace('Y', '+')
    identified = identified.replace('=', '')
    identified = identified.replace('«-', '+')
    identified = identified.replace(' + ', '+')
    identified = identified.replace('«', '-')
    identified = identified.replace('v', '-')
    identified = identified.replace('£', '5')
    identified = identified.replace('>', '+')
    identified = identified.replace('n', '6')
    identified = identified.replace('l', '1')

    tmp = identified.split('-')[0]
    print tmp
    if len(str(tmp)) == 3:
        identified = identified.replace('1-', '+')
    print "pic index: " + str(i) + " " + identified

import subprocess
import time
import os
import sys
import aircv as ac
import threading
from common.auto_adb import auto_adb
from PIL import Image
adb = auto_adb()
def matchImg(imgsrc,imgobj,confidencevalue=0.5):#imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    match_result = ac.find_template(imsrc,imobj,0.5)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    if match_result is not None:
        match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0为高，1为宽

    return match_result
def pull_screenshot():
    adb.run('shell screencap -p /sdcard/autojump.png')
    adb.run('pull /sdcard/autojump.png .')
    return Image.open('./autojump.png')
def tap(position):
    y, x = position['result']
    x=820-x
    cmd='shell input tap {x1} {y1}'.format(
    x1=x,y1=y
    )
    adb.run(cmd)
def main():
    pull_screenshot()
    position1=matchImg('autojump.png','panduan001.png',0.7)
    if position1!=None:
        position=matchImg('autojump.png','b.png',0.7)
        if position!=None:
            tap(position)
        position=matchImg('autojump.png','panduan.png',0.7)
        if position!=None:
            tap(position)
        time.sleep(2)
        pull_screenshot()
        position=matchImg('autojump.png','jieshu.png',0.7)
        if position!=None:
            tap(position)
    else:
        position=matchImg('autojump.png','jieshu.png',0.7)
        if position!=None:
            tap(position)
    global timer
    timer = threading.Timer(5.5, main)
    timer.start()
timer = threading.Timer(1, main)
timer.start()

import pyinotify,subprocess
import os
from time import sleep
import sys
global i
i = 0


def textChange(ev):
	global i
	if i < 1:
		os.system("python3 alg.py")
		#sleep(5)
		os.system("./read")
		
		i = i+1
	else:
		i = 0

wm = pyinotify.WatchManager()
wm.add_watch('/home/pi/samp_data.txt', pyinotify.IN_MODIFY, textChange)
notifier = pyinotify.Notifier(wm)

	
notifier.loop()
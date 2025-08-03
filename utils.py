from datetime import datetime
from zoneinfo import ZoneInfo
import os, platform, subprocess

def getNow():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("%d-%B-%y %I:%M:%S %p")

def getToday():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("%d-%B-%y")

def getTimeStamp():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("_%d_%B_%y_%I_%M_%S_%p_")

def openFile(fp):
		#Open files using this method
		if platform.system() == "Windows" or platform.system() == "nt":
				os.startfile(fp)
		elif platform.system() == "Darwin":
			subprocess.run(["open", fp])
		else:
			subprocess.run(["xdg-open", fp])
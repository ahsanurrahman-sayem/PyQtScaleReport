from datetime import datetime
from zoneinfo import ZoneInfo
import os, platform, subprocess

def getNow():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("%d-%b-%y %I:%M %p")

#def formateTime():
	#v = getNow()
	#return [v,str(v.strftime("%d-%b-%y %I:%M %p")),str(v.strftime("%Y-%m-%d %H:%M:%S"))]

def getToday():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("%d-%B-%y")

def getTimeStamp():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("_%d_%B_%y_%I_%M_%S_%p_")

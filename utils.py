from datetime import datetime
from zoneinfo import ZoneInfo

def getNow():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("%d-%B-%y %I:%M:%S %p")

def getToday():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("%d-%B-%y")

def getTimeStamp():
	now = datetime.now(ZoneInfo("Asia/Dhaka"))
	return now.strftime("_%d_%B_%y_%I_%M_%S_%p_")
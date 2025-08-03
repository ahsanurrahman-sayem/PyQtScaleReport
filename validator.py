from utils import getNow


def isZero( value: str):
#this method checkhs if the given value is 0?
#if its a 0 then return empty else returns timeStamp from the utils module
	return "" if value == "0" else getNow()

def isDigit(value):
	#this method checks if the value is a number, if number then returns the value else retuns a 0
	return value if value.isdigit() else 0


def isValue(value,valueToUse):
# first check if value is not empty
# if the value is empty then valueToUse otherwise return value
	return value if value is not ""  else valueToUse
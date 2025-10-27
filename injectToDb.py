from db import createTable, setDatasIntoTable, getDatasFromTable, ARSTable
import models

#createTable("vehicles",)

vehicles = ARSTable("vehicles",models.Vehicle)
print(vehicles.createTable(id="INTEGER PRIMARY KEY AUTOINCREMENT",name="TEXT"))


def addVehicle():
	for item in ["DMT-","DMN-","DMD-","CMN-","CMT-","BT-","LN-","LT-","KHT-","TROLLEY"]:
		vehicles.setDatasIntoTable(name=item)

def addItem():
	for item in ["WOOD", "M/S. ROD","SOYABEAN","RICE","LUBRICANT","OIL","TAR","BUTIMEN","WHEAT","CORN","TEEN","IRON", "SCRAP","BOOKS", "HAY","PLASTIC","BUNDLE"]:
		vehicles.setDatasIntoTable(name=item)

if __name__ == '__main__':
	#vehicles.clearTable()
	#vehicles.setDatasIntoTable(name="RUBEL",password="4")
	#vehicles.setDatasIntoTable(name="SAYEM",password="qc")
	addVehicle()
	#addItem()
	print(vehicles.getDatasFromTable())

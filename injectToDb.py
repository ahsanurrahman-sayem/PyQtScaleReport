from db import ARSTable
import models

#createTable("vehicles",)

ClientsTable = ARSTable("clients", Client, unique_fields=["name"])

ItemTable = ARSTable("items",models.Item,unique_fields=["name"])

VhclTable = ARSTable("vehicle_serials", VehicleSerial, unique_fields=["serial"])


def addVehicles():
	for item in ["DMT-","DMN-","DMD-","CMN-","CMT-","BT-","LN-","LT-","KHT-","TROLLEY"]:
		VhclTable.setDatasIntoTable(name=item)

def addItems():
	for item in ["WOOD", "M/S. ROD","SOYABEAN","RICE","LUBRICANT","OIL","TAR","BUTIMEN","WHEAT","CORN","TEEN","IRON", "SCRAP","BOOKS", "HAY","PLASTIC","BUNDLE"]:
		ItemTable.setDatasIntoTable(name=item)

def addClients():
	for item in ["ROMJAN TRADERS","HAFIZUR RAHMAN","FOOD","ANY","MOHAMMAD ALI","QUALITY AGRO","CITY LUBE","AMIRATH LUBE"]:
		ClientsTable.setDatas(name=item)

if __name__ == '__main__':
	addVehicles()
	addItems()
	addClients()
	
	print(ClientsTable.getDatas())
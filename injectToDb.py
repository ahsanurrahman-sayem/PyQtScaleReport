from db import ARSTable,addUser,getItems
import models

ClientsTable = ARSTable("clients", models.Client, unique_fields=["name"])

ItemTable = ARSTable("items",models.Item,unique_fields=["name"])

VhclTable = ARSTable("vehicle_serials", models.VehicleSerial, unique_fields=["serial"])

Operatorstable = ARSTable("users", models.User, unique_fields=["name"])


def addVehicles():
	#VhclTable.createTable()
	for item in ["DMT-","DMN-","DMD-","CMT-","CMN-","CMD-","LN-","LT-","NN-","FT-","FDH-","BT-","KHT-","TROLLEY"]:
		VhclTable.setDatas(serial=item)

def addItems():
	ItemTable.clearTable()
	ItemTable.delTable()
	ItemTable.createTable()
	for item in ["WOOD", "M/S. ROD","SOYABEAN","RICE","LUBRICANT","OIL","TAR","BUTIMEN","WHEAT","CORN","TEEN","IRON", "SCRAP","BOOKS", "HAY","PLASTIC","BUNDLE"]:
		ItemTable.setDatas(name=item)

def addClients():
	for item in ["ROMJAN TRADERS","HAFIZUR RAHMAN","CITY LUBE","AMIRATH LUBE","MOHAMMAD ALI","QUALITY AGRO","ANY","FOOD"]:
		ClientsTable.setDatas(name=item)

def add_user(u_name:str, u_password: str):
	addUser(models.User(name=u_name,password=u_password))

if __name__ == '__main__':
	VhclTable.clearTable()
	addVehicles()

	ItemTable.clearTable()
	addItems()

	ClientsTable.clearTable()
	addClients()

	def extractData(items):
		return [item.name for item in items]
	print(extractData(ARSTable("users",models.User).getDatas()))
	print(extractData(ARSTable("items",models.Item).getDatas()))
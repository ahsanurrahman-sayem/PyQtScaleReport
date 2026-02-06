from db import ARSTable,addUser,getItems
import models

ClientsTable = ARSTable("clients", models.Client, unique_fields=["name"])

ItemTable = ARSTable("items",models.Item,unique_fields=["name"])

VhclTable = ARSTable("vehicle_serials", models.VehicleSerial, unique_fields=["serial"])

OperatorsTable = ARSTable("users", models.User, unique_fields=["name"])


def addVehicles():
	VhclTable.clearTable()
	VhclTable.delTable()
	VhclTable.createTable()
	for item in ["DMT-","DMN-","DMD-","CMT-","CMN-","CMD-","LN-","LT-","NN-","FT-","FDH-","BT-","KHT-","TROLLEY","AUTO","RIKSHAW"]:
		VhclTable.setDatas(serial=item)

def addItems():
	ItemTable.clearTable()
	ItemTable.delTable()
	ItemTable.createTable()
	for item in ["WOOD", "M/S. ROD","SOYABEAN","RICE","LUBRICANT","OIL","TAR","BUTIMEN","WHEAT","CORN","TEEN","IRON", "SCRAP","BOOKS", "HAY","PLASTIC","BUNDLE"]:
		ItemTable.setDatas(name=item)

def addClients():
	ClientsTable.clearTable()
	ClientsTable.delTable()
	ClientsTable.createTable()
	for item in ["ANY","ROMJAN TRADERS","KHOKON TRADERS","HAFIZUR RAHMAN","CITY LUBE","FOOD","AMIRATH LUBE","MOHAMMAD ALI","QUALITY AGRO","IBRAHIM TRADERS","RUBEL TRADERS"]:
		ClientsTable.setDatas(name=item)

#def add_user(u_name:str, u_password: str):
#	addUser(models.User(name=u_name,password=u_password))

def add_user():
	OperatorsTable.clearTable()
	OperatorsTable.delTable()
	OperatorsTable.createTable()
	for user,password in {"SOHEL":"s","RUBEL":"4","ADI":"4"}.items():
		OperatorsTable.setDatas(name=user,password=password)
		

if __name__ == '__main__':
	
	#addVehicles()

	#addItems()

	
	addClients()
	#add_user()


	def extractData(items):
		return [item for item in items]
	#print(extractData(ARSTable("users",models.User).getDatas()))
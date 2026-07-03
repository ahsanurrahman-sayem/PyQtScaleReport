import os
import platform
import subprocess
from tabulate import tabulate

from core.db import (
	getWeightById,
	addNewWeight,
	getAllWeights,
	getLastRowId,
	updateWeight,
	del_data,
	inject,
	addUser,
	addItem,
	getUsers,
	getItems,
	getLastRowId
)

from core.support.validator import isZero, isEmpty

from core.db.models import WeightData,User,Item, Client
from core.db import ARSTable, models

from core.gen_reportAPI import gen_report
from core.support.timeUtils import getNow


def get_input(prompt):
	try:
		return input(prompt).strip()
	except KeyboardInterrupt:
		print("\nAborted.")
		exit(0)


def isZero(value):
	return "" if value == "0" else getNow()

def create_report():
	try:
		print("\n📝 Create New Weight Report")
		custom_id = get_input("Enter Custom ID (optional): ")
		weight_id = int(custom_id) if custom_id.isdigit() else None
		vehicle_no = get_input("Vehicle No: ")
		client_name = get_input("Client Name: ")
		challan_no = get_input("Challan/LC No: ")
		driver = get_input("Driver: ")
		address = get_input("Address: ")
		item_name = get_input("Item Name: ")
		qty = get_input("Quantity: ")
		contact = get_input("Contact: ")
		load_weight = get_input("Load Weight (kg): ")
		unload_weight = get_input("Unload Weight (kg): ")
	
		load_weight = load_weight if load_weight.isdigit() else "0"
		unload_weight = unload_weight if unload_weight.isdigit() else "0"
	
		data = {
			"operator": "Admin",
			"vehicle_no": vehicle_no,
			"client_name": client_name if client_name else "ANY",
			"challan_no": challan_no,
			"driver": driver,
			"address": address,
			"item_name": item_name,
			"qty": qty,
			"contact": contact,
			"load_weight": load_weight,
			"load_weight_date": isZero(load_weight),
			"unload_weight": unload_weight,
			"unload_weight_date": isZero(unload_weight),
			"net_weight": str(int(load_weight) - int(unload_weight)),
			"party_type": "PARTY"
		}

		weight_obj = WeightData(id=weight_id, **data)
		data["id"] = addNewWeight(weight_obj)
		filename = f"{data['client_name']}_weight_report_{data['id']}.pdf"
		fp = gen_report(data, filename)
	
		open_pdf(fp)
		print("✅ Report created and saved as:", filename)
	except Exception as e:
		print("!!! --*-- Exception --*-- !!!\n"+str(e)+"\nPlease insert a uniqe Custom Weight Id which is't available in the database, or just do not insert any Id as the system will auto generate the ID itself.\nThanks for using the service!")


def search_report(weight_id: int):
	data = getWeightById(weight_id)
	if not data:
		print("⚠ No data found for that ID.")
		return
	filename = f"{data.client_name}_weight_report_{data.id}.pdf"
	fp = gen_report(data.__dict__, filename)
	open_pdf(fp)
	print("✅ Report generated and opened:", filename)

def del_last_report():
	record = getLastRowId()
	if not record:
		print("⚠ No records found.")
		return
	print(f"Deleting Record ID: {record}")
	view_a_report(record)
	delete_report(record)
	

def view_all_reports():
	records = getAllWeights()
	if not records:
		print("⚠ No records found.")
		return
	table = [[
		item.id,
		item.client_name,
		item.vehicle_no,
		item.load_weight,
		item.unload_weight,
		item.net_weight,
		item.load_weight_date,
		item.unload_weight_date
	] for item in records]
	headers = ["ID", "Client", "Vehicle", "Load Weight", "Unload Weight", "Net Weight","Load Date","Unload Date"]
	
	print("\n📋 All Weight Records:\n")
	print(tabulate(table, headers, tablefmt="grid"))

def view_a_report(weight_id:int):
	data = getWeightById(weight_id)
	if not data:
		print("⚠ No data found for that ID.")
		return
	table = [
		[data.id,
		data.client_name,
		data.vehicle_no,
		data.load_weight,
		data.unload_weight,
		data.net_weight,
		data.load_weight_date,
		data.unload_weight_date]]

	headers = ["ID", "Client", "Vehicle", "Load", "Unload", "Net","Load Date","Unload Date"]
	print(f"\n📋 Weight Records:{data.id}")
	print(tabulate(table, headers, tablefmt="grid"))

def edit_report(weight_id: int):
	data = getWeightById(weight_id)
	if not data:
		print("⚠ No data found for that ID.")
		return
	print(f"Editing Record ID: {data.id}")
	view_a_report(data.id)

	id = get_input("New id:")
	load_weight = get_input("New Load Weight (kg): ")
	unload_weight = get_input("New Unload Weight (kg): ")
	client_name = get_input("New Client name:")
	vehicle_no = get_input("New vehicle number:")
	qty = get_input("New Quantity:")

	data.vehicle_no = vehicle_no if not isEmpty(vehicle_no) else data.vehicle_no
	data.load_weight = load_weight if load_weight.isdigit() else data.load_weight
	data.unload_weight = unload_weight if unload_weight.isdigit() else data.unload_weight

	data.id = id if id.isdigit() else data.id
	data.net_weight = str(int(data.load_weight) - int(data.unload_weight))
	
	data.client_name = client_name if client_name != "" else data.client_name
	data.qty = qty if qty.isdigit else data.qty

	updateWeight(data)
	print("✅ Weight data updated successfully.\nUpdated Weight Record...")
	view_a_report(data.id)
	

def delete_report(weight_id: int):
	data = getWeightById(weight_id)
	if not data:
		print("⚠ No data found for that ID.")
		return
	print(f"Deleting Record ID: {data.id}")
	view_a_report(data.id)
	del_data(data.id)

def modify_id(weight_id: int,new_id:int):
	data = getWeightById(weight_id)
	if not data:
		print("⚠ No data found for that ID.")
		return
	inject(data.id,new_id)
	view_a_report(new_id)


def add_items():
	while True:
		item = get_input("Enter Item Name: ")
		if item:
			addItem(Item(name=item))
		else:
			return

def view_items():
	items = getItems()
	if items:
		table = [[
			item.name,
		] for item in items]
		headers = ["Item Name"]
		print("\n📋 All Items's:\n")
		print(tabulate(table, headers, tablefmt="grid"))
	else:
		print(f"Items:{items}")
		
def add_user():
	u_name: str = get_input("Enter new user name ")
	password: str = get_input(f"Enter {u_name}'s password: ")
	if u_name and password:
		addUser(User(id=None,name=u_name,password=password))
	else:
		pass

def view_users():
	users = getUsers()
	if users:
		table = [[
			user.name,
			user.password
		] for user in users]
		headers = ["User","Password"]
	
		print("\n📋 All User's:\n")
		print(tabulate(table, headers, tablefmt="grid"))
	else:
		print(f"Users:{users}")

def add_client():
	while True:
		item = get_input("Enter Client Name: ")
		if item:
			addItem(Client(id=None,name=item))
		else:
			return

def get_all_clients():
	headers=["Client","id"]
	table = [[client.name,client.id] for client in ARSTable("clients", models.Client, unique_fields="name").getDatas()]
	print("\nAll Clients:\n")
	print(tabulate(table,headers,tablefmt="grid"))

def open_pdf(fp):
	try:
		if platform.system() == "Windows" or platform.system() == "nt":
			os.startfile(fp)
		elif platform.system() == "Darwin":
			subprocess.run(["open", fp])
		else:
			subprocess.run(["xdg-open", fp])
	except Exception as e:
		print(f"⚠ Could not open PDF automatically: {e}")


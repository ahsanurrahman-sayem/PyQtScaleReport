import os
import platform
import subprocess
from tabulate import tabulate

from db import (
	getWeightById,
	addNewWeight,
	getAllWeights,
	getLastRowId,
	updateWeight,
	del_data,
	inject
)
from models import WeightData
from pdf_generator import generate_pdf
from utils import getNow


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
		#weight_id = int(custom_id) if custom_id.isdigit() and custom_id != getLastRowId() else None #or i could pass getLastRowId()
		weight_id = int(custom_id) if custom_id.isdigit() else None
		"""
		if weight_id is getLastRowId():
				print("variable 'custom_id' got - default last row id of database, need to auto increment.")
		else:
			print("variable 'weight_id' got custom weight id, creating custom report")
		"""

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
		fp = generate_pdf(data, filename)
	
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
	fp = generate_pdf(data.__dict__, filename)
	open_pdf(fp)
	print("✅ Report generated and opened:", filename)


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
		item.net_weight
	] for item in records]
	headers = ["ID", "Client", "Vehicle", "Load Weight", "Unload Weight", "Net Weight"]
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
		data.net_weight]]

	headers = ["ID", "Client", "Vehicle", "Load", "Unload", "Net"]
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
	qty = get_input("New Quantity:")

	data.id = id if id.isdigit() else data.id

	data.load_weight = load_weight if load_weight.isdigit() else data.load_weight
	data.load_weight_date = data.load_weight_date if data.load_weight_date != "" else getNow()\

	data.unload_weight = unload_weight if unload_weight.isdigit() else data.unload_weight
	data.unload_weight_date = data.unload_weight_date if data.unload_weight_date != "" else getNow()
	
	data.net_weight = str(int(load_weight) - int(unload_weight))
	
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
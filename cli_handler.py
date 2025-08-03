import os
import platform
import subprocess
from tabulate import tabulate

from db import (
	getWeightById,
	addNewWeight,
	getAllWeights,
	getLastRowId,
	updateWeight
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
	print("\n📝 Create New Weight Report")
	custom_id = get_input("Enter Custom ID (optional): ")
	weight_id = int(custom_id) if custom_id.isdigit() else getLastRowId()

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
		"client_name": client_name,
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
	final_id = addNewWeight(weight_obj)
	data["id"] = final_id
	filename = f"{data['client_name']}_weight_report_{final_id}.pdf"
	fp = generate_pdf(data, filename)

	open_pdf(fp)
	print("✅ Report created and saved as:", filename)


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

	headers = ["ID", "Client", "Vehicle", "Load", "Unload", "Net"]
	print("\n📋 All Weight Records:\n")
	print(tabulate(table, headers, tablefmt="grid"))


def edit_report(weight_id: int):
	data = getWeightById(weight_id)
	if not data:
		print("⚠ No data found for that ID.")
		return

	print(f"\nEditing Record ID: {data.id}")
	print(f"Current Load Weight: {data.load_weight}")
	print(f"Current Unload Weight: {data.unload_weight}")

	load_weight = get_input("New Load Weight (kg): ")
	unload_weight = get_input("New Unload Weight (kg): ")

	load_weight = load_weight if load_weight.isdigit() else "0"
	unload_weight = unload_weight if unload_weight.isdigit() else "0"

	data.load_weight = load_weight
	data.load_weight_date = data.load_weight_date if data.load_weight_date != "" else getNow()
	data.unload_weight = unload_weight
	data.unload_weight_date = data.unload_weight_date if data.unload_weight_date != "" else getNow()
	data.net_weight = str(int(load_weight) - int(unload_weight))

	updateWeight(data)
	print("✅ Weight data updated successfully.")


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
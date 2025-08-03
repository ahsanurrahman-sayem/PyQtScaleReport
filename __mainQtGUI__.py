from db import getWeightById, addNewWeight, getAllWeights, getLastRowId, updateWeight
from models import WeightData

from pdf_generator import generate_pdf
from utils import getNow, openFile
from validator import isZero, isDigit


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import sys, os, platform, subprocess, win32event, win32api, winerror


class ScaleReportApp(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Scale Weight Report")
		if getattr(sys, 'frozen', False):
			ico_path = os.path.join(sys._MEIPASS, "favicon.ico")
		else:
			ico_path = "favicon.ico"

		self.setWindowIcon(QtGui.QIcon(ico_path))
		self.setGeometry(100, 100, 900, 390)
		self.initUI()

	def initUI(self):
		self.tabs = QtWidgets.QTabWidget()
		self.setCentralWidget(self.tabs)

		self.create_tab = QtWidgets.QWidget()
		
		self.modify_tab = QtWidgets.QWidget()

		self.view_tab = QtWidgets.QWidget()
		self.search_tab = QtWidgets.QWidget()

		self.tabs.addTab(self.create_tab, "➕ Create New Weight Report")
		self.tabs.addTab(self.modify_tab,"✏ Edit Weight By ID")
		self.tabs.addTab(self.view_tab, "📋 View All Weight Reports")
		self.tabs.addTab(self.search_tab, "🔍 Search Weight Report by ID")
		


		self.initCreateTab()
		self.createModifyTab()
		self.initSearchTab()
		self.initViewTab()


	def initCreateTab(self):
		layout = QtWidgets.QFormLayout()
		self.create_fields = {}

		labels = [
			"Operator","Id", "Vehicle No", "Client Name", "Challan/LC No", "Driver", "Address",
			"Item Name", "Quantity", "Contact", "Load Weight (kg)", "Unload Weight (kg)"
		]

		for label in labels:
			entry = QtWidgets.QLineEdit()
			entry.returnPressed.connect(self.focusNextEmptyEntry)	# Bind Enter key
			self.create_fields[label] = entry
			layout.addRow(QtWidgets.QLabel(label), entry)

		submit_btn = QtWidgets.QPushButton("✅Submit")
		submit_btn.clicked.connect(self.submit_entry)
		layout.addWidget(submit_btn)

		self.create_tab.setLayout(layout)


	def initSearchTab(self):
		layout = QtWidgets.QFormLayout()

		self.search_input = QtWidgets.QLineEdit()
		
		# Create a temporary widget to hold the nested form layout
		form_widget = QtWidgets.QWidget()
		form_layout = QtWidgets.QFormLayout(form_widget)
		form_layout.addRow(QtWidgets.QLabel("Enter Weight ID:"), self.search_input)

		layout.addRow(form_widget)

		search_btn = QtWidgets.QPushButton("🔍 Search Report")
		search_btn.clicked.connect(self.search_entry_func)
		layout.addRow(search_btn)

		self.search_tab.setLayout(layout)

	def createModifyTab(self):
		layout = QtWidgets.QFormLayout()

		self.modify_id_entry = QtWidgets.QLineEdit()
		layout.addRow(QtWidgets.QLabel("Enter Weight ID:"), self.modify_id_entry)

		load_btn = QtWidgets.QPushButton("\U0001F50D Load Data")
		load_btn.clicked.connect(self.load_modify_data)
		layout.addRow(load_btn)

		self.modify_load_entry = QtWidgets.QLineEdit()
		layout.addRow(QtWidgets.QLabel("Load Weight (kg):"), self.modify_load_entry)

		self.modify_unload_entry = QtWidgets.QLineEdit()
		layout.addRow(QtWidgets.QLabel("Unload Weight (kg):"), self.modify_unload_entry)

		save_btn = QtWidgets.QPushButton("\U0001F4BE Save Changes")
		save_btn.clicked.connect(self.save_modified_weights)
		layout.addRow(save_btn)

		self.modify_tab.setLayout(layout)

	def initViewTab(self):
		layout = QtWidgets.QVBoxLayout()
		self.tree = QtWidgets.QTableWidget()
		self.tree.setColumnCount(6)
		self.tree.setHorizontalHeaderLabels(["ID", "Client", "Vehicle", "Load", "Unload", "Operator"])
		self.tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.tree.cellDoubleClicked.connect(self.view_pdf_by_id)

		refresh_btn = QtWidgets.QPushButton("🔄 Refresh")
		refresh_btn.clicked.connect(self.load_data)
		layout.addWidget(self.tree)
		layout.addWidget(refresh_btn)
		self.view_tab.setLayout(layout)
		self.load_data()

	def isZero(self, value: str):
		return "" if value == "0" else getNow()
	def getFieldValue(self,value):
	#return the value from QtEntryField Object
		return self.create_fields[value].text().strip()

	def filedValue(self,value:QtWidgets.QLineEdit):
	#selects a field object and return text from it
		return value.text.strip()

	def focusNextEmptyEntry(self):
		for entry in self.entries.values():
			if entry.text().strip() == "":
				entry.setFocus()
				return

	def load_modify_data(self):
		weight_id = self.modify_id_entry.text().strip()
		if not weight_id.isdigit():
			QMessageBox.critical(self, "Invalid Input", "Weight ID must be a number.")
			return

		data = getWeightById(int(weight_id))
		if not data:
			QMessageBox.information(self, "Not Found", "No data found for that ID.")
			return
		else:
			self.current_modify_id = data.id
			self.modify_load_entry.clear()
			self.modify_unload_entry.clear()
			self.modify_load_entry.setText(str(int(data.load_weight)))
			self.modify_unload_entry.setText(str(int(data.unload_weight)))
	def submit_entry(self):
		try:
			custom_id = getFieldValue("Id")
			weight_id = int(custom_id) if custom_id.isdigit() else None
			load_weight = str(isDigit(getFieldValue("Load Weight (kg)")))
			unload_weight = str(isDigit(getFieldValue("Unload Weight (kg)")))

			field_keys = {
					"vehicle_no": "Vehicle No",
					"client_name": "Client Name",
					"challan_no": "Challan/LC No",
					"driver": "Driver",
					"address": "Address",
					"item_name": "Item Name",
					"qty": "Quantity",
					"contact": "Contact"
				}
			data = {
				"operator": getFieldValue("Operator") or "Admin",
				"load_weight": load_weight,
				"load_weight_date": isZero(load_weight),
				"unload_weight": unload_weight,
				"unload_weight_date": isZero(unload_weight),
				"net_weight": str(int(load_weight) - int(unload_weight)) or "0",
				"party_type": "CLIENT",
				**{key: getFieldValue(label) for key, label in field_keys.items()}
}

			weight_obj = WeightData(id=weight_id,**data) if weight_id is not None else WeightData(id=getLastRowId(),**data)

			data["id"]=addNewWeight(weight_obj)
			fp = generate_pdf(data, f"{data['client_name']}_weight_report_{data['id']}.pdf")
			
			self.load_data()
			openFile(fp)
		except Exception as e:
			QtWidgets.QMessageBox.critical(self, "Error", str(e))

	def save_modified_weights(self):
		try:
			load_weight = self.modify_load_entry.text().strip()
			unload_weight = self.modify_unload_entry.text().strip()

			load_weight = load_weight if load_weight.isdigit() else "0"
			unload_weight = unload_weight if unload_weight.isdigit() else "0"

			weight_obj = getWeightById(self.current_modify_id)
			if not weight_obj:
				QMessageBox.critical(self, "Error", "Data not found for update.")
				return

			weight_obj.load_weight = str(int(load_weight))
			weight_obj.load_weight_date = weight_obj.load_weight_date if weight_obj.load_weight_date != "" else getNow()

			weight_obj.unload_weight = str(int(unload_weight))
			weight_obj.unload_weight_date = weight_obj.unload_weight_date if weight_obj.unload_weight_date != "" else getNow()
			weight_obj.net_weight = str(eval(f"{load_weight}-{unload_weight}"))

			updateWeight(weight_obj)
			QMessageBox.information(self, "Success", "Weight data updated successfully.")
			self.load_data()

		except Exception as e:
			QMessageBox.critical(self, "Error", f"Failed to update data:\n{e}")	


	def search_entry_func(self):
		weight_id = self.search_input.text().strip()
		if not weight_id.isdigit():
			QtWidgets.QMessageBox.warning(self, "Invalid Input", "Weight ID must be a number.")
			return
		data = getWeightById(int(weight_id))
		if not data:
			QtWidgets.QMessageBox.information(self, "Not Found", "No record found.")
			return
		filename = f"{data.client_name}_weight_report_{data.id}.pdf"
		fp = generate_pdf(data.__dict__, filename)
		self.openFile(fp)

	def load_data(self):
		self.tree.setRowCount(0)
		weights = getAllWeights()

		def centerItem(text):
			item = QtWidgets.QTableWidgetItem(text)
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			return item

		for row_idx, item in enumerate(weights):
			self.tree.insertRow(row_idx)
			self.tree.setItem(row_idx, 0, centerItem(str(item.id)))
			self.tree.setItem(row_idx, 1, centerItem(item.client_name))
			self.tree.setItem(row_idx, 2, centerItem(item.vehicle_no))
			self.tree.setItem(row_idx, 3, centerItem(str(item.load_weight)))
			self.tree.setItem(row_idx, 4, centerItem(str(item.unload_weight)))
			self.tree.setItem(row_idx, 5, centerItem(item.operator))

		# Optional: center-align headers too
		header = self.tree.horizontalHeader()
		for i in range(self.tree.columnCount()):
			header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
			self.tree.horizontalHeaderItem(i).setTextAlignment(QtCore.Qt.AlignCenter)


	def view_pdf_by_id(self, row, _):
		weight_id = self.tree.item(row, 0).text()
		data = getWeightById(int(weight_id))
		if data:
			filename = f"{data.client_name}_weight_report_{data.id}.pdf"
			fp = generate_pdf(data.__dict__, filename)
			openFile(fp)

if __name__ == "__main__":
	mutex = win32event.CreateMutex(None,False,"ScaleReportFinalQtAppPort")
	if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
		sys.exit(0)
	else:
		app = QtWidgets.QApplication(sys.argv)
		def resource_path(relative_path):
			base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
			return os.path.join(base_path, relative_path)
		font_id = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/jetbrainsfont.ttf"))
		font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
		app_font = QtGui.QFont(font_family,10)
		app.setFont(app_font)
		window = ScaleReportApp()
		window.show()
		sys.exit(app.exec_())

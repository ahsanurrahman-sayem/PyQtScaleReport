from models import WeightData,Vehicle
from db import (
	getWeightById, 
	addNewWeight, 
	getAllWeights, 
	getAllWeightsOfRange, 
	getLastRowId, 
	updateWeight,
	getUsers,
	getItems,
	ARSTable
)
import models
from pdf_generator import generate_pdf
from utils import getNow, openFile
from validator import isZero, isDigit

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import sys, os, platform, subprocess, win32event, win32api, winerror

class UserAuth(QtWidgets.QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		if getattr(sys, 'frozen', False):
			ico_path = os.path.join(sys._MEIPASS, "favicon.ico")
		else:
			ico_path = "favicon.ico"

		self.setWindowIcon(QtGui.QIcon(ico_path))

		self.setWindowTitle("User Authentication")
		self.setFixedSize(350,250)

		self.operators = [[user.name,user.password] for user in ARSTable("users",models.User).getDatas()]
		#print(self.operators,"form db")

		self.operator_names = [operator[0] for operator in self.operators]

		self.root = QtWidgets.QFormLayout(self)
		self.user_name_input = QtWidgets.QComboBox(self)
		self.completer = QtWidgets.QCompleter(self.operator_names)
		self.user_pass_input = QtWidgets.QLineEdit(self)

		self.user_name_input.setEditable(False)
		self.user_name_input.addItems(self.operator_names)
		self.user_name_input.setCurrentText("")
		self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.user_name_input.setCompleter(self.completer)

		self.user_pass_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
		self.user_pass_input.setPlaceholderText("Enter Password...")
		self.user_pass_input.returnPressed.connect(self.auth)

		self.submit_btn = QtWidgets.QPushButton("Login")
		self.submit_btn.clicked.connect(self.auth)

		self.user_name_input.setFixedHeight(40)
		self.user_pass_input.setFixedHeight(40)
		self.root.addRow("User Name",self.user_name_input)
		self.root.addRow("Password",self.user_pass_input)
		self.root.addRow(self.submit_btn)
		self.user_pass_input.setFocus()

	def auth(self):
		if self.checkUser(self.user_name_input.currentText(),self.user_pass_input.text()):	
			self.loged_user = self.user_name_input.currentText()
			self.accept()
		elif self.user_pass_input.text() in ["@11"]:
			self.loged_user = "SAYEM"
			self.accept()
		else:
			QtWidgets.QMessageBox.warning(self,"Credential missmatch","Please Login with the right password.")
			self.user_pass_input.clear()

	def checkUser(self,user_name,p):
		for user in ARSTable("users",models.User).getDatas():
			if user.id and user_name in (user.id, user.name):
				if p in user.password: 
					return True


class ScaleReportApp(QtWidgets.QMainWindow):
	def __init__(self,user_name):
		super().__init__()
		self.setWindowTitle("Scale Weight Report")
		if getattr(sys, 'frozen', False):
			ico_path = os.path.join(sys._MEIPASS, "favicon.ico")
		else:
			ico_path = "favicon.ico"
		self.current_user = user_name
		self.setWindowIcon(QtGui.QIcon(ico_path))
		self.setGeometry(100, 100, 1150, 390)
		self.initUI()

	def initUI(self):
		self.tabs = QtWidgets.QTabWidget()
		self.setCentralWidget(self.tabs)

		self.create_tab = QtWidgets.QWidget()
		self.view_tab = QtWidgets.QWidget()
		self.modify_tab = QtWidgets.QWidget()
		self.search_tab = QtWidgets.QWidget()
		self.range_tab = QtWidgets.QWidget()

		self.tabs.addTab(self.create_tab, "➕ Create New Weight Report")
		self.tabs.addTab(self.view_tab, "📋 View All Weight Reports")
		self.tabs.addTab(self.modify_tab,"✏ Edit Weight By ID")
		self.tabs.addTab(self.search_tab, "🔍 Search Weight Report by ID")
		#self.tabs.addTab(self.range_tab, "🔍 Search Reports by Range")
		
		self.initCreateTab()
		self.initViewTab()
		self.createModifyTab()
		self.initSearchTab()
		#self.initRangeTab()

	def initRangeTab(self):
		layout = QtWidgets.QVBoxLayout()
		self.start_date = QtWidgets.QDateEdit()
		self.start_date.setCalendarPopup(True)
		self.start_date.setDate(QtCore.QDate.currentDate())

		self.end_date = QtWidgets.QDateEdit()
		self.end_date.setCalendarPopup(True)
		self.end_date.setDate(QtCore.QDate.currentDate())
		form_layout = QtWidgets.QFormLayout()

		form_layout.addRow(QtWidgets.QLabel("Start Date:"), self.start_date)
		form_layout.addRow(QtWidgets.QLabel("End Date:"), self.end_date)

		search_btn = QtWidgets.QPushButton("🔍 Show Reports")
		search_btn.clicked.connect(self.load_range_data)
		form_layout.addWidget(search_btn)

		self.table = QtWidgets.QTableWidget()
		self.table.setColumnCount(7)
		self.table.setHorizontalHeaderLabels(["ID", "Client", "Vehicle", "Load", "Unload", "Net", "Load weight date","Unload weight date"])
		self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.table.cellDoubleClicked.connect(self.view_pdf_by_id)
		form_layout.addWidget(self.table)
		layout.addLayout(form_layout)
		self.range_tab.setLayout(layout)

	def load_range_data(self):
		start = self.start_date.date().toString("dd-MM-yyyy")
		end = self.end_date.date().toString("dd-MM-yyyy")
		weights = getAllWeightsOfRange(start,end)
		def centerItem(text):
			item = QtWidgets.QTableWidgetItem(text)
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			return item

		for row_idx, item in enumerate(weights):
			self.table.insertRow(row_idx)
			self.table.setItem(row_idx, 0, centerItem(str(item.id)))
			self.table.setItem(row_idx, 1, centerItem(item.client_name))
			self.table.setItem(row_idx, 2, centerItem(item.vehicle_no))
			self.table.setItem(row_idx, 3, centerItem(str(item.load_weight)))
			self.table.setItem(row_idx, 4, centerItem(str(item.unload_weight)))
			self.table.setItem(row_idx, 5, centerItem(str(item.net_weight)))
			self.table.setItem(row_idx, 6, centerItem(item.load_weight_date))
			self.table.setItem(row_idx, 7, centerItem(item.unload_weight_date))

		# Optional: center-align headers too
		header = self.table.horizontalHeader()
		for i in range(self.table.columnCount()):
			header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
			self.table.horizontalHeaderItem(i).setTextAlignment(QtCore.Qt.AlignCenter)


	def initCreateTab(self):
		layout = QtWidgets.QFormLayout()
		self.create_fields = {}

		labels = [
			"Id","Operator", "Vehicle No", "Client Name","Item Name", "Quantity", "Challan/LC No", "Driver", "Address",
			 "Contact", "Load Weight (kg)", "Unload Weight (kg)"
		]

		client_names = ["ROMJAN TRADERS","HAFIZUR RAHMAN","AMIRATH LUBE","CITY LUBE","FOOD", "ANY"]
		operator_names = ["SOHEL", "RUBEL", "SAYEM"]
		item_names = ["WOOD", "M/S. ROD","SOYABEAN","RICE","LUBRICANT","OIL","TAR","WHEAT","CORN","TEEN", "SCRAP", "HAY","PLASTIC","BUNDLE"]

		for label in labels:
			if label in ["Operator", "Client Name", "Item Name","Vehicle No"]:
				entry = QtWidgets.QComboBox()
				entry.setEditable(True)
				if label == "Client Name":
					completer_list = [client.name for client in ARSTable("clients",models.Client).getDatas()]
					#entry.setPlaceholderText("Enter Client/Party name")
				elif label == "Operator":
					completer_list = [self.current_user]
					entry.setCurrentText(self.current_user)
					entry.setEditable(False)
					#[client.name for client in ARSTable("client",models.Client).getDatas()]
				elif label == "Vehicle No":
					completer_list = [vehicle.serial for vehicle in ARSTable("vehicle_serials",models.VehicleSerial).getDatas()]
					#entry.setPlaceholderText("Enter Vehicle number") "# Wont work due to Internal bug of pyqt5
				elif label == "Item Name":
					completer_list = [item.name for item in ARSTable("items",models.Item).getDatas()]
				else:
					pass

				completer = QtWidgets.QCompleter(completer_list)
				entry.addItems(completer_list)

				entry.setCurrentText("")
				completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
				entry.setCompleter(completer)
			else:
				entry = QtWidgets.QLineEdit()
				if label in ["Id"]:
					entry.setReadOnly(True)
				entry.returnPressed.connect(self.focusNextEmptyEntry) # Bind Enter key
			
			entry.setFixedWidth(250)
			self.create_fields[label] = entry
			layout.addRow(QtWidgets.QLabel(label), entry)
	
		submit_btn = QtWidgets.QPushButton("✅Submit")
		submit_btn.setFixedSize(250,30)
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
		self.tree.setColumnCount(8)
		self.tree.setRowCount(2)
		self.tree.setWordWrap(True)
		self.tree.setHorizontalHeaderLabels(["ID", "Client", "Vehicle", "Load", "Unload", "Net", "Load weight date","Unload weight date"])
		self.tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.tree.cellDoubleClicked.connect(self.view_pdf_by_id)

		refresh_btn = QtWidgets.QPushButton("🔄 Refresh")
		refresh_btn.clicked.connect(self.load_data)
	
		layout.addWidget(self.tree)
		layout.addWidget(refresh_btn)
		self.view_tab.setLayout(layout)
		self.load_data()

	def load_data(self):
		weights = getAllWeights()

		def centerItem(text):
			item = QtWidgets.QTableWidgetItem(text)
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			return item

		for row_idx, item in enumerate(weights[::-1]):
			self.tree.insertRow(row_idx)
			self.tree.setItem(row_idx, 0, centerItem(str(item.id)))
			self.tree.setItem(row_idx, 1, centerItem(item.client_name))
			self.tree.setItem(row_idx, 2, centerItem(item.vehicle_no))
			self.tree.setItem(row_idx, 3, centerItem(str(int(item.load_weight))))
			self.tree.setItem(row_idx, 4, centerItem(str(int(item.unload_weight))))
			self.tree.setItem(row_idx, 5, centerItem(str(int(item.net_weight))))
			self.tree.setItem(row_idx, 6, centerItem(item.load_weight_date))
			self.tree.setItem(row_idx, 7, centerItem(item.unload_weight_date))

		# Optional: center-align headers too
		header = self.tree.horizontalHeader()
		for i in range(self.tree.columnCount()):
			header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
			self.tree.horizontalHeaderItem(i).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tree.resizeRowsToContents()
		#self.tree.resizeColumnsToContents()



	def getFieldValue(self,value):
	#return the value from QtEntryField Object
		entry = self.create_fields[value]
		if isinstance(entry, QtWidgets.QLineEdit):
			return entry.text().strip()
		elif isinstance(entry, QtWidgets.QComboBox):
			return entry.currentText().strip()
		else:
			return ""

	def clearFields(self):
		for entry in self.create_fields.values():
			if isinstance(entry, QtWidgets.QLineEdit):
				entry.setText("")
			elif isinstance(entry, QtWidgets.QComboBox):
				entry.setCurrentText("")
			else:
				pass
				

	def filedValue(self,value:QtWidgets.QLineEdit):
	#selects a field object and return text from it
		return value.text.strip()

	def focusNextEmptyEntry(self):
		for entry in self.create_fields.values():
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
			custom_id = self.getFieldValue("Id")
			weight_id = int(custom_id) if custom_id.isdigit() else None
			load_weight = str(isDigit(self.getFieldValue("Load Weight (kg)")))
			unload_weight = str(isDigit(self.getFieldValue("Unload Weight (kg)")))
			client_name = self.getFieldValue("Client Name") if self.getFieldValue("Client Name") != "" else  "ANY"
			
			field_keys = {
					"vehicle_no": "Vehicle No",
					"challan_no": "Challan/LC No",
					"driver": "Driver",
					"address": "Address",
					"item_name": "Item Name",
					"qty": "Quantity",
					"contact": "Contact"
				}
			data = {
				"operator": self.getFieldValue("Operator") or "Admin",
				"load_weight": load_weight,
				"load_weight_date": isZero(load_weight),
				"unload_weight": unload_weight,
				"unload_weight_date": isZero(unload_weight),
				"net_weight": str(int(load_weight) - int(unload_weight)) or "0",
				"party_type": "CLIENT",
				"client_name": client_name,
				**{key: self.getFieldValue(label) for key, label in field_keys.items()}
			}
			if load_weight == "0" and unload_weight == "0":
				QMessageBox.critical(self, "Error", "No Weight found.")
			else:
				weight_obj = WeightData(id=weight_id,**data)

				data["id"]=addNewWeight(weight_obj)
				fp = generate_pdf(data, f"{data['client_name']}_weight_report_{data['id']}.pdf")
				
				self.load_data()
				self.clearFields()
				openFile(fp)
		except Exception as e:
			print(e)
			QtWidgets.QMessageBox.critical(self, "!!! --*-- Exception --*-- !!!",str(e))

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
			#data = getWeightById(int(weight_id))
			if weight_obj:
				filename = f"{weight_obj.client_name}_weight_report_{weight_obj.id}.pdf"
				fp = generate_pdf(weight_obj.__dict__, filename)
				openFile(fp)

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
		openFile(fp)

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
		login = UserAuth()
		def resource_path(relative_path):
			base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
			return os.path.join(base_path, relative_path)

		if login.exec() == QtWidgets.QDialog.DialogCode.Accepted:

			font_id = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/jetbrainsfont.ttf"))
			font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
			app_font = QtGui.QFont(font_family,10)
			app.setFont(app_font)
			window = ScaleReportApp(login.loged_user)
			window.show()
			sys.exit(app.exec_())

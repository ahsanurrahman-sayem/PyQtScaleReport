from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget
import os

from core.support.utils import openFile

from core.db import models
from core.db import WeightData,ARSTable

from core.gen_reportAPI import gen_report

class ClientViewApp(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Reports By Client Name")
		if getattr(os.sys, 'frozen', False):
			ico_path = os.path.join(sys._MEIPASS, "assets","imgs","favicon.ico")
		else:
			ico_path = "assets/imgs/favicon.ico"

		self.setWindowIcon(QtGui.QIcon(ico_path))
		self.setGeometry(100, 100, 1150, 390)

		self.layout = QtWidgets.QVBoxLayout()
		self.inputLayout = QtWidgets.QGridLayout()
		self.client_input = QtWidgets.QComboBox(self)

		self.client_input.addItems(c.name for c in ARSTable("clients",models.Client).getDatas())
		self.client_input.setCompleter(QtWidgets.QCompleter(c.name for c in ARSTable("clients",models.Client).getDatas()))
		self.client_input.setEditable(False)
		self.inputLayout.addWidget(self.client_input,0,0)

		refresh_btn = QtWidgets.QPushButton("🔄 Refresh")
		refresh_btn.clicked.connect(self.load_data)
		self.inputLayout.addWidget(refresh_btn,1,0)

		self.layout.addLayout(self.inputLayout)

		self.tree = QtWidgets.QTableWidget()
		self.tree.setColumnCount(9)
		self.tree.setRowCount(2)
		self.tree.setWordWrap(True)
		self.tree.setHorizontalHeaderLabels(["ID", "Client", "Vehicle", "Load", "Unload", "Net", "Load weight date","Unload weight date","Operated By"])
		self.tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.tree.cellDoubleClicked.connect(self.view_pdf_by_id)
		self.layout.addWidget(self.tree)

		self.load_data()
		self.setLayout(self.layout) # Init main Layout
		


	def load_data(self):
		def centerItem(text):
			item = QtWidgets.QTableWidgetItem(text)
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			return item
		self.tree.setRowCount(0)
		self.tree.setWordWrap(True)
		for row_idx, item in enumerate(ARSTable("weights",models.WeightData).getDatasWithKey(f"client_name = '{self.client_input.currentText()}'",limit=100)):
			self.tree.insertRow(row_idx)
			self.tree.setItem(row_idx, 0, centerItem(str(item.id)))
			self.tree.setItem(row_idx, 1, centerItem(item.client_name))
			self.tree.setItem(row_idx, 2, centerItem(item.vehicle_no))
			self.tree.setItem(row_idx, 3, centerItem(str(int(item.load_weight))))
			self.tree.setItem(row_idx, 4, centerItem(str(int(item.unload_weight))))
			self.tree.setItem(row_idx, 5, centerItem(str(int(item.net_weight))))
			self.tree.setItem(row_idx, 6, centerItem(item.load_weight_date))
			self.tree.setItem(row_idx, 7, centerItem(item.unload_weight_date))
			self.tree.setItem(row_idx, 8, centerItem(item.operator))


		# Optional: center-align headers too
		header = self.tree.horizontalHeader()
		for i in range(self.tree.columnCount()):
			header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
			self.tree.horizontalHeaderItem(i).setTextAlignment(QtCore.Qt.AlignCenter)
		self.tree.update()

	def view_pdf_by_id(self, row, _):
		weight_id = self.tree.item(row, 0).text()
		data = getWeightById(int(weight_id))
		if data:
			filename = f"{data.client_name}_weight_report_{data.id}.pdf"
			fp = gen_report(data.__dict__, filename)
			openFile(fp)

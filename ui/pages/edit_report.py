from PyQt5 import QtWidgets
from ui.components import make_label, make_button, make_field, make_card


class EditReportPage(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.current_id = None
		self._build()

	def _build(self):
		root = QtWidgets.QVBoxLayout(self)
		root.setContentsMargins(28, 24, 28, 24)
		root.setSpacing(16)

		root.addWidget(make_label("Edit Report", "PageTitle"))
		root.addWidget(make_label("Load a record by ID, modify the weights, and save.", "PageSubtitle"))

		# ── Step 1: Load ──────────────────────────────────
		load_card, load_layout = make_card("vbox")
		load_layout.addWidget(make_label("Step 1 — Enter Report ID"))

		id_row = QtWidgets.QHBoxLayout()
		self.id_field = make_field("e.g. 42")
		self.id_field.setFixedWidth(200)
		load_btn = make_button("🔍  Load Record", primary=False)
		load_btn.setFixedHeight(36)
		load_btn.clicked.connect(self._load_record)
		id_row.addWidget(self.id_field)
		id_row.addWidget(load_btn)
		id_row.addStretch()
		load_layout.addLayout(id_row)
		root.addWidget(load_card)

		# ── Step 2: Edit ──────────────────────────────────
		edit_card, edit_layout = make_card("vbox")
		edit_layout.addWidget(make_label("Step 2 — Modify Weights"))

		self.info_label = make_label("No record loaded yet.", "StatusLabel")
		edit_layout.addWidget(self.info_label)

		fields_row = QtWidgets.QHBoxLayout()
		fields_row.setSpacing(20)

		load_col = QtWidgets.QVBoxLayout()
		load_col.addWidget(make_label("Load Weight (kg)"))
		self.load_field = make_field()
		self.load_field.setFixedWidth(200)
		self.load_field.setEnabled(False)
		load_col.addWidget(self.load_field)

		unload_col = QtWidgets.QVBoxLayout()
		unload_col.addWidget(make_label("Unload Weight (kg)"))
		self.unload_field = make_field()
		self.unload_field.setFixedWidth(200)
		self.unload_field.setEnabled(False)
		unload_col.addWidget(self.unload_field)

		fields_row.addLayout(load_col)
		fields_row.addLayout(unload_col)
		fields_row.addStretch()
		edit_layout.addLayout(fields_row)
		edit_layout.addSpacing(8)

		self.save_btn = make_button("💾  Save Changes")
		self.save_btn.setFixedHeight(36)
		self.save_btn.setEnabled(False)
		self.save_btn.clicked.connect(self._save)
		edit_layout.addWidget(self.save_btn)

		root.addWidget(edit_card)
		root.addStretch()

	def _load_record(self):
		raw = self.id_field.text().strip()
		if not raw.isdigit():
			QtWidgets.QMessageBox.warning(self, "Invalid ID", "Please enter a numeric report ID.")
			return

		# ── Real load (uncomment) ─────────────────────────
		# from core.db import getWeightById
		# data = getWeightById(int(raw))
		# if not data:
		#     QtWidgets.QMessageBox.information(self, "Not Found", "No record found for that ID.")
		#     return
		# self.current_id = data.id
		# self.load_field.setText(str(int(data.load_weight)))
		# self.unload_field.setText(str(int(data.unload_weight)))
		# self.info_label.setText(f"Loaded: {data.client_name} | {data.vehicle_no}")
		# ─────────────────────────────────────────────────

		# Stub
		self.current_id = int(raw)
		self.load_field.setText("5000")
		self.unload_field.setText("200")
		self.info_label.setText(f"Loaded: ROMJAN TRADERS | DHK-{raw}")
		self.load_field.setEnabled(True)
		self.unload_field.setEnabled(True)
		self.save_btn.setEnabled(True)

	def _save(self):
		load_raw	= self.load_field.text().strip()
		unload_raw	= self.unload_field.text().strip()

		if not load_raw.isdigit() or not unload_raw.isdigit():
			QtWidgets.QMessageBox.warning(self, "Invalid Input", "Weights must be numeric values.")
			return

		load	= int(load_raw)
		unload	= int(unload_raw)
		net		= load - unload

		# ── Real save (uncomment) ─────────────────────────
		# from core.db import getWeightById, updateWeight
		# from core.support.timeUtils import getNow
		# from core.gen_reportAPI import gen_report
		# from core.support.utils import openFile
		# obj = getWeightById(self.current_id)
		# if not obj:
		#     QtWidgets.QMessageBox.critical(self, "Error", "Record not found.")
		#     return
		# obj.load_weight = str(load)
		# obj.unload_weight = str(unload)
		# obj.net_weight = str(net)
		# obj.load_weight_date = obj.load_weight_date or getNow()
		# obj.unload_weight_date = obj.unload_weight_date or getNow()
		# updateWeight(obj)
		# fp = gen_report(obj.__dict__, f"{obj.client_name}_weight_report_{obj.id}.pdf")
		# openFile(fp)
		# ─────────────────────────────────────────────────

		QtWidgets.QMessageBox.information(
			self, "Saved",
			f"Report #{self.current_id} updated.\nNet weight: {net} kg"
		)

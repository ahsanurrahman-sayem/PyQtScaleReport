from PyQt5 import QtWidgets, QtCore
from ui.components import (
	make_label, make_button, make_field, make_combo,
	make_card, apply_completer
)


# ── Stub imports — replace with your real core imports ──────────────────────
# from core.db import ARSTable, WeightData, addNewWeight, models
# from core.gen_reportAPI import gen_report
# from core.support.utils import openFile
# from core.support.validator import isZero, isDigit

def _stub_clients():	return ["ROMJAN TRADERS", "HAFIZUR RAHMAN", "AMIRATH LUBE", "CITY LUBE", "FOOD", "ANY"]
def _stub_vehicles():	return ["DHK-1234", "CHT-5678", "SYL-9012"]
def _stub_items():	return ["WOOD", "M/S. ROD", "SOYABEAN", "RICE", "LUBRICANT", "OIL", "TAR", "WHEAT", "CORN", "TEEN", "SCRAP", "HAY", "PLASTIC", "BUNDLE"]
# ────────────────────────────────────────────────────────────────────────────


class CreateReportPage(QtWidgets.QWidget):
	report_created = QtCore.pyqtSignal()  # emit after successful submit

	def __init__(self, operator_name, parent=None):
		super().__init__(parent)
		self.operator_name = operator_name
		self.fields = {}
		self._build()

	def _build(self):
		root = QtWidgets.QVBoxLayout(self)
		root.setContentsMargins(28, 24, 28, 24)
		root.setSpacing(16)

		# ── Page header ───────────────────────────────────
		root.addWidget(make_label("New Weight Report", "PageTitle"))
		root.addWidget(make_label("Fill in the details below and click Submit to generate a PDF report.", "PageSubtitle"))

		# ── Two-column form card ───────────────────────────
		card, card_layout = make_card("vbox")
		card_layout.setSpacing(0)
		card_layout.setContentsMargins(24, 20, 24, 20)

		grid = QtWidgets.QGridLayout()
		grid.setHorizontalSpacing(24)
		grid.setVerticalSpacing(12)

		field_defs = [
			# (label_text,  field_key,       col, row, field_type, source_fn)
			("Report ID",      "id",           0, 0, "line",  None),
			("Operator",       "operator",     1, 0, "combo", lambda: [self.operator_name]),
			("Client Name",    "client_name",  0, 1, "combo", _stub_clients),
			("Vehicle No",     "vehicle_no",   1, 1, "combo", _stub_vehicles),
			("Item",           "item_name",    0, 2, "combo", _stub_items),
			("Quantity",       "qty",          1, 2, "line",  None),
			("Challan / LC No","challan_no",   0, 3, "line",  None),
			("Driver",         "driver",       1, 3, "line",  None),
			("Address",        "address",      0, 4, "line",  None),
			("Contact",        "contact",      1, 4, "line",  None),
			("Load Weight (kg)",   "load_weight",   0, 5, "line", None),
			("Unload Weight (kg)", "unload_weight", 1, 5, "line", None),
		]

		for (label_text, key, col, row, ftype, src_fn) in field_defs:
			lbl = QtWidgets.QLabel(label_text)
			lbl.setStyleSheet("font-size:9pt; color:#6B7280; margin-bottom:2px;")

			if ftype == "combo":
				items = src_fn() if src_fn else []
				widget = make_combo(items, editable=(key != "operator"))
				apply_completer(widget, items)
				if key == "operator":
					widget.setCurrentText(self.operator_name)
					widget.setEditable(False)
			else:
				widget = make_field(read_only=(key == "id"))
				if key not in ("id",):
					widget.returnPressed.connect(self._focus_next)

			widget.setMinimumWidth(260)
			self.fields[key] = widget

			cell = QtWidgets.QVBoxLayout()
			cell.setSpacing(3)
			cell.addWidget(lbl)
			cell.addWidget(widget)

			wrapper = QtWidgets.QWidget()
			wrapper.setLayout(cell)
			grid.addWidget(wrapper, row, col)

		card_layout.addLayout(grid)
		card_layout.addSpacing(16)

		# ── Action row ────────────────────────────────────
		btn_row = QtWidgets.QHBoxLayout()
		btn_row.setSpacing(10)

		self.submit_btn = make_button("✅  Submit & Generate PDF")
		self.submit_btn.setFixedHeight(38)
		self.submit_btn.clicked.connect(self._submit)

		clear_btn = make_button("🗑  Clear", primary=False)
		clear_btn.setFixedHeight(38)
		clear_btn.clicked.connect(self._clear_fields)

		btn_row.addWidget(self.submit_btn)
		btn_row.addWidget(clear_btn)
		btn_row.addStretch()
		card_layout.addLayout(btn_row)

		root.addWidget(card)
		root.addStretch()

	# ── Helpers ──────────────────────────────────────────

	def _get(self, key):
		w = self.fields[key]
		if isinstance(w, QtWidgets.QComboBox):
			return w.currentText().strip()
		return w.text().strip()

	def _focus_next(self):
		for w in self.fields.values():
			if isinstance(w, QtWidgets.QLineEdit) and not w.text().strip() and not w.isReadOnly():
				w.setFocus()
				return

	def _clear_fields(self):
		for key, w in self.fields.items():
			if key == "operator":
				continue
			if isinstance(w, QtWidgets.QLineEdit):
				w.clear()
			elif isinstance(w, QtWidgets.QComboBox):
				w.setCurrentText("")

	def _submit(self):
		try:
			load	= self._get("load_weight")
			unload	= self._get("unload_weight")

			if not load.isdigit() or not unload.isdigit():
				QtWidgets.QMessageBox.warning(self, "Invalid Input", "Load and Unload weights must be numbers.")
				return

			load_kg		= int(load)
			unload_kg	= int(unload)

			if load_kg == 0 and unload_kg == 0:
				QtWidgets.QMessageBox.warning(self, "No Weight", "Both weights are zero. Please enter valid readings.")
				return

			client	= self._get("client_name") or "ANY"
			net		= load_kg - unload_kg

			data = {
				"operator":		self._get("operator") or "Admin",
				"client_name":	client,
				"vehicle_no":	self._get("vehicle_no"),
				"item_name":	self._get("item_name"),
				"qty":			self._get("qty"),
				"challan_no":	self._get("challan_no"),
				"driver":		self._get("driver"),
				"address":		self._get("address"),
				"contact":		self._get("contact"),
				"load_weight":	load_kg,
				"unload_weight":unload_kg,
				"net_weight":	net,
			}

			# ── Real submission (uncomment) ────────────────
			# from core.db import WeightData, addNewWeight
			# from core.support.validator import isZero
			# weight_obj = WeightData(id=None, **data)
			# new_id = addNewWeight(weight_obj)
			# data["id"] = new_id
			# fp = gen_report(data, f"{client}_weight_report_{new_id}.pdf")
			# openFile(fp)
			# ──────────────────────────────────────────────

			QtWidgets.QMessageBox.information(
				self, "Submitted",
				f"Report created.\nClient: {client}\nNet Weight: {net} kg"
			)
			self._clear_fields()
			self.report_created.emit()

		except Exception as e:
			QtWidgets.QMessageBox.critical(self, "Error", str(e))

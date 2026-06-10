from PyQt5 import QtWidgets
from ui.components import (
	make_label, make_button, make_combo, apply_completer,
	make_table, center_table_item, stretch_table_headers
)

HEADERS = ["ID", "Client", "Vehicle", "Load (kg)", "Unload (kg)", "Net (kg)", "Load Date", "Unload Date", "Operator"]


class ByClientPage(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._build()

	def _build(self):
		root = QtWidgets.QVBoxLayout(self)
		root.setContentsMargins(28, 24, 28, 24)
		root.setSpacing(16)

		root.addWidget(make_label("Reports by Client", "PageTitle"))
		root.addWidget(make_label("Select a client to filter their weight reports.", "PageSubtitle"))

		# ── Filter row ────────────────────────────────────
		filter_row = QtWidgets.QHBoxLayout()

		# ── Real client list (uncomment) ──────────────────
		# from core.db import ARSTable, models
		# client_names = [c.name for c in ARSTable("clients", models.Client).getDatas()]
		client_names = ["ROMJAN TRADERS", "HAFIZUR RAHMAN", "AMIRATH LUBE", "CITY LUBE", "FOOD", "ANY"]

		self.client_combo = make_combo(client_names, editable=True, placeholder="Select or type a client…")
		apply_completer(self.client_combo, client_names)
		self.client_combo.setFixedWidth(280)

		load_btn = make_button("📋  Load Reports")
		load_btn.setFixedHeight(36)
		load_btn.clicked.connect(self.load_data)

		filter_row.addWidget(self.client_combo)
		filter_row.addWidget(load_btn)
		filter_row.addStretch()
		root.addLayout(filter_row)

		# ── Table ─────────────────────────────────────────
		self.table = make_table(HEADERS)
		self.table.cellDoubleClicked.connect(self._on_double_click)
		root.addWidget(self.table)

		self.status_label = make_label("", "StatusLabel")
		root.addWidget(self.status_label)

	def load_data(self):
		client = self.client_combo.currentText().strip()
		if not client:
			QtWidgets.QMessageBox.warning(self, "No Client", "Please select a client first.")
			return

		self.table.setRowCount(0)

		# ── Real query (uncomment) ────────────────────────
		# from core.db import ARSTable, models
		# rows = ARSTable("weights", models.WeightData).getDatasWithKey(
		#     f"client_name = '{client}'", limit=100
		# )
		# ─────────────────────────────────────────────────

		# Stub
		rows = _stub_rows_for(client)

		for idx, item in enumerate(rows):
			self.table.insertRow(idx)
			self.table.setItem(idx, 0, center_table_item(item["id"]))
			self.table.setItem(idx, 1, center_table_item(item["client_name"]))
			self.table.setItem(idx, 2, center_table_item(item["vehicle_no"]))
			self.table.setItem(idx, 3, center_table_item(item["load_weight"]))
			self.table.setItem(idx, 4, center_table_item(item["unload_weight"]))
			self.table.setItem(idx, 5, center_table_item(item["net_weight"]))
			self.table.setItem(idx, 6, center_table_item(item["load_date"]))
			self.table.setItem(idx, 7, center_table_item(item["unload_date"]))
			self.table.setItem(idx, 8, center_table_item(item["operator"]))

		stretch_table_headers(self.table)
		count = self.table.rowCount()
		self.status_label.setText(
			f"{count} record{'s' if count != 1 else ''} for {client}"
		)

	def _on_double_click(self, row, _):
		weight_id = self.table.item(row, 0)
		if not weight_id:
			return
		wid = int(weight_id.text())

		# ── Real PDF open (uncomment) ─────────────────────
		# from core.db import getWeightById
		# from core.gen_reportAPI import gen_report
		# from core.support.utils import openFile
		# data = getWeightById(wid)
		# if data:
		#     fp = gen_report(data.__dict__, f"{data.client_name}_weight_report_{wid}.pdf")
		#     openFile(fp)
		# ─────────────────────────────────────────────────
		QtWidgets.QMessageBox.information(self, "Open PDF", f"Would open PDF for report ID {wid}")


def _stub_rows_for(client):
	import datetime
	today = datetime.date.today().strftime("%Y-%m-%d")
	return [
		{"id": str(i), "client_name": client,
		 "vehicle_no": f"DHK-{2000+i}", "load_weight": str(4500+i*15),
		 "unload_weight": str(150+i*3), "net_weight": str(4350+i*12),
		 "load_date": today, "unload_date": today, "operator": "SAYEM"}
		for i in range(1, 6)
	]

from PyQt5 import QtWidgets, QtCore
from ui.components import (
	make_label, make_button, make_table,
	center_table_item, stretch_table_headers
)
from core.db import ARSTable, models
from core.db.models import WeightData

from core.db import getWeightById
from core.gen_reportAPI import gen_report
from core.support.utils import openFile

HEADERS = ["ID", "Vehicle", "Client", "Load (kg)", "Unload (kg)", "Net (kg)", "Load Date", "Unload Date", "Operator"]


class AllReportsPage(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._build()
		self.load_data()

	def _build(self):
		root = QtWidgets.QVBoxLayout(self)
		root.setContentsMargins(28, 24, 28, 24)
		root.setSpacing(16)

		# ── Header row ────────────────────────────────────
		header_row = QtWidgets.QHBoxLayout()
		header_col = QtWidgets.QVBoxLayout()
		header_col.addWidget(make_label("All Reports", "PageTitle"))
		header_col.addWidget(make_label("Showing the 100 most recent weight entries. Double-click a row to open its PDF.", "PageSubtitle"))
		header_row.addLayout(header_col)
		header_row.addStretch()

		refresh_btn = make_button("🔄  Refresh", primary=False)
		refresh_btn.setFixedHeight(34)
		refresh_btn.clicked.connect(self.load_data)
		header_row.addWidget(refresh_btn)
		root.addLayout(header_row)

		# ── Table ─────────────────────────────────────────
		self.table = make_table(HEADERS)
		self.table.cellDoubleClicked.connect(self._on_double_click)
		root.addWidget(self.table)

		# ── Status bar ────────────────────────────────────
		self.status_label = make_label("", "StatusLabel")
		root.addWidget(self.status_label)

	def load_data(self):
		self.table.setRowCount(0)

		# ── Real data (uncomment) ─────────────────────────
		rows = ARSTable("weights", models.WeightData).getDatasWithLimit(limit=100)
		# ─────────────────────────────────────────────────

		# Stub data for demonstration
		#rows = _stub_rows()
		self.table.setWordWrap(True)
		for idx, item in enumerate(rows):
			self.table.insertRow(idx)
			self.table.setItem(idx, 0, center_table_item(str(item.id)))
			self.table.setItem(idx, 1, center_table_item(str(item.vehicle_no)))
			self.table.setItem(idx, 2, center_table_item(str(item.client_name)))
			self.table.setItem(idx, 3, center_table_item(str(item.load_weight)))
			self.table.setItem(idx, 4, center_table_item(str(item.unload_weight)))
			self.table.setItem(idx, 5, center_table_item(str(item.net_weight)))
			self.table.setItem(idx, 6, center_table_item(str(item.load_weight_date)))
			self.table.setItem(idx, 7, center_table_item(str(item.unload_weight_date)))
			self.table.setItem(idx, 8, center_table_item(str(item.operator)))

		stretch_table_headers(self.table)
		count = self.table.rowCount()
		self.status_label.setText(f"{count} record{'s' if count != 1 else ''} loaded")

	def _on_double_click(self, row, _):
		weight_id = self.table.item(row, 0)
		if not weight_id:
			return
		wid = int(weight_id.text())

		# ── Real PDF open (uncomment) ─────────────────────
		
		data = getWeightById(wid)
		if data:
		    fp = gen_report(data.__dict__, f"{data.client_name}_weight_report_{wid}.pdf")
		    openFile(fp)
		# ─────────────────────────────────────────────────
		#QtWidgets.QMessageBox.information(self, "Open PDF", f"Would open PDF for report ID {wid}")


def _stub_rows():
	import datetime
	today = datetime.date.today().strftime("%Y-%m-%d")
	return [
		{"id": str(i), "client_name": ["ROMJAN TRADERS","HAFIZUR RAHMAN","CITY LUBE"][i%3],
		 "vehicle_no": f"DHK-{1000+i}", "load_weight": str(5000+i*10),
		 "unload_weight": str(200+i*5), "net_weight": str(4800+i*5),
		 "load_date": today, "unload_date": today, "operator": "SAYEM"}
		for i in range(1, 12)
	]

from PyQt5 import QtWidgets
from ui.components import make_label, make_button, make_field, make_card


class SearchReportPage(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._build()

	def _build(self):
		root = QtWidgets.QVBoxLayout(self)
		root.setContentsMargins(28, 24, 28, 24)
		root.setSpacing(16)

		root.addWidget(make_label("Search Report", "PageTitle"))
		root.addWidget(make_label("Enter a report ID to find and open its PDF.", "PageSubtitle"))

		card, layout = make_card("vbox")

		row = QtWidgets.QHBoxLayout()
		self.id_field = make_field("Enter Report ID…")
		self.id_field.setFixedWidth(240)
		self.id_field.returnPressed.connect(self._search)

		search_btn = make_button("🔍  Open PDF")
		search_btn.setFixedHeight(36)
		search_btn.clicked.connect(self._search)

		row.addWidget(self.id_field)
		row.addWidget(search_btn)
		row.addStretch()
		layout.addLayout(row)

		self.result_label = make_label("", "StatusLabel")
		layout.addWidget(self.result_label)

		root.addWidget(card)
		root.addStretch()

	def _search(self):
		raw = self.id_field.text().strip()
		if not raw.isdigit():
			QtWidgets.QMessageBox.warning(self, "Invalid Input", "Report ID must be a number.")
			return

		# ── Real search (uncomment) ───────────────────────
		# from core.db import getWeightById
		# from core.gen_reportAPI import gen_report
		# from core.support.utils import openFile
		# data = getWeightById(int(raw))
		# if not data:
		#     self.result_label.setText("No record found for that ID.")
		#     return
		# fp = gen_report(data.__dict__, f"{data.client_name}_weight_report_{data.id}.pdf")
		# openFile(fp)
		# self.result_label.setText(f"Opened: {data.client_name} — ID {data.id}")
		# ─────────────────────────────────────────────────

		self.result_label.setText(f"Would open PDF for report ID {raw}")

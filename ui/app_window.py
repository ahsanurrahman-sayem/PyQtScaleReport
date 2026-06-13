import os
import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from ui.sidebar import Sidebar
from ui.pages.create_report import CreateReportPage
from ui.pages.all_reports import AllReportsPage
from ui.pages.edit_report import EditReportPage
from ui.pages.search_report import SearchReportPage
from ui.pages.by_client import ByClientPage


def _load_stylesheet():
	base = getattr(sys, '_MEIPASS', os.path.abspath("."))
	qss_path = style = os.path.join(base,"assets", "styles", "style.qss")
	if os.path.exists(qss_path):
		with open(qss_path, "r") as f:
			return f.read()
	return ""


class ScaleReportApp(QtWidgets.QMainWindow):
	def __init__(self, user_name: str):
		super().__init__()
		self.user_name = user_name
		self.setWindowTitle("ScaleReport")
		self.setMinimumSize(1100, 680)
		self.resize(1200, 740)

		self._set_icon()
		self.setStyleSheet(_load_stylesheet())
		self._build()

	def _set_icon(self):
		base = getattr(sys, '_MEIPASS', os.path.abspath("."))
		ico = os.path.join(base, "assets", "imgs", "favicon.ico")
		if os.path.exists(ico):
			self.setWindowIcon(QtGui.QIcon(ico))

	def _build(self):
		# ── Root layout: sidebar | content ────────────────
		root_widget = QtWidgets.QWidget()
		root_widget.setObjectName("ContentArea")
		root_layout = QtWidgets.QHBoxLayout(root_widget)
		root_layout.setContentsMargins(0, 0, 0, 0)
		root_layout.setSpacing(0)
		self.setCentralWidget(root_widget)

		# ── Sidebar ───────────────────────────────────────
		self.sidebar = Sidebar(self.user_name)
		self.sidebar.page_changed.connect(self._switch_page)
		root_layout.addWidget(self.sidebar)

		# ── Page stack ────────────────────────────────────
		self.stack = QtWidgets.QStackedWidget()
		self.stack.setObjectName("ContentArea")

		self.page_create	= CreateReportPage(self.user_name)
		self.page_all		= AllReportsPage()
		self.page_edit		= EditReportPage()
		self.page_search	= SearchReportPage()
		self.page_client	= ByClientPage()

		self.stack.addWidget(self.page_create)   # 0
		self.stack.addWidget(self.page_all)      # 1
		self.stack.addWidget(self.page_edit)     # 2
		self.stack.addWidget(self.page_search)   # 3
		self.stack.addWidget(self.page_client)   # 4

		root_layout.addWidget(self.stack)

		# Refresh table after a new report is created
		self.page_create.report_created.connect(self.page_all.load_data)

	def _switch_page(self, index: int):
		self.stack.setCurrentIndex(index)

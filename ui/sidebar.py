from PyQt5 import QtWidgets, QtCore
from ui.components import make_label


class NavButton(QtWidgets.QPushButton):
	def __init__(self, text, parent=None):
		super().__init__(text, parent)
		self.setObjectName("NavButton")
		self.setCursor(QtCore.Qt.PointingHandCursor)
		self.setCheckable(False)
		self._active = False

	def set_active(self, active: bool):
		self._active = active
		self.setProperty("active", "true" if active else "false")
		self.style().unpolish(self)
		self.style().polish(self)


class Sidebar(QtWidgets.QWidget):
	page_changed = QtCore.pyqtSignal(int)

	NAV_ITEMS = [
		("➕  New Report", "Create and submit a new weight entry"),
		("📋  All Reports", "Browse recent weight records"),
		("✏️  Edit by ID", "Modify load/unload weights"),
		("🔍  Search by ID", "Find and view a specific report"),
		("👤  By Client", "Filter reports by client name"),
	]

	def __init__(self, operator_name, parent=None):
		super().__init__(parent)
		self.setObjectName("Sidebar")
		self.operator_name = operator_name
		self._buttons = []
		self._build()

	def _build(self):
		root = QtWidgets.QVBoxLayout(self)
		root.setContentsMargins(0, 0, 0, 0)
		root.setSpacing(0)

		# ── App branding ──────────────────────────────────
		title = make_label("⚖ ScaleReport", "AppTitle")
		root.addWidget(title)
		subtitle = make_label("Weight Management", "AppSubtitle")
		root.addWidget(subtitle)

		# ── Divider ───────────────────────────────────────
		div = QtWidgets.QFrame()
		div.setObjectName("Divider")
		div.setFrameShape(QtWidgets.QFrame.HLine)
		root.addWidget(div)
		root.addSpacing(8)

		# ── Nav items ─────────────────────────────────────
		nav_container = QtWidgets.QWidget()
		nav_container.setObjectName("Sidebar")
		nav_layout = QtWidgets.QVBoxLayout(nav_container)
		nav_layout.setContentsMargins(0, 0, 0, 0)
		nav_layout.setSpacing(2)

		for idx, (label, _) in enumerate(self.NAV_ITEMS):
			btn = NavButton(label)
			btn.clicked.connect(lambda checked, i=idx: self._on_nav(i))
			nav_layout.addWidget(btn)
			self._buttons.append(btn)

		root.addWidget(nav_container)
		root.addStretch()

		# ── Operator badge ────────────────────────────────
		badge = QtWidgets.QWidget()
		badge.setObjectName("OperatorBadge")
		badge_layout = QtWidgets.QVBoxLayout(badge)
		badge_layout.setContentsMargins(16, 10, 16, 10)
		badge_layout.setSpacing(2)

		op_label = make_label("Logged in as", "StatusLabel")
		op_name = make_label(self.operator_name, "StatusValue")
		badge_layout.addWidget(op_label)
		badge_layout.addWidget(op_name)
		root.addWidget(badge)

		self._set_active(0)

	def _on_nav(self, index):
		self._set_active(index)
		self.page_changed.emit(index)

	def _set_active(self, index):
		for i, btn in enumerate(self._buttons):
			btn.set_active(i == index)

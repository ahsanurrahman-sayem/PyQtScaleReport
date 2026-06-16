from PyQt5 import QtWidgets, QtCore, QtGui


def make_label(text, object_name=None, wrap=False) -> QtWidgets.QLabel:
	lbl = QtWidgets.QLabel(text)
	if object_name:
		lbl.setObjectName(object_name)
	if wrap:
		lbl.setWordWrap(True)
	return lbl


def make_button(text, primary=True, danger=False, icon=None) -> QtWidgets.QPushButton:
	btn = QtWidgets.QPushButton(text)
	if danger:
		btn.setObjectName("DangerButton")
	elif not primary:
		btn.setObjectName("SecondaryButton")
	if icon:
		btn.setIcon(QtGui.QIcon(icon))
	return btn


def make_field(placeholder="", read_only=False) -> QtWidgets.QLineEdit:
	field = QtWidgets.QLineEdit()
	field.setPlaceholderText(placeholder)
	field.setReadOnly(read_only)
	return field


def make_combo(items=None, editable=True, placeholder="") -> QtWidgets.QComboBox:
	combo = QtWidgets.QComboBox()
	combo.setEditable(editable)
	if items:
		combo.addItems(items)
		combo.setCurrentText("")
	if placeholder and editable:
		combo.lineEdit().setPlaceholderText(placeholder)
	return combo


def make_divider() -> QtWidgets.QFrame:
	line = QtWidgets.QFrame()
	line.setObjectName("Divider")
	line.setFrameShape(QtWidgets.QFrame.HLine)
	return line


def make_card(layout_type="form") -> QtWidgets.QWidget:
	card = QtWidgets.QWidget()
	card.setObjectName("Card")
	if layout_type == "form":
		layout = QtWidgets.QFormLayout(card)
		layout.setSpacing(12)
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
	elif layout_type == "vbox":
		layout = QtWidgets.QVBoxLayout(card)
		layout.setSpacing(12)
		layout.setContentsMargins(20, 20, 20, 20)
	elif layout_type == "hbox":
		layout = QtWidgets.QHBoxLayout(card)
		layout.setSpacing(12)
		layout.setContentsMargins(20, 20, 20, 20)
	return card, layout


def center_table_item(text) -> QtWidgets.QTableWidgetItem:
	item = QtWidgets.QTableWidgetItem(str(text))
	item.setTextAlignment(QtCore.Qt.AlignCenter)
	if len(str(text)) > 5:
		item.setData(QtCore.Qt.TextWordWrap,True)
	return item


def stretch_table_headers(table):
	header = table.horizontalHeader()
	header.setDefaultAlignment(QtCore.Qt.AlignCenter)
	for i in range(table.columnCount()):
		header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
		hitem = table.horizontalHeaderItem(i)
		if hitem:
			hitem.setTextAlignment(QtCore.Qt.AlignCenter)


def make_table(headers) -> QtWidgets.QTableWidget:
	table = QtWidgets.QTableWidget()
	table.setColumnCount(len(headers))
	table.setHorizontalHeaderLabels(headers)
	table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
	table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
	table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
	table.setWordWrap(True)
	table.setAlternatingRowColors(True)
	table.verticalHeader().setVisible(False)
	table.setShowGrid(False)
	table.verticalHeader().setSectionResizeMode(
		QtWidgets.QHeaderView.ResizeToContents
	)
	return table


def apply_completer(combo, items) -> QtWidgets.QCompleter:
	completer = QtWidgets.QCompleter(items)
	completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
	completer.setFilterMode(QtCore.Qt.MatchContains)
	combo.setCompleter(completer)

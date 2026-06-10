import sys
import os

# Prevent multiple instances (Windows only)
try:
	import win32event, win32api, winerror
	WINDOWS = True
except ImportError:
	WINDOWS = False

from PyQt5 import QtWidgets, QtGui
from ui.app_window import ScaleReportApp
from core.app import UserAuthApp  # Uncomment when integrating auth


def resource_path(relative_path):
	base = getattr(sys, '_MEIPASS', os.path.abspath("."))
	return os.path.join(base, relative_path)


def main():
	if WINDOWS:
		mutex = win32event.CreateMutex(None, False, "ScaleReportFinalQtAppPort")
		if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
			sys.exit(0)

	app = QtWidgets.QApplication(sys.argv)
	app.setStyle("Fusion")

	# Font setup
	font_path = resource_path("assets/fonts/jetbrainsfont.ttf")
	if os.path.exists(font_path):
		font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
		families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
		if families:
			app.setFont(QtGui.QFont(families[0], 10))
	else:
		app.setFont(QtGui.QFont("Segoe UI", 10))

	# Auth (uncomment when integrating)
	login = UserAuthApp()
	if login.exec() != QtWidgets.QDialog.DialogCode.Accepted:
	    sys.exit(0)
    user = login.loged_user

	#user = "SAYEM"  # placeholder

	window = ScaleReportApp(user)
	window.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

from cli_handler import del_last_report, view_all_reports
from os import system
if __name__ == "__main__":
	i = input("Press enter: ")
	if i == "":
		print("Nothing to do!")
		system('exit')
	view_all_reports()
	del_last_report()
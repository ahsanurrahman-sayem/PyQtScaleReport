from os import system as sys
import argparse
from cli_handler import create_report, search_report, view_all_reports, edit_report, delete_report

def cl():
	sys("clear")

def main():
	catList={
		'1':"1. Create a new report",
		'2':"2. Search a report by ID",
		'3':"3. View all reports",
		'4':"4. Edit a report",
		'5':"5. Delete a report",
		'0':"0. Exit",
	}

	parser = argparse.ArgumentParser(description="Scale Report CLI")

	parser.add_argument('-c', '--create', action='store_true', help='Create a new weight report interactively')
	parser.add_argument('-s', '--search', type=int, metavar='ID', help='Search a report by ID and generate PDF')
	parser.add_argument('-v', '--view-all', action='store_true', help='View all weight records in a table')
	parser.add_argument('-e', '--edit', type=int, metavar='ID', help='Edit load/unload weights for a given ID')
	parser.add_argument('-d', '--delete', type=int, metavar='ID', help='Delete weight report of given ID')

	args = parser.parse_args()
	
	if args.create:
		create_report()
	elif args.search is not None:
		search_report(args.search)
	elif args.view_all:
		view_all_reports()
	elif args.edit is not None:
		edit_report(args.edit)
	elif args.delete is not None:
		delete_report(args.edit)
	else:
		while True:
			print("\n=== Scale Report CLI Menu ===")
			for index,(key,value) in enumerate(catList.items()):
					print(value)
			choice = input("\nEnter your choice: ").strip()
			cl()
			if choice == '1':
				create_report()
			elif choice == '2':
				report_id = input("Enter report ID to search: ")
				if report_id.isdigit():
					search_report(int(report_id))
			elif choice == '3':
				view_all_reports()
			elif choice == '4':
				report_id = input("Enter report ID to edit: ")
				if report_id.isdigit():
					edit_report(int(report_id))
					view_all_reports()
			elif choice == '5':
				report_id = input("Enter report ID to delete: ")
				if report_id.isdigit():
					delete_report(int(report_id))
					view_all_reports()
			elif choice == '0':
				break
			else:
				print("Invalid choice. Please try again.")

if __name__ == "__main__":
	main()
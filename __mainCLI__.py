from os import system
import argparse
from core.cli import (
	create_report,
	search_report,
	view_all_reports,
	view_a_report,
	add_items,
	view_items,
	add_user,
	view_users,
	edit_report,
	modify_id,
	delete_report,
	add_client,
	del_last_report,
	get_all_clients,
)

def cl():
	pass
	#system("Clear-Host")
	#sys("clrscr")

def main():
	catList={
		'1':"1. Create a new report",
		'2':"2. Search a report by ID",
		'3':"3. View all reports\n",
		'4':"4. Edit a report",
		'5':"5. Delete a report",
		'6':"6. Modify id of a report\n",
		'7':"7. Add item",
		'8':"8. View items\n",
		'9':"9. Add User",
		'10':"10. View Users\n",
		'11':"11. Add Client\n",
        	'12':"12. View All Client's listed\n",
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
		delete_report(args.delete)
	else:
		try:
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
						#view_all_reports()
				elif choice == '5':
					report_id = input("Enter report ID to delete: ")
					if report_id.isdigit():
						delete_report(int(report_id))
						view_all_reports()
					else:
						view_all_reports()
						del_last_report()
	
				elif choice == '6':
					report_id = input("Enter current id:")
					new_id = input("Enter modified id:")
					if report_id.isdigit():
						modify_id(report_id,new_id)
				elif choice == '7':
					add_items()
				elif choice == '8':
					view_items()
				elif choice == '9':
					add_user()
				elif choice == '10':
					view_users()
				elif choice == '11':
					add_client()
				elif choice == '12':
					get_all_clients()
				elif choice == '0':
					break
				else:
					print("Invalid choice. Please try again.")
		except Exception as e:
		    raise e
if __name__ == "__main__":
	main()

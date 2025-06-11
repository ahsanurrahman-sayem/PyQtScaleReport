import argparse
from cli_handler import create_report, search_report, view_all_reports, edit_report

def main():
	parser = argparse.ArgumentParser(description="Scale Report CLI")

	parser.add_argument('-c', '--create', action='store_true', help='Create a new weight report interactively')
	parser.add_argument('-s', '--search', type=int, metavar='ID', help='Search a report by ID and generate PDF')
	parser.add_argument('-v', '--view-all', action='store_true', help='View all weight records in a table')
	parser.add_argument('-e', '--edit', type=int, metavar='ID', help='Edit load/unload weights for a given ID')

	args = parser.parse_args()

	if args.create:
		create_report()
	elif args.search is not None:
		search_report(args.search)
	elif args.view_all:
		view_all_reports()
	elif args.edit is not None:
		edit_report(args.edit)
	else:
		parser.print_help()

if __name__ == "__main__":
	main()
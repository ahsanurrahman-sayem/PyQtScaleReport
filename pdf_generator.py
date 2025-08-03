import os
from fpdf import FPDF
from utils import getToday,getNow

REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

class WeightReportPDF(FPDF):
	def __init__(self, operator: str):
		super().__init__()
		self.operator = operator
		self.set_margin(0.0)
	def isEmpty(self,var):
		if var == "0":
			return "0"
		return var
	def isToDate(self,var):
		if var != None:
			return var
		return ""
	def header(self):
		self.set_font("Helvetica", "B", 18)
		self.cell(0, 10, "SR BRIDGE SCALE", ln=True, align="C")
		self.set_font("Helvetica", size=12)
		self.cell(0, 8, "RAIPUR ROAD TULATOLI LAKSHMIPUR Mob. 01731273113, 01722200634", ln=True, align="C")
		self.ln(4)
		self.set_font("Helvetica", "B", 16)
		self.set_x(80)
		self.cell(50, 10, "Weight Report", border=1, align="C")
		self.set_font("Helvetica", "B", 10)
		self.set_x(148)
		self.cell(0, 10, f"Operator: {self.operator}", ln=True, align="R")
		self.ln(4)

	def footer(self):
		self.set_y(120)
		self.set_font("Helvetica", style="B", size=9)
		labels = ["Received by", "Supervised by", "Operated by", "Authorized by"]
		self.cell(10, 0, "", border="1", align="C")
		for label in labels:
			self.cell(25, 10, label, border="T", align="C")
			self.cell(10, 0, "", border="1", align="C")
		self.ln(10)

	def report_table(self, data: dict):
		self.set_font("Helvetica", style="B", size=11)
		rows = [
			["Weight ID", f": {data['id']}", "Scale ID: 1", " ", "Party Type", f"{data['party_type']:<43} Print Date: {getToday()}"],
			["Vehicle No", f": {data['vehicle_no']}", "", "", "Client Name", data["client_name"]],
			["Challan/LC No", ": " + data.get("challan_no", ""), "", "", "Address", data.get("address", "")],
			["Item Name", ": " + data["item_name"], "QTY:", data.get("qty", ""), "Contact", data.get("contact", "")],
			["Load Weight", ": " + str(int(data["load_weight"])), "Kg", "", "Load Date", self.isToDate(data["load_weight_date"])],
			["Unload Weight", ": " + str(int(data["unload_weight"])), "Kg", "Deduct", "Unload Date", self.isToDate(data["unload_weight_date"])],
			["Net Weight", ": " + str(int(self.isEmpty(data["load_weight"])) - int(self.isEmpty(data["unload_weight"]))) or "0", "Kg", "", "Driver", data.get("driver", "")]
		]
		col_widths = [30, 30, 8, 40, 20, 80]
		for row in rows:
			for i, item in enumerate(row):
				border = 'TB'
				align = 'L'
				if i == 0:
					border = 'LTB'
				if i == 5:
					border = 'RTB'
					self.set_font("Helvetica", style="B", size=9)
					if item.__contains__("Print Date:"):
						align= 'R'
						border = 'RTB'
						self.set_font("Helvetica", style="B", size=9)
				if i == 4:
					align = 'R'
					border = 'RTB'
				self.cell(col_widths[i], 9, item, border=border, align=align)
				self.set_font("Helvetica", style="B", size=11)
			self.ln()

def generate_pdf(data, filename: str):
	pdf = WeightReportPDF(data["operator"])
	pdf.add_page()
	pdf.report_table(data)
	file_path = os.path.join(REPORT_DIR, filename)
	pdf.output(file_path)
	return file_path
import sqlite3
from models import WeightData

DB_FILE = "weights.db"

def getConnection():
	conn = sqlite3.connect(DB_FILE)
	cursor = conn.cursor()
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS weights (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		operator TEXT,
		vehicle_no TEXT,
		client_name TEXT,
		challan_no TEXT,
		driver TEXT,
		address TEXT,
		item_name TEXT,
		qty REAL,
		contact TEXT,
		load_weight REAL,
		load_weight_date TEXT,
		unload_weight REAL,
		unload_weight_date TEXT,
		net_weight TEXT,
		party_type TEXT
	)
	""")
	conn.commit()
	return conn

def getAllWeights():
	conn = getConnection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM weights")
	rows = cursor.fetchall()
	conn.close()
	return [WeightData(*row) for row in rows]

def getWeightById(weight_id):
	conn = getConnection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM weights WHERE id=?", (weight_id,))
	row = cursor.fetchone()
	conn.close()
	if row:
		return WeightData(*row)
	return None
def updateWeight(weight: WeightData):
	conn = getConnection()
	cursor = conn.cursor()
	cursor.execute("""
		UPDATE weights SET
			load_weight = ?, load_weight_date = ?,
			unload_weight = ?, unload_weight_date = ?,
			net_weight = ?
		WHERE id = ?
	""", (
		weight.load_weight,
		weight.load_weight_date,
		weight.unload_weight,
		weight.unload_weight_date,
		weight.net_weight,
		weight.id
	))
	conn.commit()
	conn.close()

def addNewWeight(data: WeightData):
	conn = getConnection()
	cursor = conn.cursor()

	if data.id is not None:
		cursor.execute("""
		INSERT INTO weights (
			id, operator, vehicle_no, client_name, challan_no, driver,
			address, item_name, qty, contact,
			load_weight, load_weight_date,
			unload_weight, unload_weight_date, net_weight,
			party_type
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		""", (
			data.id, data.operator, data.vehicle_no, data.client_name, data.challan_no, data.driver,
			data.address, data.item_name, data.qty, data.contact,
			data.load_weight, data.load_weight_date,
			data.unload_weight, data.unload_weight_date, data.net_weight,
			data.party_type
		))
		conn.commit()
		weight_id = data.id
	else:
		cursor.execute("""
		INSERT INTO weights (
			operator, vehicle_no, client_name, challan_no, driver,
			address, item_name, qty, contact,
			load_weight, load_weight_date,
			unload_weight, unload_weight_date, net_weight,
			party_type
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		""", (
			data.operator, data.vehicle_no, data.client_name, data.challan_no, data.driver,
			data.address, data.item_name, data.qty, data.contact,
			data.load_weight, data.load_weight_date,
			data.unload_weight, data.unload_weight_date, data.net_weight,
			data.party_type
		))
		conn.commit()
		weight_id = cursor.lastrowid

	conn.close()
	return weight_id

def getLastRowId():
	conn = getConnection()
	cursor = conn.cursor()
	weight_id = cursor.lastrowid

	conn.close()
	return weight_id
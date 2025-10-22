import sqlite3
from models import WeightData
import os
import shutil
import sys


def inject(id:int,weight_id:int):
	with getConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
		UPDATE weights SET
			id = ?
		WHERE id = ?
	""", (id,weight_id)
	)
		conn.commit()


def getLocalDb():
	base_dir = os.path.join(os.environ.get("ProgramData"),"ScaleReport")
	if not os.path.exists(base_dir):
		os.makedirs(base_dir, exist_ok = True)
	return os.path.join(base_dir, "weights.db")


def getConnection():
	#conn = sqlite3.connect("weights.db")
	conn = sqlite3.connect(getLocalDb())
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
		)"""
	)
	conn.commit()
	return conn

def getAllWeights():
	with getConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM weights")
		rows = cursor.fetchall()
		return [WeightData(*row) for row in rows]

def getAllWeightsOfRange(start_date, end_date):
	with getConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("""SELECT * FROM weights WHERE (load_weight_date BETWEEN ? AND ?) OR (unload_weight_date BETWEEN ? AND ?)""", (start_date, end_date, start_date, end_date))
		rows = cursor.fetchall()
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
<<<<<<< HEAD
			net_weight = ?, client_name = ?
=======
			net_weight = ?, client_name = ?, qty = ?
>>>>>>> 1e351f310de6b3f1c0defa3469e0c6e37a290709
		WHERE id = ?
	""", (
		weight.load_weight,
		weight.load_weight_date,
		weight.unload_weight,
		weight.unload_weight_date,
		weight.net_weight,
		weight.client_name,
<<<<<<< HEAD
=======
		weight.qty,
>>>>>>> 1e351f310de6b3f1c0defa3469e0c6e37a290709
		weight.id
	))
	conn.commit()
	conn.close()

def updateAndItem(id, item, value):
	# whitelist valid column names to prevent SQL injection
	valid_columns = {
		"id","operator","vehicle_no","client_name","challan_no","driver",
		"address","item_name","qty","contact","load_weight","load_weight_date",
		"unload_weight","unload_weight_date","net_weight","party_type"
	}

	if item not in valid_columns:
		raise ValueError(f"Invalid column name: {item}")

	conn = getConnection()
	cursor = conn.cursor()

	# build SQL dynamically (only the column name part is f-stringed)
	sql = f"UPDATE weights SET {item} = ? WHERE id = ?"
	cursor.execute(sql, (value, id))
	conn.commit()
	conn.close()


def addNewWeight(data: WeightData):
	conn = getConnection()
	cursor = conn.cursor()
	#print("addNewWeight() has been called - with arg: ",data.id)
	# --> if data.id is not getLastRowId():
		#print("method got custom argument while init - ",data.id)
		# custom id
	if data.id is not None:
		#Custom ID Section
		cursor.execute("""
			INSERT INTO weights (
				id, operator,
				vehicle_no,
				client_name, 
				challan_no,
				driver,
				address,
				item_name, 
				qty, contact,
				load_weight,
				load_weight_date,
				unload_weight,
				unload_weight_date,
				net_weight,
				party_type) VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
		""", (data.id, data.operator, data.vehicle_no, data.client_name, data.challan_no, data.driver, data.address, data.item_name, data.qty, data.contact, data.load_weight, data.load_weight_date, data.unload_weight, data.unload_weight_date, data.net_weight, data.party_type))
		conn.commit()
		weight_id = data.id
	else:
		#I want if the data.id is None then code in this scope should run.
		# Auto increament id section --> 
		cursor.execute("""
			INSERT INTO weights (
				operator, vehicle_no, client_name, challan_no, driver,
				address, item_name, qty, contact,
				load_weight, load_weight_date,
				unload_weight, unload_weight_date, net_weight,
				party_type
			)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
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
	cursor.execute("SELECT MAX(id) FROM weights")
	result = cursor.fetchone()
	conn.close()
	return result[-1] if result else None

def del_data(weight_id: int):
	conn = getConnection()
	cursor = conn.cursor()
	cursor.execute("DELETE FROM weights WHERE id = ?", (weight_id,))
	conn.commit()
	cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", ("weights",))
	conn.commit()
	conn.close()

if __name__ == '__main__':
	pass
	#1-del_data(which one to delete)
	#2-inject(modifiction,where to modify)
	
import sqlite3
from dataclasses import fields, is_dataclass
from models import WeightData, User, Item
import os,platform

def getSysDbPath(cwd=None):
	system = platform.system()
	match system:
		case 'Linux':
			return "weights.db"
		case 'Windows':
			if cwd:
				return "weights.db"
			else:
				return getDbPath()
		case _:
			return "weights.db"

def getDbPath():
	base_dir = os.path.join(os.environ.get("ProgramData"), "ScaleReport")
	if not os.path.exists(base_dir):
		os.makedirs(base_dir, exist_ok=True)
	return os.path.join(base_dir, "weights.db")

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


def getConnection():
	conn = sqlite3.connect(getSysDbPath(cwd=True))
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
			id = ?,
			load_weight = ?, load_weight_date = ?,
			unload_weight = ?, unload_weight_date = ?,
			net_weight = ?, client_name = ?, qty = ?
		WHERE id = ?
	""", (
		weight.id,
		weight.load_weight,
		weight.load_weight_date,
		weight.unload_weight,
		weight.unload_weight_date,
		weight.net_weight,
		weight.client_name,
		weight.qty,
		weight.id
	))
	conn.commit()
	conn.close()

def updateAnItem(id, item, value):
	# whitelist valid column names to prevent SQL injection
	valid_columns = {
		"id","operator","vehicle_no","client_name","challan_no","driver",
		"address","item_name","qty","contact","load_weight","load_weight_date",
		"unload_weight","unload_weight_date","net_weight","party_type"
	}

	if item not in valid_columns:
		raise ValueError(f"Invalid column name: {item}")
	
	with getConnection() as conn:
		cursor = conn.cursor()

	# build SQL dynamically (only the column name part is f-stringed)
		sql = f"UPDATE weights SET {item} = ? WHERE id = ?"
		cursor.execute(sql, (value, id))
		conn.commit()

def inject(weight_id:int,new_id:int):
	with getConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
		UPDATE weights SET
			id = ?
		WHERE id = ?
	""", (new_id,weight_id)
	)
		conn.commit()


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
			data.address, data.item_name, str(int(data.qty)) if data.qty.isdigit() else "" , data.contact,
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
	with getConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("DELETE FROM weights WHERE id = ?", (weight_id,))
		conn.commit()
		cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", ("weights",))
		conn.commit()

def getUserConnection():
	with sqlite3.connect(getSysDbPath()) as conn:
		cursor = conn.cursor()
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			password TEXT
			)"""
		)
		conn.commit()
		return conn

def addUser(user: User):
	with getUserConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO users (
			name,
			password 
			) VALUES (?, ?)""",(
				user.name,
				user.password
			)
		)
		conn.commit()
		return cursor.lastrowid

def getUsers():
	with getUserConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()
		return [User(*row) for row in rows]

def getSysDatasConnection():
	with sqlite3.connect(getSysDbPath()) as conn:
		cursor = conn.cursor()
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS items (
			name TEXT
			)"""
		)
		conn.commit()
		return conn

def addItem(item: Item):
	with getSysDatasConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO items (
			name
			) VALUES (?)""",(
				item.name,
			)
		)
		conn.commit()

def getItems():
	with getSysDatasConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM items")
		rows = cursor.fetchall()
		return [Item(*row) for row in rows]

#()

import sqlite3
from dataclasses import fields, is_dataclass

class ARSTable:
	def __init__(self, table: str, model, unique_fields=None):
		self.table: str = table
		self.model = model
		self.unique_fields = unique_fields or []	# fields that must be unique

	def _mapPythonTypeToSQLite(self, py_type):
		type_map = {
			int: "INTEGER",
			float: "REAL",
			str: "TEXT",
			bool: "INTEGER",
		}
		return type_map.get(py_type, "TEXT")

	def createTable(self):
		if not is_dataclass(self.model):
			raise TypeError(f"{self.model} must be a dataclass")

		with sqlite3.connect(getSysDbPath()) as conn:
			cursor = conn.cursor()
			columns_sql = []
			for f in fields(self.model):
				col_type = self._mapPythonTypeToSQLite(f.type)
				col_def = f"{f.name} {col_type}"

				if f.name == "id":
					col_def += " PRIMARY KEY AUTOINCREMENT"
				elif f.name in self.unique_fields:
					col_def += " UNIQUE"

				columns_sql.append(col_def)

			query = f"CREATE TABLE IF NOT EXISTS {self.table} ({', '.join(columns_sql)});"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			return True

	def _isDuplicate(self, conn, **datas):
		# Check if a record already exists with the same values for unique fields
		for field in self.unique_fields:
			if field in datas:
				cursor = conn.cursor()
				query = f"SELECT COUNT(*) FROM {self.table} WHERE {field} = ?"
				cursor.execute(query, (datas[field],))
				exists = cursor.fetchone()[0] > 0
				cursor.close()
				if exists:
					return True
		return False

	def setDatas(self, **datas):
		with sqlite3.connect(getSysDbPath()) as conn:
			if self._isDuplicate(conn, **datas):
				print(f"[WARN] Duplicate value detected in unique field(s): {self.unique_fields}. Skipping insert.")
				return None

			cursor = conn.cursor()
			cols = ', '.join(datas.keys())
			placeholders = ', '.join(['?'] * len(datas))
			values = tuple(datas.values())
			query = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders});"
			cursor.execute(query, values)
			conn.commit()
			rowid = cursor.lastrowid
			cursor.close()
			return rowid

	def getDatas(self, *columns):
		with sqlite3.connect(getSysDbPath()) as conn:
			cursor = conn.cursor()
			if columns:
				cols = ", ".join(columns)
				query = f"SELECT {cols} FROM {self.table};"
			else:
				query = f"SELECT * FROM {self.table};"
			cursor.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			return [self.model(*row) for row in rows]

	def clearTable(self):
		with sqlite3.connect(getSysDbPath()) as conn:
			cursor = conn.cursor()
			cursor.execute(f"DELETE FROM {self.table}")
			conn.commit()
			cursor.close()


if __name__ == '__main__':
	pass
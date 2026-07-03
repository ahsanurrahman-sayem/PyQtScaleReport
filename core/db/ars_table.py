
from dataclasses import fields, is_dataclass
import sqlite3
from .db import getSysDbPath

class ARSTable:
	def __init__(self, table: str, model, unique_fields=None):
		self.table: str = table
		self.model = model
		self.unique_fields = unique_fields or [] # fields that must be unique
		self.createTable()

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
				query = f"SELECT * FROM {self.table} WHERE {cols};"
			else:
				query = f"SELECT * FROM {self.table};"
			cursor.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			return [self.model(*row) for row in rows]

	def getDatasWithLimit(self, *columns, limit):
		with sqlite3.connect(getSysDbPath()) as conn:
			cursor = conn.cursor()
			if columns:
				cols = ", ".join(columns)
				query = f"SELECT * FROM {self.table} WHERE {cols} ORDER BY rowid DESC LIMIT {limit};"
			else:
				query = f"SELECT * FROM {self.table} ORDER BY rowid DESC LIMIT {limit};"
			cursor.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			return [self.model(*row) for row in rows]

	def getDatasWithKey(self, *columns, limit):
		with sqlite3.connect(getSysDbPath()) as conn:
			cursor = conn.cursor()
			if columns:
				cols = ", ".join(columns)
				query = f"SELECT * FROM {self.table} WHERE {cols} ORDER BY rowid DESC LIMIT {limit};"
			else:
				query = f"SELECT * FROM {self.table} ORDER BY rowid DESC LIMIT {limit};"
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
	def modifyColumn():
	 	pass

	def delTable(self):
		with sqlite3.connect(getSysDbPath()) as conn:
			conn.execute(f"DROP TABLE IF EXISTS {self.table}")
			conn.commit()
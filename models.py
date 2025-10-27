from dataclasses import dataclass

@dataclass
class WeightData:
	id: int
	operator: str
	vehicle_no: str
	client_name: str
	challan_no: str
	driver: str
	address: str
	item_name: str
	qty: str
	contact: str
	load_weight: str
	load_weight_date: str
	unload_weight: str
	unload_weight_date: str
	net_weight: str
	party_type: str = "CLIENT"

@dataclass
class User:
	id: int
	name: str
	password: str

@dataclass
class Item:
	id: int
	name: str

@dataclass
class Client:
	id: int
	name: str

@dataclass
class Vehicle:
	id: int
	name: str

@dataclass
class VehicleSerial:
	id: int
	serial: str
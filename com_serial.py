from PyQt5 import QtCore
import serial, threading

class SerialWeightReader(QtCore.QObject):
	weightUpdated = QtCore.pyqtSignal(str)

	def __init__(self, port='COM3', baudrate=9600):
		super().__init__()
		self.port = port
		self.baudrate = baudrate
		self.serial_conn = None
		self.reading = False

	def startReading(self):
		try:
			self.serial_conn = serial.Serial(
				port=self.port,
				baudrate=self.baudrate,
				bytesize=serial.EIGHTBITS,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				timeout=1
			)
			self.reading = True
			threading.Thread(target=self.readLoop, daemon=True).start()
		except serial.SerialException as e:
			print(f"Serial Error: {e}")

	def stopReading(self):
		self.reading = False
		if self.serial_conn and self.serial_conn.is_open:
			self.serial_conn.close()

	def readLoop(self):
		while self.reading and self.serial_conn and self.serial_conn.is_open:
			try:
				raw = self.serial_conn.read(16)
				weight = self.extractWeightFromFrame(raw)
				if weight is not None:
					self.weightUpdated.emit(str(weight / 10))
			except Exception as e:
				print(f"Read Error: {e}")
				break

	def extractWeightFromFrame(self, frame):
		try:
			if len(frame) >= 10 and frame[0] == 0x02:
				ascii_part = frame[1:9].decode('ascii', errors='ignore')
				weight_str = ascii_part.strip('+').lstrip('0')
				return int(weight_str) if weight_str else 0
			return None
		except:
			return None

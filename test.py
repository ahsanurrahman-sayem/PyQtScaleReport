from db import ARSTable
from models import WeightData
from db import getAllWeights

for x in ARSTable("weights",WeightData).getDatasWithKey("client_name  = 'ROMJAN TRADERS'",limit=3):
	print(x.client_name)

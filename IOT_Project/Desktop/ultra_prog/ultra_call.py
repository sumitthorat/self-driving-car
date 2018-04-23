import ultra_1, ultra_2, ultra_3
import time

while True:
	dist1 = ultra_1.distance()
	time.sleep(0.02)
	dist2 = ultra_2.distance()
	time.sleep(0.02)
	dist3 = ultra_3.distance()
	time.sleep(0.2)
	print(str(dist1) + "\t" + str(dist2) + "\t" + str(dist3))
	
	
	
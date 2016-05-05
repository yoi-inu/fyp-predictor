import csv
import math

latitude = 12.8100
longitude = 77.6940

with open('locations.csv', 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar="'")
  locations = list(reader)

for location in locations:
	location[0] = float(location[0])
	location[1] = float(location[1])

min_dist = 1000
min_i = -1
i = 0

for location in locations:
	this_dist = math.pow( ( latitude - location[0] ) , 2 ) + math.pow( ( longitude - location[1] ) , 2 )
	print this_dist, location
	this_dist = math.sqrt(this_dist)
	if( this_dist < min_dist ):
		min_dist = this_dist
		min_i = i
	i = i + 1

print locations[min_i]


# locations = [
# 	[12.8087, 77.6946,'Narayana hrudayalaya'],
# 	[12.9166, 77.5996,'Jayadeva Hospital'],
# 	[12.8953, 77.5981,'Fortis Hospital'],
# 	[12.8399, 77.6770,'Electronic City'],
# 	[12.8971, 77.5968,'Apollo Hospital'],
# 	[12.9308, 77.6184,'St Johns Hospital']
# ]

# min = 10000
# i = 0
# flag_final = 0

# for location in locations:
# 	distance = location[0] - latitude

# 	if(distance < 0):
# 		distance = -1 * distance

# 	if(distance < min):
# 		min = distance
# 		flag_final = i
# 	i = i + 1

# print locations[flag_final][2]
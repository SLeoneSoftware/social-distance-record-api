from math import radians, sin, cos, acos


def calculate(latOne, longOne, latTwo, longTwo):
	R = 6373.01
	latOne = radians(latOne) #40.606890
	longOne = radians(longOne) #-79.683750
	latTwo = radians(latTwo)
	longTwo = radians(longTwo)
	dist = R * acos(sin(latOne)*sin(latTwo) + cos(latOne)*cos(latTwo)*cos(longOne - longTwo))
	return dist
			

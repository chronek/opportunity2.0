#cars
#assume cars are 15
#assume board 100 X 100
import random


class car:

	def __init__(self):
		cars.append(self)

		#up: 0,down: 1,right: 2,left: 3
		self.direction = random.randrange(4)

		self.positionX = 0
		self.positionY = 0

		if self.direction == 0:
			self.positionY = 0
			self.positionX = random.randrange(1,3) * 33
		elif self.direction == 1:
			self.positionX = random.randrange(1,3) * 33
			self.positionY = 100
		elif self.direction == 2:
			self.positionY = random.randrange(1,3) * 33
			self.positionX = 0
		elif self.direction == 3:
			self.positionY = random.randrange(1,3) * 33
			self.positionX = 100

	def move(self):
		if self.direction == 0:
			self.positionX += 1
		elif self.direction == 1:
			self.positionX -= 1
		elif self.direction == 2:
			self.positionY += 1
		elif self.direction == 3:
			self.positionY -= 1


		if positionY > 100 or positionX > 100:
			cars.remove(this)




carsAmount = 20
cars = []

while len(cars) < carsAmount:
	car()

for car in cars:
	car.move()
	#print("car direction: " + str(car.direction) + " car position is: " + str(car.positionX) + ", " + str(car.positionY))
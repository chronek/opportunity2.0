import random
import time

class Car:

    def __init__(self):
        # up: 0,down: 1,right: 2,left: 3
        self.direction = random.randrange(4)

        self.positionX = 0
        self.positionY = 0

        if self.direction == 0:
            self.positionY = 0
            self.positionX = random.randrange(1, 3) * 33 + 1.5
        elif self.direction == 1:
            self.positionX = random.randrange(1, 3) * 33 - 1.5
            self.positionY = 100
        elif self.direction == 2:
            self.positionY = random.randrange(1, 3) * 33 + 1.5
            self.positionX = 0
        elif self.direction == 3:
            self.positionY = random.randrange(1, 3) * 33 - 1.5
            self.positionX = 100
            
        if self.safeDistance():    
            cars.append(self)

    def safeDistance(self):
        for car in cars:
            if car.direction == self.direction:
                if abs(car.positionX - self.positionX) < 4 and abs(car.positionY - self.positionY) < 4:
                    return False
        
        return True
        
    def collisionAvoidance(self):
        potentialX = self.positionX
        potentialY = self.positionY
        
        if self.direction == 0:
            potentialY += 1
        elif self.direction == 1:
            potentialY -= 1
        elif self.direction == 2:
            potentialX += 1
        elif self.direction == 3:
            potentialX -= 1
        
        for car in cars:
            if car != self and abs(car.positionX - potentialX) < 3 and abs(car.positionY - potentialY) < 3:
                return False
            
        return True

    def move(self):
        
        if self.collisionAvoidance():
            if self.direction == 0:
                self.positionY += 1
            elif self.direction == 1:
                self.positionY -= 1
            elif self.direction == 2:
                self.positionX += 1
            elif self.direction == 3:
                self.positionX -= 1

        if self.positionY > 100 or self.positionY < 0  or self.positionX > 100 or self.positionX < 0 :
            cars.remove(self)

    def drawCar(self):
        fill(255, 255, 255)
        ellipse(self.positionX * 7, self.positionY * 7, 15, 15)

def setup():
    size(700, 700)
    frameRate(30)

cars = []

def draw():
    
    background(11, 102, 35)
    carsAmount = 80
    
    

    if len(cars) < carsAmount:
        Car()

    for car in cars:
        print(" car position is: " + str(car.positionX) + ", " + str(car.positionY))
        car.drawCar()
        car.move()
    #time.sleep(4)

        #print("car direction: " + str(car.direction) + " car position is: " + str(car.positionX) + ", " + str(car.positionY))

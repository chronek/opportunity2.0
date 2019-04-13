import random
import time


class intersection:
    def __init__(self, xCoord, yCoord):
        intersections.append(self)
        self.xCoord = xCoord
        self.yCoord = yCoord
        
        self.time = 0
        
        #allows cars from (no direction: -1, left: 1, up: 2, right: 3, down: 4) to procede
        self.allowance = -1
        #selects the next open road
        self.next = 1

    def changeLane(self):
        self.time = 0
        
        self.allowance = self.next
        self.next = self.next + 1 if self.next < 4 else 1
        
    def checkLane(self):
        return self.allowance
    
    def drawIntersection(self):
        self.time += 1
        
        if self.allowance == -1 and self.time > 30:
            self.changeLane()
        elif self.time > 90:
            self.allowance = -1
            self.time = 0
    


class Car:

    def __init__(self):
        # up: 0,down: 1,right: 2,left: 3
        self.direction = random.randrange(4)

        self.positionX = 0
        self.positionY = 0
        
        self.speed = 1

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
        
    def collisionAvoidance(self, posX, posY):
        
        for intersection in intersections:
            if abs(intersection.xCoord - posX) < 5 and abs(intersection.yCoord - posY) < 5:
                if (self.direction != intersection.checkLane()):
                    self.speed = acceleration
                    return False
                
        
        for car in cars:
            if car != self and abs(car.positionX - posX) < 3 and abs(car.positionY - posY) < 3:
                self.speed = acceleration
                return False
        if self.speed < topSpeed:
            self.speed += acceleration
            self.speed = self.speed if self.speed < topSpeed else topSpeed   
        
         
        return True

    def move(self):
        
        if self.direction == 0:
            if self.collisionAvoidance(self.positionX, self.positionY + self.speed):
                self.positionY += self.speed
        elif self.direction == 1:
            if self.collisionAvoidance(self.positionX, self.positionY - self.speed):
                self.positionY -= self.speed
        elif self.direction == 2:
            if self.collisionAvoidance(self.positionX + self.speed, self.positionY):
                self.positionX += self.speed
        elif self.direction == 3:
            if self.collisionAvoidance(self.positionX - self.speed, self.positionY):
                self.positionX -= self.speed

        if self.positionY > 100 or self.positionY < 0  or self.positionX > 100 or self.positionX < 0 :
            cars.remove(self)

    def drawCar(self):
        fill(255, 255, 255)
        ellipse(self.positionX * 7, self.positionY * 7, 15, 15)

def setup():
    size(700, 700)
    frameRate(30)

intersections = []
cars = []
acceleration = .1
topSpeed = 1

intersection(33,33)
intersection(33,66)
intersection(66,33)
intersection(66,66)

def draw():
    
    background(11, 102, 35)
    carsAmount = 40
    
    

    if len(cars) < carsAmount:
        Car()

    for intersection in intersections:
        print("Intersection allowance: " + str(intersection.allowance))
        intersection.drawIntersection()

    for car in cars:
        #print(" car position is: " + str(car.positionX) + ", " + str(car.positionY))
        car.drawCar()
        car.move()
    #time.sleep(4)

        #print("car direction: " + str(car.direction) + " car position is: " + str(car.positionX) + ", " + str(car.positionY))

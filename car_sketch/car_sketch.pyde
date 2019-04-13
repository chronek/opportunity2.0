import random
import time

# Black roads
def drawRoads():
    fill(0)
    rect(208, 0, 49, 700) # left
    rect(436, 0, 49, 700) # right
    rect(0, 436, 700, 49) # bottom
    rect(0, 208, 700, 49) # top

def drawDashedLinesTop():
    x = -10
    while (x < 720):
        fill(255, 255, 0)
        rect(x, 231, x, 3)
        x += 10
        fill(0, 0, 0)
        rect(x, 231, x, 3)
        x += 10

def drawDashedLinesBottom():
    x = -10
    while (x < 720):
        fill(255, 255, 0)
        rect(x, 460, x, 3)
        x += 10
        fill(0, 0, 0)
        rect(x, 460, x, 3)
        x += 10

def drawDashedLinesLeft():
    y = -10
    while (y < 720):
        fill(255, 255, 0)
        rect(230, y, 3, y)
        y += 10
        fill(0, 0, 0)
        rect(230, y, 3, y)
        y += 10

def drawDashedLinesRight():
    y = -10
    while (y < 720):
        fill(255, 255, 0)
        rect(460, y, 3, y)
        y += 10
        fill(0, 0, 0)
        rect(460, y, 3, y)
        y += 10
        
def drawSquare():
    fill(25, 255, 255)
    rect(208, 208, 50, 50)
    rect(435, 208, 50, 50)
    rect(435, 435, 50, 50)
    rect(208, 435, 50, 50)

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
        
        self.red = random.randrange(255)
        self.green = random.randrange(255)
        self.blue = random.randrange(255)
        
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
        fill(self.red, self.green, self.blue)
        ellipse(self.positionX * 7, self.positionY * 7, 15, 15)

def setup():
    size(700, 700)
    frameRate(30)
    drawRoads()
    drawDashedLinesTop()
    drawDashedLinesBottom()
    drawDashedLinesLeft()
    drawDashedLinesRight()
    drawSquare()

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
    drawRoads()
    drawDashedLinesTop()
    drawDashedLinesBottom()
    drawDashedLinesLeft()
    drawDashedLinesRight()
    drawSquare()
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

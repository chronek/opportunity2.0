import random
import time

# Black roads
def drawRoads():
    fill(0)
    rect(208, 0, 49, 700)  # left
    rect(436, 0, 49, 700)  # right
    rect(0, 436, 700, 49)  # bottom
    rect(0, 208, 700, 49)  # top

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

    def __init__(self, xCoord, yCoord, id):
        intersections.append(self)
        self.xCoord = xCoord
        self.yCoord = yCoord
        
        #waiting coming from Right, UP, Left, Down
        self.waiting = [0,0,0,0]
        
        self.id = id
        
        self.time = 0
        
        # allows cars from (no direction: -1, left: 1, up: 2, right: 3, down: 0) to procede
        self.allowance = -1
        # selects the next open road
        self.next = 0

    def changeLane(self, direction):
        self.time = 0
        
        self.allowance = direction
        
        
        
    def getWaitingCars(self):
        for car in cars:
            if car.speed == acceleration and abs(car.positionX - self.xCoord) < 3:
                self.waiting[0] += 1
                
    
    
        
    def checkLane(self):
        return self.allowance
    
    def drawIntersection(self, time):
        self.time += 1
        
        if self.allowance == -1 and self.time > 30:
            self.changeLane(self.next)
            self.next = self.next + 1 if self.next < 3 else 0
        elif self.time > time:
            self.allowance = -1
            self.time = 0
    
    
    def drawIntersectionDefault(self):
        self.time += 1
        
        if self.allowance == -1 and self.time > 30:
            self.changeLane(self.next)
            self.next = self.next + 1 if self.next < 3 else 0
        elif self.time > 120:
            self.allowance = -1
            self.time = 0


class Car:

    def __init__(self):
        # up: 0,down: 1,right: 2,left: 3
        self.direction = random.randrange(4)

        self.positionX = 0
        self.positionY = 0
    
        self.stun = 0
        
        self.immunity = 0
        
        self.nextDirection = -1
        
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
            if (abs(intersection.xCoord - posX) < 5 and abs(intersection.yCoord - posY) < 5) and self.immunity != intersection.id:
                if (self.direction != intersection.checkLane()):
                    self.speed = acceleration
                    self.stun = 4
                    return False
                else:
                    #1 means keep going, 2 means turn left, 3 means turn right
                    self.nextDirection = random.randrange(1, 4)
                    
                    if self.nextDirection == 1:
                        self.nextDirection = -1
                    elif self.nextDirection == 2: #turn right
                        if self.direction == 0:
                            self.nextDirection = 2
                        elif self.direction == 1:
                            self.nextDirection = 3
                        elif self.direction == 2:
                            self.nextDirection = 0
                        elif self.direction == 3:
                            self.nextDirection = 1
                    elif self.nextDirection == 3: #turn left
                        if self.direction == 0:
                            self.nextDirection = 3
                        elif self.direction == 1:
                            self.nextDirection = 2
                        elif self.direction == 2:
                            self.nextDirection = 1
                        elif self.direction == 3:
                            self.nextDirection = 0
                        
                        
                    
                    self.immunity = intersection.id
                
                
                
        
        for car in cars:
            if car != self and abs(car.positionX - posX) < 3 and abs(car.positionY - posY) < 3 and car.direction == self.direction:
                self.speed = acceleration
                self.stun = 4
                return False
            
            
        if self.speed < topSpeed:
            self.speed += acceleration
            self.speed = self.speed if self.speed < topSpeed else topSpeed   
        
        if self.stun == 0:
            return True
        else:
            self.stun -= 1
            return False

    def proximity(self, num):
        for car in cars:
            if car != self and abs(car.positionX - self.positionX) < num and abs(car.positionY - self.positionY) < num:
                return False
            
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
        
        if self.nextDirection != -1:
            if self.nextDirection == 0:
                if abs(self.positionX - 67.5) < 1 or abs(self.positionX - 34.5) < 1:
                    if self.proximity(3):
                        self.positionX = 67.5 if abs(self.positionX - 67.5) < 1 else 34.5
                    
                        self.direction = self.nextDirection
                    self.nextDirection = -1
            elif self.nextDirection == 1:
                if abs(self.positionX - 64.5) < 1 or abs(self.positionX - 31.5) < 1:
                    if self.proximity(3):
                        self.positionX = 64.5 if abs(self.positionX - 64.5) < 1 else 31.5
                    
                        self.direction = self.nextDirection
                    self.nextDirection = -1
                self.nextDirection = 2
            elif self.nextDirection == 2:
                if abs(self.positionY - 67.5) < 1 or abs(self.positionY - 34.5) < 1:
                    if self.proximity(3):
                        self.positionY = 67.5 if abs(self.positionY - 67.5) < 1 else 34.5
                    
                        self.direction = self.nextDirection
                    self.nextDirection = -1
            elif self.nextDirection == 3:
                if abs(self.positionY - 64.5) < 1 or abs(self.positionY - 31.5) < 1:
                    if self.proximity(3):
                        self.positionY = 64.5 if abs(self.positionY - 64.5) < 1 else 31.5
                    
                        self.direction = self.nextDirection
                    self.nextDirection = -1
        
        
        

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

intersection(33,33,1)
intersection(33,66,2)
intersection(66,33,3)
intersection(66,66,4)


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
        #print("Intersection allowance: " + str(intersection.allowance))
        intersection.drawIntersectionDefault()

    for car in cars:
        # print(" car position is: " + str(car.positionX) + ", " + str(car.positionY))
        car.drawCar()
        car.move()
    # time.sleep(4)
    
    numZeroSpeed = 0
    for car in cars:
        if car.speed == acceleration:
            numZeroSpeed += 1


    print("number cars waiting per second: " + str(numZeroSpeed))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        # print("car direction: " + str(car.direction) + " car position is: " + str(car.positionX) + ", " + str(car.positionY))

import socket
import threading
import time

class trafficLight:
   def __init__(self, num):
      self.connections = []
      self.intersection = {"num":2}
      lid = num

   def connect_to_nearby(self):
      my_sock = socket.socket()
      my_sock.bind((socket.gethostname(), 5000))
      my_sock.listen()

      while(True):
         my_sock.accept()
         self.connections.append(my_sock)

   def send_to_nearby(self):
      other_sock = socket.socket()
      other_sock.connect((socket.gethostname(), 5000))
      print("Connected")

light1 = trafficLight(1)
light2 = trafficLight(2)


near = [light1, light2]

center = trafficLight(3)

main = threading.Thread(target=center.connect_to_nearby)
main.start()

time.sleep(5)
for x in near:
   x.send_to_nearby()


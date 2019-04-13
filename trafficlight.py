import socket
import threading
import time
class Connection:
   def __init__(self, conn, addr):
      self.conn = conn
      self.addr = addr
      self.light_id = 0
   
   def setName(self, lid):
      self.light_id = int(lid)


class TrafficLight:
   def __init__(self, num, nodes=1):
      self.nodes = nodes
      self.connections = []
      self.intersection = {"num":nodes}
      self.lid = num

   def connect_to_nearby(self):
      my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      my_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      my_sock.bind((socket.gethostname(), 5000))
      my_sock.listen(3)

      while(len(self.connections) < self.nodes):
         conn, addr = my_sock.accept()
         self.connections.append(Connection(conn, addr))

   def send_to_nearby(self):
      other_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      other_sock.connect((socket.gethostname(), 5000))
      self.connections.append(other_sock)
      print("Connected")

   def get_data(self):
      for x in range(len(self.connections)):
         self.connections[x].setName(self.connections[x].conn.recv(1024).decode())

   def send_data(self):
      for x in self.connections:
         x.send((str(self.lid) + '').encode())

light1 = TrafficLight(1)
light2 = TrafficLight(2)


near = [light1, light2]

center = TrafficLight(3, 2)

main = threading.Thread(target=center.connect_to_nearby)
main.start()


for x in near:
   x.send_to_nearby()

main.join()

main = threading.Thread(target=center.get_data)
main.start()

for x in near:
   x.send_data()
main.join()
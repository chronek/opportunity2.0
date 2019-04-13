import socket
import threading
import time

connections = []

class Connection:
   """initialize connection information"""
   def __init__(self, conn, addr):
      self.conn = conn
      self.addr = addr
      self.light_id = 0
      self.client = None
   
   def set_name(self, lid):
      """Set the id of the connection"""
      self.light_id = int(lid)

   def add_client(client):
      """Add the client side of the connection to the object"""
      self.client = client


class TrafficLight:
   """Traffic light object"""
   def __init__(self, num, port, nodes=1):
      self.nodes = nodes
      self.connections = []
      self.lid = num
      self.port = port

   def connect_to_peer(self):
      """Look for connections to other lights nearby"""
      my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      my_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      my_sock.bind((socket.gethostname(), self.port))
      my_sock.listen(3)

      while(True):
         conn, addr = my_sock.accept()
         connections.append(Connection(conn, addr))
         print("Accepted")

   def send_to_peer(self, port):
      """Initiate connections to nearby lights"""
      other_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      other_sock.connect((socket.gethostname(), port))
      #print("Connected")
      return other_sock

   def get_data(self):
      """Get information from peers"""
      for x in range(len(self.connections)):
         self.connections[x].set_name(self.connections[x].conn.recv(1024).decode())

   def send_data(self):
      """Send data to peers"""
      for x in self.connections:
         x.send((str(self.lid) + '').encode())


# Initialize lights
tllight = TrafficLight(1, 5000)
trlight = TrafficLight(2, 5001)
bllight = TrafficLight(3, 5002)
brlight = TrafficLight(4, 5003)

threading.Thread(target=tllight.connect_to_peer).start()
time.sleep(1)
client = trlight.send_to_peer(5000)
connections[0].add_client(client)

print(len(connections))

threading.Thread(target=trlight.connect_to_peer).start()
time.sleep(1)
client = brlight.send_to_peer(5001)
connections[1].add_client(client)

print(len(connections))

threading.Thread(target=brlight.connect_to_peer).start()
time.sleep(1)
client = bllight.send_to_peer(5002)
connections[3].add_client(client)

print(len(connections))

threading.Thread(target=bllight.connect_to_peer).start()
time.sleep(1)
client = tllight.send_to_peer(5003)
connections[4].add_client(client)

print(len(connections))

#main = threading.Thread(target=top_left_light.get_data)
#main.start()

#for x in near:
#   x.send_data()
#main.join()
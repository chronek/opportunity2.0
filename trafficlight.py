import socket
import threading
import time

connections = []
clients = []

class Connection:
   """initialize connection information"""
   def __init__(self, conn, addr):
      """Set connection and address information"""
      self.conn = conn
      self.addr = addr
      self.client = None

   def add_client(client):
      """Add the client side of socket"""
      self.client = client


class TrafficLight:
   """Traffic light object"""
   def __init__(self, num, port, nodes=1):
      self.nodes = nodes
      self.lid = num
      self.port = port

   def connect_to_peer(self):
      """Look for connections to other lights nearby"""
      my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      my_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      my_sock.bind(("127.0.0.1", self.port))
      my_sock.listen(3)

      while(self.nodes != 0):
         conn, addr = my_sock.accept()
         connections.append(Connection(conn, addr))
         self.nodes -= 1

   def send_to_peer(self, port):
      """Initiate connections to nearby lights"""
      other_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      other_sock.connect(("127.0.0.1", port))
      clients.append(other_sock)


# Initialize lights
tllight = TrafficLight(1, 5000)
trlight = TrafficLight(2, 5001)
bllight = TrafficLight(3, 5002)
brlight = TrafficLight(4, 5003)

# Set up threads to schedule
threads = []
threads.append(threading.Thread(target=tllight.connect_to_peer))
threads.append(threading.Thread(target=trlight.connect_to_peer))
threads.append(threading.Thread(target=brlight.connect_to_peer))
threads.append(threading.Thread(target=bllight.connect_to_peer))

# Start up all the traffic light listener threads
for t in threads:
   t.start()

# Wait for traffic lights to listen
time.sleep(3)

# Connect sockets to traffic lights
trlight.send_to_peer(5000)
brlight.send_to_peer(5001)
bllight.send_to_peer(5002)
tllight.send_to_peer(5003)

# Make sure all traffic lights have their communications
for t in threads:
   t.join()

# Put servers and clients together
paths = []
for x in range(len(connections)):
   for y in range(len(clients)):
      if connections[x].addr[1] == clients[y].getsockname()[1]:
         paths.append((clients[y].getpeername()[1], connections[x], clients[y]))

print(paths[0])

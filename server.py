import socket, threading
from collections import defaultdict



class Server():
    def __init__(self,host,port):
        
        self.connections = {

        }
        self.activeconnections = defaultdict(set)
        #setup the socket port
        self.alphasock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.alphasock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

        self.alphasock.bind((host, port))
      

    def get_username(self, connection):
        for username,v in self.connections.items():
            if v ==connection:
                return username
        return False

    def route_msg(self,msg, sender,receiver):
        sconn= self.connections[sender]
        if sender !=receiver:

            for username,v in self.connections.items():
                if username == receiver:
                    rconn= self.connections[receiver]    
                    msg = + sender +": " + msg
                    rconn.send(msg.encode())
                else:
                    sconn.send('The user that you have entered does not exist'.encode())
        else:
            sconn.send("You cannot send a message to yourself".encode())


    def connect_clients(self, sender,rawmsg):
        target = rawmsg.replace("C0NNECT", "")
        self.activeconnections[sender].add(target)
        print("Connected users ", sender,target)
        

    def disconnect_clients(self,sender,rawmsg):
        target = rawmsg.replace("DC0NNECT", "")
        self.activeconnections[sender].discard(target)
        print("Disconnected users ", sender,target)

    def accept_msgs(self, conn,addr):
        while True:
            data =conn.recv(1024)
            print(f"Accepted packets from {addr}")
    
            if not data:
                break
            rawmsg=data.decode().strip()
            if "U0SER" in rawmsg:
                self.add_new_client(rawmsg, conn)
                
            elif "C0NNECT" in rawmsg:
                self.connect_clients(self.get_username(conn), rawmsg)
            elif "DC0NNECT" in rawmsg:
                self.connect_clients(self.get_username(conn), rawmsg)

            else:
                targets = rawmsg.split("-")
                self.route_msg(targets[2],targets[0],targets[1]) # first section is the sender, then receiver, then msg



    def add_new_client(self, username, conn):
        self.connections[username[5:]] =conn
        print(f"registered: {username[5:]}")



server = Server("localhost",8080)
server.alphasock.listen(5)
print("Server Started...")

try:
    while True:
        conn,address =server.alphasock.accept()
        thread = threading.Thread(target=server.accept_msgs, args = (conn,address))
        thread.daemon = True
        thread.start()

except KeyboardInterrupt:
    print("Server closing.")
    server.alphasock.close()
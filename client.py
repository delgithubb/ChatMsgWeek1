import socket,threading



class Client():
    def __init__(self, username, sock):
        self.sock = sock
        self.username=username
        initmsg = "U0SER"+self.username
        sock.send(initmsg.encode())


    def send_msg(self):
        global name
        target = input("Who would you like to send the message: Type the username of the user")
        msg = input(f"Chatting with {target}, type message")
        tmsg = name+ '-' +target+ '-'+ msg
        self.sock.send(tmsg.encode())



    def receive_msg(self):
        while True:
            incmsg = self.sock.recv(1024)
            if not incmsg:
                break
            print("\n"+ incmsg.decode())

    def switch_chats(self):
        pass

    def open_connection(self):
        user = input("Who would you like to connect to. Type the username of the user")
        connectmsg = 'C0NNECT' + user
        self.sock.send(connectmsg.encode())

    def close_connection(self):
        user = input("Who would you like to disconnect to. Type the username of the user")
        disconnectmsg = 'DC0NNECT' + user
        self.sock.send(disconnectmsg.encode())


name = input("Before connecting to the server. Please your user name:")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("localhost", 65422))
    client = Client(name,sock)

    receivemsgthread=threading.Thread(target=client.receive_msg, daemon= True)
    receivemsgthread.start()
            
    while True:
        client.send_msg()

import ds_protocol
import socket
import json
import time
from ds_messenger import *
import Profile as prof
server = "168.235.86.101"
port = 3021
timestamp = str(time.time())


def work():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
        server_conn.connect((server, port))
        stuff = {}
        stuff["join"] = {
                    "username": "help",
                    "password": "mog",
                    "token": ""
                }
        print("joined")
        data_str = json.dumps(stuff)
        server_conn.sendall(data_str.encode())
        response = server_conn.recv(3021).decode()
        response_json = json.loads(response)
        print(response_json)
        if "token" in str(response_json):
            temp = str(response_json).index("token")
            token = str(response_json)[temp+9:-3]
        womp = DirectMessenger("168.235.86.101", "help", "mog")
        #message =input()
        username = womp.return_user()
        password = womp.return_pass()
        
        usernm = prof.Profile(dsuserver= server, username = username, password = password)
        womp.token = token

        womp.send("lmans", "green1")
        womp.retrieve_all()
        womp.retrieve_new()

if __name__ == "__main__":
    work()

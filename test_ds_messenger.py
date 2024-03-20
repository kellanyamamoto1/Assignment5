
import ds_protocol
import socket
import json
import time
import pathlib
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
                    "username": "cap",
                    "password": "pog",
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
        womp = DirectMessenger("168.235.86.101", "cap", "pog")
        person = prof.Profile("168.235.86.101", 'cap', 'pog')
        currrent_dir = pathlib.Path.cwd()
        path = f"{currrent_dir}\\profile.dsu"
        #message =input()
        username = womp.return_user()
        password = womp.return_pass()
        if not pathlib.Path(path).exists():
            with open(path, 'w') as file:
                person.save_profile(path)
        else:
            person.load_profile(path)
        usernm = prof.Profile(dsuserver= server, username = username, password = password)
        womp.token = token
        person.save_messages(womp.retrieve_all_string())
        womp.send("bbbmans", "green1")
        person.save_sent(womp.send_format("hi", 'green1'))
        person.load_sent()
        person.save_profile(path)
        womp.retrieve_all()
        womp.retrieve_new()

        #delete messages in dsu
        # person.del_messages()
        # person.del_sent()
        

if __name__ == "__main__":
    work()

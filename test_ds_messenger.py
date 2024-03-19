
import ds_protocol
import socket
import json
import time
server = "168.235.86.101"
port = 3021
timestamp = str(time.time())



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
    formated = ({
            "token": token,
            "directmessage": {
                "entry": "bruh",
                "recipient": "greenmmm",
                "timestamp": timestamp
        }
        })
    data_str = json.dumps(formated)

    server_conn.sendall(data_str.encode())

    response = server_conn.recv(3021).decode()
    response_json = json.loads(response)
    print(response_json)

    reciv = ({
            "token": token,
            "directmessage": "new"
        })
    data_str = json.dumps(reciv)

    server_conn.sendall(data_str.encode())

    response = server_conn.recv(3021).decode()
    response_json = json.loads(response)
    print(response_json)



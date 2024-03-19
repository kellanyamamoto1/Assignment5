import socket
import json
import time
server = "168.235.86.101"
port = 3021
timestamp = str(time.time())
class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
		
  def send(self, message:str, recipient:str) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
        server_conn.connect((self.dsuserver, port))
        formated = json.dumps({
                "token": self.token,
                "directmessage": {
                    "entry": message,
                    "recipient": recipient,
                    "timestamp": timestamp
                }
            })
        data_str = json.dumps(formated)
        server_conn.sendall(data_str.encode())
        response = server_conn.recv(3021).decode()
        response_json = json.loads(response)
        print(response_json)
    pass
        

		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass

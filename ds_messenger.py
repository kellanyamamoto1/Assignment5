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
    self.username = username
    self.password = password
		
  def send(self, message:str, recipient:str) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
        server_conn.connect((self.dsuserver, port))
        formated = ({
            "token": self.token,
            "directmessage": {
                "entry": message,
                "recipient": recipient,
                'timestamp': timestamp
            }
            })
        data_str = json.dumps(formated)
        server_conn.sendall(data_str.encode())
        response = server_conn.recv(3021).decode()
        response_json = json.loads(response)
        print(response_json)
        print(data_str)
        if "response" in response_json:
            if response_json["response"]["type"] == "ok":
                return True
            else:
                error_message = response_json["response"]["message"]
                print("Error:", error_message)
                return False
        else:
            print("Invalid response from server")
            return False
        

		
  def retrieve_new(self) -> list:
    messages = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
      server_conn.connect((self.dsuserver, port))
      formated = ({
        "token": self.token,
        "directmessage": 'new'
        })

      data_str = json.dumps(formated)
      server_conn.sendall(data_str.encode())
      response = server_conn.recv(3021).decode()
      response_json = json.loads(response)
      if "response" in response_json:
        if response_json["response"]["type"] == "ok":
            msg_list = response_json['response']['messages']
            for msg in msg_list:
                        
              msg_object = DirectMessage()
              msg_object.recipient = msg['from']
              msg_object.message = msg['message']
              msg_object.timestamp = msg['timestamp']
              messages.append(msg_object)
                    
        else:
              error_message = response_json["response"]["message"]
              print("Error:", error_message)
      else:
        print("Invalid response from server")
    return messages
 
  def retrieve_all(self) -> list:
    messages = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
      server_conn.connect((self.dsuserver, port))
      formated = ({
        "token": self.token,
        "directmessage": 'all'
            })

      data_str = json.dumps(formated)
      server_conn.sendall(data_str.encode())
      response = server_conn.recv(3021).decode()
      response_json = json.loads(response)
      if "response" in response_json:
        if response_json["response"]["type"] == "ok":
          msg_list = response_json['response']['messages']
          for msg in msg_list:
            print(msg)
            msg_object = DirectMessage()
            msg_object.recipient = msg['from']
            msg_object.message = msg['message']
            msg_object.timestamp = msg['timestamp']
            messages.append(msg_object)
                    
        else:
          error_message = response_json["response"]["message"]
          print("Error:", error_message)
      else:
            print("Invalid response from server")
    return messages
    

  def return_user(self):
        return self.username
    
  def return_pass(self):
        return self.password
    
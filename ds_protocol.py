# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

import json
import time
from collections import namedtuple
timestamp = str(time.time())
DataTuple = namedtuple('DataTuple', ['foo','baz'])


def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)


def format_for_json(action, username, password, user_token=None, message=None, bio=None, recipient=None):
  formated = None
  if action == "join":
    formated = json.dumps({
      "join": {
        "username": username,
        "password": password,
        "tokens": user_token
      }
    })
  elif action == 'post':
        if not user_token:
            raise ValueError("no user token breh go get that shi")
        formated = ({
            "token": user_token,
            "post": {
                "entry": message,
                "timestamp": timestamp
            }
        })
  elif action == 'bio':
        if not user_token:
            raise ValueError("go get it bruh bruh")
        formated = json.dumps({
            "token": user_token,
            "bio": {
                "entry": bio,
                "timestamp": timestamp
            }
        })
  elif action == 'directmessage':
        if not user_token:
            raise ValueError("no user token")
        if message:
            formated = json.dumps({
                "token": user_token,
                "directmessage": {
                    "entry": message,
                    "recipient": recipient,
                    "timestamp": timestamp
                }
            })

  return formated

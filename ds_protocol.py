# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

import test_ds_message_protocol
import json
import time
from collections import namedtuple
timestamp = str(time.time())
DataTuple = namedtuple('DataTuple', ['type', 'message'])


def json_to_dict(json_msg: str) -> dict:
    """
    Convert a JSON message to a dictionary.
    """
    try:
        return json.loads(json_msg)
    except json.JSONDecodeError:
        print("Json cannot be decoded.1")
        return {}


def json_to_list(json_msg: str) -> list:
    """
    Convert a JSON message to a list.
    """
    try:
        return json.loads(json_msg)
    except json.JSONDecodeError:
        print("Json cannot be decoded.2")
        return []


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a
    json string and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get('response', {})
        if 'type' in response and 'message' in response:
            return DataTuple(response['type'], response['message'])
    except json.JSONDecodeError:
        print("Json cannot be decoded.3")

    return None


def format_for_json(
        action,
        username,
        password,
        user_token=None,
        message=None,
        bio=None,
        recipient=None):
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
            raise ValueError("no user token1")
        formated = ({
            "token": user_token,
            "post": {
                "entry": message,
                "timestamp": timestamp
            }
        })
    elif action == 'bio':
        if not user_token:
            raise ValueError("no user token2")
        formated = json.dumps({
            "token": user_token,
            "bio": {
                "entry": bio,
                "timestamp": timestamp
            }
        })
    elif action == 'directmessage':
        if not user_token:
            raise ValueError("no user token3")
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

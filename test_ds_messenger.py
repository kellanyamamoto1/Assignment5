
import ds_protocol

# Test message for direct message sent successfully
direct_message_sent_msg = '{"response": {"type": "ok", "message": "Direct message sent"}}'

# Test message for response to request for all and new messages
all_messages_msg = {
  "response": {
    "type": "ok",
    "messages": [
      {"message": "Hello User 1!", "from": "markb", "timestamp": "1603167689.3928561"},
      {"message": "Bzzzzz", "from": "thebeemoviescript", "timestamp": "1603167689.3928561"}
    ]
  }
}


# Test message for invalid JSON
invalid_json_msg = '{}'

# Test the extract_json function with sample messages
def test_extract_json():
    assert ds_protocol.extract_json(direct_message_sent_msg) == ('ok', 'Direct message sent')
    
    assert ds_protocol.extract_json(all_messages_msg) == ('ok', [
        {"message": "Hello User 1!", "from": "markb", "timestamp": "1603167689.3928561"},
        {"message": "Bzzzzz", "from": "thebeemoviescript", "timestamp": "1603167689.3928561"}
    ])
    
    assert ds_protocol.extract_json(invalid_json_msg) == None
    print("extract_json works")
    

# Test message for JSON to dictionary conversion
json_msg = '{"key": "value"}'

# Test the json_to_dict function
def test_json_to_dict():
    assert ds_protocol.json_to_dict(json_msg) == {'key': 'value'}
    print("json_to_dict works")

# Test message for JSON to list conversion
json_list_msg = '[1, 2, 3]'

# Test the json_to_list function
def test_json_to_list():
    assert ds_protocol.json_to_list(json_list_msg) == [1, 2, 3]
    print(json_list_msg)

# Run all test functions
def run_tests():
    test_extract_json()
    test_json_to_dict()
    test_json_to_list()

# Run the tests
run_tests()

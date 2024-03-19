# Kellan Yamamoto
# 28388886
# kellany@uci.edu


import administration as admin
import ds_client
import ds_protocol
import ui as ui

if __name__ == "__main__":
    ds_client.send("168.235.86.101", 3021, "help", "mog", "fn") #token: 1269c913-8909-49ce-8f8f-f510140fcda9
    ui.start() 
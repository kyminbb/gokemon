import json

from websocket import create_connection


if __name__ == '__main__':
    ws = create_connection("ws://protected-stream-83870.herokuapp.com/")
    msg = dict()
    msg["from"] = {
        "name": "Doublade",
        "moves": ["shadowsneak", "Iron Head"]
    }
    msg["to"] = {
        "name": "Dialga"
    }
    msg = json.dumps(msg)
    print(msg)
    ws.send(msg)
    data = ws.recv()
    print(data)
    ws.close()

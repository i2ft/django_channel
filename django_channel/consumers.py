from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from django.shortcuts import render


# Connected to websocket.connect
def ws_add(message):
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    print("ws_message")
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)

def http_consumer(message):
    print("http_consumer")
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


def ws_message1(message):
    print ("ws_message")
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.

    message.reply_channel.send({
        "text": message.content['text'],
    })

`pip install -U channels`

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        ...
        'channels',
    )
    
`python manage.py startapp customer`

**cusomter.py**

    from django.http import HttpResponse
    from channels.handler import AsgiHandler
    
    def http_consumer(message):
        # Make standard HTTP response - access ASGI path attribute directly
        response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
        # Encode that response into message format (ASGI)
        for chunk in AsgiHandler.encode_response(response):
            message.reply_channel.send(chunk)
            
 
**In settings.py**
 
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgiref.inmemory.ChannelLayer",
            "ROUTING": "프로젝트이름.routing.channel_routing",
        },
    }

**In routing.py**

    from channels.routing import route
    channel_routing = [
        route("http.request", "앱이름.consumers.http_consumer"),
    ]
    
    
    
    
    
    
    
    
    
    
------------------------------------------------------------------------------
#메시지보내기

**In consumers.py**




    def ws_message(message):
        # ASGI WebSocket packet-received and send-packet message types
        # both have a "text" key for their textual data.
        message.reply_channel.send({
            "text": message.content['text'],
        })

**In routing.py**

    from channels.routing import route
    from 앱이름.consumers import ws_message
    
    channel_routing = [
        route("websocket.receive", ws_message),
    ]
    
**index.html**

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    <script>
     $( document ).ready(function() {
         socket = new WebSocket("ws://127.0.0.1:8000/chat/");
    
         socket.onmessage = function(e) {
             alert(e.data);
         }
    
    
         $( "#b" ).click(function() {
             alert("클릭")
      socket.send("hello world");
    });
        });
        </script>
    </head>
    <body>
    <button id="b" >버튼</button>
    </body>
    </html>
    
    
    
    
---

#Groups

**In consumers.py**

    from channels import Group
    
    # Connected to websocket.connect
    def ws_add(message):
        Group("chat").add(message.reply_channel)
    
    # Connected to websocket.receive
    def ws_message(message):
        Group("chat").send({
            "text": "[user] %s" % message.content['text'],
        })
    
    # Connected to websocket.disconnect
    def ws_disconnect(message):
        Group("chat").discard(message.reply_channel)
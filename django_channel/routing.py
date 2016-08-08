from channels.routing import route
from django_channel.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    route("http.request", "django_channel.consumers.http_consumer"),
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
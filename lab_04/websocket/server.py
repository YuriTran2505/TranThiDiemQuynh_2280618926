import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)
        print(f"New client connected. Total clients: {len(self.clients)}")

    def on_close(self):
        WebSocketServer.clients.remove(self)
        print(f"Client disconnected. Remaining clients: {len(self.clients)}")

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        for client in cls.clients:
            try:
                client.write_message(message)
            except:
                print("Error sending message to a client")
                cls.clients.remove(client)

class RandomWordsSelector:
    def __init__(self, word_list):
        self.word_list = word_list
    
    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)
    print("WebSocket server started on port 8888")

    io_loop = tornado.ioloop.IOLoop.current()

    word_selector = RandomWordsSelector(['apple', 'banana', 'orange', 'grape', 'melon'])
    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()),
        3000
    )
    periodic_callback.start()

    try:
        io_loop.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        periodic_callback.stop()
        io_loop.stop()

if __name__ == "__main__":
    main()
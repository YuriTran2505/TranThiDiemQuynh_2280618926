import tornado.ioloop
import tornado.websocket

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop

    def start(self):
        self.connect_and_read()

    def stop(self):
        if self.connection:
            self.connection.close()
        self.io_loop.stop()

    def connect_and_read(self):
        print("Connecting to server...")
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",
            callback=self.maybe_retry_connection,
            on_message_callback=self.on_message,
            ping_interval=30,
            ping_timeout=30,
        )

    def maybe_retry_connection(self, future) -> None:
        try:
            self.connection = future.result()
            print("Connected to server!")
            # Start reading messages
            self.connection.read_message(callback=self.on_message)
        except Exception as e:
            print(f"Connection failed: {e}, retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("Disconnected from server, reconnecting...")
            self.connect_and_read()
            return
        print(f"Received word from server: {message}")
        # Continue reading next message
        self.connection.read_message(callback=self.on_message)

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    
    try:
        io_loop.add_callback(client.start)
        io_loop.start()
    except KeyboardInterrupt:
        print("\nClient shutting down...")
        client.stop()

if __name__ == "__main__":
    main()
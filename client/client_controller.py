import socket

class ClientController:
    def __init__(self):
        self.reverse_server = socket.socket()
        self.reverse_conn = None

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def start_reverse_listener(self, port=8081):
        self.reverse_server.bind(("0.0.0.0", port))
        self.reverse_server.listen(1)
        print("Lắng nghe reverse connect tại port 8081")
        self.reverse_conn, addr = self.reverse_server.accept()
        print(f"Reverse connect từ {addr}")
        return self.reverse_conn

    def receive_data(self):
        if self.reverse_conn:
            size = int.from_bytes(self.reverse_conn.recv(4), 'big')
            data = self.reverse_conn.recv(size).decode()
            return data
        return None

    def receive_image(self):
        if self.reverse_conn:
            size = int.from_bytes(self.reverse_conn.recv(4), 'big')
            data = self.reverse_conn.recv(size)
            from io import BytesIO
            from PIL import Image
            return Image.open(BytesIO(data))
        return None

    def close(self):
        if self.reverse_conn:
            self.reverse_conn.close()
        self.reverse_server.close()
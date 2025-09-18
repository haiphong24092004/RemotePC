import socket
import os
import pyautogui
from mss import mss
from PIL import Image
import io
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import threading
import time
import sys

class ServerController:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.server_socket = socket.socket()
        self.reverse_conn = None
        self.streaming = False

    def start_server(self, host="0.0.0.0", port=8080):
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        print(f"Server lắng nghe tại {host}:{port}")
        while True:
            conn, addr = self.server_socket.accept()
            client_ip = conn.recv(1024).decode()
            print(f"Nhận IP client: {client_ip}")
            if self.reverse_connect(client_ip, 8081):
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def reverse_connect(self, client_ip, port=8081):
        try:
            self.reverse_conn = socket.socket()
            self.reverse_conn.connect((client_ip, port))
            print(f"Reverse connect đến {client_ip}:{port}")
            return True
        except Exception as e:
            print(f"Lỗi reverse connect: {e}")
            return False

    def handle_client(self, conn):
        while True:
            try:
                command = self.reverse_conn.recv(1024).decode()
                if not command:
                    break
                print(f"Lệnh từ client: {command}")

                if command.startswith("shutdown"):
                    parts = command.split()
                    hours, minutes = (int(parts[1]), int(parts[2])) if len(parts) == 3 else (0, 0)
                    response = self.schedule_shutdown(hours, minutes)
                    self.reverse_conn.send(len(response).to_bytes(4, 'big'))
                    self.reverse_conn.send(response.encode())
                elif command.startswith("restart"):
                    parts = command.split()
                    hours, minutes = (int(parts[1]), int(parts[2])) if len(parts) == 3 else (0, 0)
                    response = self.schedule_restart(hours, minutes)
                    self.reverse_conn.send(len(response).to_bytes(4, 'big'))
                    self.reverse_conn.send(response.encode())
                elif command.startswith("open_app"):
                    parts = command.split()
                    app_name, hours, minutes = (parts[1], int(parts[2]), int(parts[3])) if len(parts) == 4 else ("chrome", 0, 0)
                    response = self.schedule_open_app(app_name, hours, minutes)
                    self.reverse_conn.send(len(response).to_bytes(4, 'big'))
                    self.reverse_conn.send(response.encode())
                elif command == "cancel_schedule":
                    response = self.cancel_schedule()
                    self.reverse_conn.send(len(response).to_bytes(4, 'big'))
                    self.reverse_conn.send(response.encode())
                elif command == "start_stream":
                    self.streaming = True
                    threading.Thread(target=self.stream_screen, daemon=True).start()
                    self.reverse_conn.send("Stream started".encode())
                elif command == "stop_stream":
                    self.streaming = False
                    self.reverse_conn.send("Stream stopped".encode())
                elif command == "screenshot":
                    self.send_screenshot()
                elif command.startswith("upload_file"):
                    _, filename, size = command.split()
                    size = int(size)
                    data = self.reverse_conn.recv(size)
                    with open(filename, 'wb') as f:
                        f.write(data)
                    self.reverse_conn.send("Upload thành công".encode())
                else:
                    self.reverse_conn.send("Lệnh không hợp lệ".encode())
            except Exception as e:
                print(f"Lỗi: {e}")
                break
        self.close()

    def stream_screen(self):
        while self.streaming:
            try:
                self.send_screenshot()
                time.sleep(0.5)
            except:
                self.streaming = False
                break

    def send_screenshot(self):
        with mss() as sct:
            sct.shot(mon=-1)
        img = Image.open("mon.png")
        img = img.resize((800, 600))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=70)
        data = buffer.getvalue()
        self.reverse_conn.send(len(data).to_bytes(4, 'big'))
        self.reverse_conn.send(data)
        os.remove("mon.png")

    def schedule_shutdown(self, hours, minutes):
        now = datetime.datetime.now()
        target = now + datetime.timedelta(hours=int(hours), minutes=int(minutes))
        self.scheduler.add_job(self._shutdown, 'date', run_date=target)
        return f"Tắt máy lúc {target}"

    def schedule_restart(self, hours, minutes):
        now = datetime.datetime.now()
        target = now + datetime.timedelta(hours=int(hours), minutes=int(minutes))
        self.scheduler.add_job(self._restart, 'date', run_date=target)
        return f"Khởi động lại lúc {target}"

    def schedule_open_app(self, app, hours, minutes):
        now = datetime.datetime.now()
        target = now + datetime.timedelta(hours=int(hours), minutes=int(minutes))
        self.scheduler.add_job(self._open_app, 'date', run_date=target, args=[app])
        return f"Mở {app} lúc {target}"

    def cancel_schedule(self):
        self.scheduler.remove_all_jobs()
        return "Đã hủy tất cả lịch"

    def _shutdown(self):
        if sys.platform == "win32":
            os.system("shutdown /s /t 0")
        elif sys.platform == "linux":
            os.system("shutdown -h now")

    def _restart(self):
        if sys.platform == "win32":
            os.system("shutdown /r /t 0")
        elif sys.platform == "linux":
            os.system("reboot")

    def _open_app(self, app_name):
        if app_name.lower() == "chrome":
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        else:
            try:
                os.startfile(app_name)
            except:
                pass  

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
        self.streaming = False
        if self.reverse_conn:
            self.reverse_conn.close()
        self.server_socket.close()
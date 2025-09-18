import tkinter as tk
from tkinter import messagebox
from server_controller import ServerController
from shutdown_page import ShutdownPage
from restart_page import RestartPage
from open_app_page import OpenAppPage
from cancel_schedule_page import CancelSchedulePage
import threading

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Desktop Server")
        self.root.geometry("1100x650")
        self.root.configure(bg="#E6F0FA")
        self.root.eval('tk::PlaceWindow . center')

        self.controller = ServerController()
        self.current_page = None

        self.logo = tk.PhotoImage(file="img/logo.png")
        logo_width = self.logo.width()
        logo_height = self.logo.height()
        if logo_width > 300 or logo_height > 300:  
            scale = min(300/logo_width, 300/logo_height)
            new_width = int(logo_width * scale)
            new_height = int(logo_height * scale)
            self.logo = self.logo.subsample(int(1/scale))

        self.show_main_screen()

    def show_main_screen(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#E6F0FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_page = main_frame

        left_frame = tk.Frame(main_frame, bg="#E6F0FA")
        left_frame.pack(side="left", fill="y", padx=20)

        right_frame = tk.Frame(main_frame, bg="#E6F0FA")
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        tk.Label(left_frame, image=self.logo, bg="#E6F0FA").pack(pady=40)

        tk.Label(
            right_frame,
            text="Server Status: Chờ kết nối",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))

        ip_frame = tk.Frame(right_frame, bg="#E6F0FA")
        ip_frame.pack(pady=10)
        tk.Label(ip_frame, text="IP Client:", bg="#E6F0FA", fg="#004080", font=("Arial", 12)).pack(side="left", padx=5)
        self.client_ip_entry = tk.Entry(ip_frame, width=22, font=("Arial", 12))
        self.client_ip_entry.pack(side="left", padx=5)
        tk.Button(
            ip_frame,
            text="Kết nối",
            command=self.reverse_connect,
            font=("Arial", 12, "bold"),
            bg="#32CD32",
            fg="black",
            activebackground="#228B22",
            activeforeground="black",
            relief="raised",
            bd=2,
            width=10,
            height=2
        ).pack(side="left", padx=5)

        self.btn_config = {
            "font": ("Arial", 12, "bold"),
            "bg": "#1E90FF",
            "fg": "black",
            "activebackground": "#4682B4",
            "activeforeground": "black",
            "relief": "raised",
            "bd": 3,
            "width": 35,
            "height": 4,
            "cursor": "hand2"
        }

        buttons = [
            ("🚀 Bắt đầu Server", self.start_server),
            ("⏰ Đặt lịch tắt máy", lambda: self.show_page(ShutdownPage)),
            ("🔄 Đặt lịch khởi động", lambda: self.show_page(RestartPage)),
            ("📂 Đặt lịch mở ứng dụng", lambda: self.show_page(OpenAppPage)),
            ("❌ Hủy lịch", lambda: self.show_page(CancelSchedulePage)),
        ]

        for text, cmd in buttons:
            btn = tk.Button(right_frame, text=text, command=cmd, **self.btn_config)
            btn.pack(pady=6)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#004080"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1E90FF"))

    def show_page(self, page_class):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_class(self.root, self)
        self.current_page.pack(expand=True, fill="both")

    def start_server(self):
        threading.Thread(target=self.controller.start_server, daemon=True).start()
        messagebox.showinfo("Info", "Server đang chạy")

    def reverse_connect(self):
        ip = self.client_ip_entry.get()
        if ip:
            if self.controller.reverse_connect(ip):
                messagebox.showinfo("Thành công", "Reverse connected")
            else:
                messagebox.showerror("Lỗi", f"Không thể kết nối đến {ip}:8081")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập IP Client")

    def clear_window(self):
        if self.current_page:
            self.current_page.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
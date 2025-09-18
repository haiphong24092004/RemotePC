import tkinter as tk
from tkinter import messagebox
from client_controller import ClientController
import threading
import os
import pyperclip  

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Desktop Client")
        self.root.geometry("1100x650")
        self.root.configure(bg="#E6F0FA")
        self.root.eval('tk::PlaceWindow . center')

        self.controller = ClientController()
        self.client_ip = self.controller.get_local_ip()
        self.current_page = None

        self.logo = tk.PhotoImage(file="img/logo.png")
        logo_width = self.logo.width()
        logo_height = self.logo.height()
        if logo_width > 300 or logo_height > 300:  
            scale = min(300/logo_width, 300/logo_height)
            new_width = int(logo_width * scale)
            new_height = int(logo_height * scale)
            self.logo = self.logo.subsample(int(1/scale))

        threading.Thread(target=self.controller.start_reverse_listener, daemon=True).start()

        self.show_connect_screen()

    def show_connect_screen(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#E6F0FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_page = main_frame

        left_frame = tk.Frame(main_frame, bg="#E6F0FA")
        left_frame.pack(side="left", fill="y", padx=20)

        right_frame = tk.Frame(main_frame, bg="#E6F0FA")
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        tk.Label(left_frame, image=self.logo, bg="#E6F0FA").pack(pady=40)

        content_frame = tk.Frame(right_frame, bg="#E6F0FA")
        content_frame.pack(expand=True)  

        tk.Label(
            content_frame,
            text="Client Status: Chờ kết nối",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 20), anchor="center")

        ip_frame = tk.Frame(content_frame, bg="#E6F0FA")
        ip_frame.pack(pady=10)

        tk.Label(
            ip_frame,
            text=f"IP của máy bạn: {self.client_ip}",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 24, "bold")
        ).pack(pady=5, anchor="center")
        tk.Label(
            ip_frame,
            text="Gửi IP này cho Server để kết nối",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 14, "bold")
        ).pack(pady=5, anchor="center")

        copy_btn = tk.Button(
            ip_frame,
            text="Copy IP",
            command=lambda: pyperclip.copy(self.client_ip),
            font=("Arial", 12, "bold"),
            bg="#FFD700",
            fg="black",
            activebackground="#FFC107",
            activeforeground="black",
            relief="raised",
            bd=2,
            width=10,
            height=2,
            cursor="hand2"
        )
        copy_btn.pack(pady=5)
        copy_btn.bind("<Enter>", lambda e: copy_btn.config(bg="#FFC107"))
        copy_btn.bind("<Leave>", lambda e: copy_btn.config(bg="#FFD700"))

        connect_btn = tk.Button(
            ip_frame,
            text="Kết nối",
            command=self.send_ip_to_server,
            font=("Arial", 12, "bold"),
            bg="#32CD32",
            fg="black",
            activebackground="#228B22",
            activeforeground="black",
            relief="raised",
            bd=2,
            width=10,
            height=2,
            cursor="hand2"
        )
        connect_btn.pack(pady=10)
        connect_btn.bind("<Enter>", lambda e: connect_btn.config(bg="#228B22"))
        connect_btn.bind("<Leave>", lambda e: connect_btn.config(bg="#32CD32"))

    def show_page(self, page_class):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_class(self.root, self)
        self.current_page.pack(expand=True, fill="both")

    def send_ip_to_server(self):
        if self.controller.reverse_conn:
            self.controller.reverse_conn.send(self.client_ip.encode())
            messagebox.showinfo("Info", "IP đã được gửi, chờ Server kết nối")
            self.show_page(MainMenuPage)
        else:
            messagebox.showerror("Lỗi", "Chưa sẵn sàng kết nối ngược. Đảm bảo server đã kết nối đến cổng 8081.")

    def clear_window(self):
        if self.current_page:
            self.current_page.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()

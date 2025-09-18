import tkinter as tk
from tkinter import messagebox

class ShutdownPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg="#E6F0FA")
        self.controller = controller

        tk.Label(
            self,
            text="Đặt lịch tắt máy",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 18, "bold")
        ).pack(pady=20, expand=True)

        time_frame = tk.Frame(self, bg="#E6F0FA")
        time_frame.pack(pady=20, expand=True)
        tk.Label(
            time_frame,
            text="Giờ:",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        self.hours_entry = tk.Entry(
            time_frame,
            width=8,
            font=("Arial", 14)
        )
        self.hours_entry.pack(side="left", padx=10)
        tk.Label(
            time_frame,
            text="Phút:",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        self.minutes_entry = tk.Entry(
            time_frame,
            width=8,
            font=("Arial", 14)
        )
        self.minutes_entry.pack(side="left", padx=10)

        confirm_btn = tk.Button(
            self,
            text="Xác nhận",
            command=self.schedule_shutdown,
            bg="#32CD32",
            fg="black",
            font=("Arial", 14, "bold"),
            activebackground="#228B22",
            activeforeground="black",
            relief="raised",
            bd=4,
            width=25,
            height=2,
            cursor="hand2"
        )
        confirm_btn.pack(pady=15, expand=True)
        confirm_btn.bind("<Enter>", lambda e: confirm_btn.config(bg="#228B22"))
        confirm_btn.bind("<Leave>", lambda e: confirm_btn.config(bg="#32CD32"))

        back_btn = tk.Button(
            self,
            text="Quay lại",
            command=lambda: controller.show_main_screen(),
            bg="#FF4500",
            fg="black",
            font=("Arial", 14, "bold"),
            activebackground="#CC3700",
            activeforeground="black",
            relief="raised",
            bd=4,
            width=25,
            height=2,
            cursor="hand2"
        )
        back_btn.pack(pady=15, expand=True)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#CC3700"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#FF4500"))

    def schedule_shutdown(self):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            if hours >= 0 and minutes >= 0:
                self.controller.controller.reverse_conn.send(f"shutdown {hours} {minutes}".encode())
                response = self.controller.controller.receive_data()
                messagebox.showinfo("Thành công", response)
                self.controller.show_main_screen()
            else:
                messagebox.showerror("Lỗi", "Giờ và phút phải là số không âm")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho giờ và phút")
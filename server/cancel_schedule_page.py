import tkinter as tk
from tkinter import messagebox

class CancelSchedulePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg="#E6F0FA")
        self.controller = controller

        tk.Label(
            self,
            text="Hủy tất cả lịch",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 18, "bold")
        ).pack(pady=20, expand=True)

        tk.Label(
            self,
            text="Bạn có chắc chắn muốn hủy tất cả lịch?",
            bg="#E6F0FA",
            fg="#004080",
            font=("Arial", 14)
        ).pack(pady=20, expand=True)

        confirm_btn = tk.Button(
            self,
            text="Xác nhận",
            command=self.cancel_schedule,
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

    def cancel_schedule(self):
        self.controller.controller.reverse_conn.send("cancel_schedule".encode())
        response = self.controller.controller.receive_data()
        messagebox.showinfo("Thành công", response)
        self.controller.show_main_screen()
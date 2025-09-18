<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
        🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
    Ứng dụng tra cứu thời tiết online
</h2>

<div align="center">
    <p align="center">
        <img src="aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="fitdnu_logo.png" alt="FIT Logo" width="180"/>
        <img src="dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>


# Remote Desktop Control

Dự án **Remote Desktop Control** cho phép người dùng điều khiển máy tính từ xa theo mô hình **Client - Server**.  
Hệ thống được xây dựng bằng Python với giao diện đồ họa `Tkinter`, hỗ trợ các chức năng chính:

- Kết nối **Server ↔ Client** qua socket.
- Đặt lịch **tắt máy, khởi động lại, mở ứng dụng** từ xa.
- **Hủy lịch** đã đặt.
- Truyền dữ liệu và nhận phản hồi theo thời gian thực.
- Hỗ trợ chụp ảnh màn hình, stream màn hình từ Client về Server.

---

## 👨‍💻 Tác giả
**Nguyễn Hải Phong**

---

## 📦 Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8+
- Hệ điều hành: Windows / Linux

### 2. Cài đặt thư viện
Chạy lệnh sau để cài toàn bộ dependencies:

```bash
pip install pillow mss pyautogui apscheduler pyperclip
```

> Lưu ý: Trên Linux, có thể cần cài thêm `python3-tk` để dùng Tkinter:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🚀 Chạy chương trình

### 1. Khởi động Server
```bash
python server_gui.py
```

### 2. Khởi động Client
```bash
python client_gui.py
```

### 3. Kết nối
- Chạy **Server** trước, nhập IP của Client vào Server.
- Client sẽ hiển thị IP của mình để gửi cho Server.
- Khi kết nối thành công, bạn có thể bắt đầu sử dụng các chức năng.

---

## 📸 Demo

### Giao diện Server
![Server Demo](demo/server.png)

### Giao diện Client
![Client Demo](demo/client.png)

---

## 🛠️ Chức năng chính
- **⏰ Đặt lịch tắt máy**: Hẹn giờ tự động tắt máy client.
- **🔄 Đặt lịch khởi động lại**: Hẹn giờ restart máy client.
- **📂 Đặt lịch mở ứng dụng**: Mở ứng dụng chỉ định vào thời gian mong muốn.
- **❌ Hủy lịch**: Xóa toàn bộ các tác vụ đã đặt.
- **📸 Chụp/stream màn hình** (mở rộng từ `server_controller`).

---

## 📄 License
Dự án dành cho mục đích học tập và nghiên cứu.  
Bạn có thể tự do sử dụng và chỉnh sửa.

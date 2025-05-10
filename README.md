# Ứng Dụng Web Chuyển Đổi Giọng Nói Thành Văn Bản

Một ứng dụng web giúp người dùng nhanh chóng chuyển đổi giọng nói thành văn bản bằng cách sử dụng mô hình Whisper của OpenAI chạy cục bộ. Ứng dụng hỗ trợ cả tiếng Anh và tiếng Việt.

## Tính Năng

- Ghi âm từ web trên màn hình laptop
- Chuyển đổi sang văn bản bằng mô hình Whisper của OpenAI (audio và transcript được lưu ở backend\storage theo định dạng YYYY-MM-DD (ví dụ: 2025-05-10))
- Hỗ trợ tiếng Anh và tiếng Việt
- Chọn các kích thước mô hình Whisper khác nhau để cân bằng giữa độ chính xác và tốc độ
- Tự động lưu các bản ghi âm và bản chuyển đổi trong cấu trúc thư mục có tổ chức
- Sao chép bản chuyển đổi vào clipboard chỉ với một cú nhấp chuột

## Yêu Cầu

- Python 3.8+
- Trình duyệt web hỗ trợ MediaRecorder API (hầu hết các trình duyệt hiện đại)
- RAM và sức mạnh xử lý đủ để chạy các mô hình Whisper:
  - Đề xuất: 16GB RAM, GPU hỗ trợ CUDA (cho các mô hình trung bình/lớn)
  - Tối thiểu: 8GB RAM (cho các mô hình nhỏ/cơ bản)

## Cài Đặt và Thiết Lập

1. Sao chép kho lưu trữ này:
   ```
   git clone <repository-url>
   cd speech-to-text-app
   ```

2. Tạo một môi trường ảo Python và kích hoạt nó:
   ```
   python -m venv venv
   
   # Trên Windows
   venv\Scripts\activate
   
   # Trên macOS/Linux
   source venv/bin/activate
   ```

3. Cài đặt các gói Python cần thiết:
   ```
   pip install -r backend/requirements.txt
   ```

4. Khởi động ứng dụng:
   ```
   cd backend
   python main.py
   ```

5. Mở trình duyệt web của bạn và điều hướng đến:
   ```
   http://localhost:8000
   ```

## Cách Sử Dụng

1. Chọn ngôn ngữ bạn muốn (tiếng Anh hoặc tiếng Việt)
2. Chọn kích thước mô hình Whisper (cân bằng giữa tốc độ và độ chính xác)
3. Nhấp vào nút microphone để bắt đầu ghi âm
4. Nói vào microphone của bạn
5. Nhấp vào nút dừng để kết thúc ghi âm
6. Chờ quá trình chuyển đổi hoàn tất
7. Xem bản chuyển đổi của bạn và sử dụng nút sao chép để sao chép vào clipboard

## Cấu Trúc Thư Mục

```
speech-to-text-app/
├── backend/             # Backend Python FastAPI
│   ├── main.py          # Ứng dụng FastAPI chính
│   ├── transcription.py # Mô-đun chuyển đổi Whisper
│   └── requirements.txt # Các phụ thuộc Python
├── frontend/            # Giao diện web
│   ├── index.html       # Trang HTML chính
│   ├── css/             # Các kiểu CSS
│   │   └── style.css
│   └── js/              # JavaScript
│       └── app.js
├── storage/             # Lưu trữ bản ghi âm và bản chuyển đổi
│   └── YYYY-MM-DD/      # Thư mục theo ngày
│       └── HHMMSS/      # Thư mục theo phiên
│           ├── audio.webm       # Ghi âm
│           └── transcription.txt # Văn bản chuyển đổi
└── README.md            # Tài liệu dự án
```

## Chi Tiết Kỹ Thuật

- **Backend**: Python với FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Chuyển Đổi Giọng Nói Thành Văn Bản**: Mô hình Whisper của OpenAI (chạy cục bộ)
- **Lưu Trữ Dữ Liệu**: Hệ thống tệp cục bộ với cấu trúc thư mục có tổ chức


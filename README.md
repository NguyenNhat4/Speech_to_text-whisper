# Chuyển Đổi Giọng Nói Thành Văn Bản

 ứng dụng web giúp người dùng nhanh chóng chuyển đổi giọng nói thành văn bản bằng cách sử dụng mô hình Whisper của OpenAI chạy cục bộ. Ứng dụng hỗ trợ cả tiếng Anh và tiếng Việt.

## Tính Năng

- Ghi âm từ web trên màn hình laptop
- Chuyển đổi sang văn bản bằng mô hình Whisper của OpenAI (audio và transcript được lưu ở backend\storage theo định dạng YYYY-MM-DD (ví dụ: 2025-05-10))
- Hỗ trợ tiếng Anh và tiếng Việt
- Chọn các kích thước mô hình Whisper khác nhau để cân bằng giữa độ chính xác và tốc độ
- Tự động lưu các bản ghi âm và bản chuyển đổi trong cấu trúc thư mục có tổ chức
- Sao chép bản chuyển đổi vào clipboard chỉ với một cú nhấp chuột
## UI
![image](https://github.com/user-attachments/assets/542f58ec-81f8-45a6-90c3-1ca51eaf6ccb)


## Yêu Cầu

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


4. tải ffmpeg về hệ thống:
   ```
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg
    
    # on Arch Linux
    sudo pacman -S ffmpeg
    
    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg
    
    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg
    
    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
   ```

5. Khởi động ứng dụng:
   ```
   cd backend
   python main.py
   ```

6. Mở trình duyệt web của bạn và điều hướng đến:
   ```
   http://localhost:8000/app/
   ```


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


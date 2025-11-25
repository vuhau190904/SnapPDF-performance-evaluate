# ⚡ Quick Start Guide

Hướng dẫn nhanh để chạy JMeter performance test trong 5 phút!

## 🚀 Các Bước Nhanh

### 1. Cài Đặt JMeter
```bash
# macOS
brew install jmeter

# Hoặc download từ: https://jmeter.apache.org/download_jmeter.cgi
```

### 2. Cài Đặt Python và Pillow
```bash
# Kiểm tra Python
python3 --version

# Cài Pillow
pip install Pillow
```

### 3. Tạo Test Images
```bash
cd jmeter-performance-test
python3 generate-test-images.py
```

### 4. Cập Nhật JWT Tokens
Mở file `test-data/auth-tokens.csv` và thay thế bằng JWT tokens thực của bạn:
```csv
token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.YOUR_REAL_TOKEN_HERE
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.YOUR_REAL_TOKEN_HERE
```

### 5. Chạy Test

#### Option A: GUI Mode (để xem trực tiếp)
```bash
jmeter -t API-Performance-Test.jmx
```
Sau đó click nút ▶️ để start test.

#### Option B: Non-GUI Mode (khuyến nghị)
```bash
jmeter -n -t API-Performance-Test.jmx \
  -l results/test-results.jtl \
  -e -o results/html-report
```

### 6. Xem Kết Quả
```bash
# Mở HTML report
open results/html-report/index.html
```

---

## 📊 Test Scenarios Có Sẵn

| Scenario | Users | Images | Duration |
|----------|-------|--------|----------|
| OCR Single Image | 100 | 1 | ~2 min |
| OCR Multiple Images | 50 | 5 | ~3 min |
| OCR Stress Test | 200 | 10 | ~5 min |
| User Files Single | 100 | 1 | ~2 min |
| User Files Multiple | 50 | 5 | ~3 min |
| User Files Stress | 200 | 10 | ~5 min |

---

## 🎯 Chỉnh Sửa Base URL

Nếu API của bạn không chạy trên `localhost:3000`:

1. Mở file `API-Performance-Test.jmx` trong text editor
2. Tìm và thay thế:
   - `http://localhost:3000/ocr` → URL của bạn
   - `http://localhost:3000/user` → URL của bạn

Hoặc dùng JMeter GUI:
1. Mở JMeter
2. Load test plan
3. Click vào "API Upload Performance Test" 
4. Sửa `OCR_BASE_URL` và `USER_BASE_URL`

---

## ⚠️ Lưu Ý Quan Trọng

1. ✅ **Đảm bảo API đang chạy** trước khi test
   ```bash
   curl http://localhost:3000/health
   ```

2. ✅ **Dùng JWT tokens hợp lệ** trong file CSV

3. ✅ **Test trên môi trường staging**, không phải production

4. ✅ **Theo dõi server resources** trong khi test chạy

---

## 📈 Đọc Kết Quả Nhanh

### Metrics Quan Trọng

| Metric | Tốt | Chấp Nhận Được | Cần Cải Thiện |
|--------|-----|----------------|---------------|
| Average Response Time | < 1s | 1-3s | > 3s |
| 95th Percentile | < 3s | 3-5s | > 5s |
| Error Rate | < 0.1% | 0.1-1% | > 1% |
| Throughput | > 100 req/s | 50-100 | < 50 |

### HTML Report Sections

1. **Dashboard**: Tổng quan nhanh
2. **Charts**: Biểu đồ response time, throughput
3. **Statistics**: Chi tiết từng request
4. **Errors**: Phân tích lỗi (nếu có)

---

## 🔧 Troubleshooting Nhanh

### ❌ Lỗi: "File not found"
```bash
# Tạo lại test images
python3 generate-test-images.py
```

### ❌ Lỗi: "Connection refused"
```bash
# Kiểm tra API có chạy không
curl http://localhost:3000/ocr/health
```

### ❌ Lỗi: "401 Unauthorized"
```bash
# Cập nhật JWT tokens trong test-data/auth-tokens.csv
```

### ❌ JMeter chạy chậm
```bash
# Tăng memory cho JMeter
JVM_ARGS="-Xmx4g" jmeter -n -t API-Performance-Test.jmx -l results/test.jtl
```

---

## 💡 Tips Nhanh

1. **Test dần dần**: Bắt đầu với ít users, tăng dần
2. **Monitor server**: Mở terminal khác để `top` hoặc `htop`
3. **So sánh kết quả**: Lưu lại results để so sánh sau
4. **Disable scenarios**: Tắt thread groups không cần test
5. **Log everything**: Giữ logs để phân tích sau

---

## 📞 Cần Trợ Giúp?

- 📖 Xem **README.md** để biết chi tiết đầy đủ
- 🌐 JMeter Docs: https://jmeter.apache.org/usermanual/
- 🔌 JMeter Plugins: https://jmeter-plugins.org/

---

**Chúc bạn test thành công! 🎉**


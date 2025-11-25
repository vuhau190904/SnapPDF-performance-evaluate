# ⚡ Quick Start Guide

Hướng dẫn nhanh để chạy JMeter performance test cho API OCR Upload!

---

## 🚀 Các Bước Setup

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

# Cài Pillow để generate test images
pip install Pillow
```

### 3. Tạo Test Images
```bash
cd jmeter-performance-test
python3 generate-test-images.py
```

Sẽ tạo ra các file ảnh test:
- `sample-1kb.jpg` - 1.8 KB
- `sample-100kb.jpg` - 75.3 KB
- `sample-100kb-2.png` - 32.2 KB
- `sample-1mb.png` - 138.4 KB
- `sample-5mb.jpg` - 2240.0 KB

### 4. Cập Nhật JWT Tokens
Mở file `test-data/auth-tokens.csv` và thay thế bằng JWT tokens thực của bạn:

```csv
token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.YOUR_REAL_TOKEN_HERE
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ANOTHER_REAL_TOKEN
```

**⚠️ Lưu ý:** Cần ít nhất 1 token hợp lệ. JMeter sẽ recycle tokens nếu có nhiều requests hơn số tokens.

---

## 🎯 Chạy Performance Test

### **Cách 1: Dùng Script (Khuyến nghị)** ⭐

```bash
./run-test.sh
```

Script sẽ hiển thị menu:
```
================================================
   JMeter Performance Test Runner
================================================

Target: https://somnv.click/api/ocr/upload

Chọn test muốn chạy:
1) Test 100 requests
2) Test 1000 requests
3) Test 10000 requests
4) Chạy tất cả (tuần tự)
5) Exit

Nhập lựa chọn (1-5):
```

### **Cách 2: Chạy Từng Test Riêng**

```bash
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home"

# Test 100 requests
jmeter -n -t Test-100-Requests.jmx \
  -l results/test-100.jtl \
  -e -o results/test-100-report

# Test 1000 requests
jmeter -n -t Test-1000-Requests.jmx \
  -l results/test-1000.jtl \
  -e -o results/test-1000-report

# Test 10000 requests
jmeter -n -t Test-10000-Requests.jmx \
  -l results/test-10000.jtl \
  -e -o results/test-10000-report
```

### **Cách 3: GUI Mode (Xem Real-time)**

```bash
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home"

# Mở test trong GUI
jmeter -t Test-100-Requests.jmx
```

Trong GUI:
1. Click nút ▶️ (Start) để chạy test
2. Xem kết quả real-time ở "Summary Report"
3. Có thể pause/stop test bất cứ lúc nào

---

## 📊 Test Scenarios

| Test File | Concurrent Users | Total Requests | Ramp-up | Mục đích |
|-----------|-----------------|----------------|---------|----------|
| Test-100-Requests.jmx | 100 | 100 | 1s | Kiểm tra cơ bản |
| Test-1000-Requests.jmx | 1000 | 1000 | 5s | Load test |
| Test-10000-Requests.jmx | 10000 | 10000 | 10s | Stress test |

**Mỗi request:**
- Target: `https://somnv.click/api/ocr/upload`
- Method: POST (multipart/form-data)
- File upload: `sample-100kb.jpg` (75KB)
- Auth: Bearer Token từ CSV

---

## 📈 Xem Kết Quả

### Terminal Output
Sau khi test chạy xong, terminal hiển thị summary:
```
summary = 100 in 00:00:05 = 21.9/s Avg: 2992 Min: 2582 Max: 4011 Err: 0 (0.00%)
```

**Ý nghĩa:**
- ✅ **100 requests** hoàn thành
- ⏱️ **5 giây** tổng thời gian
- 📊 **21.9 req/s** throughput
- 📈 **2992ms** average response time
- ❌ **0 errors** (100% success)

### HTML Report
```bash
# Mở HTML report
open results/test-100-report/index.html
open results/test-1000-report/index.html
open results/test-10000-report/index.html
```

HTML Report bao gồm:
1. **Dashboard** - Tổng quan metrics (Error%, Throughput, Response Times)
2. **Over Time** - Đồ thị response time và throughput theo thời gian
3. **Throughput** - Requests per second
4. **Response Times Percentiles** - 50th, 90th, 95th, 99th percentile
5. **Statistics** - Chi tiết từng request
6. **Errors** - Phân tích lỗi (nếu có)

### Metrics Quan Trọng

| Metric | Tốt | Chấp Nhận Được | Cần Cải Thiện |
|--------|-----|----------------|---------------|
| Average Response Time | < 1s | 1-3s | > 3s |
| 95th Percentile | < 3s | 3-5s | > 5s |
| Error Rate | < 0.1% | 0.1-1% | > 1% |
| Throughput | > 100 req/s | 50-100 | < 50 |

---

## 🔧 Troubleshooting

### ❌ `command not found: jmeter`
```bash
brew install jmeter
```

### ❌ `JAVA_HOME not defined`
```bash
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home"
java -version
```

### ❌ `File not found - sample-100kb.jpg`
```bash
python3 generate-test-images.py
ls -lh test-images/
```

### ❌ `401 Unauthorized`
```bash
# Cập nhật JWT tokens hợp lệ
nano test-data/auth-tokens.csv
```

### ❌ `Results file is not empty`
```bash
# Xóa results cũ
rm -rf results/*
```

### ❌ JMeter chậm/treo với test 10000
```bash
# Tăng memory cho JMeter
export JVM_ARGS="-Xms2g -Xmx8g"
jmeter -n -t Test-10000-Requests.jmx -l results/test.jtl
```

---

## 💡 Tips

### 🎯 Chiến Lược Test
1. **Bắt đầu nhỏ:** Chạy Test 100 trước → Test 1000 → Test 10000
2. **Monitor server:** Mở terminal khác để xem `htop` hoặc `docker stats`
3. **So sánh kết quả:** Lưu reports với timestamp để track performance

### ⚡ Best Practices
- ✅ Test trên **staging/dev** environment, không phải production
- ✅ Báo team trước khi chạy stress test
- ✅ Dùng **JWT tokens test**, không phải real user tokens
- ✅ Clean up data test sau khi xong
- ✅ Document kết quả để theo dõi performance theo thời gian

### 📊 Phân Tích Kết Quả
```bash
# So sánh giữa 3 tests
cat results/test-100-summary.csv
cat results/test-1000-summary.csv
cat results/test-10000-summary.csv
```

---

## 📞 Support

- 📖 Chi tiết đầy đủ: **README.md**
- 🌐 JMeter Docs: https://jmeter.apache.org/usermanual/
- 📧 Questions? Contact team

---

**Chúc bạn test thành công! 🎉**

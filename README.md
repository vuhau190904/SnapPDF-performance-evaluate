# JMeter Performance Test - API Upload Endpoints

Comprehensive performance testing suite for OCR Upload API and User Files Upload API.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running Tests](#running-tests)
- [Test Scenarios](#test-scenarios)
- [Understanding Results](#understanding-results)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This JMeter test plan evaluates the performance of two file upload APIs:

1. **OCR Upload API** - `POST /ocr/upload`
2. **User Files Upload API** - `POST /user/files/upload`

### Test Coverage

- **Single Image Upload**: 100 concurrent users, 5 iterations
- **Multiple Images Upload**: 50 concurrent users uploading 5 images, 3 iterations
- **Stress Test**: 200 concurrent users uploading 10 images, 2 iterations

### Metrics Collected

- Response time (average, min, max, 90th/95th/99th percentile)
- Throughput (requests/second)
- Error rate (%)
- Success rate (%)
- Active threads over time

---

## 📦 Prerequisites

### Required Software

1. **Apache JMeter** (version 5.5 or higher)
   - Download: https://jmeter.apache.org/download_jmeter.cgi
   
2. **Java JDK** (version 8 or higher)
   ```bash
   java -version  # Verify installation
   ```

3. **Python 3** (for generating test images)
   ```bash
   python3 --version
   ```

4. **Pillow Library** (Python image library)
   ```bash
   pip install Pillow
   ```

### Optional (Recommended)

- **JMeter Plugins Manager**: For enhanced graphs and reporting
  - Download: https://jmeter-plugins.org/install/Install/

---

## 📁 Project Structure

```
jmeter-performance-test/
├── API-Performance-Test.jmx       # Main JMeter test plan
├── generate-test-images.py        # Script to create test images
├── README.md                       # This file
├── test-data/
│   └── auth-tokens.csv            # JWT tokens for authentication
├── test-images/                   # Generated test images (created by script)
│   ├── sample-1kb.jpg
│   ├── sample-100kb.jpg
│   ├── sample-100kb-2.png
│   ├── sample-1mb.png
│   └── sample-5mb.jpg
└── results/                       # Test results (generated during test runs)
    ├── summary-report.csv
    ├── aggregate-report.csv
    ├── errors.jtl
    └── response-time-graph.csv
```

---

## 🚀 Setup Instructions

### Step 1: Verify Java Installation

```bash
java -version
```

Expected output should show Java 8 or higher.

### Step 2: Install Apache JMeter

#### macOS (using Homebrew)
```bash
brew install jmeter
```

#### Linux
```bash
# Download JMeter
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
cd apache-jmeter-5.6.3/bin

# Add to PATH (optional)
export PATH=$PATH:$(pwd)
```

#### Windows
1. Download JMeter from https://jmeter.apache.org/download_jmeter.cgi
2. Extract to `C:\jmeter`
3. Add `C:\jmeter\bin` to PATH

### Step 3: Install Python Dependencies

```bash
pip install Pillow
```

### Step 4: Generate Test Images

Navigate to the project directory and run:

```bash
cd jmeter-performance-test
python3 generate-test-images.py
```

This will create sample images in the `test-images/` directory with various sizes:
- 1 KB (JPEG)
- 100 KB (JPEG and PNG)
- 1 MB (PNG)
- 5 MB (JPEG)

### Step 5: Configure JWT Tokens

Edit `test-data/auth-tokens.csv` to add your valid JWT tokens:

```csv
token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your_actual_token_here
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your_actual_token_here
```

**Important**: Replace the sample tokens with valid JWT tokens from your application.

### Step 6: Update Base URLs (if needed)

Open `API-Performance-Test.jmx` in a text editor and update the base URLs if your APIs are not running on localhost:

```xml
<stringProp name="Argument.value">http://your-domain.com/ocr</stringProp>
<stringProp name="Argument.value">http://your-domain.com/user</stringProp>
```

Or you can update these values in JMeter GUI:
1. Open JMeter
2. Load `API-Performance-Test.jmx`
3. Click on "API Upload Performance Test" (root element)
4. Update `OCR_BASE_URL` and `USER_BASE_URL` variables

---

## 🏃 Running Tests

### Method 1: GUI Mode (Recommended for Test Development)

```bash
cd jmeter-performance-test
jmeter -t API-Performance-Test.jmx
```

**GUI Mode Steps:**
1. JMeter GUI will open with the test plan loaded
2. Review the test configuration
3. Select which scenarios to run (enable/disable thread groups)
4. Click the green "Start" button (▶️) to run tests
5. View results in real-time through listeners

**⚠️ Warning**: GUI mode consumes more resources. Not recommended for large-scale tests.

### Method 2: Non-GUI Mode (Recommended for Production Tests)

For better performance and resource utilization:

```bash
cd jmeter-performance-test
jmeter -n -t API-Performance-Test.jmx -l results/test-results.jtl -e -o results/html-report
```

**Parameters Explained:**
- `-n`: Non-GUI mode
- `-t`: Test plan file
- `-l`: Results log file
- `-e`: Generate HTML report
- `-o`: Output folder for HTML report

### Method 3: Run Specific Scenarios

To run only specific thread groups (scenarios):

```bash
# Run only OCR Single Image Upload test
jmeter -n -t API-Performance-Test.jmx -l results/ocr-single.jtl \
  -Jthread_groups="S1 - OCR Single Image Upload (100 users)"

# Run only User Files tests
jmeter -n -t API-Performance-Test.jmx -l results/user-files.jtl \
  -Jthread_groups="S4 - User Files Single Image Upload (100 users),S5 - User Files Multiple Images Upload (50 users)"
```

### Method 4: Distributed Testing (Multiple Machines)

For extremely high load tests:

```bash
# On master machine
jmeter -n -t API-Performance-Test.jmx -R server1,server2,server3 -l results/distributed.jtl
```

---

## 📊 Test Scenarios

### Scenario 1: OCR API - Single Image Upload
- **Thread Group**: S1 - OCR Single Image Upload
- **Users**: 100 concurrent
- **Ramp-up**: 10 seconds
- **Iterations**: 5 times per user
- **Total Requests**: 500
- **Image**: 1x 100KB JPEG

**Purpose**: Baseline performance with single file uploads

### Scenario 2: OCR API - Multiple Images Upload
- **Thread Group**: S2 - OCR Multiple Images Upload
- **Users**: 50 concurrent
- **Ramp-up**: 15 seconds
- **Iterations**: 3 times per user
- **Total Requests**: 150
- **Images**: 5x mixed (1KB, 100KB, 1MB, 5MB)

**Purpose**: Test multi-file upload handling

### Scenario 3: OCR API - Stress Test
- **Thread Group**: S3 - OCR Stress Test
- **Users**: 200 concurrent
- **Ramp-up**: 30 seconds
- **Iterations**: 2 times per user
- **Total Requests**: 400
- **Images**: 10x mixed sizes

**Purpose**: Determine maximum capacity and breaking point

### Scenario 4-6: User Files API
Same configurations as OCR API scenarios, but targeting the User Files upload endpoint.

---

## 📈 Understanding Results

### Summary Report

Located at: `results/summary-report.csv`

Key metrics to analyze:

| Metric | Description | Good Target |
|--------|-------------|-------------|
| **Average Response Time** | Mean time for requests | < 2000ms |
| **Median (50th percentile)** | Half of requests faster than this | < 1500ms |
| **90th Percentile** | 90% of requests faster than this | < 3000ms |
| **95th Percentile** | 95% of requests faster than this | < 4000ms |
| **99th Percentile** | 99% of requests faster than this | < 5000ms |
| **Error Rate** | Percentage of failed requests | < 1% |
| **Throughput** | Requests per second | Higher is better |

### Aggregate Report

Located at: `results/aggregate-report.csv`

Provides detailed statistics per request type:
- Min/Max response times
- Standard deviation
- Throughput (requests/sec)
- KB/sec (bandwidth)

### HTML Report (Non-GUI Mode)

When running in non-GUI mode with `-e -o` flags, an HTML dashboard is generated at:
`results/html-report/index.html`

Open in browser to view:
- Interactive charts
- Response time distribution
- Throughput over time
- Error analysis

### View Results Tree

During GUI mode execution, shows individual request/response details:
- Request headers
- Response headers
- Response data
- Assertions results

---

## ⚙️ Configuration

### Adjusting Load Parameters

Edit the test plan in JMeter GUI to modify:

1. **Number of Users (Threads)**
   - Select Thread Group → `Number of Threads (users)`

2. **Ramp-up Time**
   - Select Thread Group → `Ramp-Up Period (in seconds)`

3. **Loop Count**
   - Select Thread Group → `Loop Count`

4. **Think Time** (time between requests)
   - Add `Constant Timer` to Thread Group
   - Set delay in milliseconds

### Changing Target Images

To use different images:

1. Place your images in `test-images/` directory
2. Open test plan in JMeter GUI
3. Navigate to HTTP Request sampler
4. Update file paths in "Files Upload" section

### Modifying Assertions

Current assertions check:
- Response code = 200
- Response contains "success" or "uploaded successfully"

To add more assertions:
1. Right-click on HTTP Request
2. Add → Assertions → Response Assertion
3. Configure assertion criteria

### Customizing Reports

To change report output locations, edit listeners:
1. Open test plan in JMeter GUI
2. Select listener (e.g., "Summary Report")
3. Update "Filename" field

---

## 🔧 Troubleshooting

### Issue: "File not found" error

**Solution**: Ensure test images are generated and paths are correct
```bash
cd jmeter-performance-test
python3 generate-test-images.py
ls -la test-images/
```

### Issue: "Connection refused" error

**Solution**: Verify target API is running
```bash
curl -X GET http://localhost:3000/health  # Check if API is up
```

### Issue: "401 Unauthorized" errors

**Solution**: Update JWT tokens in `test-data/auth-tokens.csv` with valid tokens

### Issue: High error rate during stress tests

**Possible Causes**:
- Server capacity reached
- Network bandwidth limitations
- Database connection pool exhausted
- Rate limiting on API

**Solutions**:
- Reduce concurrent users
- Increase ramp-up time
- Scale server resources
- Optimize API code

### Issue: JMeter runs out of memory

**Solution**: Increase JMeter heap size

Edit `jmeter.bat` (Windows) or `jmeter.sh` (Linux/Mac):
```bash
# Change from default (1GB) to 4GB
export HEAP="-Xms1g -Xmx4g -XX:MaxMetaspaceSize=512m"
```

Or run with parameter:
```bash
JVM_ARGS="-Xmx4g" jmeter -n -t API-Performance-Test.jmx -l results/test.jtl
```

### Issue: Graphs not displaying (Active Threads, Percentiles)

**Solution**: Install JMeter Plugins Manager

1. Download: https://jmeter-plugins.org/get/
2. Copy JAR to `lib/ext/` in JMeter directory
3. Restart JMeter
4. Use Plugins Manager to install missing plugins

---

## 💡 Best Practices

### Before Running Tests

1. ✅ Ensure target servers can handle the load
2. ✅ Notify team members about performance testing
3. ✅ Use staging/test environment (not production)
4. ✅ Verify baseline system metrics (CPU, memory, disk)
5. ✅ Backup any important data

### During Tests

1. ✅ Monitor server resources (CPU, memory, network)
2. ✅ Check application logs for errors
3. ✅ Monitor database connections
4. ✅ Track network bandwidth usage

### After Tests

1. ✅ Analyze all reports thoroughly
2. ✅ Compare results with previous test runs
3. ✅ Document any performance issues found
4. ✅ Share results with development team
5. ✅ Create action items for optimization

---

## 📞 Support & Documentation

### JMeter Resources

- Official Documentation: https://jmeter.apache.org/usermanual/
- JMeter Plugins: https://jmeter-plugins.org/
- Best Practices: https://jmeter.apache.org/usermanual/best-practices.html

### Performance Testing Tips

1. **Start Small**: Begin with low load and gradually increase
2. **Baseline First**: Establish baseline performance before changes
3. **Test Regularly**: Include performance tests in CI/CD pipeline
4. **Monitor Everything**: Server, database, network, application
5. **Document Results**: Keep historical data for comparison

---

## 🎓 Example Workflow

### Complete Test Execution Workflow

```bash
# Step 1: Navigate to project directory
cd jmeter-performance-test

# Step 2: Generate test images (first time only)
python3 generate-test-images.py

# Step 3: Verify test data
ls -la test-images/
cat test-data/auth-tokens.csv

# Step 4: Run tests in non-GUI mode
jmeter -n -t API-Performance-Test.jmx \
  -l results/$(date +%Y%m%d_%H%M%S)-test-results.jtl \
  -e -o results/$(date +%Y%m%d_%H%M%S)-html-report

# Step 5: Open HTML report
# macOS
open results/*-html-report/index.html

# Linux
xdg-open results/*-html-report/index.html

# Windows
start results\*-html-report\index.html
```

---

## 📝 Changelog

### Version 1.0.0 (2025-11-25)
- Initial release
- Added 6 test scenarios (3 per API)
- Support for single/multiple image uploads
- Stress testing capabilities
- Comprehensive reporting
- Auto-generated test images

---

## 📄 License

This test plan is provided as-is for performance testing purposes.

---

## 👥 Contributors

Performance Testing Team - 2025

---

**Happy Testing! 🚀**

For questions or issues, please contact your QA team or refer to the JMeter documentation.


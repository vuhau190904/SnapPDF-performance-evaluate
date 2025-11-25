#!/bin/bash

# Export JAVA_HOME
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   JMeter Performance Test Runner${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${YELLOW}Target:${NC} https://somnv.click/api/ocr/upload"
echo ""
echo "Chọn test muốn chạy:"
echo "1) Test 100 requests"
echo "2) Test 1000 requests"
echo "3) Test 10000 requests"
echo "4) Chạy tất cả (tuần tự)"
echo "5) Exit"
echo ""
read -p "Nhập lựa chọn (1-5): " choice

case $choice in
    1)
        echo -e "${GREEN}Đang chạy Test 100 requests...${NC}"
        rm -rf results/test-100-*
        jmeter -n -t Test-100-Requests.jmx \
            -l results/test-100-results.jtl \
            -e -o results/test-100-report
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Xong! Đang mở report...${NC}"
            open results/test-100-report/index.html
        else
            echo -e "${RED}❌ Test thất bại!${NC}"
        fi
        ;;
    2)
        echo -e "${GREEN}Đang chạy Test 1000 requests...${NC}"
        rm -rf results/test-1000-*
        jmeter -n -t Test-1000-Requests.jmx \
            -l results/test-1000-results.jtl \
            -e -o results/test-1000-report
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Xong! Đang mở report...${NC}"
            open results/test-1000-report/index.html
        else
            echo -e "${RED}❌ Test thất bại!${NC}"
        fi
        ;;
    3)
        echo -e "${GREEN}Đang chạy Test 10000 requests...${NC}"
        rm -rf results/test-10000-*
        jmeter -n -t Test-10000-Requests.jmx \
            -l results/test-10000-results.jtl \
            -e -o results/test-10000-report
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Xong! Đang mở report...${NC}"
            open results/test-10000-report/index.html
        else
            echo -e "${RED}❌ Test thất bại!${NC}"
        fi
        ;;
    4)
        echo -e "${GREEN}Đang chạy tất cả tests...${NC}"
        rm -rf results/*
        
        echo -e "${BLUE}[1/3] Test 100 requests...${NC}"
        jmeter -n -t Test-100-Requests.jmx \
            -l results/test-100-results.jtl \
            -e -o results/test-100-report
        
        echo -e "${BLUE}[2/3] Test 1000 requests...${NC}"
        jmeter -n -t Test-1000-Requests.jmx \
            -l results/test-1000-results.jtl \
            -e -o results/test-1000-report
        
        echo -e "${BLUE}[3/3] Test 10000 requests...${NC}"
        jmeter -n -t Test-10000-Requests.jmx \
            -l results/test-10000-results.jtl \
            -e -o results/test-10000-report
        
        echo -e "${GREEN}✅ Xong tất cả! Đang mở reports...${NC}"
        open results/test-100-report/index.html
        sleep 1
        open results/test-1000-report/index.html
        sleep 1
        open results/test-10000-report/index.html
        ;;
    5)
        echo "Thoát."
        exit 0
        ;;
    *)
        echo -e "${RED}Lựa chọn không hợp lệ!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✨ Done!${NC}"

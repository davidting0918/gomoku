# Backend Testing Guide

## 設置測試環境

### 前置需求
1. 確保 MongoDB 在本地運行（預設端口 27017）
2. 安裝測試依賴套件（已包含在 requirements.txt 中）

### 運行測試

#### 運行所有測試
```bash
cd backend
python -m pytest tests/ -v
```

#### 運行特定的用戶端點測試
```bash
cd backend  
python -m pytest tests/test_user_endpoints.py -v
```

#### 運行特定測試函數（創建2個用戶的測試）
```bash
cd backend
python -m pytest tests/test_user_endpoints.py::TestUserEndpoints::test_create_two_users_endpoint -v -s
```

## 測試說明

### test_create_two_users_endpoint
這個測試會：
1. 使用 `/user/create` 端點創建 2 個測試用戶
2. 驗證 API 回應格式正確
3. 確認用戶正確存儲在測試資料庫中
4. 驗證密碼已正確雜湊處理
5. 確保兩個用戶有不同的 ID

### test_duplicate_email_prevention  
測試重複 email 註冊的防護機制

### test_user_service_with_test_db
直接測試 UserService 與測試資料庫的整合

## 測試資料庫配置

- 測試資料庫: `gomoku_test`
- 每次測試後會自動清理所有測試資料
- 測試與生產環境完全隔離

## 測試數據

測試會創建以下兩個用戶：
- 用戶1: test.user1@example.com (Test User 1)
- 用戶2: test.user2@example.com (Test User 2)

## 故障排除

如果測試失敗，請檢查：
1. MongoDB 服務是否正在運行
2. 是否有端口衝突（MongoDB 預設使用 27017）
3. 測試資料庫權限是否正確

# 透過 Flask 實現 Google 第三方驗證

## 需求
+ Python
+ ngrok
+ client_secret.json
+ config.py
```
#config.py

class Config:
    SECRET_KEY = 'GOASLZ-XXXXXXXXXXXXX'
    GOOGLE_CLIENT_ID = '699XXXXXXXX-oeXXXXXXXX.apps.googleusercontent.com'
    REDIRECT_URL = 'http://localhost/callback' # or 'ngrok產生網址/callback'
    CLIENT_SECTETS_FILE = 'client_secret.json' 
```


## run in localhost

### 建立虛擬環境
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 運行

```
python app.py
```

### 展示

```
http://localhost/
```

## run in 公網

### 建立映射公網ip
```
ngrok http 80
```
### 其他手動設定
```
在 https://console.cloud.google.com 專案中 -> API和服務 -> 憑證 -> OAuth 2.0 用戶端 ID -> 將 已授權的 JavaScript 來源 改為ngrok產生網址 已授權的重新導向 URI 改為ngrok產生網址/callback
```
```
修正config.py中的 REDIRECT_URL 到 'ngrok產生網址/callback'
```

### 建立虛擬環境
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 運行

```
python app.py
```



### 展示

```
ngrok產生網址/
```
# دليل الإعداد والتثبيت
## Setup and Installation Guide

### المتطلبات النظام
- **نظام التشغيل**: Windows / macOS / Linux
- **Python**: الإصدار 3.8 أو أحدث
- **RAM**: 4 GB كحد أدنى
- **المساحة**: 500 MB للتثبيت الأساسي

### خطوات التثبيت

#### 1. استنساخ المستودع
```bash
git clone https://github.com/joorygassim42-cell/smart-civil-defense-platform.git
cd smart-civil-defense-platform
```

#### 2. إنشاء بيئة افتراضية
```bash
# على Windows
python -m venv venv
venv\\Scripts\\activate

# على macOS و Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. تحديث pip
```bash
pip install --upgrade pip
```

#### 4. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

#### 5. التحقق من التثبيت
```bash
python -c "import streamlit; print('Streamlit installed successfully')"
```

### التشغيل

#### الطريقة 1: التشغيل الأساسي
```bash
streamlit run app.py
```

#### الطريقة 2: التشغيل مع خيارات متقدمة
```bash
streamlit run app.py --logger.level=debug
```

#### الطريقة 3: التشغيل على منفذ مخصص
```bash
streamlit run app.py --server.port 8080
```

### الوصول للتطبيق
- **URL المحلي**: http://localhost:8501
- **URL الشبكة**: http://<your-ip>:8501

### استكشاف الأخطاء

#### مشكلة: "ModuleNotFoundError: No module named 'streamlit'"
**الحل**: تأكد من تثبيت المكتبات
```bash
pip install -r requirements.txt
```

#### مشكلة: المنفذ 8501 مستخدم بالفعل
**الحل**: استخدم منفذ مختلف
```bash
streamlit run app.py --server.port 8502
```

#### مشكلة: البيانات العربية تظهر بشكل خاطئ
**الحل**: تأكد من ترميز الملفات UTF-8
```bash
# على Windows
chcp 65001
```

### الإعدادات الموصى بها

#### ملف `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#E8E8E8"
textColor = "#333333"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"
```

### النشر على الإنترنت

#### خيار 1: Streamlit Cloud
1. انتقل إلى https://streamlit.io/cloud
2. قم بتسجيل الدخول
3. انقر على "New app"
4. حدد هذا المستودع
5. انقر على "Deploy"

#### خيار 2: Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

#### خيار 3: AWS / Google Cloud / Azure
- استخدم Docker للنشر
```bash
docker build -t smart-defense-platform .
docker run -p 8501:8501 smart-defense-platform
```

### ملف Dockerfile (اختياري)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

### التطوير المحلي

#### تثبيت أدوات التطوير
```bash
pip install pytest black flake8
```

#### تنسيق الكود
```bash
black app.py
```

#### فحص الكود
```bash
flake8 app.py
```

#### تشغيل الاختبارات
```bash
pytest tests/
```

### المراجع المفيدة
- [توثيق Streamlit](https://docs.streamlit.io)
- [توثيق Pandas](https://pandas.pydata.org/docs)
- [Python للمبتدئين](https://python.readthedocs.io)

---
**للمساعدة**: فتح issue في المستودع أو التواصل مع فريق الدعم.

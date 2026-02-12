FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 소스코드 복사
COPY . .

# 3. 봇 실행 (-u 옵션: 로그 즉시 출력)
CMD ["python", "-u", "main.py"]

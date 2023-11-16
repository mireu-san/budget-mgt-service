FROM python:3.11.6-alpine3.18

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 파일 복사 및 컨테이너 기준, 해당 /app/ 경로로 복사
COPY . /app/

# 서버 시작
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]

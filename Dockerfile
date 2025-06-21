
FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



WORKDIR /app


COPY requirements.txt .


RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt


COPY ./project /app/


EXPOSE 8000


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


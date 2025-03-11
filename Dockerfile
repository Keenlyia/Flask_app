# Використовуємо офіційний Python-образ
FROM python:3.11

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли проєкту в контейнер
COPY . .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт для Flask
EXPOSE 5000

# Запускаємо додаток
CMD ["python", "main.py"]
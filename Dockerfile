# Usa imagem oficial do Python (Slim é mais leve e seguro que Fedora completo)
FROM python:3.13-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m appuser
USER appuser
EXPOSE 5000
CMD ["python", "src/main.py"]

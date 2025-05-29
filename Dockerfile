# 1. Base image
FROM python:3.11-slim

# 2. Set working dir
WORKDIR /app

# 3. Copy only requirements, install deps first (cache)
COPY apps/backend/requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 4. Copy backend source
COPY apps/backend/ .

# 5. Expose port
EXPOSE 8000

# 6. Launch
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

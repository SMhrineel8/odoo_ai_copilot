# 1. Use official Python image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy and install dependencies
COPY apps/backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy backend source code
COPY apps/backend/ .

# 5. Expose the port
EXPOSE 8000

# 6. Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

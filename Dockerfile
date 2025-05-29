# 1. Base image
FROM python:3.11-slim

# 2. Set workdir
WORKDIR /app/backend

# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy only the requirements first (cache layer)
COPY apps/backend/requirements.txt ./requirements.txt

# 5. Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy backend source code
COPY apps/backend/ .

# 7. Expose the port the app runs on
EXPOSE 8000

# 8. Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

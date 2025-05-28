# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install pip + system deps
RUN apt-get update && apt-get install -y build-essential

# Copy files
COPY ./apps/backend /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port (important for Railway)
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

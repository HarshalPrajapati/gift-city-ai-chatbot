# -----------------------------
# Base Image
# -----------------------------
FROM python:3.12-slim

# -----------------------------
# Environment Variables
# -----------------------------
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Working Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Install System Packages
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Copy Requirements
# -----------------------------
COPY requirements.txt .

# -----------------------------
# Install Python Packages
# -----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy Project
# -----------------------------
COPY . .

# -----------------------------
# Expose Port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start FastAPI
# -----------------------------
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
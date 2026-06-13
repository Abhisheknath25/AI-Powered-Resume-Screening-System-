FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

WORKDIR /app

# Install system dependencies if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY sample_resume_swe.txt .

# Create directory for models if needed and make sure it has permissions
RUN mkdir -p backend/model_files && chmod -R 777 backend/model_files

# Expose port
EXPOSE 7860

# Run the app
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]

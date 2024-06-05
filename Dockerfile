FROM python:3.12.2-slim-bullseye

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PORT=8080

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app/

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Define the command to run the application
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8080"]

# Expose the port
EXPOSE 8080

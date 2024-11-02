# 1. Start with a lightweight Python image
FROM python:3.12-slim-bullseye

# 2. Show logs directly in the container's stdout
ENV PYTHONUNBUFFERED=1

# 3. Set a working directory inside the container
WORKDIR /app

# 4. Update and upgrade system packages
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    # Add common dependencies here if needed, like 'gcc' for compiling C extensions
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements into the container and Install Python dependencies & packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the Django project into the container
COPY . /app/

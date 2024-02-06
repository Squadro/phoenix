# Stage 1: Build Stage
FROM python:3.10-slim-buster AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /phoenix

COPY . /phoenix

# Copy only the necessary files (requirements.txt and manage.py) into the container at /app


# Install dependencies required for building (e.g., build-essential, libpq-dev)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        lsb-release \
        wget \
        gnupg \
    && rm -rf /var/lib/apt/lists/*


# Import the GPG key for the PostgreSQL APT repository
RUN wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg

# Add the PostgreSQL APT repository
RUN echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Update package lists and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        screen \
    && rm -rf /var/lib/apt/lists/*

RUN touch requirements_changed

# Install Python dependencies from requirements.txt only if the placeholder file changes
RUN [ -e requirements_changed ] && pip install --no-cache-dir -r requirements.txt || true


# Stage 2: Production Stage
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR phoenix

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /phoenix/ /phoenix/

# Install system dependencies


# Expose port 8080
EXPOSE 8080

# Copy the .env file to the working directory
COPY .env phoenix/.env

# Version label for the Docker image
LABEL version="1.0"

# Start the application with the default command
CMD python3 manage.py runserver
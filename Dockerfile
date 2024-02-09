# Stage 1: Build Stage
FROM python:3.10-slim-buster AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /phoenix

# Copy only the necessary files (requirements.txt and manage.py) into the container at /phoenix
COPY requirements.txt /phoenix/

# Install build dependencies
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

# Install PostgreSQL client and screen
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        screen \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a placeholder file to detect changes in requirements.txt
RUN touch requirements_changed

# Stage 2: Production Stage
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /phoenix

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /phoenix/ /phoenix/

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        screen \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

COPY . /phoenix/

LABEL version="1.0"

# Set environment variable for manage.py command
ENV DJANGO_MANAGE_CMD consume_message


CMD sh -c "gunicorn -w 2 -b 0.0.0.0:8080 phoenix.wsgi:application & python manage.py $DJANGO_MANAGE_CMD && wait"

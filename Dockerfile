# Use a base Python image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the entire app folder into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

# Expose port 8000 for the Django application
EXPOSE 8000

# Run the Django server
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "phoenix.wsgi:application", "-c", "config.py"]
CMD ["python", "manage.py", "consume_message"]
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "bonito_recommendations.wsgi:application"]
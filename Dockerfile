FROM python:3.8-alpine

# Set working directory inside the container
WORKDIR /app

# Install dependencies for Django
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . .

# Set environment variables (optional - could be passed externally)
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Expose the port Django will run on
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

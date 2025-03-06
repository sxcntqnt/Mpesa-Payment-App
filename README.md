## Mpesa-Payment-App

This is a RESTful payment application built with the Python Django framework, integrating the Mpesa REST APIs. The application supports all available transactions in the Mpesa sandbox environment.

## Features:
- Integrates with Mpesa APIs for payment processing.
- Implements popular Mpesa transactions in the sandbox environment.
- Provides endpoints for handling payment requests and responses.
- Configurable for local, test, and production environments.

## Table of Contents

- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Security Considerations](#security-considerations)

## Getting Started

These instructions will help you set up the application on your local machine for development and testing purposes. For production environments, please follow the security considerations at the end of this guide.

### Prerequisites

- Python 3.8 or higher
- Django 3.x or higher
- PostgreSQL (or another database of your choice)
- Redis (for caching and Celery task management)
- RabbitMQ (for message brokering with Celery)

Make sure you have `pip` installed, and use a virtual environment to manage your dependencies.

1. Clone the repository

```bash
git clone https://github.com/your-username/mpesa-payment-app.git
cd mpesa-payment-app
```
2. Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Environment Variables

##Before you can run the application, you must configure the following environment variables in a .env file located at the root of your project.

Example .env file:
```
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings.production  # Adjust based on environment
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key

# Allowed Hosts (for production)
ALLOWED_HOSTS='your-production-domain.com'

# Database Configuration
DB_NAME='your_database_name'
DB_USER='your_database_user'
DB_PASSWORD='your_database_password'
DB_HOST='your_database_host'
DB_PORT='5432'

# Redis Configuration
REDIS_HOST='your-redis-host'

# RabbitMQ Configuration (for Celery)
BROKER_URL='amqp://your-rabbitmq-url'

# Mpesa API Credentials
CONSUMER_KEY='your-consumer-key'
CONSUMER_SECRET='your-consumer-secret'
SHORTCODE='your-shortcode'  # Typically N/A in the sandbox
```
5.  Running the Application
##Migrate the Database

Run the following command to create the necessary database tables:
```
python manage.py migrate
```
6. Create a Superuser
##To access the Django admin panel, you can create a superuser:
```
python manage.py createsuperuser
```
7. Start the Development Server
##
```
python manage.py runserver
```

8. Usage

##Once the server is running, you can interact with the Mpesa API through the available endpoints. These endpoints are exposed as RESTful services.
###Theycan be used to initiate and receive payment requests through the Callback URL

For test environments, a static URL is required to receive transaction responses from Mpesa. You will need to set up a callback URL in the Mpesa sandbox portal and associate it with the respective transactions. The URL should be publicly accessible, or you can use tools like ngrok to expose a local server for testing.
```
curl -X POST http://127.0.0.1:8000/api/payment \
     -H "Content-Type: application/json" \
     -d '{"amount": 100, "phone_number": "0712345678", "shortcode": "your_shortcode"}'
```


9. License

#This project is licensed under the MIT License.

##Feel free to contribute, submit issues, and fork this repository for further enhancements!

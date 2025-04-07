# ARTICLES DATABASE REST API

## Prerequisites

Ensure you have the following installed before setting up the API:

- Python (>=3.13)
- PostgreSQL (or your preferred database)

### Installation

Instructions on how to install the necessary dependencies and set up the project.

```bash
# Clone the repository
git clone https://github.com/pantgram/ArticlesRESTapi.git

# Navigate to the project directory
cd ArticlesRESTapi

# Create a virtual environment
python -m venv "environment name"

# Activate the virtual environment

source "environment name"/bin/activate

# Go to app directory
cd app

#  Install dependencies
pip install -r requirements.txt



# Create the .env file for configuring the database connection variables
touch .env
```

The .env file should be structured like this (for a PostgreSQL connection):

    Those are example values

    DB_USER = 'user'
    DB_PASSWORD = 'mypass'
    DB_HOST = '127.0.0.1'
    DB_NAME = 'dbname'
    DB_PORT = '5432'

In the settings.py file you can adjust the database settings for your preffered database

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': os.environ.get('DB_NAME'),
'USER': os.environ.get('DB_USER'),
'PASSWORD': os.environ.get('DB_PASSWORD'),
'HOST': os.environ.get('DB_HOST'),
'PORT': os.environ.get('DB_PORT'),
}
}

Ensure that the database server is running

```bash

# Create the migration for the database
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate

# Populate the database with sample data
python manage.py loaddata sample_data.json

# Run the server
python manage.py runserver

```

### Running the API

The server now is running on 127.0.0.1:8000/

USERS

A user that wants to have access to the api can make a POST request to the api/Users/auth/token endpoint with a request body like this:

    Those are example values

    {
    "email" : "test01@gmail.com",
    "first_name" : "TEST",
    "last_name" : "user",
    "password" : "TestPass10!"

}

    He will receive a response payload

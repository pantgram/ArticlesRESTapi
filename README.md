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

    Those are example values.

    DB_USER = 'user'
    DB_PASSWORD = 'mypass'
    DB_HOST = '127.0.0.1'
    DB_NAME = 'dbname'
    DB_PORT = '5432'

In the settings.py file you can adjust the database settings for your preffered database.

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

The server now runs at `127.0.0.1:8000/`.

## Authentication

### POST `/api/Users/auth/token`

Creates a new user and retrieves authorization tokens, or authenticates an existing user.

**Request Body:**

```json
{
  "email": "test01@gmail.com",
  "first_name": "TEST",
  "last_name": "user",
  "password": "TestPass10!"
}
```

**Successful Response:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** The access token must be included in subsequent requests as a Bearer token in the Authorization header.

**Error Response:**

```json
{
  "error": "Invalid credentials"
}
```

### POST `/api/Users/auth/token/refresh`

Obtains a new token pair using a refresh token.

**Request Body:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** Once used, refresh tokens are blacklisted and cannot be reused.

## User Endpoints

### GET `/api/Users/me`

Returns details of the currently authenticated user.

### GET `/api/Users/`

Returns a list of all users.

### GET, PUT, DELETE `/api/Users/<user_id>/`

- **GET**: Retrieves details for a specific user
- **PUT/DELETE**: Restricted to admin users only

## Content Management

### Articles

#### GET `/api/Articles/`

Returns a list of all articles.

#### GET, PUT, DELETE `/api/Articles/<article_id>/`

- **GET**: Retrieves details for a specific article
- **PUT/DELETE**: Restricted to admin users or the article's author

### Comments

#### GET, PUT, DELETE `/api/Comments/<comment_id>/`

- **GET**: Retrieves details for a specific comment
- **PUT/DELETE**: Restricted to admin users or the article's author

### Tags

#### GET, PUT, DELETE `/api/Tags/<tag_id>/`

- **GET**: Retrieves details for a specific tag
- **PUT/DELETE**: Restricted to admin users only

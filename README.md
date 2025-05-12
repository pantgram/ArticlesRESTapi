# ARTICLES DATABASE REST API

## Prerequisites

Ensure you have the following installed before setting up the API:

- Python (>=3.10)
- PostgreSQL (or your preferred database)

## Installation

Instructions on how to install the necessary dependencies and set up the project.

```bash
# Clone the repository
git clone https://github.com/pantgram/ArticlesRESTapi.git

# Navigate to the project directory
cd ArticlesRESTapi

# Create a virtual environment
python -m venv env

# Activate the virtual environment

source env/bin/activate

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

### POST `/api/users/auth/token/register`

Creates a new user and retrieves authorization tokens

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
  "error": "User with the same email already exists"
}
```

### POST `/api/users/auth/token/login`

Authenticates an existing user.

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

### POST `/api/users/auth/token/refresh`

Obtains a new token pair using a refresh token.

**Request Body:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** Once used, refresh tokens are blacklisted and cannot be reused.

## User Endpoints

### GET `/api/users/me`

Returns details of the currently authenticated user.

### GET `/api/users/`

Returns a list of all users.

### GET, PUT, DELETE `/api/users/<user_id>/`

- **GET**: Retrieves details for a specific user
- **PUT/DELETE**: Restricted to admin users only

## Content Management

### Articles

#### GET `/api/articles/`

Returns a list of all articles.

**Filter Parameters:**

- `year`: Filter articles by publication year
- `month`: Filter articles by publication month
- `authors`: Filter articles by author IDs
- `tags`: Filter articles by tag IDs
- `keyword`: Search articles by keyword
- `ordering`: Order results by specified field

**Examples:**

```
/api/articles/?year=2025
/api/articles/?month=4&year=2024
/api/articles/?authors=1,2,3
/api/articles/?tags=5,8
/api/articles/?keyword=technology
/api/articles/?ordering=publication_date
```

#### POST `/api/articles/`

Creates a new article.

**Request Body Example:**

```json
{
  "title": "Understanding REST APIs",
  "abstract": "This article explores the principles of REST architecture and how to implement RESTful services.",
  "authors": [1, 3],
  "tags": ["Europe", "Tag 1"]
}
```

**Note:** The `publication_date` field is automatically set to the current date and the `authors` list is automatically appended with the current user.

#### GET, PUT, DELETE `/api/articles/<article_id>/`

- **GET**: Retrieves details for a specific article
- **PUT/DELETE**: Restricted to admin users or the article's author

**PUT Request Body Example:**

```json
{
  "title": "Understanding REST APIs - Updated",
  "abstract": "An updated exploration of REST architecture principles and implementation best practices.",
  "authors": [1, 3, 4],
  "tags": ["Europe", "Tag 1", "Tag 2"]
}
```

**Note:** The `publication_date` is set to the current date.

#### GET `/api/articles/export/csv/`

Exports all articles as a downloadable CSV file.

**Filter Parameters:**

- `year`: Filter articles by publication year
- `month`: Filter articles by publication month
- `authors`: Filter articles by author IDs
- `tags`: Filter articles by tag IDs
- `ids`: Filter articles by article IDs
- `keyword`: Search articles by keyword
- `ordering`: Order results by specified field

**Examples:**

```
/api/articles/export/csv/?year=2025
/api/articles/export/csv/?month=4&year=2024
/api/articles/export/csv/?authors=1,2,3
/api/articles/export/csv/?tags=5,8
/api/articles/export/csv/?ids=4,5
/api/articles/export/csv/?keyword=technology
/api/articles/export/csv/?ordering=publication_date
```

### Comments

#### GET `/api/comments/`

Returns a list of all comments.

**Filter Parameters:**

- `year`: Filter comments by publication year
- `month`: Filter comments by publication month
- `author`: Filter comments by author ID
- `article`: Filter comments by article ID
- `keyword`: Search comments by keyword
- `ordering`: Order results by specified field

**Examples:**

```
/api/comments/?year=2025
/api/comments/?month=4&year=2024
/api/comments/?author=1
/api/comments/?article=5
/api/comments/?keyword=technology
/api/comments/?ordering=publication_date
```

#### POST `/api/comments/`

Creates a new comment.

**Request Body Example:**

```json
{
  "text": "This is a great article with valuable insights!",
  "article": 5
}
```

**Note:** The `author` field is automatically set to the current authenticated user and the `publication_date` is set to the current date.

#### GET, PUT, DELETE `/api/comments/<comment_id>/`

- **GET**: Retrieves details for a specific comment
- **PUT/DELETE**: Restricted to admin users or the article's author

**PUT Request Body Example:**

```json
{
  "text": "This is an updated comment with additional thoughts after reading the article again.",
  "article": 5
}
```

**Note:** The `publication_date` is set to the current date.

### Tags

#### GET `/api/tags/`

Returns a list of all tags.

**Filter Parameters:**

- `name`: Filter tags by name
- `keyword`: Search tags by keyword
- `ordering`: Order results by specified field

**Examples:**

```
/api/tags/?name=Europe
/api/tags/?keyword=technology
/api/tags/?ordering=name
```

#### POST `/api/tags/`

Creates a new tag.

**Request Body Example:**

```json
{
  "name": "Python"
}
```

**Note:** Tag names must be unique.

#### GET, PUT, DELETE `/api/tags/<tag_id>/`

- **GET**: Retrieves details for a specific tag
- **PUT/DELETE**: Restricted to admin users only

**PUT Request Body Example:**

```json
{
  "name": "Python Programming"
}
```

## Testing

```bash

# Run the unit tests
python manage.py test

```

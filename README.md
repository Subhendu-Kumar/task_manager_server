# Task Manager App API

A FastAPI application with Prisma & NeonDB for managing tasks and user authentication.

## Overview

This Task Manager App provides a RESTful API for user authentication and task management. It includes features for user registration, login, token-based authentication, and full CRUD operations for tasks.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Prisma** - Next-generation ORM for database operations
- **NeonDB** - Serverless PostgreSQL database
- **JWT Bearer Authentication** - Secure token-based authentication

## API Endpoints

### Authentication

#### Sign Up

- **POST** `/auth/signup`
- Create a new user account
- **Request Body:**
  ```json
  {
    "name": "string",
    "email": "user@example.com",
    "password": "string"
  }
  ```
- **Response:** `201 Created`

#### Login

- **POST** `/auth/login`
- Authenticate user and receive access token
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "string"
  }
  ```
- **Response:** `200 OK` with authentication token

#### Verify Token

- **GET** `/auth/token/verify`
- Verify the validity of the current JWT token
- **Headers:** `Authorization: Bearer <token>`
- **Response:** `200 OK`

#### Get User Profile

- **GET** `/auth/user`
- Retrieve current user information
- **Headers:** `Authorization: Bearer <token>`
- **Response:** `200 OK` with user data

### Task Management

#### Create Task

- **POST** `/task/add`
- Create a new task
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "hexColor": "string",
    "dueAt": "2024-01-01T00:00:00Z" // optional
  }
  ```
- **Response:** `201 Created`

#### List All Tasks

- **GET** `/task/list`
- Retrieve all tasks for the authenticated user
- **Headers:** `Authorization: Bearer <token>`
- **Response:** `200 OK` with array of tasks

#### Delete Task

- **DELETE** `/task/{task_id}`
- Delete a specific task by ID
- **Headers:** `Authorization: Bearer <token>`
- **Parameters:** `task_id` (string, required)
- **Response:** `200 OK`

#### Sync Tasks

- **POST** `/task/sync`
- Synchronize tasks (batch operation)
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "hexColor": "string",
      "dueAt": "2024-01-01T00:00:00Z",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }
  ]
  ```
- **Response:** `201 Created`

### System Endpoints

#### Root

- **GET** `/`
- API root endpoint
- **Response:** `200 OK`

#### Health Check

- **GET** `/health`
- Check API health status
- **Response:** `200 OK`

## Authentication

This API uses JWT Bearer token authentication. After successful login, include the token in the Authorization header for protected endpoints:

```
Authorization: Bearer <your-jwt-token>
```

## Data Models

### User Registration (SignupUser)

```json
{
  "name": "string",
  "email": "user@example.com",
  "password": "string"
}
```

### User Login (LoginUser)

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

### Task Creation (TaskCreate)

```json
{
  "title": "string",
  "description": "string",
  "hexColor": "string",
  "dueAt": "2024-01-01T00:00:00Z" // optional
}
```

### Task Sync (TaskSyncModel)

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "hexColor": "string",
  "dueAt": "2024-01-01T00:00:00Z",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created
- `422` - Validation Error (Unprocessable Entity)
- `401` - Unauthorized (invalid/missing token)
- `404` - Not Found
- `400` - Bad Request
- `500` - Internal Server Error

### Validation Error Response

```json
{
  "detail": [
    {
      "loc": ["field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database (NeonDB)
- Prisma CLI

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:

   ```bash
    # database
    DATABASE_URL="your postgresql url"

    # jwt

    JWT_SECRET=<your secret key>
    JWT_ALGORITHM=HS256
    JWT_EXP_DELTA_SECONDS=86400
   ```

4. Generate Prisma client:

```bash
prisma generate
```

5. Run database migrations:
   ```bash
   prisma migrate dev --name init
   ```
6. Start the development server:
   ```bash
   fastapi dev main.py
   ```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

- ✅ User registration and authentication
- ✅ JWT token-based security
- ✅ Task CRUD operations
- ✅ Task categorization with hex colors
- ✅ Due date management
- ✅ Task synchronization
- ✅ Health monitoring
- ✅ Input validation and error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

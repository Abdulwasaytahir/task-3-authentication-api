# Secure Authentication API

A secure user authentication REST API built with FastAPI, PostgreSQL, SQLAlchemy, bcrypt password hashing, and JWT authentication.

This project demonstrates how user registration, password security, login authentication, JWT tokens, and protected API routes work together.

## Features

- User registration
- PostgreSQL database integration
- SQLAlchemy ORM
- Password hashing with bcrypt
- Password verification
- JWT access token generation
- JWT token verification
- Token expiration
- OAuth2 Bearer authentication
- Protected API route
- Unauthorized request handling
- Swagger UI authentication and testing
- Environment variables using `.env`

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Passlib
- bcrypt
- Python-JOSE
- OAuth2
- Uvicorn
- python-dotenv

## Project Structure

```text
authentication-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── auth.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
How Authentication Works
1. Registration

The user sends:

{
  "name": "Ali",
  "email": "ali@gmail.com",
  "password": "AliPassword123"
}

The password is never stored directly in the database.

Instead:

Plain Password
      ↓
bcrypt hashing
      ↓
Password Hash
      ↓
PostgreSQL

The database stores the password hash rather than the original password.

2. Login

The user provides their email and password.

Email + Password
       ↓
Find user in database
       ↓
Verify password against password hash
       ↓
Password correct?
       ↓
Generate JWT

If authentication succeeds, the API returns an access token.

Example:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
3. Protected Route

The protected endpoint requires a valid Bearer token.

GET /protected
Authorization: Bearer <access_token>

The API:

Receive JWT
    ↓
Verify JWT
    ↓
Check expiration
    ↓
Extract user ID
    ↓
Find user
    ↓
Allow access

Without a valid token:

401 Unauthorized
API Endpoints
Method	Endpoint	Description	Authentication
GET	/	Check API status	Not required
POST	/register	Register a new user	Not required
POST	/login	Login and receive JWT	Not required
GET	/protected	Access authenticated user information	Required
Installation
1. Clone the repository
git clone https://github.com/Abdulwasaytahir/authentication-api.git
2. Enter the project directory
cd authentication-api
3. Create a virtual environment

Windows:

python -m venv .venv
4. Activate the virtual environment
.venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root:

DATABASE_URL=postgresql+psycopg2://USERNAME:PASSWORD@localhost:5432/authentication_db
SECRET_KEY=your-secret-key

Do not commit .env to GitHub.

Database Setup

Create a PostgreSQL database named:

authentication_db

Update the .env file with your PostgreSQL username and password.

When the application starts, SQLAlchemy creates the required users table.

The table contains:

id
name
email
password_hash

The password_hash column stores the hashed password.

Running the API

Start the development server:

uvicorn app.main:app --reload

The API will run at:

http://127.0.0.1:8000
Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs

From Swagger UI you can:

Register a user.
Authorize using the OAuth2 login.
Receive a JWT token.
Access the protected endpoint.
Testing Authentication
Register
POST /register

Example request:

{
  "name": "Ali",
  "email": "ali@gmail.com",
  "password": "AliPassword123"
}
Login

Use the Swagger Authorize button.

Enter:

username: ali@gmail.com
password: AliPassword123

The username field contains the user's email because OAuth2's standard password flow uses the field name username.

Protected Route

After authorization:

GET /protected

A successful response returns the authenticated user's information.

Without authorization:

401 Unauthorized
Security

This project follows several basic security practices:

Passwords are hashed before being stored.
Plain-text passwords are not stored in the database.
JWT tokens are used for authentication.
JWT tokens have an expiration time.
Protected routes require authentication.
Database credentials are stored in environment variables.
.env is excluded from version control.
Learning Objectives

This project was built to understand:

Authentication vs authorization
Password hashing
Password verification
JWT authentication
Bearer tokens
OAuth2 password flow
FastAPI dependencies
Protected routes
Database-backed authentication
Token expiration
Basic API security
Future Improvements

Possible extensions include:

Role-based access control
Refresh tokens
Logout/token revocation
Password reset functionality
Email verification
User profile management
More advanced authorization rules
Author

Abdul Wasay Tahir

BS Computer Science Student

GitHub:

https://github.com/Abdulwasaytahir
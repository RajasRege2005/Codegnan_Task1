# FastAPI API Gateway Service

This is a backend service developed with FastAPI to manage API access, generation of credentials, and enforce usage limits per credential. 

## Features of the Task
- **API Access Management:** Clients obtain a securely generated API key (stored securely as a SHA-256 hash). Keys are non-recoverable and strictly tied to client credentials.
- **Rate Limiting:** Enforces strict request limits for APIs using an in-memory cache technique (easily expandable to Redis for distributed caching).
- **Usage Tracking:** Records global API request counts asynchronously using FastAPI Background Tasks for non-blocking operations.
- **Custom Exception Handling:** Returns user-friendly JSON responses with formatted Rate Limit (`429 Too Many Requests`) errors.
- **RESTful Protected Endpoints:** Demonstrates securing specific routes using dependency injection (`Depends`) and header parsing.
- **Auto-generated Documentation:** Swagger UI and ReDoc to easily test and explore endpoints natively.

## Setup Instructions

### 1. Requirements
- Ensure you have Python 3.9+ installed.

### 2. Environment Setup
```bash
python -m venv venv

venv\Scripts\activate  

pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the `task1` root directory and define your environment variables. At a minimum, you will need a database URL:
```env
DATABASE_URL=sqlite:///./test.db
```

### 4. Run the Server
Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```

## Things to Keep in Mind to Run the Project
1. **`.env` File is Required:** Ensure the `.env` file is present in the `task1` folder before starting the server. Without `DATABASE_URL`, the application will fail to initialize the database connection.
2. **Database Initialization:** The application will auto-create the necessary SQLite tables on local startup via `models.Base.metadata.create_all(bind=engine)` found in `main.py`.
3. **Rate Limit Parameters:** The rate limit bounds (e.g., 100 requests) and the window span (e.g., 60 seconds) are managed in `dependencies.py` via `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW_SEC`. Adjust these metrics as per your testing bounds.
4. **API Key Generation:** Generated API keys are shown to the user *only once* during creation. Make sure to keep it somewhere safe — it cannot be recovered.
5. **Background Increment:** The global request count is updated asynchronously as a background task. This allows for near-instant responses to clients while database modifications happen independently.

## API Documentation & Testing

### Interactive Documentation (Swagger)
Once the server is running, navigate to:
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Testing with Postman
Import the `SaaS API Gateway.postman_collection.json` file into Postman:
1. Run **"Obtain Credentials"** — this auto-saves the returned API key to the collection variables.
2. Run **"Access Protected Resource"** to test a verified route.
3. To test the rate limiter, quickly run "Access Protected Resource" multiple times above the set threshold (e.g., 100 times in 1 minute) to see the `429 Too Many Requests` limit.

## Structure
- `main.py`: App init, custom exception handlers, and routers linking.
- `database.py`: SQLAlchemy setup and connection configuration.
- `models.py`: Database models mapping.
- `schemas.py`: Payload validation schemas via Pydantic.
- `security.py`: Secure key generation and SHA-256 hashing functions.
- `dependencies.py`: Core logic for API key verification, rate limiting cache, and database session injection.
- `routers/`:
  - `auth.py`: Credential and API Key generation endpoints.
  - `resource.py`: Demonstrative protected API endpoint utilizing dependencies.

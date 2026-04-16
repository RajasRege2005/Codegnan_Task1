# FastAPI API Gateway Service

This is a backend service developed with FastAPI to manage API access, generation of credentials, and enforce usage limits per credential. 

## Features
- **API Access Management:** Clients obtain a securely generated API key (stored securely as SHA-256 hash).
- **Rate Limiting:** Enforces request limits for APIs using an in-memory cache technique (expandable to Redis).
- **Usage Tracking:** Records global API request count asynchronously via background tasks.
- **RESTful protected endpoints**.
- Auto-generated Swagger Documentation.

## Setup Instructions

### 1. Requirements
Ensure you are using Python 3.9+ 

### 2. Environment Setup
```bash
python -m venv venv
source venv/Scripts/activate  
pip install -r requirements.txt
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```

### 4. Interactive Documentation (Swagger)
Once the server is running, navigate to:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 5. Testing with Postman
Import the `SaaS API Gateway.postman_collection.json` file into Postman:
1. Run "Obtain Credentials" - this auto-saves the returned API key to variables.
2. Run "Access Protected Resource".
3. To test the rate limiter, quickly run "Access Protected Resource" multiple times above the set threshold (e.g., 100 times in 1 minute).

## Structure
- `main.py`: App init and routers linking.
- `database.py`: SQLAlchemy setup (using SQLite).
- `models.py`: Database models.
- `schemas.py`: Payload validation schemas via Pydantic.
- `security.py`: Secure key generation and hashing functions.
- `dependencies.py`: The `verify_api_key_and_rate_limit` logic and database session injection.
- `routers/`:
  - `auth.py`: Credential generation endpoint.
  - `resource.py`: Demonstrative protected API endpoint.

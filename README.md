# Projet Fin d'Année Habiba

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API Gateway
uvicorn gateway:app --reload --port 8000

# Run the Book Service API (in another terminal)
uvicorn book_api:app --reload --port 8001

# Run the User Service API (in another terminal)
uvicorn user_api:app --reload --port 8002
```

## Usage

1. Go to `http://localhost:8000/docs` to see the API Gateway documentation.
2. Go to `http://localhost:8000/` and login with the following credentials:
   - username: `Habiba`
   - password: `habiba@12`
3. Add endpoints for book service API and user service API:
   1. Book endpoint:
      - Endpoint: `book`
      - Ip: `localhost`
      - Port: `8001`
   2. User endpoint:
      - Endpoint: `user`
      - Ip: `localhost`
      - Port: `8002`
4. Go to `http://localhost:8000/book` and `http://localhost:8000/user` to see the API Gateway in action.

## Misc

```bash
# Use the following commands to seed more data in the database

curl -X POST http://localhost:8001/ -H "Content-Type: application/json" -d '{"title": "Mon livre", "author": "Yasmina Khadra", "description": "Mohammed Moulessehoul, better known by the pen name Yasmina Khadra.", "rating": "4" }'
curl -X POST http://localhost:8001/ -H "Content-Type: application/json" -d '{"title": "Women", "author": "Charles Bukowski", "description": "Henry Charles Bukowski was a German-American poet, novelist, and short story writer.", "rating": "5" }'

curl -X POST http://localhost:8002/ -H "Content-Type: application/json" -d '{"Email_address": "admin@test.com", "password": "password"}'
curl -X POST http://localhost:8002/ -H "Content-Type: application/json" -d '{"Email_address": "test@test.com", "password": "test"}'
```

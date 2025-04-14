# goit-pythonweb-hw-10


Create the .env file

```.env
POSTGRES_DB=contacts_app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password1
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
DEBUG=True
DB_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
ALLOWED_CORS=["http://localhost:8000","http://localhost:3000"]

MAIL_USERNAME=temp-pythonweb-hw-10@meta.ua
MAIL_PASSWORD=example
MAIL_FROM=temp-pythonweb-hw-10@meta.ua
MAIL_PORT=465
MAIL_SERVER=smtp.meta.ua


CLOUDINARY_NAME=name
CLOUDINARY_API_KEY=api_key
CLOUDINARY_API_SECRET=api_secret

```

Up containers 
```
make up
```
Run migration in docker

```
make migr
```

Up database only
```
make db
```

Run locally (dev mode)
```
make run
```

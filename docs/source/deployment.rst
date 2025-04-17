.. _deployment:

Deployment
==========

This guide covers different deployment options for the UContact REST API Service.

Docker Compose Deployment
-------------------------

The application can be deployed using Docker Compose, which sets up all required services:

1. FastAPI application with Uvicorn
2. PostgreSQL database
3. Redis for caching

1. Install all dependencies and run database migration:

  $ make install

2. Setup nginx:

  $ sudo apt install nginx

3. Create nginx config:

Example of nginx configuration file:

.. code-block:: nginx

    server {
        listen 80;
        server_name your_domain.com;

        location / {
            include proxy_params;
            proxy_pass http://localhost:3000;
        }
    }

4. Links sites and restart Nginx

  $ sudo cp ucontact.conf /etc/nginx/sites-available/ucontact
  $ sudo ln -s /etc/nginx/sites-available/ucontact /etc/nginx/sites-enabled/
  $ sudo nginx -t
  $ sudo systemctl restart nginx

Congrats! Now you can use your application.


You can also modify ``compose.yaml`` and ``Dockerfile`` to you needs:

Docker Compose Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use a ``compose.yaml`` file:

.. literalinclude:: ../../compose.yaml
   :language: yaml
   :linenos:


Dockerfile
~~~~~~~~~~

Example of Dockerfile:

.. literalinclude:: ../../Dockerfile
   :language: dockerfile
   :linenos:

Deployment Commands
-------------------

The application includes several Makefile commands for easy deployment:

Database Management
~~~~~~~~~~~~~~~~~~~

.. code-block:: make

    # Create new database and run migrations
    make newdb:
        docker-compose exec db createdb -U postgres contacts_db
        make updb

    # Update database with latest migrations
    make updb:
        alembic upgrade head

    # Create new migration
    make migration message="migration message":
        alembic revision --autogenerate -m "$(message)"

Service Management
~~~~~~~~~~~~~~~~~~

.. code-block:: make

    # Start all services
    make up:
        poetry export --without-hashes -f requirements.txt --output requirements.txt
        docker-compose up -d

    # Start Redis instance only
    make upredis:
        docker run --name redis-hw012 -p 6379:6379 -d redis:8.0-rc1

    # Run migrations in Docker
    make migr:
        @img=$$(docker ps -aqf "name=goit-pythonweb-hw-012_app") && \
        docker exec -it $$img sh -c "alembic upgrade head"

Manual Deployment
-----------------

For manual deployment without Docker:

1. Install PostgreSQL and Redis::

    sudo apt update
    sudo apt install postgresql redis-server

2. Create database and user::

    sudo -u postgres psql
    CREATE DATABASE contacts_db;
    CREATE USER myuser WITH PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE contacts_db TO myuser;

3. Set up Python environment::

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

4. Configure environment variables::

    cp .example.env .env
    # Edit .env with your configuration

5. Run migrations::

    make migrate

6. Start the application with Uvicorn::

    make run

7. Configure Nginx as reverse proxy::

    sudo apt install nginx
    sudo cp ucontact.conf /etc/nginx/sites-available/ucontact
    sudo ln -s /etc/nginx/sites-available/ucontact /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx



Congrats! Now you can use your application.
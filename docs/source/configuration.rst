.. _configuration:

Configuration
============

The UContact REST API Service uses environment variables for configuration. These settings can be configured through a `.env` file or system environment variables.

Environment Variables
-------------------

Database Configuration
~~~~~~~~~~~~~~~~~~~~

* ``POSTGRES_DB`` - PostgreSQL database name
* ``POSTGRES_USER`` - PostgreSQL username
* ``POSTGRES_PASSWORD`` - PostgreSQL password
* ``POSTGRES_PORT`` - PostgreSQL port (default: 5432)
* ``POSTGRES_HOST`` - PostgreSQL host (default: localhost)

Redis Configuration
~~~~~~~~~~~~~~~~~

* ``REDIS_HOST`` - Redis server host (default: localhost)
* ``REDIS_PORT`` - Redis server port (default: 6379)
* ``REDIS_PASSWORD`` - Redis password (if required)

JWT Authentication
~~~~~~~~~~~~~~~~

* ``SECRET_KEY`` - Secret key for JWT token generation
* ``ALGORITHM`` - JWT encryption algorithm (default: HS256)
* ``ACCESS_TOKEN_EXPIRE_MINUTES`` - JWT token expiration time in minutes (default: 15)
* ``REFRESH_TOKEN_EXPIRE_MINUTES`` - JWT refresh token expiration time in minutes (default: 7 days)

Email Configuration
~~~~~~~~~~~~~~~~~

* ``MAIL_USERNAME`` - SMTP username for email notifications
* ``MAIL_PASSWORD`` - SMTP password
* ``MAIL_FROM`` - Sender email address
* ``MAIL_PORT`` - SMTP port (default: 587)
* ``MAIL_SERVER`` - SMTP server hostname
* ``MAIL_FROM_NAME`` - Sender name in emails
* ``MAIL_TLS`` - Use TLS for email (true/false)
* ``MAIL_SSL`` - Use SSL for email (true/false)


Example .env File
---------------

Here's an example `.env` file with default values::

    # PostgreSQL Configuration
    POSTGRES_DB=contacts_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_password
    POSTGRES_PORT=5432
    POSTGRES_HOST=localhost

    # Redis Configuration
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_PASSWORD=

    # JWT Configuration
    SECRET_KEY=your_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Email Configuration
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_app_password
    MAIL_FROM=your_email@gmail.com
    MAIL_PORT=587
    MAIL_SERVER=smtp.gmail.com
    MAIL_FROM_NAME=UContact Service
    MAIL_TLS=True
    MAIL_SSL=False

Configuration Module
------------------

The configuration settings are managed in `src/conf/config.py`. This module:

* Loads environment variables
* Provides configuration classes for different components
* Validates configuration values
* Sets default values when needed

Example configuration usage::

    from src.conf.config import settings

    # Access database settings
    db_url = settings.DB_URL

    # Access JWT settings
    secret_key = settings.SECRET_KEY
.. _authentication:

Authentication
==============

The UContact REST API Service uses JWT (JSON Web Token) based authentication with email verification.

Authentication Flow
-------------------

1. **Registration**: Users register with email, username, and password
2. **Email Verification**: A verification link is sent to the user's email
3. **Login**: Users login with username/password to receive JWT tokens
4. **API Access**: Protected endpoints are accessed using the JWT token
5. **Token Refresh**: Expired tokens can be refreshed using a refresh token

API Endpoints
-------------

Register
~~~~~~~~

.. http::post:: /api/auth/register

Register a new user with email verification.

**Request Body**:

.. code-block:: json

    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepassword123"
    }

**Response**:

.. code-block:: json

    {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2025-04-16T12:00:00",
        "avatar": null,
        "is_verified": false
    }

Login
~~~~~~

.. http::post:: /api/auth/login

Authenticate user and receive JWT tokens.

**Request Body** (form-data):

- ``username``: User's username
- ``password``: User's password

**Response**:

.. code-block:: json

    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "bearer"
    }

Refresh Token
~~~~~~~~~~~~~~

.. http::post:: /api/auth/refresh-token

Generate new JWT tokens using a refresh token.

**Request Body**:

.. code-block:: json

    {
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }

**Response**:

.. code-block:: json

    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "bearer"
    }

Email Verification
~~~~~~~~~~~~~~~~~~

.. http::get:: /api/auth/confirmed_email/{token}

Verify user's email address using the verification token sent via email.

**Response**:

.. code-block:: json

    {
        "message": "Email verified successfully"
    }

API Implementation
------------------

Authentication Router
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.api.auth
   :members:
   :undoc-members:
   :show-inheritance:

Authentication Service
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.services.auth
   :members:
   :undoc-members:
   :show-inheritance:

Using Authentication
--------------------

To use authentication in your requests:

1. Register a new user account
2. Verify your email using the link sent to your email
3. Login to get JWT tokens
4. Include the access token in the Authorization header:

.. code-block:: bash

    curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." http://localhost:8000/api/contacts

Token Expiration
----------------
- Access tokens expire after 15 minutes (by default)
- Refresh tokens expire after 7 days (by default)
- Use the refresh token endpoint to get new tokens before expiration
.. _api:

API Reference
=============

.. contents:: Resource Types
   :local:
   :depth: 2

Common Conventions
------------------

Date and Time Format
~~~~~~~~~~~~~~~~~~~~

All ``datetime`` fields (created_at, updated_at) must be in ISO 8601 format in UTC time
(using time zone designator "Z") and expressed to millisecond precision as
recommended by the `W3C Date and Time Formats Note`_ eg. ``2025-04-16T12:28:54.744Z``

.. _`W3C Date and Time Formats Note`: https://www.w3.org/TR/NOTE-datetime

Date fields (birthday) must be in ISO 8601 date format time Date in UTC	``2025-04-16``
Also **birthday** field must be in the past.

Authentication
~~~~~~~~~~~~~~

All API endpoints except authentication endpoints require JWT authentication.
Include the JWT token in the Authorization header::

    Authorization: Bearer <your_jwt_token>


Rate Limiting
~~~~~~~~~~~~~

The API implements rate limiting to prevent abuse:

- 5 requests per minute for authenticated users to /me endpoint
- no limit for authenticated user for other endpoints
- 20 requests per minute for unauthenticated requests for all endpoint

Resource Types
--------------

Contact
~~~~~~~

A Contact represents a person in your address book.

**Attributes:**

- ``id`` (integer): Unique identifier
- ``first_name`` (string): First name of the contact
- ``last_name`` (string): Last name of the contact
- ``email`` (string): Email address
- ``phone`` (string): Phone number in international format
- ``birthday`` (string, ISO 8601 Date): Contact's birthday
- ``additional_data`` (object, nullable): Additional contact information
- ``created_at`` (string, ISO 8601): Creation timestamp
- ``updated_at`` (string, ISO 8601): Last update timestamp

**Example:**

.. code-block:: json

    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": {
            "company": "Example Corp",
            "position": "Developer"
        },
        "created_at": "2025-04-16T12:28:54.744Z",
        "updated_at": "2025-04-16T12:28:54.744Z"
    }

User
~~~~

Represents an authenticated user of the API.

**Attributes:**

- ``id`` (integer): Unique identifier
- ``username`` (string): User's username
- ``email`` (string): User's email address
- ``created_at`` (string, ISO 8601): Account creation timestamp
- ``avatar`` (string, nullable): URL to user's avatar
- ``is_verified`` (boolean): Email verification status

**Example:**

.. code-block:: json

    {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2025-04-16T12:28:54.744Z",
        "avatar": null,
        "is_verified": true
    }

Error Responses
---------------

The API uses conventional HTTP response codes to indicate the success or failure of requests.

**Common Error Codes:**

- ``400 Bad Request``: Invalid request payload or parameters
- ``401 Unauthorized``: Missing or invalid authentication
- ``403 Forbidden``: Authenticated but not authorized
- ``404 Not Found``: Resource not found
- ``422 Unprocessable Entity``: Validation error
- ``429 Too Many Requests``: Rate limit exceeded
- ``500 Internal Server Error``: Server error

**Error Response Format:**

.. code-block:: json

    {
        "detail": "Error message describing what went wrong"
    }

Pagination
----------

List endpoints support pagination using ``skip`` and ``limit`` parameters:

- ``skip``: Number of records to skip (default: 0)
- ``limit``: Maximum number of records to return (default: 100, max: 1000)

**Example:**
.. http:get:: /api/contacts/?skip=0&limit=10

**Response Headers:**

- ``X-Total-Count``: Total number of records
- ``X-Page-Count``: Total number of pages
- ``X-Current-Page``: Current page number
- ``X-Per-Page``: Records per page

Filtering
---------

The API supports advanced filtering using query parameters. See :ref:`query_syntax` for detailed information about filtering capabilities.

Caching
-------

The API implements Redis-based caching for improved performance:

- GET requests are cached for 10 seconds
- List endpoints are cached for 10 seconds
- Upcoming birthdays are cached for 1 hour

Cache is automatically invalidated when related resources are modified.
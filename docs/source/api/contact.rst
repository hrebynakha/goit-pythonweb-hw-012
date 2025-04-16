.. _api_contacts:

Contact API
==========

The Contact API provides endpoints for managing user contacts, including CRUD operations, filtering, and birthday notifications.

Swagger/Redoc UI documentation (Demo) 
-------------------------------------

* Interactive API documentation: https://try.api.ucontacts.d0s.site/docs
* Alternative API documentation: https://try.api.ucontacts.d0s.site/redoc

API Endpoints
-----------

List Contacts
~~~~~~~~~~~~

.. http:get:: /api/contacts/

   Get a paginated and filtered list of contacts.

   **Example request**:

   .. sourcecode:: http

      GET /api/contacts/?skip=0&limit=10&query=john HTTP/1.1
      Host: example.com
      Authorization: Bearer <token>

   **Query Parameters**:

   - ``skip`` (optional): Number of records to skip (default: 0)
   - ``limit`` (optional): Maximum number of records to return (default: 100)
   - ``query`` (optional): Search query to filter contacts

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [
        {
          "id": 1,
          "first_name": "John",
          "last_name": "Doe",
          "email": "john@example.com",
          "phone": "+1234567890",
          "birthday": "1990-01-01",
          "additional_data": null,
          "created_at": "2025-04-16T12:00:00",
          "updated_at": "2025-04-16T12:00:00"
        }
      ]

Upcoming Birthdays
~~~~~~~~~~~~~~~~

.. http:get:: /api/contacts/get-upcoming-birthday

   Get contacts with upcoming birthdays within a specified time range.

   **Query Parameters**:

   - ``skip`` (optional): Number of records to skip (default: 0)
   - ``limit`` (optional): Maximum number of records to return (default: 100)
   - ``time_range`` (optional): Days to look ahead for birthdays (default: 7)

Get Contact
~~~~~~~~~~

.. http:get:: /api/contacts/(int:contact_id)

   Get a specific contact by ID.

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": null,
        "created_at": "2025-04-16T12:00:00",
        "updated_at": "2025-04-16T12:00:00"
      }

Create Contact
~~~~~~~~~~~~

.. http:post:: /api/contacts/

   Create a new contact.

   **Example request**:

   .. sourcecode:: http

      POST /api/contacts/ HTTP/1.1
      Host: example.com
      Authorization: Bearer <token>
      Content-Type: application/json

      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01"
      }

Update Contact
~~~~~~~~~~~~

.. http:put:: /api/contacts/(int:contact_id)

   Update an existing contact.

   **Example request**:

   .. sourcecode:: http

      PUT /api/contacts/1 HTTP/1.1
      Host: example.com
      Authorization: Bearer <token>
      Content-Type: application/json

      {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01"
      }

Delete Contact
~~~~~~~~~~~~

.. http:delete:: /api/contacts/(int:contact_id)

   Delete a contact.

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": null,
        "created_at": "2025-04-16T12:00:00",
        "updated_at": "2025-04-16T12:00:00"
      }

Error Responses
-------------

.. http:any:: /api/contacts/*

   **Example error responses**:

   .. sourcecode:: http

      HTTP/1.1 401 Unauthorized
      Content-Type: application/json

      {
        "detail": "Not authenticated"
      }

   .. sourcecode:: http

      HTTP/1.1 404 Not Found
      Content-Type: application/json

      {
        "detail": "Contact not found"
      }

Implementation Details
-------------------

API Layer
~~~~~~~~

.. automodule:: src.api.contacts
   :members:
   :undoc-members:
   :show-inheritance:

Service Layer
~~~~~~~~~~~

.. automodule:: src.services.contacts
   :members:
   :undoc-members:
   :show-inheritance:

Repository Layer
~~~~~~~~~~~~~

.. automodule:: src.repository.contacts
   :members:
   :undoc-members:
   :show-inheritance:

Models and Schemas
---------------

Contact Model
~~~~~~~~~~~

.. autoclass:: src.schemas.contacts.ContactModel
   :members:
   :undoc-members:

Contact Response
~~~~~~~~~~~~~

.. autoclass:: src.schemas.contacts.ContactResponse
   :members:
   :undoc-members:

Caching
------

The Contact API implements Redis-based caching for improved performance:

- Contact lists are cached for 10 seconds
- Individual contacts are cached for 10 seconds
- Upcoming birthday lists are cached for 1 hour

Cache is automatically invalidated when contacts are modified.
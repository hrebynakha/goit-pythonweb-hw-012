.. _query_syntax:

Query Syntax
===========

The UContact API uses `fastapi-sa-orm-filter <https://pypi.org/project/fastapi-sa-orm-filter/>`_ for powerful and flexible filtering capabilities.

Filter Operators
--------------

The following operators are available for filtering:

- ``eq``: Exact match (equals)
- ``ne``: Not equal
- ``gt``: Greater than
- ``lt``: Less than
- ``gte``: Greater than or equal
- ``lte``: Less than or equal
- ``in_``: Match any value in a list
- ``not_in``: Not match any value in a list
- ``like``: SQL LIKE pattern matching
- ``ilike``: Case-insensitive LIKE
- ``not_like``: SQL NOT LIKE
- ``between``: Range between two values
- ``startswith``: Starts with pattern
- ``endswith``: Ends with pattern
- ``contains``: Contains pattern

Available Filters
---------------

.. automodule:: src.filters.contacts
   :members:
   :undoc-members:
   :show-inheritance:

The following fields support filtering:

Text Fields
~~~~~~~~~~

- ``first_name``: First name of the contact
    - Supported operators: eq, in_, like, startswith, contains
- ``last_name``: Last name of the contact
    - Supported operators: eq, in_, like, startswith, contains
- ``email``: Email address
    - Supported operators: eq, in_, like, startswith, contains
- ``phone``: Phone number
    - Supported operators: eq, in_, like, startswith

Date Fields
~~~~~~~~~~

- ``birthday``: Contact's birthday
    - Supported operators: eq, gt, lt, between
- ``created_at``: Record creation timestamp
    - Supported operators: eq, gt, lt, between
- ``updated_at``: Last update timestamp
    - Supported operators: eq, gt, lt, between

Query Examples
------------

Basic Filtering
~~~~~~~~~~~~~

1. Find contacts with first name "John"::

    GET /api/contacts/?query=first_name:eq:John

2. Find contacts whose email starts with "john"::

    GET /api/contacts/?query=email:startswith:john

3. Find contacts with phone numbers containing "555"::

    GET /api/contacts/?query=phone:contains:555

Multiple Conditions
~~~~~~~~~~~~~~~~

You can combine multiple filters using ``,`` as AND operator::

    GET /api/contacts/?query=first_name:eq:John,last_name:eq:Doe

Date Range Queries
~~~~~~~~~~~~~~~~

1. Find contacts born after 1990::

    GET /api/contacts/?query=birthday:gt:1990-01-01

2. Find contacts created in the last week::

    GET /api/contacts/?query=created_at:gt:2025-04-09

3. Find contacts with birthdays between dates::

    GET /api/contacts/?query=birthday:between:1990-01-01,2000-12-31

List Operations
~~~~~~~~~~~~~

1. Find contacts with specific first names::

    GET /api/contacts/?query=first_name:in_:["John","Jane","Bob"]

Pattern Matching
~~~~~~~~~~~~~~

1. Find contacts whose last name contains "smith" (case-insensitive)::

    GET /api/contacts/?query=last_name:ilike:%smith%

2. Find contacts whose email is from specific domain::

    GET /api/contacts/?query=email:endswith:@example.com

Complex Queries
~~~~~~~~~~~~~

Find contacts named John, created after 2025-01-01, with gmail address::

    GET /api/contacts/?query=first_name:eq:John,created_at:gt:2025-01-01,email:endswith:@gmail.com

Response Pagination
----------------

All filtered queries support pagination using ``skip`` and ``limit`` parameters::

    GET /api/contacts/?query=first_name:eq:John&skip=0&limit=10

Error Handling
------------

If an invalid filter is provided, the API will return a 400 Bad Request with an error message::

    {
        "detail": "Invalid filter operator 'invalid' for field 'first_name'"
    }

Performance Considerations
-----------------------

- Use specific filters when possible (eq instead of like)
- Combine multiple conditions to reduce the result set
- Consider using pagination for large result sets
- Complex queries with multiple conditions may impact performance
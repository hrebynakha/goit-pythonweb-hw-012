.. _authorization:

Authorization
=============

The UContact REST API implements role-based access control (RBAC) to manage user permissions and access to resources.

User Roles
----------

The system supports the following roles:

Administrator
~~~~~~~~~~~~~

**Role:** ``admin``

Permissions:
    - View own contacts
    - View system statistics and metrics
    - Modify their avatar and settings
    - Access admin-only endpoints
    - Manage user roles

Regular User
~~~~~~~~~~~~

**Role:** ``user``

Permissions:
    - Manage own contacts (CRUD operations)
    - Update own profile information(except avatar)
    - View own contacts
    - Search and filter own contacts
    - Access birthday notifications

Restrictions:
    - Cannot update avatar
    - Cannot modify system settings
    - Cannot access admin endpoints

Role Assignment
---------------

Roles are assigned through the following methods:

1. Default Role
~~~~~~~~~~~~~~~

New users are automatically assigned the ``user`` role upon registration.

2. Admin Assignment
~~~~~~~~~~~~~~~~~~~

Administrators can modify user avatar and role.

Permission Checking
-------------------

The API implements permission checking using role-specific decorators:

.. code-block:: python

    @router.get("/protected/admin/route")
    async def protected_admin_route(
        user: User = Depends(get_current_admin_user),
    ):  
    # Only admins can access this endpoint
    pass


Error Responses
---------------

When attempting to access unauthorized resources:

.. code-block:: http

    HTTP/1.1 403 Forbidden
    Content-Type: application/json

    {
        "detail": "Not authorized to perform this action"
    }

Future Enhancements
-------------------

Planned role-based features:

1. Custom Roles
~~~~~~~~~~~~~~~
- Create custom roles with specific permissions
- Fine-grained access control
- Role hierarchies

2. Role Groups
~~~~~~~~~~~~~~
- Group users by department or team
- Shared access to contacts within groups
- Group-specific permissions

3. Temporary Permissions
~~~~~~~~~~~~~~~~~~~~~~~~
- Time-limited role assignments
- Temporary access elevation
- Permission delegation

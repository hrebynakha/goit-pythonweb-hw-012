.. _about:

About UContacts
=============

Overview
--------

UContacts is a modern, secure REST API service designed for efficient contact management. Built with FastAPI and modern Python practices, it provides a robust solution for storing and managing personal and business contacts.

History
-------

The project was initiated in 2025 by Hrebynakha Anatolii as part of the GoIT Python Web Development course. It has evolved from a simple contact management system into a full-featured API service with advanced capabilities like contact filtering, birthday notifications, and role-based access control.

Key Features
----------

- **Modern Architecture**: Built with FastAPI for high performance and async support
- **Secure Authentication**: JWT-based authentication with email verification
- **Role-Based Access**: Flexible authorization system with admin and user roles
- **Advanced Filtering**: Powerful contact search and filtering capabilities
- **Redis Caching**: Optimized performance with intelligent caching
- **Birthday Notifications**: Smart notification system for upcoming birthdays
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Comprehensive Documentation**: Detailed API documentation with Swagger/ReDoc UI

Technology Stack
-------------

Backend Framework
~~~~~~~~~~~~~~
- FastAPI (Python 3.10+)
- Uvicorn ASGI server
- SQLAlchemy ORM
- Alembic migrations

Database & Caching
~~~~~~~~~~~~~~~
- PostgreSQL for persistent storage
- Redis for caching and session management

Security
~~~~~~~
- JWT authentication
- Password hashing with bcrypt
- Email verification
- CORS support

DevOps & Deployment
~~~~~~~~~~~~~~~~
- Docker containerization
- Docker Compose orchestration
- Nginx reverse proxy
- GitHub Actions CI/CD

Contributing
-----------

UContacts is an open-source project, and contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

We appreciate:

- Bug reports
- Feature suggestions
- Documentation improvements
- Code contributions

Future Plans
----------

We're continuously working to improve UContacts. Upcoming features include:

1. **Enhanced Contact Management**
   - Contact groups and tags
   - Bulk operations
   - Contact sharing

2. **Advanced Security**
   - Two-factor authentication
   - OAuth2 social login
   - API key management

3. **Integration Features**
   - Calendar integration
   - Email client integration
   - Contact import/export

4. **Performance Improvements**
   - GraphQL API support
   - Enhanced caching strategies
   - Real-time updates

License
-------

UContacts is released under the MIT License. See the LICENSE file for more details.

Contact
-------

- **Author**: Hrebynakha Anatolii
- **GitHub**: https://github.com/hrebynakha/goit-pythonweb-hw-012
- **Demo**: https://try.api.ucontacts.d0s.site

For support or inquiries, please open an issue on GitHub or contact the maintainers directly.
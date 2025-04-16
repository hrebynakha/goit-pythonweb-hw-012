<!-- omit in toc -->
# <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png" width="25" /> UContacts API

> UContacts is a modern, secure REST API for efficient contact management, built with FastAPI and PostgreSQL.

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.MD)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen)](https://goit-pythonweb-hw-012.readthedocs.io/en/latest/)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/hrebynakha/goit-pythonweb-hw-012/ci.yml?branch=master)](https://github.com/hrebynakha/goit-pythonweb-hw-012/actions)

> 💝 A lot of my free time, evenings, and weekends goes into making UContacts happen; please consider starring or contributing! 😊

- [📦 Features](#-features)
- [📘 Documentation](#-documentation)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [🙌 Contributing](#-contributing)
- [🌎 Roadmap](#-roadmap)

UContacts is a REST API service for managing personal and business contacts. It supports JWT authentication, role-based access, advanced filtering, birthday notifications, and more. Built with FastAPI for high performance and modern Python standards.

## 📦 Features

- FastAPI backend with async support
- PostgreSQL database
- Redis caching
- JWT authentication and email verification
- Role-based access control (admin/user)
- Advanced contact filtering and search
- Birthday notifications
- Docker & Docker Compose support
- Swagger and ReDoc API docs

## 📘 Documentation

Comprehensive documentation is available:
- [App Documentation](https://goit-pythonweb-hw-012.readthedocs.io/en/latest/)
- [Swagger API Docs (try it live!)](https://try.api.ucontacts.d0s.site/docs)
- [ReDoc API Docs](https://try.api.ucontacts.d0s.site/redoc)

## 🚀 Quick Start

Clone the repository:
```bash
git clone https://github.com/hrebynakha/goit-pythonweb-hw-012.git
cd goit-pythonweb-hw-012
```

Create your `.env` file (see `docs/source/configuration.rst` for details):
```ini
POSTGRES_DB=contacts_app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password1
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
DB_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

Run the app and database with Docker Compose:
```bash
make up
```

Initialize the database and run migrations:
```bash
make migrate
```

Start the API server:
```bash
make run
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## ⚙️ Configuration

See full configuration options in [App Documentation](https://goit-pythonweb-hw-012.readthedocs.io/en/latest/configuration.html).

## 🙌 Contributing

Pull Requests, Bug Reports and Feature Requests are welcome! Feel free to help out with Issues and Projects!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🌎 Roadmap

You can find a list of planned features and enhancements in the [documentation roadmap](docs/source/about.rst#future-plans).

- Enhanced contact management (groups, tags, sharing)
- Two-factor authentication & OAuth2
- Calendar/email integration
- Real-time updates

---

Made with ❤️ by Hrebynakha Anatolii
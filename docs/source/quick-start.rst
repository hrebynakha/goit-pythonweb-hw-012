.. _quick_start:

Quick Start
===========

This guide will help you get the UContact REST API Service up and running quickly.

Prerequisites
-------------

Before starting, ensure you have the following installed:

* Python 3.10 or higher
* PostgreSQL
* Redis

Installation
------------

1. Clone the repository::

    $ git clone https://github.com/hrebynakha/goit-pythonweb-hw-012.git
    $ cd goit-pythonweb-hw-012

2. Create and activate a virtual environment::

    $ python -m venv venv
    $ source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies::

    $ pip install -r requirements.txt

Configuration
-------------

1. Create a `.env` file based on `.example.env`::

    $ cp .example.env .env

2. Update the environment variables in `.env` with your database and Redis credentials.

Running the Application
-----------------------

1. Create the database::

    $ make newdb

2. Initialize the database migration::

    $ make migrate

3. Start the application::

    $ make run

The API will be available at http://localhost:8000

API Documentation
-----------------

Once the application is running, you can access:

* Interactive API documentation: http://localhost:8000/docs
* Alternative API documentation: http://localhost:8000/redoc
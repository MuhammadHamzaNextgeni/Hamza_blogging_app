# Django Blogging App

A full-featured blogging platform built with Django, PostgreSQL, and Django REST Framework, featuring user authentication, content creation, interactivity, REST APIs, background tasks, and Docker support.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Setup & Installation](#setup--installation)
5. [Project Structure](#project-structure)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Filters](#filters)
9. [Background Tasks](#background-tasks)
10. [Testing](#testing)
11. [Dockerization](#dockerization)
12. [Deployment](#deployment)

---

## Project Overview

This blogging app is developed over an 8-week plan focusing on:

- Custom user models and authentication
- Blog posts with comments and likes
- REST API for future frontend expansion
- Asynchronous tasks for email notifications and PDF generation
- Filtering blog posts
- Dockerized environment for easy deployment

---

## Features

- **User Management**
  - Custom user model with bio
  - Sign-up, login, logout
  - User-friendly templates with Bootstrap styling

- **Blog Content**
  - Create, read, update, and delete posts
  - Add comments and likes
  - Display post and comment counts
  - Post filtering by author, date, or keywords

- **API**
  - Token-based REST API using Django REST Framework
  - Endpoints for listing posts, retrieving single post, and comments

- **Background Tasks**
  - Email notifications for post comments via Celery and Redis
  - Generate PDFs of posts asynchronously

- **Dockerized**
  - Easily run with Docker and Docker Compose
  - PostgreSQL database support

---

## Tech Stack

- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Frontend: Bootstrap
- Async Tasks: Celery, Redis
- Containerization: Docker
- Optional: Ngrok for public URLs during development

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- PostgreSQL (if not using Docker for DB)

### Steps

1. Clone the repository:

```bash
git clone <repository_url>
cd django-blog-app

2. Set up virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure PostgreSQL database in settings.py.

4. Run migrations:

python manage.py makemigrations
python manage.py migrate

5. Create a superuser:

python manage.py createsuperuser

6. Run the development server:

python manage.py runserver

Project Structure

django_blog/

├── core/               # Core app for settings, context processors, utils, signals
├── users/              # Custom User model and authentication
├── posts/              # Blog posts, comments, likes
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS)
├── api/                # DRF API
├── celery_tasks/       # Async tasks for emails & PDFs
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt


Usage

Home page lists all blog posts

Click on a post to see details and comments

Authenticated users can add posts, comments, and likes

Use the navigation bar to sign up, login, or logout

Admin panel available at /admin/

API Endpoints

Endpoint	Method	Description
/api/posts/	GET	List all posts
/api/posts/<id>/	GET	Retrieve a single post
/api/comments/	GET	List all comments
/api/comments/<id>/	GET	Retrieve a single comment


Filters

Posts can be filtered via URL query parameters:

/posts/?author=john&keyword=django&date_from=2025-01-01&date_to=2025-10-10

Background Tasks

- Email notifications to post authors when comments are added

- PDF generation of posts

- Uses Celery + Redis for async processing

Testing

python manage.py test

Dockerization

Build and run containers:

- docker-compose up --build

Services included: Django app, PostgreSQL, Redis

Access app at http://localhost:8000

Deployment

Collect static files:

- python manage.py collectstatic

- Configure production settings, WSGI server (Gunicorn/uWSGI)

- Deploy with Docker or cloud provider

Credits

Developed by Muhammad Hamza Mushtaque. Designed for scalability and easy integration with frontend frameworks.
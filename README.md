# TimeAware

TimeAware is a productivity app that lets you effortlessly and precisely track your activities. It can be an effective tool in building good habits, or getting rid of bad ones.

  <p align="center"> 
    <strong>Explore the documentation</strong>
    <br />
    <br />
    <a href="https://timeaware.fly.dev/">Live Production Website</a>
    ·
    <a href="https://github.com/Filbog/timeaware-django/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Filbog/timeaware-django/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Technical Details](#technical-details)
- [Running the Code on Your Local Machine](#running-the-code-on-your-local-machine)
- [Roadmap](#roadmap)
- [Contact](#contact)

## Project Description

TimeAware - as the name suggests - helps users be more aware on what they spend their time on. It enables users add activities, measure time spent on them and later display that data as charts. The project has all the typical CRUD functionality for custom-built models via Django ORM. The whole app - idea, design, architectural, code - is built from scratch.

## Features

- Sign up with email to have full access to the app's functionality
- Create and manage activities (CRUD) and categorize them by type (positive/negative/neutral)
- Track the activities with a tracker built with Javascript
- Tracking data visualisation with Chart.js

## Technical Details
### Back End and Database
- This App is built predominantly with Django framework
- I've built it with class-based views to solidify my knowledge on them
- Django ORM used for communication with the database (PostgreSQL for production, SQLite for local environment)
- Classic CRUD implementation with creating and managing activities
- Registration and user management: Django's built-in authentication system with custom registration view and form, enriched with sending email confirmation link for creating the user account as well as password recovery
### Front End
- Django's templates in conjunction with plain Javascript were all I needed to achieve my desired result and functionality
- For styling, I've used Bootstrap 5
- Django Crispy Forms was used to render forms in the app
- I've used Chart.js for data visualisation part
### Deployment
- The app is fully up-and-running on https://timeaware.fly.dev/ 
- FlyIO was the platform of choice for deploying my app. This PaaS is pretty reliable and relatively inexpensive.
- What also led me to using FlyIO is its relative simplicity to create and connect a PostgreSQL database and establish environment variables such as email credentials or the app's secret key
- WhiteNoise package to handle static files (for production)

## Running the Code on Your Local Machine
### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git
- A virtual environment tool (optional but recommended)

### Clone the Repository

```sh
git clone https://github.com/Filbog/timeaware-django.git
cd timeaware-django
```
### Create and Activate a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install Dependencies
```sh
pip install -r requirements.txt
```
### Create and Configure the .env File
Create a .env file in the project root and add the following environment variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
```
You can generate your 'SECRET_KEY' using:
```sh
python -c "import secrets; print(secrets.token_urlsafe())"
```
### Apply Migrations and Collect Static Files
```sh
python manage.py migrate
python manage.py collectstatic
```
### Run the Development Server
```sh
python manage.py runserver
```
Open your browser and navigate to http://127.0.0.1:8000 to see the application in action.

## Roadmap
Features I'd love to implement in the future:
- Adding a "search" functionality
- Filtering displayed activities by their "positive/negative/netural" badges
- Adding activities to "Favorites"
- PWA, Offline functionality

## Contact
Message me via email: f.boguslawski101@gmail.com
Or on Linkedin: https://www.linkedin.com/in/filip-boguslawski/




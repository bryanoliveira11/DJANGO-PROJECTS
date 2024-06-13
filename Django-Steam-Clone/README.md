# Django Steam Clone

This project is a clone of the popular digital distribution platform, Steam, built using Django. The purpose of this project is for fun and to learn more about Django and web development.

## Installation

### Prerequisites

- Python 3.x
- Django 3.x
- Git

### Steps

1. Clone the repository

    ```bash
    git clone https://github.com/bryanoliveira11/DJANGO-PROJECTS
    cd django-steam-clone
    ```

2. Create and activate a virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser to access the Django admin

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server

    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000/` to see the application.

## Project Structure

- `SteamClone/` - Main settings folder
- `store/` - Django app containing models, views, templates, and static files about the store page
- `base_templates/` - Base HTML templates
- `base_static/` - Base Static files (CSS, JavaScript, images)
- `requirements.txt` - List of dependencies
- `manage.py` - Django management script

## Acknowledgements

- Django documentation
- Steam platform for inspiration

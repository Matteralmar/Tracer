# Tracer

Django build bug-tracking system

---

## Getting Started

To run this project locally you will need to set your environment variables

1. Create a virtual environment inside the project by running `virtualenv venv` or other commands in your terminal
2. Activate venv using `source venv/bin/activate`
3. Install all the needed packages from "requirements.txt"
4. Install PostgreSQL to your computer, create new database and connect it to the project
5. Create a new file named `.env` inside the your project folder
6. Copy all the variables from `bugTrack/.template.env` and assign your own values to them
7. Configure your settings.py to match your `.env` file
8. Make migrations by running `python manage.py migrate` in your terminal
9. Run `export READ_DOT_ENV_FILE=True` inside your terminal so that your environment variables file will be read
10. Run server using `python manage.py runserver` command

# Tracer project made by Georgiy Vasyliev

Django build bug-tracking system

---

## Getting Started

To run this project locally you will need to set your environment variables

1. Create a virtual environment inside the project by running `virtualenv venv` or other commands in your terminal
3. Activate venv using `source local/bin/activate`
4. Install all the needed packages from "requirements.txt" `pip install -r requirements.txt`
5. If some requirements are not installed, install them using `pip install <requirment>` (if pip not installed or not updated then install it or update it)
6. Add generated secret key into SECRET_KEY field in bugTrack/settings.py. Generate it using `python -c "import secrets; print(secrets.token_urlsafe(50))"`
7. Change DATABASES field in the same file to: DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': 'mydatabase',}}
8. Make migrations by running `python manage.py migrate` in your terminal
9. Run server using `python manage.py runserver` command
10. Press http://127.0.0.1:8000/ and enjoy the run!













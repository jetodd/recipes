# Recipes

Check if Python is installed using:
```python --version```

If it isn't installed need to install Python from:
https://www.python.org/downloads/

Check if Pip is installed using:
```python -m pip --version```

Install Pip if not already installed:
https://www.makeuseof.com/tag/install-pip-for-python/

Install Django:
```pip install Django```

To update initial database with models change into the directory with manage.py and run:
```python manage.py migrate```

Then populate the database using:
```python manage.py add_recipes```

Finally create a super user with
```python manage.py createsuperuser```

To run application use:
```python manage.py runserver```

Application will run by default locally on http://127.0.0.1:8000/recipes/

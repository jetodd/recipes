# Recipes

Check if Python is installed using:
python --version

If it isn't installed need to install Python from:
https://www.python.org/downloads/

Check if Pip is installed using:
python -m pip --version

Install Pip:
https://www.makeuseof.com/tag/install-pip-for-python/

Install Django:
pip install Django

To create initial database change into the directory with manage.py and run:
python manage.py migrate

Then populate the database using:
python manage.py add_recipes

Finally create a super user with
python manage.py createsuperuser

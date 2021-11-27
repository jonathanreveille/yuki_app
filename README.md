## Welcome to my final project of the Python Developer Course for OpenClassrooms

#### I have decided to create an application that allows pet owners to set tasks, schedules for their cats

## What is in this project ? 

* Use of Django Framework 3.2.7
* Use of OOP and Python 3.8
* Database PosgreSQL
* Database for media files: AWS S3 Bucket
* Function based views, and Class based views of Django
* Use of virtualenv instead of pipenv this time
* Respect and follow recommendations from PEP8 (style guide) with flake8
* Tests and use of Coverage to check % of code tested

If you want to use this application, make sure to store all sensitive values
in a **.env** file that you create at the **root** of the project.

What you will be able to do in this application :

## For pet owners and catsitters 
1. Create a Profile
2. Customize your profile
3. Create a pet and customize pet profile
4. Create your own tasks
5. Create schedules from your tasks for a specific or more cats
6. Search for the schedule of a specific cat
7. Create a section to search/find other user
8. Create a section where users can message each other
9. Create a section where we can book a catsitter on specific dates
10. Check the future or ongoing catsittings.

## Media Files
They are all stored with Amazon S3 Bucket. Please adapt your project with
your own AWS S3 Bucket, else, comment out sections with media files in
settings and store everything in your database first. I recommend having
an S3 Bucket to test the application on any new features.

## Activate virtual environment (venv)
Create your virtual env (Windows Machine):
- ```py -m venv env --system-site-packages```
- ```env\Scripts\Activate```
- ```pip install -r requirements.txt```

## To Run Test with Coverage
To run tests locally :
- ```python manage.py test -v2```
- ```coverage run --source="." manage.py test```
Any contribution should always test the code, coverage should not go below 85%.

## Launch the project locally
- ```cd src/```
- ```python manage.py runserver```
- Go to localhost:8000 on your favorite browser

## Launch with docker-compose for local development
If you use Docker and containers, there is a docker-compose file that
is configured at the root of the project. Make sure you create the database
with your own credentials.

If you wish to develop a new feature on the project, make sure to create a test for your
function, and use flake8 and autopep8 please.

I would like to specially thank **Thierry Chappuis** and **Jimmy Kumako** for their mentoring throughout this project.

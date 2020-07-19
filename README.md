# TeacherDirectory

## Pre-requisites 
- Python 3.7 or above should be installed
- Download/Clone the repository 
- Browse to the downloaded location(##manage.py should be your working directory##)

## Installation
```
pip install -r requirements.txt
```

## Running Project
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser (follow the instructions)
python manage.py collectstatic
python manage.py runserver
```

## Working URLs

localhost:8000(local domain, this will be prefix for below mentioned URLs)
- Homepage (/directory/home)
- Directory Page (/directory/teachers)
- Teacher Details Page (/directory/teacher/<emailid>)
- Importer (/directory/import)
  
## Import Data

import data should be of CSV format.

## Database

SQLite 3

## Rest API

Django Rest Farmework

## Login Page

Access Permission Granted


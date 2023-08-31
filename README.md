# dte-workout-app
Workout journal with django

## Creating django project
First and foremost, because I work locally it is good practice to set up a virtual environment, so that the packages for this project are installed into the project folder(a sub-folder named 'venv') instead of having them  installed globally on this machine.

### Setting up the environment
Step one: Create virtual environment in folder named **venv**.
Step two: Select the virtual environment in IDE. I am using VS Code on a windows workstation. So for me it is Ctrl+Shift+P fowllowed by 'Select Interpreter'.

![vs code select interpreter](documentation/images/vs_code_select_interpreter.png)

![vs code select interpreter 1](documentation/images/vs_code_select_interpreter_1.png)

On a linux machine it is necessary to enter the follwing instruction in the terminal:
<code>source ./venv/bin/activate</code>

Step three:  Install django. I am using version 4.2.2
Step four: Install django-allauth. I am using version 0.54.0
Step five: Install psycopg2 for mapping models to database. I am using version 2.9.6
Step six: Run the startprject command in the Terminal

**Summary:**
1) <code>virtualenv venv</code>
2) **Select the interpreter from the forlder 'venv'**
3) <code>pip install Django==4.2.2</code>
4) <code>pip install django-allauth==0.54.0</code>
5) <code>pip install psycopg2==2.9.6</code>
6) <code>django-admin startproject prj .</code>

### Setting up a database for the project
For this Project I have decided to use an external database on one of the servers that I rent. It is a PostgreSQL Server with pgAdmin as a Management Tool. In order to set up a new database I need to first log in to pgAdmin.

![pgAdmin login image](documentation/images/pg_admin_login.png)

Then I need to create a database.

![pgAdmin first step createing database](documentation/images/pg_admin_create_database_1.png)

Next I need to name the database and assign a user as its owner. In other words, a user that can edit the database.
I already have a user for this app, so I just need to select him from a dropdown menu. In this case the username is workoutapp and they have all the privilleges that are necessary for editing this database.

![pagAdmin naming the database](documentation/images/pg_admin_create_database_2.png)

Here is the code that will be executed when I press **save**.

![pgaAdmin commiting the database](documentation/images/pg_admin_create_database_20.png)

Now the database is ready to be used. At least for django it is, because django will authomatically map the models to this database when the **manage.py migrate** script is executed. Alongside all the models that I will define in the scope of this project, django will also map models from other apps that I am going to use in this project, such as django-allauth, the users for django.contrib.auth and so on.

![pgAdmin save database](documentation/images/pg_admin_save_databse.png)

#### Adding database to settings.py
First of all, since I am going to store the project on GitHub, I cannot publicly share the credentials used for the database. So I will store them in a file that will be **added to gitignore**. In settings.py I will only use variables that correspond to the credentials.

I need to import the **environment variables** that I defined in **env.py**.
Since, I am using a wildcard-import <code>from .env import *</code> I need to let the linter know that it is fine.
I am doing that because there are no classes defined in that file only a number of **os.eniron** assignments. 
Which you can see as a setting for pylint in form of a coment: <code># pylint: disable=wildcard-import</code>
Also,I need to override the standard SQLite engine setting in settings.py by providing my set of settings:

<code>
# pylint: disable=wildcard-import

from pathlib import Path
import os
if os.path.exists('organizer_api_prj/env.py'):
    from .env import *

...

DATABASES = {

    "default": {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.environ['DB_NAME'],

        'USER': os.environ['DB_USER'],

        'PASSWORD': os.environ['DB_PASSWORD'],

        'HOST': os.environ['DB_HOST'],

        'PORT': os.environ['DB_PORT'],
    }
}

</code>

## Setting up the project
Now that I have the project and the database for the project has been specified, I need to migrate all the django models to the database and create a superuser. All of them will be mapped to the database.

In the terminal I enter the following intructions:
1) python manage.py migrate
2) <code>python manage.py createsuperuser</code>
2) Enter username, password and confirm password

### Setting up a folder for templates
1) Create templates forlder in the project folder: **prj/templates**
2) Add thhe folder to settings.py under TEMPLATES 
3) Create base template for the project under **prj/templates/base.html**

<code>
TEMPLATES = [

    {

        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'prj/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],

        },

    },

]
</code>


### Setting up Allauth
1) Register django-allauth in settings.py under INSTALLED_APPS
2) Register alluth.url in urls.py in the project folder
3) Copy the folder /lib/site-packages/allauth/templates to the project's template folder
4) Run the **migrate** command for allauth to commit its tables to the database
5) In settings.py set SITE_ID, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
6) See if it works (Test)

---
## Styles and CSS
I will store all styles for the application in a single file that will be contained in the **static/css** folder.

It is mandatory that the location of static files be specified in settings.py like so:

<code>
STATICFILES_DIRS = [
    BASE_DIR / "static",    
]
</code>

---
## Authentication forms
Allauth offers an application that handles authentication, so it is not necessary to create everything from scratch.
In order to modify the looks of the forms used in the process I copied all the templates from the app in to the projects 
teamplates folder, as documented two sections above in **Setting up Allauth**. To make the login, logout and signup forms
look different from the default allauth design, I need to edit them and apply the styles that I previously prepared in
**static/css/stlyes.css**.
Furthermore, I need to remove a few things from those forms and add a different layout using **bootstrap**.

---
## EXERCISE APP
The exercise app contains the model for exercises, which the user can define lor later use their workouts.
There will be three types of exercsies:
1) Weight Liftig - Can be used for anything that envolves lifting weights over a number of repetitions.
2) Running - Can be used for any activity that envolvs running or jogging over time
3) Endurance - Can be used for exercises that require to do a number of repetitions over time


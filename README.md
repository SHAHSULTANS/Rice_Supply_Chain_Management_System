# Auto_rice_mill_management_system

# for setting up virtual environment for mac

    python3 -m venv .venv
# for windows
    py -3 -m venv .venv

# for activate path for mac

    source .venv/bin/activate

# for Windows
    
    .venv\scripts\activate

# for installing django framework

    pip install djangorestframework

# for starting django app

    python3 manage.py startapp "app_name"

## if change anything in database schema

    python3 manage.py makemigrations
### makemigrations- 
    create change and store in a file 
    
# for migrating default table for auth

    python3 manage.py migrate
### migrate - 
	apply the pending change created by makemigrations

# for creating super user

    python3 manage.py createsuperuser
    username:abdullah
    email:shakibrybmn@gmail.com
    pass:1234

# To run serve
    python3 manage.py runserver
   
# set static teplate urls
		STATICFILES_DIRS = [
    BASE_DIR / "static"
		]
# for templates
		'DIRS': [BASE_DIR / "templates"],
		
		
# define applicatins
	INSTALLED_APPS = [
    'home.apps.HomeConfig',
    ]
# set apps urls to project urls

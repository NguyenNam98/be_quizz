# Django Rest Framework 
***

## Prerequisites
- Python=>3.10
## How to start service api
1) Virtual Environment - Open a terminal and use the following command to create a virtual environment.
```
python -m venv venv
```
Now activate the virtual environment with the following command.
```
# windows machine
venv\Scripts\activate.bat

#mac/linux
source venv/bin/activate
```
2) install packages
Let's go ahead and install our project requirements. Add the following code to you terminal.

```
pip install -r requirements.txt
```
3) Create .env file by .env.template
4) Migrate database

```
python manage.py makemigrations
python manage.py migrate
```
5) Run service 

```
python manage.py runserver
```
### Create user
1) Supper user

```
python manage.py createsuperuser

```
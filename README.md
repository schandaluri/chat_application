## Chat Application

### functionality

* Can Add new user
* Can send one-to-one messages
* Can see old chats

## Setup

Create virtual python environment and activate

```shell script
    python3 -m venv venv
    source venv/bin/activate
```

Install pip requirements 

```shell script
    pip install -r requirements.txt
```

Migrate database

```shell script
    ./manage.py migrate
```

Create super user to access app

```shell script
    ./manage.py createsuperuser
```

Spin up application

```shell script
    ./manage.py runserver
```

Now you can access application at 8000 and login with superuser.

To create new users, click on users link in navbar, enter required info and click on save.


## Authentication
Application supports two types of authentications now.
* session based authentication
* Basic authentication - helpful for api testing

## APIS
 Swagger UI - /api/chat/
 
 * POST /messages/ - to create the message
 * GET /messages/{receiver}/ - to get the messages of a user
 * GET /messages/stats/ - to get the count of unread messages.
  It will check for new messages and wait until new messages are created. If 
  a new messages is intended to current user it will return response.
   If no new messages in 28 seconds, it will return empty response.


     
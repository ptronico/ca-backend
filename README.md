# ca-backend

[API-DOCS](API-DOCS.md) | [General assumptions and comments](Assumptions.md)

----

This backend software implements a simple REST API that allows users to post and retrieve their reviews. It was built with Django and Django REST Framework. The tests are powered by pytest framework.

----

### App setup

The following instructions will clone the repository, create a new virtual environment, install dependencies, run the migrations and prepare the app for running:

```console
$ git clone git@github.com:ptronico/ca-backend.git
$ cd ca-backend
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
$ cd src
$ python manage.py migrate
```

For simplicity we are running SQLite database.

### Running the tests

For running testing just run the `pytest` command in the source code `src` directory. For complete HTML coverage report you can optionally pass the `--cov-report=html` argument, as shown below:

```console
$ pytest --cov-report=html
```

### Data setup

You can optionally load fixture data for easy playing with the app. To do that run the following command:

```console
$ python manage.py loaddata ../fixture_data.json
```

For logging as `superuser` you can use the following credentials. By default, in the `dev` settings, REST Framework is set up for using `TokenAuthentication` and `SessionAuthentication`. That way you can go to all endpoints if logged as superuser.

```
Username: superuser
Password: 12345
```

### Running the app

```console
$ python manage.py runserver
```

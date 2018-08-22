## Flask Bootstrap
This is a model project to bootstrap and advanced flask application. If tries as much as it can to avoid
`cyclic redundancy` and the `factory method` that is popular amongst Flask developers.

## bootstrap.py
* The file [bootstrap.py](modelate/bootstrap.py) ensures that *all necessary environment variables* are
present before the application can start up!
* If you want to add any extra environment variable and have it validated, do so within the file
[bootstrap.py](modelate/bootstrap.py).

## config.py
* Some configurations for `flask_session`, `recaptcha`, `celery` and `redis` can be found within the
[config.py](modelate/config.py). Do adjust it to taste.

## Good to know: Variables
Some variables are explained while it is assumed that you would understand the other variables by
their names.
* `SITE_NAME`: The name for your site. It will come in handy if you scale your application and want to know
the application that is currently serving request. You can always call this from within
* `MODELATE_STATUS`: Status of the site: `development`, `live` or `test`. Only one can be
chosen at any particular time.
* `SECRET_KEY`: The application's secret key
* `DB_TYPE`: `POSTGRES` or `MYSQL`

## Database of Choice
Your application can work with either Postgres or MySQL. You can do all the settings within the
[bootstrap.py](modelate/bootstrap.py) and [config.py](modelate/config.py).

However, when it comes to the design of your main application, you would have to choose one of the DBs and work
with it. This should reflect in your DB schema et al. However, Postgres was used as the DB of choice in preparing
this application.

> Note the following DB practises.
    
* It will not be a bad idea if you back up your live DB data and use them during development.
* Use only *alphanumberic* characters for your DB username and passwords!
* If you have a foreign key in Postgres, index the foreign key.

## Design Principles
* Th application can be used for both `API development` and `Web applications`
* `wsgi.py` file was added so that you could easily do the following:
    - `flask run` and have the application running on the development environment
    - `flask db --help` and have the migrations sorted out. But then, I do not advise using this method for
the migration.
The section, *migrations*, will properly explain this part
* The library *webob* will be used in some parts for testing purpose.

## During development
The following have been prepared as default:
* A Mac was used during development while the production environment was Ubuntu. You might need to alter some variables
for this application to work on Windows!
* Alter the [variables.sh](bash/dev/variables.sh) to taste
* Change your the `/Users/chukwudinwachukwu/PycharmProjects/modplate`, as contained in the bash files to taste
* Remember to run `chmod +x ...` on the bash files on your local PC
* A bash folder contains some bash scripts that you can work with to bootstrap the necessary variables et al.

## Steps to run this application
1. `git clone https://ichux@bitbucket.org/ichux/flask-bootstrap.git`
2. Create a virtual environment
    - activate it
    - *cd* into the cloned repository, `cd flask-bootstrap`
    - run ```pip install -r requirements.txt```
3. Properly set your variables within [variables.sh](bash/dev/variables.sh) to taste.
4. `source bash/dev/bootstrap.sh`
5. `flask run`

## Migrations
* [manage.py](./manage.py) allows you to run the following
    - ```python manage.py dbi```
    - ```python manage.py dbm```
    - ```python manage.py dbr```
    - ```python manage.py dbu_sql```
    - ```python manage.py dbu_no_sql```
* For best results with `alembic/flask-migrate`, use only *alphanumberic* characters for your DB username and passwords!
* You can alter the [manage.py](./manage.py) file to taste.
* The initial assumption will have you to have migrations that are easy to follow through, e.g. serial numbering
* When you need to make your own `sql statements` or `revisions`, use `python manage.py dbr`

## To run tests
* Stay within the directory that houses the `modelate` folder and type the following:
* run `source bash/dev/reset.sh`
* then run `python -m unittest discover -s tests/`

> Note
* It will be a good practise if you used the same type of DB for your development, test or live. This will ensure that
you can replicate problems, if need be.
* Variables for test come within the file [variables.sh](bash/test/variables.sh)
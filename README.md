## Modelate: Flask Bootstrapping Application
This is a model project to bootstrap any flask application: advanced or not. If tries as much as it can to avoid
`cyclic redundancy` and the `factory method` that is popular among Flask developers.

`modelate` == `MODEL templATE`

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
[config.py](modelate/config.py).

However, when it comes to the design of your main application, you would have to choose one of the DBs and work
with it. This should reflect in your DB schema et al. However, Postgres was used as the DB of choice in preparing
this application.

> Note the following DB practises.

* Use only *alphanumeric* characters for your DB username and passwords!
* If you have a foreign key in Postgres, index the foreign key.

## Design Principles
* The application can be used for both `API development` and `Web applications`
* `wsgi.py` file was added so that you could easily do the following:
    - `flask run` and have the application running on the development environment
    - `flask db --help` and have the migrations sorted out.

## Steps to run this application
1. Ensure you have docker/docker-compose installed on your OS of choice
2. `git clone https://ichux@bitbucket.org/ichux/modelate.git`
3. Type `make` and choose from the options it displays to bootstrap your application

## Migrations
* For best results with `alembic/flask-migrate`, use only *alphanumberic* characters for your DB username and passwords!
* Your migration might not work if you already have tables in the DB from a previous migration that also appears in your
present migration

> After you add a model, `import it` within the [__init__.py](modelate/__init__.py) and then run your migration(s).

## Alembic
* [Learn more](http://alembic.zzzcomputing.com/en/latest/ops.html)
* [Limitations](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)
* By default, alembic does not track column type changes. But you can achieve this by setting
`compare_type=True` in `env.py`. e.g.

```
context.configure(connection=connection,
                      target_metadata=target_metadata,
                      process_revision_directives=process_revision_directives,
                      compare_type=True,  # add this line
                      **current_app.extensions['migrate'].configure_args)
```

## To run tests
* run `make tests`

> Note
* It will be a good practise if you used the same type of DB for your development, test or live. This will ensure that
you can replicate problems, if need be.

## Tidbits
Check out [tidbits.txt](./tidbits.txt) for extra information that could come in handy for you when you code.


****
MIT © [ichux](https://www.linkedin.com/in/ichux)
****
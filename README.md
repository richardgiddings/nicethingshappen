# README

Nice things happen every day. Why not share them with others? A site to share these nice things with others. The site can be seen at https://www.nicethingshappen.co.uk/

![Alt text](site.png?raw=true "site")

Currently tested on Django 2.0.4. Django-rq and Redis are used for email queueing and PostgreSQL for the database. The site is currently setup to deploy to Heroku with a Procfile. To use with Heroku you currently need the Heroku Postgres and Redis to Go add-ons. 

There is some gibberish detection used for when a NiceThing is added to reject random character presses. This uses https://github.com/rrenaud/Gibberish-Detector 

The following configuration variables are also needed on Heroku:

For email:
* ADMIN_EMAIL
* ADMIN_NAME
* DEFAULT_FROM_EMAIL
* EMAIL_HOST
* EMAIL_HOST_PASSWORD
* EMAIL_HOST_USER
* EMAIL_PORT

and:
* SECRET_KEY
* DJANGO_SETTINGS_MODULE (nicethingshappen.settings.production)


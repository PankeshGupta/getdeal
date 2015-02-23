# getdeal

## Running

1. Install redis. (see [redis](redis.io/download))
3. Install git `sudo apt-get install git`
4. Clone the repository `getdeal`

## Development

This tutorial shows the steps to run the project localy on a ubuntu machine.

1. Initialize and activate a virtual environment (see [virtualenv](http://virtualenv.org))
2. Install required dependencies (see `requirement` subdirectory) 
   Example: `pip install -r <type>.txt` (for this case type == developements)
3. Change into subdirectory `settings`, and copy `local_template.py` to `local.py`, and make sure that the following environment variables are defined:

  * **name_db** DB name
  * **user_db** DB user
  * **pass_db** DB user password
  * **email configuration** To use gmail, just update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`. If you intend to use another provider, you need to check their configuration page.


  Optional settings:

    + **SECRET_KEY** you need to generate a new unique secret key for the project.

4. Running locally
    `pyhton manage.py syncdb`
    `pyhton manage.py migrate`
    `python manage.py runserver`
   

## Scrapy

In order to run scrapy, you need both celery daemon and scrapy daemon runing.


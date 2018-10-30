https://flask-migrate.readthedocs.io/en/latest/
http://flask-sqlalchemy.pocoo.org/2.3/quickstart/
https://docs.sqlalchemy.org/en/latest/core/


cd app
python3 -m venv venv
. venv/bin/activate

export FLASK_ENV=development
flask run
pip install wheel
install pip
install flask
install flup - for fcgi server
install - server uwsgi


python app.py
uwsgi --socket 0.0.0.0:9000 --protocol=http -w wsgi:app

psql "dbname=flaskapp host=ab user=admin password=root port=5432"

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')


$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py db --help
from flaskext.mysql import MySQL
from decouple import config

mysql = MySQL()

def configure_mysql(app):
    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = config('MYSQL_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = config('MYSQL_PASSWORD')
    app.config['MYSQL_DATABASE_DB'] = config('MYSQL_DB')
    app.config['MYSQL_DATABASE_HOST'] = config('MYSQL_HOST')
    mysql.init_app(app)

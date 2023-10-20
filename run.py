from app import app
from db import configure_mysql

if __name__ == "__main__":
    configure_mysql(app)
    app.run(debug=True)

from app import app
from app.utils.DB import DBB


if __name__ == "__main__":

    DBB.connect()
    app.run(debug=True)



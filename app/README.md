# App

This folder contains the code for the app, which is hosted on Heroku [here](https://rnsportalv2.herokuapp.com/ "Website").

To run locally you need to clone this repository.

`git clone https://github.com/chaiboub23/schedule-website.git`

Then go into the app folder.

`cd app`

Then install the following modules with `pip`:
* Flask==1.1.2
* Flask-Cors==3.0.10
* gunicorn==20.1.0
* icalendar==4.0.7
* python-dateutil==2.8.1
* pytz==2021.1

Then go to root folder

`cd ..`

Then create a file called `wsgi.py`.

`touch wsgi.py`

Then copy the following code into the file

```python
from app.main import app

if __name__ == "__main__":
    app.run()
```

Then run with Flask

`flask run`

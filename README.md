# Dive-Music Company Management Project
The Dive-Music Company Management Project models a company that is responsible for creating songs and managing and assigning musicians to those songs. 

This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.  
## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

- Variable and function names are clear.
- Endpoints are logically named.
- Code is commented appropriately.
- Secrets are stored as environment variables.

### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM I'll use handle the lightweight sqlite database. I'll primarily work in app.py and can reference models.py.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension I'll use to handle cross origin requests from my frontend server.
- [Auth0](https://auth0.com/docs/) is the authentication and authorization system I'll use to handle users with different roles with more secure and easy ways
- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.
- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment

### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.
#### Database Setup

With Postgres running, In terminal run:

```
createdb divebeapp
```

#### Running Tests

To run the tests, run
  
```dropdb divebeapp_test
createdb divebeapp_test
python test_app.py  
```

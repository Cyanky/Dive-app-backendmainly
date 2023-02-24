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

#### Auth0 Setup

You need to setup an Auth0 account.

Environment variables needed: (setup.sh)

```
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Your AUTHO_DOMAIN in your auth0 account
export ALGORITHMS="RS256"
export API_AUDIENCE="xxxxx" # Your API_AUDIENCE set in your auth0 account
```

##### Roles

Create three roles for users under `Users & Roles` section in Auth0

- Musician agency
  - Can view musicians
  - Add or delete a musician from the database
  - Modify musicians
- Song producer
  - Can view musicians and songs
  - Add or delete a song from the database
  - Modify songs, assign musicians to the songs

##### Permissions

Following permissions should be created under created API settings.

- `get:musicians`

- `get:songs`

- `delete:musicians`

- `delete:songs`

- `post:musicians`

- `post:songs`

- `patch:musicians`

- `patch:songs`

  

##### Set JWT Tokens in `auth_config.json`

Use the following link to create users and sign them in. This way, you can generate

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

#### Launching The App

1. Initialize and activate a virtualenv:

   ```
   python3 -m venv env
   source env/bin/activate
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure database path to connect local postgres database in `models.py`

   ```
   database_path = "postgres://{}/{}".format('localhost:5432', 'capstone')
   ```

**Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```

For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

1. Setup the environment variables for Auth0 under `setup.sh` running:

   ```
   source ./setup.sh 
   ```

2. To run the server locally, execute:

   ```
   export FLASK_APP=flaskr
   export FLASK_DEBUG=True
   export FLASK_ENVIRONMENT=debug
   flask run --reload
   ```

## API Documentation

### Models

There are two models:

- Musician
  - name
  - e_mail
  - phone
  - websit
  - introduction
  - avatar_link
  - genres
  - songs
- Song
  - name
  - introduction
  - cover_link
  - song_link
  - genre
  - musician_id

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}, 400
```

The API will return three error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable

### Unittest Example
```
 #  Test routes with method ['PATCHE''DELETE']
    # ------------------------------------------------------------

    def test_update_song_for_Song_Producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().patch("/songs/5", json={"cover_link":"sjkdlfjlkjwoeiur"}, headers=header_obj)
        data = json.loads(res.data)
        song = Song.query.filter(Song.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(song.format()["cover_link"], "sjkdlfjlkjwoeiur")

    def test_400_for_failed_update_song(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().patch("/songs/5", headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")
```

### Endpoints

*** Postman is recommended to be used to check these endpoints

#### GET /musician

- Get all musicians

- Require `get:musicians` permission

### Endpoints

*** All can be successfully checked in Postman

#### GET /musician

- Get all musicians

- Require `get:musicians` permission

- **Example Request:** `curl 'http://localhost:5000/musicians'`

- **Expected Result:**

  ```
  {
      "musicians": [
          {
              "avatar_link": "sjdklfjwioeuro",
              "e_mail": "1234@ss.com",
              "genres": "R&B",
              "id": 1,
              "introduction": "sdf",
              "name": "Cyanky",
              "phone": "123",
              "songs": [
                  {
                      "cover_link": "pzxlkcjlvawef",
                      "genre": null,
                      "id": 1,
                      "introduction": "ererere",
                      "musician_id": 1,
                      "name": "DIVE",
                      "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
                  }
              ],
              "website": "http://22.com"
          }
      ],
      "success": true,
      "total_musicians": 1
  }
  ```

#### GET /musician/int:musician_id

- Get specific musician with unique musician id

- Require `get:musicians` permission

- **Example Request:** `curl 'http://localhost:5000/musicians/1'`

- **Expected Result:**

  ```
  {
      "musicians": {
          "avatar_link": "sjdklfjwioeuro",
          "e_mail": "1234@ss.com",
          "genres": "R&B",
          "id": 1,
          "introduction": "sdf",
          "name": "Cyanky",
          "phone": "123",
          "songs": [
              {
                  "cover_link": "pzxlkcjlvawef",
                  "genre": null,
                  "id": 1,
                  "introduction": "ererere",
                  "musician_id": 1,
                  "name": "DIVE",
                  "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
              }
          ],
          "website": "http://22.com"
      },
      "success": true
  }
  ```

#### GET /songs

- Get all song
- Requires `get:songs` permission
- **Expected Result:**

```
{
    "songs": [
        {
            "cover_link": "pzxlkcjlvawef",
            "genre": null,
            "id": 1,
            "introduction": "ererere",
            "musician_id": 1,
            "name": "DIVE",
            "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
        }
    ],
    "success": true,
    "total_songs": 1
}
```

#### POST /musicians

- Creates a new musician.

- Requires `post:musicians` permission

- Requires the name.

- **Example JSON Body:** 

  ```
  {
              "name": "Jingchen Xie",
              "e_mail": "qpoweiru@sdhfl.com",
              "phone": "3849302908",
              "website": "https://cyanky.github.io/",
              "introduction": "She's coming now!",
              "avatar_link": "jskldfjoeuojsfdjkl",
              "genres": "R&B"
  }
  ```

- **Example Response:**

  ```
  {
      "created": 2,
      "musicians": [
          {
              "avatar_link": "sjdklfjwioeuro",
              "e_mail": "1234@ss.com",
              "genres": "R&B",
              "id": 1,
              "introduction": "sdf",
              "name": "Cyanky",
              "phone": "123",
              "songs": [
                  {
                      "cover_link": "pzxlkcjlvawef",
                      "genre": null,
                      "id": 1,
                      "introduction": "ererere",
                      "musician_id": 1,
                      "name": "DIVE",
                      "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
                  }
              ],
              "website": "http://22.com"
          },
          {
              "avatar_link": "jskldfjoeuojsfdjkl",
              "e_mail": "qpoweiru@sdhfl.com",
              "genres": "R&B",
              "id": 2,
              "introduction": "She's coming now!",
              "name": "Jingchen Xie",
              "phone": "3849302908",
              "songs": [],
              "website": "https://cyanky.github.io/"
          }
      ],
      "success": true,
      "total_musicians": 2
  }
  ```

#### POST /songs

- Creates a new song.
- Requires `post:songs` permission
- Requires the name and the song link. ** check the musician id to assign the song to an existing musician. 
- **Example JSON Body:** 

```
{
            "name": "Get up",
            "introduction": "to the top",
            "cover_link": "woeiruojwl",
            "song_link": "https://cyanky.github.io/",
            "genre": "R&B",
            "musician_id": 10
}
```

- **Example Response:**

```
{
    "created": 3,
    "songs": [
        {
            "cover_link": "pzxlkcjlvawef",
            "genre": null,
            "id": 1,
            "introduction": "ererere",
            "musician_id": 1,
            "name": "DIVE",
            "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
        }
    ],
    "success": true,
    "total_songs": 2
}
```

#### PATCH /musicians/int:musicians_id

- Edit an existing musician.

- Requires `patch:musicians` permission

- **Example JSON Body:** 

  ```
  {
              "e_mail": "werpiop@sser.com"
  }
  ```

- **Example Response:** 

  ```
  {
      "success": true,
      "updated": {
          "avatar_link": "jskldfjoeuojsfdjkl",
          "e_mail": "werpiop@sser.com",
          "genres": "R&B",
          "id": 2,
          "introduction": "She's coming now!",
          "name": "Jingchen Xie",
          "phone": "3849302908",
          "songs": [],
          "website": "https://cyanky.github.io/"
      }
  }
  ```

#### PATCH /songs/int:songs_id

- Edit an existing song.
- Requires `patch:songs` permission
- **Example JSON Body:** 

```
{
            "name": "Get up",
            "introduction": "to the top",
            "cover_link": "woeiruojwl",
            "song_link": "https://cyanky.github.io/",
            "genre": "R&B",
            "musician_id": 2
        }
```

- **Example Response:** 

```
{
    "success": true,
    "updated": {
        "cover_link": "woeiruojwl",
        "genre": "R&B",
        "id": 3,
        "introduction": "to the top",
        "musician_id": 2,
        "name": "Get up",
        "song_link": "https://cyanky.github.io/"
    }
}
```

#### DELETE /musicians/int:musicians_id

- Delete a existing musician.
- Requires `delete:musicians` permission
- **Example Response:** 

```
{
    "deleted": 3,
    "musicians": [
        {
            "avatar_link": "sjdklfjwioeuro",
            "e_mail": "1234@ss.com",
            "genres": "R&B",
            "id": 1,
            "introduction": "sdf",
            "name": "Cyanky",
            "phone": "123",
            "songs": [
                {
                    "cover_link": "pzxlkcjlvawef",
                    "genre": null,
                    "id": 1,
                    "introduction": "ererere",
                    "musician_id": 1,
                    "name": "DIVE",
                    "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
                }
            ],
            "website": "http://22.com"
        },
        {
            "avatar_link": "jskldfjoeuojsfdjkl",
            "e_mail": "werpiop@sser.com",
            "genres": "R&B",
            "id": 2,
            "introduction": "She's coming now!",
            "name": "Jingchen Xie",
            "phone": "3849302908",
            "songs": [],
            "website": "https://cyanky.github.io/"
        }
    ],
    "success": true,
    "total_musicians": 2
}
```

#### DELETE /songs/int:songs_id

- Delete a existing song.
- Requires `delete:songs` permission
- **Example Response:** 

```
{
    "deleted": 3,
    "songs": [
        {
            "cover_link": "pzxlkcjlvawef",
            "genre": null,
            "id": 1,
            "introduction": "ererere",
            "musician_id": 1,
            "name": "DIVE",
            "song_link": "https://open.spotify.com/track/5w4q9Es264UdYYr2AjnPhU?si=988d1cf25bf24d05"
        }
    ],
    "success": true,
    "total_songs": 1
}
```


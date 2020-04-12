# Intro

The Casting Agency API supports a basic castic agency by allowing users to query the database for movies and actors. There are three different user roles (and related permissions), which are:
- Casting agent: Can view actors and movies.
- Casting director: Can view, add, modify, or delete actors; can view and modify movies.
- Executive producer: Can view, add, modify, or delete actors and movies. 

# Running the API [TODO]

API endpoints can be accessed via https://capstone-fsnd-varlese.herokuapp.com/

Auth0 information for endpoints that require authentication can be found in `setup.sh`.

# Running tests

To run the unittests, first CD into the Capstone folder and run the following command:
```
python -m agency.tests
```

# API Documentation

Errors
`401`
`403`
`404`
`422`

Note: all error handlers return a JSON object with the request status and error message.

401
- 401 error handler is returned when there is an issue with the authentication necessary for the action being requested. 
```
{
	"error": 401,
	"message": "Authentication error.",
	"success": false
}
```
403
- 403 error handler occurs when the requested action is not allowed, i.e. incorrect permissions.
```
{
	"error": 403,
	"message": "Forbidden.",
	"success": false
}
```
404
- 404 error handler occurs when a request resource cannot be found in the database, i.e. an actor with a nonexistent ID is requested.
```
{
	"error": 404,
	"message": "Item not found.",
	"success": false
}
```
422
- 422 error handler is returned when the request contains invalid arguments, i.e. a difficulty level that does not exist.
```
{
	"error": 422,
	"message": "Request could not be processed.",
	"success": false
}
```

Endpoints
`GET '/actors'`
`GET '/movies'`
`POST '/add-actor'`
`POST '/add-movie'`
`PATCH '/actors/<int:actor_id>'`
`PATCH '/movies/<int:movie_id>'`
`DELETE '/actors/<int:actor_id>'`
`DELETE '/movies/<int:movie_id>'`

GET '/actors'
- Fetches a JSON object with a list of actors in the database.
- Request Arguments: None
- Returns: An object with a single key, actors, that contains multiple objects with a series of string key pairs.
```
{
    "actors": [
        {
            "age": "45",
            "gender": "male",
            "id": 1,
            "name": "Leonardo DiCaprio"
        },
        {
            "age": "42",
            "gender": "male",
            "id": 2,
            "name": "Jensen Ackles"
        },
        {
            "age": "70",
            "gender": "female",
            "id": 3,
            "name": "Meryl Streep"
        },
        {
            "age": "37",
            "gender": "female",
            "id": 4,
            "name": "Anne Hathaway"
        }
    ],
    "success": true
}
```
GET '/movies'
- Fetches a JSON object with a list of movies in the database.
- Request Arguments: None
- Returns: An object with a single key, movies, that contains multiple objects with a series of string key pairs.
```
{
    "movies": [
        {
            "id": 1,
            "release": "December 19, 1997",
            "title": "Titatic"
        },
        {
            "id": 3,
            "release": "January 16, 2009",
            "title": "My Bloody Valentine"
        },
        {
            "id": 4,
            "release": "May 23rd, 1980",
            "title": "The Shining"
        }
    ],
    "success": true
}
```
POST '/add-actor'
- Posts a new actor to the database, including the name, age, gender, and actor ID, which is automatically assigned upon insertion.
- Request Arguments: Requires three string arguments: name, age, gender.
- Returns: An actor object with the age, gender, actor ID, and name.

```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```
POST '/add-movie'
- Posts a new movie to the database, including the title, release, and movie ID, which is automatically assigned upon insertion.
- Request Arguments: Requires two string arguments: title, release.
- Returns: A movie object with the movie ID, release, and title.

```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```
PATCH '/actors/<int:actor_id>'
- Patches an existing actor in the database.
- Request arguments: Actor ID, included as a parameter following a forward slash (/), and the key to be updated passed into the body as a JSON object. For example, to update the age for '/actors/6'
```
{
	"age": "36"
}
```
- Returns: An actor object with the full body of the specified actor ID.
```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```
PATCH '/movies/<int:movie_id>'
- Patches an existing movie in the database.
- Request arguments: Movie ID, included as a parameter following a forward slash (/), and the key to be updated, passed into the body as a JSON object. For example, to update the age for '/movies/5'
```
{
	"release": "November 3, 2017"
}
```
- Returns: A movie object with the full body of the specified movie ID.
```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```
DELETE '/actors/<int:actor_id>'
- Deletes an actor in the database via the DELETE method and using the actor id.
- Request argument: Actor id, included as a parameter following a forward slash (/).
- Returns: ID for the deleted question and status code of the request.
```
{
	'id': 5,
	'success': true
}
```
DELETE '/movies/<int:movie_id>'
- Deletes a movie in the database via the DELETE method and using the movie id.
- Request argument: Movie id, included as a parameter following a forward slash (/).
- Returns: ID for the deleted question and status code of the request.
```
{
	'id': 5,
	'success': true
}
```
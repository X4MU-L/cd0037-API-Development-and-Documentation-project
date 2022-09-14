# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
	"1": "Science",
	"2": "Art",
	"3": "Geography",
	"4": "History",
	"5": "Entertainment",
	"6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API DOCUMENTATION

## ERROR HANDLING

Errors are presented in json format:

```
{
    'success': False,
    'error' : 404,
    'message': 'page not found'
}
```

The API will return These error messages when needed:
404:Resource not Found, 400: Bad Request, 422: not Processable, 403: Forbidden, 500: Server Error

## ENDPOINTS

### GET /categories

General:

    Returns a list of categories, success value
    Results are paginated in groups of 10.

Sample: `curl http://127.0.0.1:5000/categories`

```
    {
        "categories":
            {"1":"Science",
            "2":"Art",
            "3":"Geography",
            "4":"History",
            "5":"Entertainment",
            "6":"Sports"},
        "success":true
    }
```

### GET /questions?page=${int}'

General:

    Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    Arguments: page - integer
    Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

Sample: `curl http://127.0.0.1:5000/questions?page=1`

Return Body:

```
  {
     "category":
            { "1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"
            },
    "questions":
            [{ "answer":"Agra", "category":3, "difficulty":2, "id":1, "question":"The Taj Mahal is located in which Indian city?" }, {"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},{"answer":"Agra","category":3,"difficulty":2,"id":3,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":4,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},{"answer":"Agra","category":3,"difficulty":2,"id":6,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":7,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":8,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"}],
    "success":true,
    "total_querstions":23,
    "current_category": null

  }

```

## DELETE /questions/${int}

Sample:

```
  curl -X DELETE http://127.0.0.1:5000/questions/1

```

Response Body:

```
  {
    "success":true,
    "total_question":22,
    "deleted_id": 1
  }

```

## POST /questions

General:
Sends a post request in order to add a new question
Request Body:

```
  "{ 'question': 'Choose a versatile language', 'answer': 'python', 'category': 4, 'difficulty': 3 }"

`Sample: `
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"what is the most vesatile language", "answer":"python", "category":"4", "difficulty":"3"}'

```

Response Body:

```
  {
    "success":true,
    "created_id":24,
    "created_question":"what is the most vesatile language","questions":[
            {
              "answer":"Agra", "category":3, "difficulty":2, "id":1, "question":"The Taj Mahal is located in which Indian city?" }, {"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},{"answer":"Agra","category":3,"difficulty":2,"id":3,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":4,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},{"answer":"Agra","category":3,"difficulty":2,"id":6,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":7,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":8,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"
            }
          ],
    "total_questions":23
  }

```

## POST /questions

General:
Sends a post request in order to search for a specific question by search term
Request Body:
`"{ 'searchterm':'tom' }"`
Sample:

```
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"tom"}'

```

Response Body:

```
  {
    "current_category":null,
    "questions":
          [{
            "answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          }],
    "success":true,
    "total_questions":1
  }

```

## GET /categories/${int}/questions

General:

    Fetches questions for a cateogry specified by id request argument
    Request Arguments: id - integer
    Returns: An object with questions for the specified category, total questions, and current category string paginated in groups of 10.

Sample:

```
  curl http://127.0.0.1:5000/categories/3/questions

```

Return Body:

```
  {
    "category":"Geography",
    "questions":
            [
              {
                "answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa?"},{"answer":"The Palace of Versailles","category":3,"difficulty":3,"id":14,"question":"In which royal palace would you find the Hall of Mirrors?"},{"answer":"Agra","category":3,"difficulty":2,"id":15,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":1,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":2,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":3,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":4,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":5,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":6,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Agra","category":3,"difficulty":2,"id":7,"question":"The Taj Mahal is located in which Indian city?"
              }
            ],
    "success":true,
    "total_questions":12
  }

```

## POST /quizzes

General:

    Sends a post request in order to get the next question
    Request Body:
        ```
            {
                "questions": [10, 6, 17]
                'category': {
                    'id': 0,
                    'type': 'All'
                }
            }
        ```

Sample:
`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"category":{"type":"All","id":0}, "questions":[10, 6, 17]}'`

Response Body:

```
  {
    "question":
              {
                "answer":"Jackson Pollock","category":2,"difficulty":2,"id":19,"question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
              },
    "success":true
  }

```

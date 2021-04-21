# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

ENDPOINTS

GET '/categories'
- Fetches:
    - Dictionary of categories where keys are ids and values are corresponding string of the category
- Request Arguments: None
- Returns an object with keys:
    - 'success': Success flag boolean
    - 'categories': Contains a object of id: category_string and key:value pairs. 
```

{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
GET '/questions'
- Fetches: 
    - Paginated (by 10) list of questions
    - Dictionary of categories
    - Total number of questions
    - Current category
- Request Arguments: 
    - 'page': Current page
- Returns an object with keys:
    - 'success': Success flag boolean
    - 'questions': Paginated (by 10) list of questions
    - 'total_questions': Total number of questions
    - 'categories': Dictionary of categories
    - 'current_category': The current category

DELETE '/questions/<int:question_id>' 
- Deletes question by question_id
- Request Arguments: 
    - 'question_id': Question's id
- Returns an object with keys:
    - 'success': Success flag boolean
    - 'deleted': Id of question deleted

POST '/questions'
- Create new question
- Request Arguments: 
    - 'question': Question
    - 'answer': Answer to question
    - 'difficulty': Question difficulty
    - 'category': Question category 
- Returns an object with keys:
    - 'success': Success flag boolean
    - 'created': Id of question created

POST '/search'
- Search for a question
- Request Arguments: 
    - 'search': Search term
- Returns: Object with keys:
    - 'success': Success flag boolean
    - 'questions': List of questions
    - 'total_questions': Total number of questions
    - 'current_category': Current category

GET '/categories/:category_id/questions'
- Fetches:
    - List of questions in a category
- Request Arguments: 
    - 'category_id': Category id
- Returns an object with keys:
    - 'success': Success flag boolean
    - 'questions': Paginated (by 10) list of questions
    - 'current_category': Current category

POST '/quizzes'
- Fetches:
    - One question for game play
- Request arguments:
    - 'quiz_category': Quiz category
    - 'previous_ids': Previous question ids
- Returns an object with keys:
    - 'success': Success flag boolean
    - 'question': Question for game play

ERRORS

ERROR 400
    - Returns:
    ```
    {
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }
    ```

ERROR 404
    - Returns:
    ```
    {
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }
    ```

ERROR 422
    - Returns:
    ```
    {
      'success': False, 
      'error': 422,
      'message': 'Unprocessable'
    }
    ```

ERROR 500
    - Returns:
    ```
    {
      'success': False, 
      'error': 500,
      'message': 'Internal server error'
    }
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
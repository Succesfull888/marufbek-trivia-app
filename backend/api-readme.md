# Full Stack API Final Project


## Full Stack Trivia

# Pre-requisites
Developers using this project should already have Python3, pip and node installed on their local machines.

# About app
Udacitrivia quiz game which can play,add, delete, search and category questions. It is very interactive.Whis is the part udacity full-stack nanodegree program.This project is task for students to create simple API.A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.
The code base is done by Udacity and I only added and filled the required code and functions to make this work.
## To run the project do the followings step by step
1.Open the project folder  (starter/)
2.Run it in terminal 
cd backend
# for Mac users  
python3 -m venv venv
source venv\bin\activate
# for Windows users
py -3 -m venv venv
venv\Scripts\activate

3.Install dependencies
From the backend folder run

pip3 install -r requirements.txt

4.Start/stop the PostgreSQL server
# Mac users
which postgres
postgres --version
# Start/stop
pg_ctl -D /usr/local/var/postgres start
pg_ctl -D /usr/local/var/postgres stop 

# Populate database 
open SQL SHELL or create database using psql in current terminal
>psql dropdb trivia
>psql createdb trivia
> psql -d trivia_test -U postgres -a -f trivia.psql
# windows users
*Find the database directory, it should be something like that: C:\Program Files\PostgreSQL\13\data
*Then, in the command line, execute the folllowing command

# Start the server
pg_ctl -D "C:\Program Files\PostgreSQL\13\data" start
# Stop the server
pg_ctl -D "C:\Program Files\PostgreSQL\13\data" stop

If it shows that the port already occupied error, run:
sudo su - 
ps -ef | grep postmaster | awk '{print $2}'
kill <PID> 

# in case if it doesn't work you can :
sudo -su kill PID

5.Type these commands
>set FLASK_APP=flaskr
>set FLASK_ENV=development
>flask run  
or
>py -3 -m flask run
http://127.0.0.1/5000
6.Type in your terminal 
> cd ..
>cd frontend
Make sure you have installed node.js before
>npm install
it takes a little time in some computers,less than minutes
>npm start

7.Finally it runs http://localhost:3000/   Close the terminal if you wish to stop the frontend server.

# ENDPOINTS DOCUMENTATION
One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



Endpoints created:
*1st Endpoind handles GET requests for questions , including pagination.It returns list of questions and the number of questions.It is paginated every 10questions
*2nd using GET request requests all categories
*3rd  Using question id DELETE the question
*4th POST new question by getting data from frontend question,answer,difficulty,category
*5th POST endpoint to get questions based on category.
*6th search questions using searchTerm
*7th  POST endpoint to get questions to play the quiz. This endpoint takes category and previous question parameters and returns a random questions within the given category, if provided, and that is not one of the previous questions.
  

# EROR Handling
the api will return following error types
404-'Not Found'
422-'Unprocessable'
400-'bad request'
500-'internal server'

GET '/questions'
Returns: A multiple key/value pairs object with the following structure:
success: can take values True or False deppending on the successfullnes of the endpoint's execution.
questions: contains a list of the fetched questions. Each question is a key/value pairs object containing id, question, category and diffficulty.
total_questions: the number of questions returned.
current_category: list of the categories of the returned questions list.
categories: dictionary of categories available in the database.

Ex:
{
  "categories": {
    "1": "Science"
  },
  "current_category": [
    1
  ],
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 5
}

DELETE '/questions/<int:question_id>'
Deletes the question selected by question_id.

{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
  ],
  "deleted": 3,
  "success": true,
  "total_questions": 17
}

POST '/questions'
posts new question
Request Arguments: a key/value pairs object whit the following content:
question: string containing the question itself.
answer: answer's string.
difficulty: difficulty level.
category: category ID field.

Ex:
{
    answer: "Nobody!"
    category: 4
    difficulty: 2
    question: "Who is the best?"
}

POST '/questions_search'
Returns a set of questions based on a search term.
Request Arguments:
searchTerm: string to search in questions string.

{
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 1
}

Get all questions from a category
curl http://127.0.0.1:5000/categories/2/questions
{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "It depends",
      "category": 1,
      "difficulty": 1,
      "id": 77,
      "question": "Can birds fly?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 5
}

>View the [README within ./frontend for more details.](./frontend/README.md)
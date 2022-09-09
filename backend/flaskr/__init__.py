import sys
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """ 

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


    #A PAGINATION FUNCTION
    PAGINATE_BY = 10
    def paginated_questions(request,selection):
        page = request.args.get("page",1,type=int)
        start = (page - 1) * PAGINATE_BY
        end = start + PAGINATE_BY
        formatted_questions = [question.format() for question in selection]
        return formatted_questions[start:end]
    """
    
    
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.type).all()
        if len(categories) == 0:
            abort(404)

        return jsonify({
            "success":True,
            "categories":{category.id : category.type for category in categories}
        })


 
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginated_questions(request,selection)
        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) ==0:
            abort(404)
        return jsonify({
            "success":True,
            "categories":{category.id : category.type for category in categories},
            "questions":current_questions,
            "total_questions":len(selection),
            "current_category": None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>",methods=["DELETE"])
    def delete_question(question_id):
        question_to_delete = Question.query.filter(Question.id == question_id).one_or_none()
        if question_to_delete is None:
            abort(404)
        try:
            question_to_delete.delete()
            selection = Question.query.order_by(Question.id).all()
        
            return jsonify({
            "success":True,
            "deleted_id":question_id,
            "total_questions":len(selection), 
        })
        except:
            abort(400)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        # currently have errors -- needs retesting
        body = request.get_json()
        if not body:
            abort(400)

        new_answer = body.get("answer")
        new_difficulty = body.get("difficulty")
        new_question = body.get("question")
        new_category = body.get("category")
        search_term = body.get("searchTerm")


        if search_term:
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = paginated_questions(request,selection)
            return jsonify({
                "success":True,
                "questions":current_questions,
                "total_questions":len(selection),
                "current_category": None
            })
        
        
        if (new_answer and new_difficulty and new_question and new_category):
            if type(( new_difficulty and new_category)) != int:
                    abort(422)

            try:
                # check if new_question and new_category is an int
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty)
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginated_questions(request,selection)
                
                return jsonify({
                    "success":True,
                    'created_id': question.id,
                    'created_question': question.question,
                    'questions': current_questions,
                    'total_questions': len(selection)
                })

            except:
                question.reverse()
                abort(500)
        else:
            abort(422)
      
                

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_by_category(category_id):
        
        category = Category.query.filter(Category.id == category_id).one_or_none()
        if category is None:
            abort(404)
        print(category)
        selection = Question.query.filter(Question.category == str(category.id)).order_by(Question.id).all()
        paginated = paginated_questions(request,selection)
        return jsonify({
                "success":True,
                "questions":paginated,
                "total_questions":len(selection),
                "current_category": category.type
            })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_trivia_quizzes():

        body = request.get_json()
        if not body:
            abort(400)

        try:
            previous_questions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")

            if quiz_category["id"] == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                            Question.id.notin_(previous_questions), 
                            Question.category == quiz_category["id"]).all()
                print(questions)
            question = None
            if(questions):
                question = random.choice(questions)
                return jsonify({
                    'success': True,
                    'question': question.format()
                })
            return jsonify({
                    'success': True,
                    'question': question
                })
            
        except:
            print(sys.exc_info())
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.

    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"Resorses not found",
            
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":422,
            "message":"unprocessable",
        }), 422

    
    @app.errorhandler(500)
    def not_modified(error):
        return jsonify({
            "success":False,
            "error":500,
            "message":"Internal Server error"
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success":False,
            "error":405,
            "message":"Method not allowed",
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success":False,
            "error":400,
            "message":"Bad Request",
        }), 400
    return app


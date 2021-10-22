import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categorry():
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        if (len(categories_dict) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'categories': categories_dict,
            'message': 'Done'
        })

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        total_questions = len(questions)
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        if (len(current_questions) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'message': 'Done',
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict
        })

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()
        if (category is None):
            abort(400)
        selection = Question.query.filter_by(category=category.id).all()
        paginated = paginate_questions(request, selection)
        data = {
            'success': True,
            'questions': paginated,
            'total_questions': len(Question.query.all()),
            'current_category': category.type}
        return jsonify(data)

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            if (len(questions) == 0):
                abort(404)
            paginated = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'message': 'Done',
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })
        else:
            question = body.get('question')
            answer = body.get('answer')
            difficulty = body.get('difficulty')
            category = body.get('category')
            if ((question is None)or(answer is None)
                    or(difficulty is None)or(category is None)):
                abort(422)
            try:
                question = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
                question.insert()
                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'message': 'Done',
                    'created': question.id,
                    'question_created': question.question,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                  })
            except Exception:
                abort(422)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
            if question == 0:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'message': 'Done',
                'deleted': question.id
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz_with_randomly_questions():
        body = request.get_json()
        previous_question = body.get('previous_questions')
        category = body.get('quiz_category')
        if ((category is None) or (previous_question == 0)):
            abort(400)
        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()
        total = len(questions)

        def random_quizzes():
            return questions[random.randrange(0, len(questions), 1)]

        def faced_quiz(question):
            used = False
            for id in previous_question:
                if (id == question.id):
                    used = True
            return used
        question = random_quizzes()
        while (faced_quiz(question)):
            question = random_quizzes()
            if (len(previous_question) == total):
                return jsonify({
                    'success':  True,
                    'message': 'Done'
                })
        return jsonify({
            'success': True,
            'question':  question.format(),
            'message': 'Done'
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found :-("
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "BAD request"
        }), 400
    return app
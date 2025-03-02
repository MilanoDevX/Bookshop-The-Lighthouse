"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Book, Author
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/users', methods=['GET'])
def get_all_users():
    user_list = User.query.all()
    serialized_users = [ item.serialize() for item in user_list ]
    return jsonify(serialized_users), 200


@api.route('/books', methods=['GET'])
def get_all_books():
    book_list = Book.query.all()
    serialized_books = [ item.serialize() for item in book_list ]
    return jsonify(serialized_books), 200


@api.route('/authors', methods=['GET'])
def get_all_authors():
    authors_list = Author.query.all()
    serialized_authors = [ item.serialize() for item in authors_list ]
    return jsonify(serialized_authors), 200


@api.route('/books/<int:id>', methods=['GET'])
def get_one_book(id):
    searched_book = Book.query.get(id) # Just by id, or None
    if searched_book != None:
        return jsonify(searched_book.serialize()), 200
    return jsonify({"error": "Book not found"}), 404


@api.route('/books', methods=['POST'])
def add_new_book():
    try:
        body = request.json
        title = body.get('title')
        author_id = body.get('author_id')

        if author_id == None: 
            return jsonify({ "error": "author_id is required" }), 400
        
        searched_author = Author.query.get(author_id)

        if searched_author == None:
            return jsonify({ "error": f"the author with id {author_id} is not found in the database" }), 404

        new_book = Book(title=title, author=searched_author)

        db.session.add(new_book) # adds it to RAM from server
        db.session.commit() # assigns an id to the new book, and stores it in SQL
        return jsonify(new_book.serialize()), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@api.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get(book_id)

    if book == None:
            return jsonify({ "error": f"the book with id {book_id} is not found in the database" }), 404
    
    db.session.delete(book)
    db.session.commit()

    return jsonify({ "msg": "Successful book deletion" }), 200




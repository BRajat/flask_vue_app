from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from data_model import Books

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'coding'

@app.before_first_request
def create_table():
    db.create_all()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/books', methods = ['GET'])
def get_books():
    books = Books.get_all_books()
    return jsonify({'books': Books.get_all_books()})

@app.route('/books', methods=['POST'])
def add_book():
    response_object = {'status':'success'}
    post_data = request.get_json()
    book = Books(post_data.get('title'),post_data.get('author'),post_data.get('read'))
    book.save_to_db()
    response_object['message'] = 'Book added!'    
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT'])
def update(book_id):
    response_object = {'status': 'success'}
    book = Books.find_by_id(book_id)
    if request.method == 'PUT':
        post_data = request.get_json()
        if book:
            for k,v in post_data.items():
                setattr(book,k,v)
        book.save_to_db()
        response_object['message'] = 'Book updated!'
    return jsonify(response_object)
    
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    response_object = {'status': 'success'}
    book = Books.find_by_id(book_id)
    if request.method == 'DELETE':
        book.delete_from_db()
        response_object['message'] = 'Book Removed!'
    return jsonify(response_object)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
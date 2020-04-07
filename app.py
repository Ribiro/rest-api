from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

books = [
    {
        'name': 'river between',
        'author': 'ngugi wa thiongo',
        'isbn': 12345
    },
    {
        'name': 'river and source',
        'author': 'margaret ogola',
        'isbn': 123
    }
]


@app.route('/books')
def get_books():
    return jsonify({'books': books})

# send a post request to add books to our books endpoint
# {
#     'name': 'new',
#     'author': 'ribiro',
#     'isbn': 1234567
# }


def valid_book_object(book_object):
    if "name" in book_object and "author" in book_object and "isbn" in book_object:
        return True
    else:
        return False

# add an new book
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        new_book = {
            'name': request_data['name'],
            'author': request_data['author'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalid_error_msg = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in similar to this { "name": "book name", "author": "author name", "isbn": 1234}'
        }
        response = Response(json.dumps(invalid_error_msg), 400, mimetype='application/json')
        return response

# update books using put
@app.route('/books/<int:isbn>', methods=['PUT'])
def update_books(isbn):
    request_data = request.get_json()

    if valid_book_object(request_data):
        new_book = {
            'name': request_data['name'],
            'author': request_data['author'],
            'isbn': isbn
        }
        i = 0
        for book in books:
            current_isbn = book['isbn']
            if current_isbn == isbn:
                books[i] = new_book
            i += 1
        response = Response("", status=204)
        return response
    else:
        invalid_error_msg = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in similar to this { "name": "book name", "author": "author name", "isbn": 1234}'
        }
        response = Response(json.dumps(invalid_error_msg), 400, mimetype='application/json')
        return response

# update by patch
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "name" in request_data:
        updated_book['name'] = request_data['name']
    if "author" in request_data:
        updated_book['author'] = request_data['author']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response

# get book by isbn
@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book["name"],
                'author': book["author"]
            }
    return jsonify(return_value)


# delete http route
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalid_isbn = {
        "error": "isbn not found"
    }
    response = Response(json.dumps(invalid_isbn), status=404, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run()

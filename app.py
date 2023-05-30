# from flask import Flask, request, jsonify
# import firebase_admin
# from firebase_admin import credentials, firestore
# import os

# # Initialize Firebase App
# cred = credentials.Certificate('key.json')
# firebase_admin.initialize_app(cred)

# # Initialize Firestore DB clientt
# db = firestore.client()

# app = Flask(__name__)

# # Create a new item
# @app.route('/add_doc', methods=['POST'])
# def create_item():
#     try:
#         data = request.get_json()
#         item_ref = db.collection(request.headers.get('Collection-Name')).document()
#         item_ref.set(data)
#         return jsonify({"status" : 200, "id" : item_ref.id})
#     except Exception as e:
#         print(e)
#         return f"An Error Occurred: {e}"
    
    

# # Get all items
# @app.route('/items', methods=['GET'])
# def get_items():
#     items = []
#     for doc in db.collection(request.headers.get('Collection-Name')).stream():
#         items.append(doc.to_dict())
#     return jsonify(items)

# # Get a single item by ID
# @app.route('/items/<item_id>', methods=['GET'])
# def get_item(item_id):
#     doc = db.collection(request.headers.get('Collection-Name')).document(item_id).get()
#     if doc.exists:
#         return jsonify(doc.to_dict())
#     else:
#         return jsonify({'error': 'Item not found'}), 404

# # Get a single ite by search field value
# @app.route('/search/<field>/<value>')
# def search_document(field, value):
#     doc = db.collection(request.headers.get('Collection-Name')).where(field, '==', value).limit(1).get()
#     if len(doc) > 0:
#         document = doc[0]
#         return jsonify(document.to_dict())
#     else:
#         return jsonify({'message': 'No matching document found.'})
    
# # Update an existing item
# @app.route('/items/<item_id>', methods=['PUT'])
# def update_item(item_id):
#     data = request.json
#     item_ref = db.collection(request.headers.get('Collection-Name')).document(item_id)
#     item_ref.update(data)
#     return jsonify({'message': 'Item updated successfully'})

# # Delete an item
# @app.route('/items/<item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     db.collection(request.headers.get('Collection-Name')).document(item_id).delete()
#     return jsonify({'message': 'Item deleted successfully'})


#     # Return the matching documents as JSON response
#     return jsonify(matching_documents)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase App
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB clientt
db = firestore.client()

app = Flask(__name__)

# Create a new item
@app.route('/add_doc/<uid>', methods=['POST'])
def create_item_by_id(uid):
    try:
        data = request.get_json()
        item_ref = db.collection(request.headers.get('Collection-Name')).document(uid)
        item_ref.set(data)
        return jsonify({"status" : 200, "id" : item_ref.id})
    except Exception as e:
        print(e)
        return f"An Error Occurred: {e}"
    
@app.route('/add_doc', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        item_ref = db.collection(request.headers.get('Collection-Name')).document()
        item_ref.set(data)
        return jsonify({"status" : 200, "id" : item_ref.id})
    except Exception as e:
        print(e)
        return f"An Error Occurred: {e}"

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for doc in db.collection(request.headers.get('Collection-Name')).stream():
        items.append(doc.to_dict())
    return jsonify(items)

# Get filtered items
@app.route('/items_filter', methods=['GET'])
def get_items_filters():
    items = []
    for uid_key, uid in request.args.items():
        print(uid)
        doc = db.collection(request.headers.get('Collection-Name')).document(uid).get()
        items.append(doc.to_dict())
    print(items)
    return jsonify(items)

# Get a single item by ID
@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    doc = db.collection(request.headers.get('Collection-Name')).document(item_id).get()
    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({'error': 'Item not found'}), 404

# Get a single item by search field value
@app.route('/search/<field>/<value>')
def search_document(field, value):
    doc = db.collection(request.headers.get('Collection-Name')).where(field, '==', value).limit(1).get()
    if len(doc) > 0:
        document = doc[0]
        return jsonify(document.to_dict())
    else:
        return jsonify({'message': 'No matching document found.'})

# Get documents by multiple field values
@app.route('/search_multiple')
def search_documents_multiple():
    collection_name = request.headers.get('Collection-Name')
    query = db.collection(collection_name)
    
    # Iterate over the query parameters and apply filters
    for key, value in request.args.items():
        query = query.where(key, '==', value)
    
    docs = query.get()
    
    if len(docs) > 0:
        documents = [doc.to_dict() for doc in docs]
        return jsonify(documents)
    else:
        return jsonify({'message': 'No matching documents found.'})

# Get documents by multiple field values
@app.route('/search_multiple/<startPrice>/<endPrice>')
def search_documents_multiple2(startPrice, endPrice):
    collection_name = request.headers.get('Collection-Name')
    query = db.collection(collection_name)
    
    # Iterate over the query parameters and apply filters
    for key, value in request.args.items():
        query = query.where(key, '==', value)
    docs = query.get()
    
    if len(docs) > 0:
        # documents = [doc.to_dict() for doc in docs]
        documents = [doc.to_dict() for doc in docs if doc.to_dict().get('price', 0) <= float(endPrice) and doc.to_dict().get('price', 0) >= float(startPrice)]

        return jsonify(documents)
    else:
        return jsonify([])

# Get a list of items item by search if field contains some value
@app.route('/search_contain/<field>/<value>')

def search_documents(field, value):
    docs = db.collection(request.headers.get('Collection-Name')).where(field, '>=', value).where(field, '<=', value + u'\uf8ff').get()
    if len(docs) > 0:
        documents = [doc.to_dict() for doc in docs]
        return jsonify(documents)
    else:
        return jsonify([])

# Update an existing item
@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item_ref = db.collection(request.headers.get('Collection-Name')).document(item_id)
    item_ref.update(data)
    return jsonify({'message': 'Item updated successfully'})

# update an item
@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    db.collection(request.headers.get('Collection-Name')).document(item_id).delete()
    return jsonify({'message': 'Item deleted successfully'})

# update an array field - delete an item from the array
@app.route('/delete_from_array/<item_id>', methods=['PUT'])
def delete_item_from_array(item_id):
    collection_name = request.headers.get('Collection-Name')
    field_name = request.args.get('field')
    element_to_delete = request.args.get('element')

    # Delete the element from the array field
    db.collection(collection_name).document(item_id).update({
        field_name: firestore.ArrayRemove([element_to_delete])
    })

    return jsonify({'message': 'Item deleted successfully'})

@app.route('/add_to_array/<item_id>', methods=['PUT'])
def add_element_to_array(item_id):
    collection_name = request.headers.get('Collection-Name')
    field_name = request.args.get('field')
    element_to_add = request.args.get('element')

    # Add the element to the array field
    db.collection(collection_name).document(item_id).update({
        field_name: firestore.ArrayUnion([element_to_add])
    })

    return jsonify({'message': 'Element added successfully'})


    # Return the matching documents as JSON response
    return jsonify(matching_documents)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
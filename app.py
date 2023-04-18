from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase App
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB client
db = firestore.client()

app = Flask(__name__)

# Create a new item
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

# Get a single item by ID
@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    doc = db.collection(request.headers.get('Collection-Name')).document(item_id).get()
    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({'error': 'Item not found'}), 404

# Update an existing item
@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item_ref = db.collection(request.headers.get('Collection-Name')).document(item_id)
    item_ref.update(data)
    return jsonify({'message': 'Item updated successfully'})

# Delete an item
@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    db.collection(request.headers.get('Collection-Name')).document(item_id).delete()
    return jsonify({'message': 'Item deleted successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

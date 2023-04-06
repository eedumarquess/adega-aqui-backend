from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)

@app.route('/items', methods=['GET'])
def get_all_items():
  all_items = {}
  for key in r.scan_iter():
    data = r.hgetall(key)
    decoded_data = {}
    for k, v in data.items():
        decoded_data[k.decode()] = v.decode()
    all_items[key.decode()] = decoded_data
  return jsonify(all_items)

@app.route('/item/<id>', methods=['GET'])
def get_item(id):
  data = r.hgetall(id.encode('utf-8'))
  decoded_data = {}
  for key, value in data.items():
      decoded_data[key.decode()] = value.decode()
  return jsonify(decoded_data)

@app.route('/items', methods=['POST'])
def create_item():
  id = request.json['id']
  data = request.json['data']
  r.hmset(id, data)
  return jsonify({'message': 'Item created successfully!'})

@app.route('/item/<id>', methods=['PATCH'])
def update_item(id):
  data = request.json['data']
  r.hmset(id, data)
  return jsonify({'message': 'Item updated successfully!'})

@app.route('/item/<id>', methods=['DELETE'])
def delete_item(id):
  r.delete(id)
  return jsonify({'message': 'Item deleted successfully!'})

if __name__ == '__main__':
  app.run(debug=True)
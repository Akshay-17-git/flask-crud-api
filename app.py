from flask import Flask, jsonify, request, abort

app = Flask(__name__)

items = [
    {"id": 1, "name": "Item A"},
    {"id": 2, "name": "Item B"}
]

def find_item(i):
    return next((it for it in items if it["id"] == i), None)

@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(items)

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    it = find_item(item_id)
    if not it:
        abort(404)
    return jsonify(it)

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name required"}), 400
    new_id = max(i["id"] for i in items) + 1 if items else 1
    it = {"id": new_id, "name": name}
    items.append(it)
    return jsonify(it), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    it = find_item(item_id)
    if not it:
        abort(404)
    data = request.get_json() or {}
    it["name"] = data.get("name", it["name"])
    return jsonify(it)

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    it = find_item(item_id)
    if not it:
        abort(404)
    items.remove(it)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)

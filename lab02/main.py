import os
import uuid
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

products = []
next_id = 1

UPLOAD_FOLDER = "icons"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/product", methods=["POST"])
def add_product():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data"}), 400

    if "name" not in data:
        return jsonify({"error": "No name"}), 400
    
    if "description" not in data:
        return jsonify({"error": "No description"}), 400

    product = {
        "id": next_id,
        "name": data["name"],
        "description": data["description"],
        "icon": None,
    }

    products.append(product)
    next_id += 1

    return jsonify(product), 201


@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return jsonify({"error": "No product"}), 404

    return jsonify(product)


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/product/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return jsonify({"error": "No product"}), 404

    if "name" in data:
        product["name"] = data["name"]

    if "description" in data:
        product["description"] = data["description"]

    if "icon" in data:
        product["icon"] = data["icon"]

    return jsonify(product)


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    global products

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return jsonify({"error": "No product"}), 404

    products = [p for p in products if p["id"] != product_id]

    return jsonify(product)


@app.route("/product/<int:product_id>/image", methods=["POST"])
def upload_icon(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    data = request.get_json()

    if not product:
        return jsonify({"error": "No product"}), 404
    
    if "icon" not in data:
        return jsonify({"error": "No icon"}), 400
    
    icon = data["icon"]

    if not icon:
        return jsonify({"error": "No icon"}), 400
    
    product["icon"] = icon

    return jsonify(product)


@app.route("/product/<int:product_id>/image", methods=["GET"])
def get_icon(product_id):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return jsonify({"error": "No product"}), 404

    if not product.get("icon"):
        return jsonify({"error": "No icon"}), 404

    return send_from_directory(
        UPLOAD_FOLDER,
        product["icon"]
    )


if __name__ == "__main__":
    app.run(debug=True)
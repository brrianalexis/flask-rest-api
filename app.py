import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init
app = Flask(__name__)

# Example
# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({'msg': 'Hello, world 😄'})

basedir = os.path.abspath(os.path.dirname(__file__))
# DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB
db = SQLAlchemy(app)
# Init Marshmallow
ma = Marshmallow(app)


class Product(db.Model):
    """Product class"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class ProductSchema(ma.Schema):
    """Product schema"""

    class Meta:
        """Fields of the Product schema"""

        fields = ("id", "name", "description", "price", "quantity")


# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Routes


@app.route("/products", methods=["POST"])
def add_product():
    """Adds a new product to the DB"""
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    new_product = Product(name, description, price, quantity)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route("/products", methods=["GET"])
def get_products():
    """Gets all products from the DB"""
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result)


@app.route("/products/<id>", methods=["GET"])
def get_one_product(id):
    """Gets one product from the DB"""
    product = Product.query.get(id)

    return product_schema.jsonify(product)


@app.route("/products/<id>", methods=["PUT"])
def update_one_product(id):
    """Updates a product from the DB"""
    product = Product.query.get(id)

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)


@app.route("/products/<id>", methods=["DELETE"])
def delete_one_product(id):
    """Deletes one product from the DB"""
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run server
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/db'
app.config['JWT_SECRET_KEY'] = 'adkewla;sldkgkdsa;ejglaskejgaset'
db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- Моделі ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='client')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.Column(db.String(200))


# --- Інваріанти ---
def validate_product(name, price):
    if not name or len(name) < 3:
        raise ValueError("Назва товару має бути довшою за 3 символи")
    if price < 0:
        raise ValueError("Ціна не може бути від'ємною")

# --- API Endpoints ---

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Користувач вже існує"}), 409
    new_user = User(username=data['username'], password=generate_password_hash(data['password']))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Користувач створений"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
    return jsonify({"message": "Невірний логін або пароль"}), 401

@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.json
    try:
        validate_product(data['name'], data['price']) # Виконання інваріантів
        new_product = Product(name=data['name'], price=data['price'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Товар додано"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Товар не знайдено"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Товар видалено"}), 200

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in products]), 200


@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.json

    items = data.get('items')
    if not items:
        return jsonify({"message": "Замовлення не може бути пустим"}), 400

    if isinstance(items, list):
        items_str = ", ".join(items)
    else:
        items_str = str(items)

    if len(items_str) > 200:
        return jsonify({"message": "Замовлення занадто велике"}), 400

    current_user_id = get_jwt_identity()

    new_order = Order(user_id=int(current_user_id), items=items_str)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Замовлення створено", "order_id": new_order.id}), 201


@app.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    current_user_id = get_jwt_identity()

    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({"message": "Замовлення не існує"}), 404

    # чи належить замовлення цьому користувачу
    if str(order.user_id) != current_user_id:
        return jsonify({"message": "Користувач не існує або доступ заборонено"}), 409

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Замовлення видалено"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

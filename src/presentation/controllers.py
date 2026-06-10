from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from src.infrastructure.models import db, UserEntity
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from src.application.handlers import ProductHandler, OrderHandler, UserHandler
from src.presentation.dto import CreateProductDTO, CreateOrderDTO, RegisterUserDTO
from src.domain.errors import DomainError
from src.presentation.di import get_product_handler, get_order_handler, get_user_handler

bp = Blueprint('api', __name__)

@bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    dto = CreateProductDTO(**request.json)
    handler = get_product_handler()
    try:
        pid = handler.add_product(dto.name, dto.price)
        return jsonify({"id": pid}), 201
    except DomainError as e:
        return jsonify({"message": str(e)}), 400

@bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    dto = CreateOrderDTO(**request.json)
    handler = get_order_handler()
    try:
        oid = handler.create_order(user_id=get_jwt_identity(), items=dto.items)
        return jsonify({"id": oid}), 201
    except DomainError as e:
        return jsonify({"message": str(e)}), 400

@bp.route('/register', methods=['POST'])
def register():
    dto = RegisterUserDTO(**request.json)
    handler = get_user_handler()
    try:
        uid = handler.register_user(dto.username, dto.password)
        return jsonify({"id": uid}), 201
    except DomainError as e:
        return jsonify({"message": str(e)}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = db.session.query(UserEntity).filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
    return jsonify({"message": "Невірний логін або пароль"}), 401

@bp.route('/products', methods=['GET'])
def get_products():
    handler = get_product_handler()
    products = handler.list_all()
    return jsonify([{"id": p.id, "name": p.name} for p in products]), 200

@bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    handler = get_product_handler()
    try:
        handler.delete_product(id)
        return jsonify({"message": "Товар видалено"}), 200
    except DomainError as e:
        return jsonify({"message": str(e)}), 404

@bp.route('/orders/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    handler = get_order_handler()
    try:
        handler.delete_order(order_id)
        return jsonify({"message": "Замовлення видалено"}), 200
    except DomainError as e:
        return jsonify({"message": str(e)}), 404

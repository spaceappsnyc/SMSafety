from app.api import bp
from flask import jsonify, url_for, request
from app.models import User
from app import db
from app.api.errors import bad_request

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'phone_number' not in data and 'email' not in data:
        return bad_request('must include phone number or email')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    if User.query.filter_by(phone_number=data['phone_number']).first():
        return bad_request('please use a different phone number')
        
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass

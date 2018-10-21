from app.api import bp
from flask import jsonify, url_for, request
from app.models import User, Party
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

    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return bad_request('Please use a different email address')
    elif 'phone_number' in data:
        if User.query.filter_by(phone_number=data['phone_number'].strip()).first():
            return bad_request('Please use a different phone number')
    else:
        return bad_request('Must include phone number or email')

    user = User()
    user.from_dict(data, new_user=True)

    party = Party()
    party.users.append(user)

    db.session.add(party)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users', methods=['PUT'])
@bp.route('/users/update', methods=['PUT', 'POST'])
def update_user():
    data = request.get_json() or {}

    if 'phone_number' not in data:
        return bad_request('Must include phone number')

    user = User.query.filter_by(phone_number=data['phone_number'].strip()).first()
    if not user:
        return bad_request('User not found')

    user.from_dict(data, new_user=False)
    db.session.commit()

    return jsonify(user.to_dict())

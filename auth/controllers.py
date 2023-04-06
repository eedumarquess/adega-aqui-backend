from flask import jsonify, request
from . import auth
from .models import User
import jwt
import datetime
import redis
from functools import wraps

# JWIT Configuration
JWT_SECRET_KEY = 'chave-secreta-aqui'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_TIME_SECONDS = 3600

# Configurações do Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

def token_required(func):
  @wraps(func)
  def decorated(*args, **kwargs):
    token = request.headers.get('Authorization')

    if not token:
      return jsonify({'message': 'Token is missing!'}), 401

    try:
      data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
      current_user_id = data['id']
    except:
      return jsonify({'message': 'Token is invalid!'}), 401

    if not redis_db.exists(current_user_id):
      return jsonify({'message': 'Token is invalid!'}), 401

    return func(current_user_id, *args, **kwargs)

  return decorated

@auth.route('/register', methods=['POST'])
def register():
  data = request.get_json()

  user = User(username=data['username'], password=data['password'])
  user.save()

  return jsonify({'message': 'User created successfully!'})

@auth.route('/login', methods=['POST'])
def login():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return jsonify({'message': 'Could not verify credentials!'}), 401

  user = User.query.filter_by(username=auth.username).first()

  if not user:
    return jsonify({'message': 'Could not verify credentials!'}), 401

  if user.password != auth.password:
    return jsonify({'message': 'Could not verify credentials!'}), 401

  token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_TIME_SECONDS)}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

  redis_db.set(user.id, token.decode('UTF-8'), ex=JWT_EXPIRATION_TIME_SECONDS)

  return jsonify({'token': token.decode('UTF-8')})

@auth.route('/profile')
@token_required
def profile(current_user_id):
  current_user_token = redis_db.get(current_user_id)
  current_user = User.query.filter_by(id=current_user_id).first()

  return jsonify({'username': current_user.username})
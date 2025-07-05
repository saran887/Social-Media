from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os
from datetime import timedelta
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '7c925857d7738479b3b22da48e97e6a518f531c184c1c0cb4a5dd573cacd59e3'
app.config['JWT_SECRET_KEY'] = 's23f2e-twAivceCI3dqb_NGshO4EGCCCuWCZmLZn1D6qzvezbZWw4NDVtFcwGanjvdUXyNGiceMPtDMNlPgAbQ'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
jwt = JWTManager(app)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['social_media']
users_collection = db['users']
posts_collection = db['posts']

# Create indexes for better performance
try:
    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    posts_collection.create_index('user_id')
    posts_collection.create_index('created_at')
except Exception as e:
    print(f"Index creation warning: {e}")

# Import models after db initialization
from Models.User import User
from Models.Post import Post

# Password validation function
def validate_password(password):
    """
    Validate password with constraints:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

# Email validation function
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Email is valid"
    return False, "Invalid email format"

# Authentication routes
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['email', 'username', 'password', 'full_name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        email = data['email']
        username = data['username']
        password = data['password']
        full_name = data['full_name']
        
        # Validate email
        is_valid_email, email_message = validate_email(email)
        if not is_valid_email:
            return jsonify({'error': email_message}), 400
        
        # Validate password
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            return jsonify({'error': password_message}), 400
        
        # Check if user already exists
        if User.find_by_email(email):
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.find_by_username(username):
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name
        )
        
        new_user.save()
        
        return jsonify({'message': 'User registered successfully'}), 201
        
    except DuplicateKeyError:
        return jsonify({'error': 'Email or username already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'error': 'Email and password required'}), 400
        
        email = data['email']
        password = data['password']
        
        # Find user by email
        user = User.find_by_email(email)
        
        if not user or not check_password_hash(user.hashed_password, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.email)
        
        return jsonify({
            'access_token': access_token,
            'token_type': 'bearer',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'full_name': user.full_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_email = get_jwt_identity()
        user = User.find_by_email(current_user_email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not all(key in data for key in ['old_password', 'new_password']):
            return jsonify({'error': 'Old password and new password required'}), 400
        
        old_password = data['old_password']
        new_password = data['new_password']
        
        # Verify old password
        if not check_password_hash(user.hashed_password, old_password):
            return jsonify({'error': 'Invalid old password'}), 401
        
        # Check if new password is same as old password
        if old_password == new_password:
            return jsonify({'error': 'New password must be different from old password'}), 400
        
        # Validate new password
        is_valid_password, password_message = validate_password(new_password)
        if not is_valid_password:
            return jsonify({'error': password_message}), 400
        
        # Update password
        new_hashed_password = generate_password_hash(new_password)
        user.update_password(new_hashed_password)
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        
        if 'email' not in data:
            return jsonify({'error': 'Email required'}), 400
        
        email = data['email']
        
        # Validate email
        is_valid_email, email_message = validate_email(email)
        if not is_valid_email:
            return jsonify({'error': email_message}), 400
        
        # Check if user exists
        user = User.find_by_email(email)
        if not user:
            return jsonify({'error': 'Email not found'}), 404
        
        # In a real application, you would send an email with reset link
        # For now, we'll just return a success message
        return jsonify({'message': 'Password reset instructions sent to your email'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_email = get_jwt_identity()
        user = User.find_by_email(current_user_email)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Post routes
@app.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    try:
        posts = Post.find_all()
        return jsonify([{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'created_at': post.created_at.isoformat() if post.created_at else None
        } for post in posts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        current_user_email = get_jwt_identity()
        user = User.find_by_email(current_user_email)
        
        data = request.get_json()
        
        if not all(key in data for key in ['title', 'content']):
            return jsonify({'error': 'Title and content required'}), 400
        
        new_post = Post(
            title=data['title'],
            content=data['content'],
            user_id=user.id
        )
        
        new_post.save()
        
        return jsonify({
            'id': new_post.id,
            'title': new_post.title,
            'content': new_post.content,
            'user_id': new_post.user_id,
            'created_at': new_post.created_at.isoformat() if new_post.created_at else None
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def root():
    return jsonify({'message': 'Social Media Platform API with MongoDB'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

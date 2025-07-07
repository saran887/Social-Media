from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['social_media']
users_collection = db['users']

class User:
    def __init__(self, email, username, hashed_password, full_name=None, is_active=True, created_at=None, updated_at=None, password_history=None):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.password_history = password_history or []
    
    def to_dict(self):
        return {
            'email': self.email,
            'username': self.username,
            'hashed_password': self.hashed_password,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'password_history': self.password_history
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            email=data.get('email'),
            username=data.get('username'),
            hashed_password=data.get('hashed_password'),
            full_name=data.get('full_name'),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            password_history=data.get('password_history', [])
        )
    
    def save(self):
        if hasattr(self, '_id'):
            # Update existing user
            self.updated_at = datetime.utcnow()
            users_collection.update_one(
                {'_id': self._id},
                {'$set': self.to_dict()}
            )
        else:
            # Insert new user
            user_data = self.to_dict()
            result = users_collection.insert_one(user_data)
            self._id = result.inserted_id
        return self
    
    @staticmethod
    def find_by_email(email):
        user_data = users_collection.find_one({'email': email})
        if user_data:
            user = User.from_dict(user_data)
            user._id = user_data['_id']
            return user
        return None
    
    @staticmethod
    def find_by_username(username):
        user_data = users_collection.find_one({'username': username})
        if user_data:
            user = User.from_dict(user_data)
            user._id = user_data['_id']
            return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        try:
            user_data = users_collection.find_one({'_id': ObjectId(user_id)})
            if user_data:
                user = User.from_dict(user_data)
                user._id = user_data['_id']
                return user
        except:
            pass
        return None
    
    def update_password(self, new_hashed_password):
        # Add the current password to history, keep only last 3
        if self.hashed_password:
            self.password_history = [self.hashed_password] + self.password_history[:2]
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()
        users_collection.update_one(
            {'_id': self._id},
            {'$set': {
                'hashed_password': self.hashed_password,
                'updated_at': self.updated_at,
                'password_history': self.password_history
            }}
        )
    
    @property
    def id(self):
        return str(self._id) if hasattr(self, '_id') else None

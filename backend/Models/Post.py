from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['social_media']
posts_collection = db['posts']

class Post:
    def __init__(self, title, content, user_id, created_at=None, updated_at=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Post(
            title=data.get('title'),
            content=data.get('content'),
            user_id=data.get('user_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def save(self):
        if hasattr(self, '_id'):
            # Update existing post
            self.updated_at = datetime.utcnow()
            posts_collection.update_one(
                {'_id': self._id},
                {'$set': self.to_dict()}
            )
        else:
            # Insert new post
            post_data = self.to_dict()
            result = posts_collection.insert_one(post_data)
            self._id = result.inserted_id
        return self
    
    @staticmethod
    def find_all():
        posts_data = posts_collection.find().sort('created_at', -1)
        posts = []
        for post_data in posts_data:
            post = Post.from_dict(post_data)
            post._id = post_data['_id']
            posts.append(post)
        return posts
    
    @staticmethod
    def find_by_id(post_id):
        try:
            post_data = posts_collection.find_one({'_id': ObjectId(post_id)})
            if post_data:
                post = Post.from_dict(post_data)
                post._id = post_data['_id']
                return post
        except:
            pass
        return None
    
    @staticmethod
    def find_by_user_id(user_id):
        posts_data = posts_collection.find({'user_id': user_id}).sort('created_at', -1)
        posts = []
        for post_data in posts_data:
            post = Post.from_dict(post_data)
            post._id = post_data['_id']
            posts.append(post)
        return posts
    
    def delete(self):
        if hasattr(self, '_id'):
            posts_collection.delete_one({'_id': self._id})
    
    @property
    def id(self):
        return str(self._id) if hasattr(self, '_id') else None

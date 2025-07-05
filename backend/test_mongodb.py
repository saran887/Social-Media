#!/usr/bin/env python3
"""
MongoDB Test Script for Social Media Platform
This script tests the MongoDB connection and basic CRUD operations.
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
import sys

def test_mongodb_connection():
    """Test MongoDB connection and basic operations."""
    
    try:
        print("🔍 Testing MongoDB Connection...")
        
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['social_media']
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Test collections
        users_collection = db['users']
        posts_collection = db['posts']
        print("✅ Collections accessed successfully!")
        
        # Test user creation
        print("\n🧪 Testing User Creation...")
        test_user = {
            'email': 'test@example.com',
            'username': 'testuser',
            'hashed_password': generate_password_hash('TestPass123!'),
            'full_name': 'Test User',
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Insert test user
        result = users_collection.insert_one(test_user)
        print(f"✅ Test user created with ID: {result.inserted_id}")
        
        # Test user retrieval
        found_user = users_collection.find_one({'email': 'test@example.com'})
        if found_user:
            print("✅ Test user retrieved successfully!")
        else:
            print("❌ Failed to retrieve test user")
            return False
        
        # Test post creation
        print("\n🧪 Testing Post Creation...")
        test_post = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'user_id': str(result.inserted_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Insert test post
        post_result = posts_collection.insert_one(test_post)
        print(f"✅ Test post created with ID: {post_result.inserted_id}")
        
        # Test post retrieval
        found_post = posts_collection.find_one({'title': 'Test Post'})
        if found_post:
            print("✅ Test post retrieved successfully!")
        else:
            print("❌ Failed to retrieve test post")
            return False
        
        # Test post listing
        all_posts = list(posts_collection.find())
        print(f"✅ Found {len(all_posts)} posts in database")
        
        # Clean up test data
        print("\n🧹 Cleaning up test data...")
        users_collection.delete_one({'email': 'test@example.com'})
        posts_collection.delete_one({'title': 'Test Post'})
        print("✅ Test data cleaned up!")
        
        print("\n🎉 All MongoDB tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_indexes():
    """Test if indexes are properly created."""
    
    try:
        print("\n🔍 Testing Database Indexes...")
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client['social_media']
        
        # Check user indexes
        user_indexes = list(db['users'].list_indexes())
        email_index = any(idx['key'] == [('email', 1)] for idx in user_indexes)
        username_index = any(idx['key'] == [('username', 1)] for idx in user_indexes)
        
        if email_index:
            print("✅ Email index found")
        else:
            print("❌ Email index missing")
            
        if username_index:
            print("✅ Username index found")
        else:
            print("❌ Username index missing")
        
        # Check post indexes
        post_indexes = list(db['posts'].list_indexes())
        user_id_index = any(idx['key'] == [('user_id', 1)] for idx in post_indexes)
        created_at_index = any(idx['key'] == [('created_at', 1)] for idx in post_indexes)
        
        if user_id_index:
            print("✅ User ID index found")
        else:
            print("❌ User ID index missing")
            
        if created_at_index:
            print("✅ Created at index found")
        else:
            print("❌ Created at index missing")
        
        return email_index and username_index and user_id_index and created_at_index
        
    except Exception as e:
        print(f"❌ Index test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MongoDB Test Suite for Social Media Platform")
    print("=" * 55)
    
    # Test connection and basic operations
    connection_ok = test_mongodb_connection()
    
    # Test indexes
    indexes_ok = test_indexes()
    
    if connection_ok and indexes_ok:
        print("\n✨ All tests passed! MongoDB is ready for use.")
        print("You can now run the Flask application: python app.py")
    else:
        print("\n❌ Some tests failed. Please check your MongoDB setup.")
        sys.exit(1) 
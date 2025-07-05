#!/usr/bin/env python3
"""
MongoDB Setup Script for Social Media Platform
This script initializes the MongoDB database and creates necessary indexes.
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import sys

def setup_mongodb():
    """Setup MongoDB database and collections with proper indexes."""
    
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Create database
        db = client['social_media']
        print("✅ Database 'social_media' created/accessed")
        
        # Create collections
        users_collection = db['users']
        posts_collection = db['posts']
        print("✅ Collections 'users' and 'posts' created/accessed")
        
        # Create indexes for better performance
        print("Creating indexes...")
        
        # User indexes
        users_collection.create_index('email', unique=True)
        print("✅ Created unique index on users.email")
        
        users_collection.create_index('username', unique=True)
        print("✅ Created unique index on users.username")
        
        # Post indexes
        posts_collection.create_index('user_id')
        print("✅ Created index on posts.user_id")
        
        posts_collection.create_index('created_at')
        print("✅ Created index on posts.created_at")
        
        # Create compound index for efficient queries
        posts_collection.create_index([('user_id', 1), ('created_at', -1)])
        print("✅ Created compound index on posts (user_id, created_at)")
        
        print("\n🎉 MongoDB setup completed successfully!")
        print("\nDatabase: social_media")
        print("Collections: users, posts")
        print("Indexes created for optimal performance")
        
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ Error: Could not connect to MongoDB server")
        print("Please make sure MongoDB is running on localhost:27017")
        print("\nTo start MongoDB:")
        print("- Windows: Start MongoDB service or run 'mongod'")
        print("- macOS: brew services start mongodb-community")
        print("- Linux: sudo systemctl start mongod")
        return False
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False

def check_mongodb_status():
    """Check if MongoDB is running and accessible."""
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        return True
    except:
        print("❌ MongoDB is not accessible")
        return False

if __name__ == "__main__":
    print("🚀 MongoDB Setup for Social Media Platform")
    print("=" * 50)
    
    # Check if MongoDB is running
    if not check_mongodb_status():
        print("\nPlease start MongoDB before running this script.")
        sys.exit(1)
    
    # Setup database
    if setup_mongodb():
        print("\n✨ You can now run the Flask application!")
        print("Run: python app.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1) 
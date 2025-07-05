import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7c925857d7738479b3b22da48e97e6a518f531c184c1c0cb4a5dd573cacd59e3'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 's23f2e-twAivceCI3dqb_NGshO4EGCCCuWCZmLZn1D6qzvezbZWw4NDVtFcwGanjvdUXyNGiceMPtDMNlPgAbQ'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # MongoDB Configuration
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE') or 'social_media'
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS') or 'http://localhost:3000'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, you should set these environment variables
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    # MONGODB_URI = os.environ.get('MONGODB_URI')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGODB_DATABASE = 'social_media_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 
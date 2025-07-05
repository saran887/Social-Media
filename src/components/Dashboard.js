import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ title: '', content: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/posts');
      setPosts(response.data);
    } catch (error) {
      toast.error('Failed to fetch posts');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    if (!newPost.title.trim() || !newPost.content.trim()) {
      toast.error('Please fill in all fields');
      return;
    }

    try {
      setIsCreating(true);
      const response = await axios.post('/posts', newPost);
      setPosts([response.data, ...posts]);
      setNewPost({ title: '', content: '' });
      toast.success('Post created successfully!');
    } catch (error) {
      toast.error('Failed to create post');
    } finally {
      setIsCreating(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Social Media Platform</h1>
          <div className="user-info">
            <span>Welcome, {user?.full_name || user?.username}!</span>
            <div className="header-actions">
              <Link to="/change-password" className="header-link">
                Change Password
              </Link>
              <button onClick={logout} className="logout-button">
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-container">
          {/* Create Post Section */}
          <section className="create-post-section">
            <h2>Create a New Post</h2>
            <form onSubmit={handleCreatePost} className="create-post-form">
              <div className="form-group">
                <label htmlFor="title">Title</label>
                <input
                  type="text"
                  id="title"
                  value={newPost.title}
                  onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
                  placeholder="Enter post title"
                  maxLength={255}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="content">Content</label>
                <textarea
                  id="content"
                  value={newPost.content}
                  onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
                  placeholder="What's on your mind?"
                  rows={4}
                  required
                />
              </div>
              <button 
                type="submit" 
                className="create-post-button"
                disabled={isCreating}
              >
                {isCreating ? 'Creating...' : 'Create Post'}
              </button>
            </form>
          </section>

          {/* Posts Section */}
          <section className="posts-section">
            <h2>Recent Posts</h2>
            {isLoading ? (
              <div className="loading">Loading posts...</div>
            ) : posts.length === 0 ? (
              <div className="no-posts">No posts yet. Be the first to create one!</div>
            ) : (
              <div className="posts-list">
                {posts.map((post) => (
                  <article key={post.id} className="post-card">
                    <div className="post-header">
                      <h3 className="post-title">{post.title}</h3>
                      <span className="post-date">{formatDate(post.created_at)}</span>
                    </div>
                    <div className="post-content">
                      <p>{post.content}</p>
                    </div>
                    <div className="post-footer">
                      <span className="post-author">Posted by User #{post.user_id}</span>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard; 
import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import './Dashboard.css';
import ChangePassword from './ChangePassword';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ title: '', content: '', visibility: 'public' });
  const [postImage, setPostImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);
  const navigate = useNavigate();
  const BACKEND_URL = "http://localhost:5000";

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

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setPostImage(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImagePreview(reader.result);
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
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
      const formData = new FormData();
      formData.append('title', newPost.title);
      formData.append('content', newPost.content);
      if (postImage) formData.append('image', postImage);
      formData.append('visibility', newPost.visibility);
      const response = await axios.post('/posts', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setPosts([response.data, ...posts]);
      setNewPost({ title: '', content: '', visibility: 'public' });
      setPostImage(null);
      setImagePreview(null);
      toast.success('Post created successfully!');
    } catch (error) {
      toast.error('Failed to create post');
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeletePost = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this post?')) return;
    try {
      await axios.delete(`/posts/${postId}`);
      setPosts(posts => posts.filter(post => post.id !== postId));
      toast.success('Post deleted');
    } catch (error) {
      toast.error('Failed to delete post');
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
              <button onClick={() => setShowCreatePost(true)} className="post-header-button">Post</button>
              {user && (
                <button onClick={() => setShowProfile(true)} className="profile-header-button">Profile</button>
              )}
              <button onClick={logout} className="logout-button">Logout</button>
            </div>
          </div>
        </div>
      </header>

      {/* Profile Modal */}
      {showProfile && user && (
        <div className="profile-modal">
          <section className="profile-section">
            <div className="profile-header">
              <div className="profile-avatar">
                <img src={`https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name || user.username)}&background=1877f2&color=fff&size=96`} alt="Avatar" />
              </div>
              <div className="profile-details">
                <h2>{user.full_name || user.username}</h2>
                <p className="profile-username">@{user.username}</p>
                <p className="profile-email">{user.email}</p>
                <p className="profile-date">Joined: {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
                <p className="profile-bio">Bio: <span className="profile-bio-placeholder">This is your bio. (Edit coming soon)</span></p>
                <div className="profile-actions">
                  <button onClick={() => navigate('/change-password')} className="change-password-button">Change Password</button>
                  <button className="edit-profile-button" disabled>Edit Profile</button>
                </div>
              </div>
            </div>
            <div className="profile-stats">
              <div className="profile-stat">
                <span className="stat-number">{posts.filter(p => p.user?.id === user.id).length}</span>
                <span className="stat-label">Posts</span>
              </div>
            </div>
            <div className="profile-recent-posts">
              <h3>Recent Posts</h3>
              {posts.filter(p => p.user?.id === user.id).length === 0 ? (
                <p className="no-recent-posts">You haven't posted yet.</p>
              ) : (
                <ul className="recent-posts-list">
                  {posts.filter(p => p.user?.id === user.id).slice(0, 3).map(post => (
                    <li key={post.id} className="recent-post-item">
                      <span className="recent-post-title">{post.title}</span>
                      <span className="recent-post-date">{formatDate(post.created_at)}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <button onClick={() => setShowProfile(false)} className="close-modal-button" style={{marginTop: 24}}>Close Profile</button>
          </section>
        </div>
      )}

      {/* Create Post Modal */}
      {showCreatePost && (
        <div className="create-post-modal">
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
              <div className="form-group">
                <label htmlFor="image">Image (optional)</label>
                <input
                  type="file"
                  id="image"
                  accept="image/*"
                  onChange={handleImageChange}
                />
                {imagePreview && (
                  <div className="image-preview-container">
                    <img src={imagePreview} alt="Preview" className="image-preview" />
                    <button type="button" className="remove-image-btn" onClick={() => { setPostImage(null); setImagePreview(null); }}>Remove</button>
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>Visibility</label>
                <div className="visibility-toggle">
                  <label>
                    <input
                      type="radio"
                      name="visibility"
                      value="public"
                      checked={newPost.visibility === 'public'}
                      onChange={() => setNewPost({ ...newPost, visibility: 'public' })}
                    />
                    Public
                  </label>
                  <label>
                    <input
                      type="radio"
                      name="visibility"
                      value="private"
                      checked={newPost.visibility === 'private'}
                      onChange={() => setNewPost({ ...newPost, visibility: 'private' })}
                    />
                    Private
                  </label>
                </div>
              </div>
              <button 
                type="submit" 
                className="create-post-button"
                disabled={isCreating}
              >
                {isCreating ? 'Creating...' : 'Create Post'}
              </button>
            </form>
            <button onClick={() => setShowCreatePost(false)} className="close-modal-button" style={{marginTop: 18}}>Close</button>
          </section>
        </div>
      )}

      {/* Only show the feed if not creating a post */}
      {!showCreatePost && (
        <main className="dashboard-main">
          <div className="dashboard-container">
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
                      <div className="post-user-row">
                        <img
                          src={post.user?.username ? `https://ui-avatars.com/api/?name=${encodeURIComponent(post.user.full_name || post.user.username)}&background=1877f2&color=fff&size=40` : undefined}
                          alt="Avatar"
                          className="post-avatar"
                        />
                        <div className="post-user-meta">
                          <span className="post-username">{post.user?.username || 'Unknown'}</span>
                          <span className="post-date">{formatDate(post.created_at)}</span>
                        </div>
                        <span className={`post-visibility ${post.visibility}`}>{post.visibility === 'private' ? '🔒' : '🌍'}</span>
                      </div>
                      {post.image_url && (
                        <div className="post-image-container">
                          <img
                            src={post.image_url.startsWith('http') ? post.image_url : `${BACKEND_URL}${post.image_url}`}
                            alt="Post"
                            className="post-image"
                          />
                        </div>
                      )}
                      <div className="post-content">
                        <p>{post.content}</p>
                      </div>
                      {user && post.user_id === user.id && (
                        <button className="delete-post-btn" onClick={() => handleDeletePost(post.id)} title="Delete Post">🗑️</button>
                      )}
                    </article>
                  ))}
                </div>
              )}
            </section>
          </div>
        </main>
      )}
    </div>
  );
};

export default Dashboard; 
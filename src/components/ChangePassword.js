import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const ChangePassword = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { changePassword } = useAuth();
  const navigate = useNavigate();
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm();

  const oldPassword = watch('old_password');
  const newPassword = watch('new_password');

  // Password validation function
  const validatePassword = (password) => {
    const errors = [];
    
    if (password.length < 8) {
      errors.push('At least 8 characters');
    }
    if (!/[A-Z]/.test(password)) {
      errors.push('One uppercase letter');
    }
    if (!/[a-z]/.test(password)) {
      errors.push('One lowercase letter');
    }
    if (!/\d/.test(password)) {
      errors.push('One number');
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push('One special character');
    }
    
    return errors;
  };

  const onSubmit = async (data) => {
    // Check if new password is same as old password
    if (data.old_password === data.new_password) {
      alert('New password must be different from old password');
      return;
    }

    setIsLoading(true);
    const success = await changePassword(data.old_password, data.new_password);
    setIsLoading(false);
    if (success) {
      navigate('/dashboard');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Change Password</h2>
        <p className="auth-subtitle">Update your password</p>
        
        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
          <div className="form-group">
            <label htmlFor="old_password">Current Password</label>
            <input
              type="password"
              id="old_password"
              {...register('old_password', {
                required: 'Current password is required'
              })}
              placeholder="Enter your current password"
              className={errors.old_password ? 'error' : ''}
            />
            {errors.old_password && <span className="error-message">{errors.old_password.message}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="new_password">New Password</label>
            <input
              type="password"
              id="new_password"
              {...register('new_password', {
                required: 'New password is required',
                validate: (value) => {
                  if (value === oldPassword) {
                    return 'New password must be different from current password';
                  }
                  const errors = validatePassword(value);
                  return errors.length === 0 || 'Password does not meet requirements';
                }
              })}
              placeholder="Enter your new password"
              className={errors.new_password ? 'error' : ''}
            />
            {errors.new_password && <span className="error-message">{errors.new_password.message}</span>}
            
            {/* Password requirements */}
            {newPassword && (
              <div className="password-requirements">
                <h4>Password Requirements:</h4>
                <ul>
                  <li className={newPassword.length >= 8 ? 'valid' : 'invalid'}>
                    At least 8 characters
                  </li>
                  <li className={/[A-Z]/.test(newPassword) ? 'valid' : 'invalid'}>
                    One uppercase letter
                  </li>
                  <li className={/[a-z]/.test(newPassword) ? 'valid' : 'invalid'}>
                    One lowercase letter
                  </li>
                  <li className={/\d/.test(newPassword) ? 'valid' : 'invalid'}>
                    One number
                  </li>
                  <li className={/[!@#$%^&*(),.?":{}|<>]/.test(newPassword) ? 'valid' : 'invalid'}>
                    One special character
                  </li>
                  <li className={newPassword !== oldPassword ? 'valid' : 'invalid'}>
                    Different from current password
                  </li>
                </ul>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="confirm_password">Confirm New Password</label>
            <input
              type="password"
              id="confirm_password"
              {...register('confirm_password', {
                required: 'Please confirm your new password',
                validate: (value) => value === newPassword || 'Passwords do not match'
              })}
              placeholder="Confirm your new password"
              className={errors.confirm_password ? 'error' : ''}
            />
            {errors.confirm_password && <span className="error-message">{errors.confirm_password.message}</span>}
          </div>

          <button 
            type="submit" 
            className="auth-button" 
            disabled={isLoading}
          >
            {isLoading ? 'Changing Password...' : 'Change Password'}
          </button>
        </form>

        <div className="auth-footer">
          <button 
            onClick={() => navigate('/dashboard')} 
            className="auth-link-button"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChangePassword; 
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
  const [success, setSuccess] = useState(false);

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
    const result = await changePassword(data.old_password, data.new_password);
    setIsLoading(false);
    if (result) {
      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        navigate('/dashboard');
      }, 1800);
    }
  };

  const handleClose = () => {
    navigate('/dashboard');
  };

  return (
    <div className="change-password-modal-ui">
      <div className="change-password-card">
        <h2>Change Password</h2>
        <p className="change-password-subtitle">Set a new password for your account</p>
        {success ? (
          <div className="change-password-success">Password changed successfully!</div>
        ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="change-password-form">
          <div className="change-password-step">
            <label htmlFor="old_password">Current Password</label>
            <input
              type="password"
              id="old_password"
              {...register('old_password', { required: 'Current password is required' })}
              placeholder="Enter your current password"
              className={errors.old_password ? 'error' : ''}
            />
            {errors.old_password && <span className="error-message">{errors.old_password.message}</span>}
          </div>
          <div className="change-password-step">
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
            <div className="change-password-requirements">
              <span>Password must include:</span>
              <ul>
                <li className={newPassword && newPassword.length >= 8 ? 'valid' : 'invalid'}>8+ characters</li>
                <li className={newPassword && /[A-Z]/.test(newPassword) ? 'valid' : 'invalid'}>Uppercase letter</li>
                <li className={newPassword && /[a-z]/.test(newPassword) ? 'valid' : 'invalid'}>Lowercase letter</li>
                <li className={newPassword && /\d/.test(newPassword) ? 'valid' : 'invalid'}>Number</li>
                <li className={newPassword && /[!@#$%^&*(),.?":{}|<>]/.test(newPassword) ? 'valid' : 'invalid'}>Special character</li>
                <li className={newPassword && newPassword !== oldPassword ? 'valid' : 'invalid'}>Different from current password</li>
              </ul>
            </div>
          </div>
          <div className="change-password-step">
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
          <button type="submit" className="change-password-button" disabled={isLoading}>
            {isLoading ? 'Changing...' : 'Change Password'}
          </button>
        </form>
        )}
        <button onClick={handleClose} className="close-modal-button" style={{marginTop: 18}}>Close</button>
      </div>
    </div>
  );
};

export default ChangePassword; 
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import Login from './Login';
import Signup from './Signup';
import App from '../../App';

const AuthWrapper: React.FC = () => {
  const { isAuthenticated, login } = useAuth();
  const [isLoginMode, setIsLoginMode] = useState(true);

  const handleLogin = (token: string, email: string) => {
    login(token, email);
  };

  const handleSignup = (token: string, email: string) => {
    login(token, email);
  };

  const switchToSignup = () => {
    setIsLoginMode(false);
  };

  const switchToLogin = () => {
    setIsLoginMode(true);
  };

  if (isAuthenticated) {
    return <App />;
  }

  return (
    <>
      {isLoginMode ? (
        <Login onLogin={handleLogin} onSwitchToSignup={switchToSignup} />
      ) : (
        <Signup onSignup={handleSignup} onSwitchToLogin={switchToLogin} />
      )}
    </>
  );
};

export default AuthWrapper; 
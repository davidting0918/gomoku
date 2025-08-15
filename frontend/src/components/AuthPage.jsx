import React, { useState } from "react";
import { LoginForm } from "./LoginForm";
import { SignUpForm } from "./SignUpForm";

export function AuthPage({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);

  const handleSignUpClick = () => {
    setIsLogin(false);
  };

  const handleLoginClick = () => {
    setIsLogin(true);
  };

  return (
    <div>
      {isLogin ? (
        <LoginForm onSignUpClick={handleSignUpClick} onLoginSuccess={onLoginSuccess} />
      ) : (
        <SignUpForm onLoginClick={handleLoginClick} />
      )}
    </div>
  );
}

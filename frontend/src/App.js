import React, { useState } from "react";
import GomokuGame from "./Board";
import { AuthPage } from "./components/AuthPage";
import { Navigation } from "./components/Navigation";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState("");

  const handleLoginSuccess = (email) => {
    setIsAuthenticated(true);
    setUserEmail(email || "用戶");
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserEmail("");
  };

  return (
    <main>
      {isAuthenticated ? (
        <div>
          <Navigation onLogout={handleLogout} userEmail={userEmail} />
          <div className="pt-16">
            <GomokuGame />
          </div>
        </div>
      ) : (
        <AuthPage onLoginSuccess={handleLoginSuccess} />
      )}
    </main>
  );
}

export default App;

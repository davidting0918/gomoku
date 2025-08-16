import React, { useState } from "react";
import { Button } from "./button";

export function LoginForm({ onSignUpClick, onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // TODO: 實現登入邏輯
      console.log("登入:", { email, password });
      
      // 模擬登入成功
      setTimeout(() => {
        if (onLoginSuccess) {
          onLoginSuccess(email);
        }
      }, 1000);
      
    } catch (error) {
      console.error("登入失敗:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setIsLoading(true);
    try {
      // TODO: 實現Google登入邏輯
      console.log("Google登入");
      
      // 模擬Google登入成功
      setTimeout(() => {
        if (onLoginSuccess) {
          onLoginSuccess("Google用戶");
        }
      }, 1000);
      
    } catch (error) {
      console.error("Google登入失敗:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* 標題 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">歡迎回來</h1>
          <p className="text-gray-400">登入您的帳戶繼續遊戲</p>
        </div>

        {/* 登入表單 */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 電子郵件欄位 */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
              電子郵件
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-100 placeholder-gray-500"
              placeholder="輸入您的電子郵件"
            />
          </div>

          {/* 密碼欄位 */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
              密碼
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-100 placeholder-gray-500"
              placeholder="輸入您的密碼"
            />
          </div>

          {/* 忘記密碼連結 */}
          <div className="text-right">
            <a href="#" className="text-sm text-blue-400 hover:text-blue-300 transition-colors">
              忘記密碼？
            </a>
          </div>

          {/* 登入按鈕 */}
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "登入中..." : "登入"}
          </Button>
        </form>

        {/* 分隔線 */}
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-700"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-gray-950 text-gray-400">或</span>
          </div>
        </div>

        {/* Google登入按鈕 */}
        <Button
          onClick={handleGoogleLogin}
          disabled={isLoading}
          className="w-full py-3 bg-white text-gray-900 hover:bg-gray-100 border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed mb-6"
        >
          <div className="flex items-center justify-center space-x-2">
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span>使用Google帳戶登入</span>
          </div>
        </Button>

        {/* 註冊連結 */}
        <div className="text-center">
          <p className="text-gray-400">
            還沒有帳戶？{" "}
            <button
              onClick={onSignUpClick}
              className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
            >
              立即註冊
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

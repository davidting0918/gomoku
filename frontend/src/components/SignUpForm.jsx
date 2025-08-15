import React, { useState } from "react";
import { Button } from "./button";

export function SignUpForm({ onLoginClick }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};
    
    if (!email) {
      newErrors.email = "電子郵件為必填欄位";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "請輸入有效的電子郵件地址";
    }
    
    if (!password) {
      newErrors.password = "密碼為必填欄位";
    } else if (password.length < 6) {
      newErrors.password = "密碼至少需要6個字符";
    }
    
    if (!confirmPassword) {
      newErrors.confirmPassword = "請確認密碼";
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = "密碼不匹配";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      // TODO: 實現註冊邏輯
      console.log("註冊:", { email, password });
    } catch (error) {
      console.error("註冊失敗:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSignUp = async () => {
    setIsLoading(true);
    try {
      // TODO: 實現Google註冊邏輯
      console.log("Google註冊");
    } catch (error) {
      console.error("Google註冊失敗:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* 標題 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">創建帳戶</h1>
          <p className="text-gray-400">加入我們開始遊戲</p>
        </div>

        {/* 註冊表單 */}
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
              className={`w-full px-4 py-3 bg-gray-800 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-100 placeholder-gray-500 ${
                errors.email ? 'border-red-500' : 'border-gray-700'
              }`}
              placeholder="輸入您的電子郵件"
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-400">{errors.email}</p>
            )}
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
              className={`w-full px-4 py-3 bg-gray-800 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-100 placeholder-gray-500 ${
                errors.password ? 'border-red-500' : 'border-gray-700'
              }`}
              placeholder="創建密碼（至少6個字符）"
            />
            {errors.password && (
              <p className="mt-1 text-sm text-red-400">{errors.password}</p>
            )}
          </div>

          {/* 確認密碼欄位 */}
          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
              確認密碼
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className={`w-full px-4 py-3 bg-gray-800 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-100 placeholder-gray-500 ${
                errors.confirmPassword ? 'border-red-500' : 'border-gray-700'
              }`}
              placeholder="再次輸入密碼"
            />
            {errors.confirmPassword && (
              <p className="mt-1 text-sm text-red-400">{errors.confirmPassword}</p>
            )}
          </div>

          {/* 條款同意 */}
          <div className="flex items-start space-x-2">
            <input
              id="terms"
              type="checkbox"
              required
              className="mt-1 w-4 h-4 text-blue-600 bg-gray-800 border-gray-700 rounded focus:ring-blue-500 focus:ring-2"
            />
            <label htmlFor="terms" className="text-sm text-gray-400">
              我同意{" "}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                服務條款
              </a>{" "}
              和{" "}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                隱私政策
              </a>
            </label>
          </div>

          {/* 註冊按鈕 */}
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "註冊中..." : "創建帳戶"}
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

        {/* Google註冊按鈕 */}
        <Button
          onClick={handleGoogleSignUp}
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
            <span>使用Google帳戶註冊</span>
          </div>
        </Button>

        {/* 登入連結 */}
        <div className="text-center">
          <p className="text-gray-400">
            已經有帳戶？{" "}
            <button
              onClick={onLoginClick}
              className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
            >
              立即登入
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

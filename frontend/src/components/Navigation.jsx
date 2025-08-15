import React from "react";

export function Navigation({ onLogout, userEmail }) {
  return (
    <nav className="absolute top-0 left-0 right-0 z-10 bg-gray-900/80 backdrop-blur-sm border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/標題 */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-white">五子棋</h1>
          </div>

          {/* 用戶信息和登出按鈕 */}
          <div className="flex items-center space-x-4">
            {userEmail && (
              <span className="text-gray-300 text-sm">
                歡迎，{userEmail}
              </span>
            )}
            <button
              onClick={onLogout}
              className="bg-red-600 text-white rounded px-4 py-2 hover:bg-red-700 transition-colors text-sm"
            >
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

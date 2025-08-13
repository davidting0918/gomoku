# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Gomoku (Five-in-a-Row) game implementation with:
- **Backend**: FastAPI Python server with game logic
- **Frontend**: React.js web application with Tailwind CSS
- **AI Model**: In-development Python AI components for game strategy

## Development Commands

### Backend (Python/FastAPI)
```bash
# Run backend server (from project root)
cd backend
python main.py
# Server runs on http://localhost:8000

# Run tests
cd backend
python -m pytest tests/

# Install dependencies
pip install -r requirements.txt
```

### Frontend (React)
```bash
# Start development server (from frontend directory)
cd frontend
npm start
# Runs on http://localhost:3000

# Build for production
npm run build

# Run tests
npm test

# Install dependencies
npm install
```

## Architecture

### Backend Structure (`backend/`)
- `main.py`: FastAPI application entry point with CORS middleware
- `core/models.py`: Pydantic models (Move, Board, Game) with 19x19 board size
- `core/routers.py`: API endpoints (/game/board, /game/move, /game/reset)
- `core/services.py`: Game logic including win detection and move validation
- `tests/test_gomoku.py`: Test cases for game functionality

### Frontend Structure (`frontend/src/`)
- `App.js`: Main application component
- `Board.jsx`: Game board UI with React hooks and Tailwind CSS
- `api/gomokuApi.js`: Axios-based API client for backend communication
- `components/button.jsx`: Reusable button component
- `lib/utils.js`: Utility functions including `cn()` for class names

### Game Logic
- 19x19 board size (standard Gomoku)
- Win condition: 5 pieces in a row (horizontal, vertical, diagonal)
- Backend uses global game state with piece tracking by coordinate lists
- Frontend renders board with hover previews and real-time game state sync

### AI Model Development (`ai_model/`)
- `data_generation/`: Contains game core and strategy implementations (in early development)
- Currently minimal implementation - likely for training data generation or AI player strategies

## API Endpoints
- `GET /game/board`: Get current game state
- `POST /game/move`: Make a move (requires player, x, y coordinates)
- `POST /game/reset`: Reset game to initial state

## Testing
- Backend tests use FastAPI TestClient
- Frontend uses React Testing Library (configured in package.json)
- Run backend tests with `python -m pytest tests/` from backend directory
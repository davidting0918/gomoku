// src/Board.jsx
"use client";

import React, { useState, useEffect } from "react";
import api from "./api/gomokuApi";
import { cn } from "./lib/utils";
import { Button } from "./components/button";

const BOARD_SIZE = 19;
const EMPTY = 0;
const BLACK = 1;
const WHITE = 2;

export default function GomokuGame() {
  const [board, setBoard] = useState(
    Array(BOARD_SIZE).fill(0).map(() => Array(BOARD_SIZE).fill(EMPTY))
  );
  const [currentPlayer, setCurrentPlayer] = useState(BLACK);
  const [winner, setWinner] = useState(null);
  const [hoveredCell, setHoveredCell] = useState(null);

  const fetchGame = async () => {
    const res = await api.getBoard();
    const grid = Array(BOARD_SIZE).fill(0).map(() => Array(BOARD_SIZE).fill(EMPTY));
    res.board.black.forEach(([x, y]) => grid[y][x] = BLACK);
    res.board.white.forEach(([x, y]) => grid[y][x] = WHITE);
    setBoard(grid);
    setWinner(res.winner);
    if (!res.winner) {
      setCurrentPlayer(res.board.black.length > res.board.white.length ? WHITE : BLACK);
    }
  };

  useEffect(() => {
    fetchGame();
  }, []);

  const handleCellClick = async (row, col) => {
    if (board[row][col] !== EMPTY || winner) return;
    const player = currentPlayer === BLACK ? "black" : "white";
    try {
      await api.makeMove(col, row, player);
      await fetchGame();
    } catch (err) {
      alert(err.response?.data?.detail || "Move failed");
    }
  };

  const restartGame = async () => {
    await api.resetGame();
    await fetchGame();
    setHoveredCell(null);
  };

  const playerTurnText = winner
    ? winner === "black" ? "Black Wins!" : "White Wins!"
    : currentPlayer === BLACK ? "Black's Turn" : "White's Turn";

  return (
    <div className="min-h-screen bg-gray-950 text-gray-50 flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-8 text-center">{playerTurnText}</h1>

      <div
        className="relative bg-gray-800 rounded-lg shadow-lg mb-8 overflow-hidden"
        style={{
          "--cell-size": `min(36px, calc((100vw - 64px) / ${BOARD_SIZE}))`,
          "--stone-size": `min(32px, calc(var(--cell-size) * ${32 / 36}))`,
          "--line-color": "rgb(55 65 81)",
          width: `calc(var(--cell-size) * ${BOARD_SIZE})`,
          height: `calc(var(--cell-size) * ${BOARD_SIZE})`
        }}
      >
        <div
          className="absolute inset-0 rounded-md"
          style={{
            backgroundSize: "var(--cell-size) var(--cell-size)",
            backgroundImage: `
              linear-gradient(to right, var(--line-color) 1px, transparent 1px),
              linear-gradient(to bottom, var(--line-color) 1px, transparent 1px)
            `,
            backgroundPosition: `calc(var(--cell-size) / 2) calc(var(--cell-size) / 2)`
          }}
        />
        <div className="absolute inset-0 border border-[var(--line-color)] rounded-md" />

        {Array.from({ length: BOARD_SIZE }).map((_, rowIndex) =>
          Array.from({ length: BOARD_SIZE }).map((__, colIndex) => {
            const cellValue = board[rowIndex][colIndex];
            const isHovered = hoveredCell?.row === rowIndex && hoveredCell?.col === colIndex;
            const showPreview = cellValue === EMPTY && !winner && isHovered;

            return (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={cn(
                  "absolute flex items-center justify-center",
                  cellValue === EMPTY && !winner && "cursor-pointer"
                )}
                style={{
                  top: `calc(var(--cell-size) * ${rowIndex} + var(--cell-size) / 2)`,
                  left: `calc(var(--cell-size) * ${colIndex} + var(--cell-size) / 2)`,
                  width: "var(--cell-size)",
                  height: "var(--cell-size)",
                  transform: "translate(-50%, -50%)"
                }}
                onClick={() => handleCellClick(rowIndex, colIndex)}
                onMouseEnter={() => setHoveredCell({ row: rowIndex, col: colIndex })}
                onMouseLeave={() => setHoveredCell(null)}
              >
                {(cellValue !== EMPTY || showPreview) && (
                  <div
                    className={cn(
                      "w-[var(--stone-size)] h-[var(--stone-size)] rounded-full shadow-md",
                      cellValue === BLACK && "bg-black",
                      cellValue === WHITE && "bg-white",
                      showPreview && currentPlayer === BLACK && "bg-black/30",
                      showPreview && currentPlayer === WHITE && "bg-white/30"
                    )}
                  />
                )}
              </div>
            );
          })
        )}
      </div>

      <Button onClick={restartGame}>Restart Game</Button>
    </div>
  );
}

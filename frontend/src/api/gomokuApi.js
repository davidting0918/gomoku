import axios from "axios";

const BASE_URL = "http://localhost:8000";

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
});

const api = {
  async getBoard() {
    const res = await client.get("/game/board");
    return res.data;
  },
  async makeMove(x, y, player) {
    return client.post("/game/move", { x, y, player });
  },
  async resetGame() {
    return client.post("/game/reset");
  }
};

export default api;

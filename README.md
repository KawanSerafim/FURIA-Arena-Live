# 🐾 FURIA Arena Live - AI Second Screen Experience

> 🇧🇷 **Ler em Português:** [Clique aqui para ver a documentação em Português](README.pt-br.md)

> **Version:** 1.0.1 (Stable)  
> **Deploy:** [Live Demo on Render](https://furia-arena-live.onrender.com)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AI](https://img.shields.io/badge/AI-Google_Gemini-orange?style=for-the-badge&logo=google&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 🎯 About the Project

**FURIA Arena Live** is a "Second Screen" application designed to engage esports fans during CS2 matches. The system creates a real-time chat room where an **AI-powered Bot ("Furião")** interacts with fans, celebrates scores, and answers team-related questions, all while being fully context-aware of the current match state.

This project was developed as a submission for a **Software Engineering Technical Challenge**.

---

## ⚠️ Note on Data Architecture (Vision vs. Prototype)

For the purpose of this MVP (Minimum Viable Product) and technical demonstration, the system operates in **"Sandbox Mode"**.

* **The Ideal Vision:** In a production environment, the application would consume official esports webhooks or APIs (such as HLTV, Pandascore, or Grid) to automate score updates and match events.
* **Current Implementation:** To ensure full testability and control during the demo presentation, an **Admin Command System** was implemented. This allows the operator to manually simulate events (goals, map changes, game over), triggering immediate reactions from both the AI and the Frontend via WebSockets.

---

## 🚀 Key Features

### 📡 Real-Time & Connectivity
* **WebSockets (Full-Duplex):** Instant bidirectional communication between server and clients. Zero latency for chat messages and score updates.
* **Dynamic HUD:** The scoreboard, tournament name, and map update across all connected clients instantly without page refreshes (SPA feel).

### 🧠 Artificial Intelligence (Powered by Gemini 2.0 Flash)
* **"Furião" Bot:** A persona configured to act as a hardcore fan.
* **Context Awareness:** The bot "knows" the game state. If you ask "Are we winning?", it analyzes the current scoreboard before answering.
* **Memory Management:** The system automatically resets the AI's short-term memory when critical context changes (e.g., changing the opponent) to prevent hallucinations.

### ❤️ Sentiment Analysis (The Thermometer)
* **Visual Engagement:** An algorithm analyzes chat messages in real-time. Supportive words ("Let's go", "Win") heat up the thermometer; complaints cool it down.

### 📱 Responsive UX/UI
* **Mobile First:** Interface fully adapted for mobile devices, handling virtual keyboards and iPhone Safe Areas correctly.
* **Dark Mode:** Visual identity aligned with the FURIA brand.

---

## 🛠️ Engineering & Design Patterns

The codebase follows **Clean Architecture** principles to ensure scalability and testability.

### 1. Observer Pattern (Backend)
Used to decouple the Business Logic (`GameEngine`) from the Transport Layer (`ConnectionManager`).
> *When the score changes, the Engine simply "notifies". The Connection Manager listens and broadcasts the update to thousands of connected fans.*

### 2. Clean Architecture & SOLID
* `app/models`: **Pydantic DTOs** for strict data validation.
* `app/services`: Pure logic (AI, Game Rules), with no HTTP dependencies.
* `app/routers`: Controllers managing only input/output data.

### 3. Singleton
Single state management for the match, ensuring all users see the exact same synchronized scoreboard.

---

## 🎮 Admin Command Guide (Sandbox)

Since we are not connected to a real CS2 API, use these chat commands to **simulate** the match flow:

| Command | Action | System Reaction |
| :--- | :--- | :--- |
| `/gol` | Add 1 point to FURIA | Score updates, Thermometer rises, AI celebrates. |
| `/perdeu` | Add 1 point to Opponent | Score updates, Thermometer drops, AI reacts. |
| `/adv [NAME]` | Change Opponent Name | HUD updates, AI memory reset for new context. |
| `/mapa [NAME]` | Change Map (e.g., Mirage) | HUD updates, AI comments on the map. |
| `/jogo [NAME]` | Change Tournament Name | HUD updates (e.g., "Shanghai Major"). |
| `/reset` | Reset Everything | Score 0-0, AI rebooted. |

---

## 💻 Local Installation & Run

### Prerequisites
* Python 3.10+
* Google Gemini API Key (Google AI Studio)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/FURIA-Arena-Live.git](https://github.com/your-username/FURIA-Arena-Live.git)
    cd FURIA-Arena-Live
    ```

2.  **Create virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # or
    .\.venv\Scripts\activate   # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=YourKeyHere
    ```

5.  **Run the server:**
    ```bash
    python -m app.main
    ```

6.  **Access:** Open `http://localhost:8000` in your browser.

---

## 📂 Project Structure

```text
├── app/
│   ├── core/           # Configs (Env vars)
│   ├── models/         # Pydantic Schemas (DTOs)
│   ├── routers/        # WebSocket Endpoints
│   ├── services/       # Business Logic (AI, Engine, Socket Manager)
│   └── main.py         # Application Entrypoint
├── static/             # Frontend (HTML, CSS, JS separated)
├── .env                # (Not versioned)
└── requirements.txt    # Dependencies
```

---

📄 Disclaimer
This is an educational and non-official project, developed as part of a technical portfolio. It has no commercial affiliation with FURIA Esports, Valve, or Google. All trademarks belong to their respective owners.

Developed with 🖤 and ☕ by Kawan Serafim.
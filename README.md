# ⚡ CodePilot AI

> **Next-generation pair programming and code-debugging assistant built for high-speed AI inference.**

---

## 🚀 Overview
**CodePilot AI** is an intelligent developer assistant designed to help programmers debug code, structure clean architectures, and optimize queries instantly. It features a sleek cyberpunk glassmorphism UI, real-time conversational memory, interactive quick-action prompt cards, and high-speed LLM response generation.

---

## 🛠️ Tech Stack & Architecture
* **Frontend & UI:** Python, Streamlit
* **Styling:** Custom CSS Glassmorphism & Cyberpunk Dark Theme[cite: 1]
* **AI Inference Core:** OpenAI Python Client configured for high-speed API endpoints (Groq / Nebius AI Cloud)[cite: 1]
* **State Management:** Streamlit Session State for in-memory session persistence[cite: 1]

---

## 📂 Project Structure
The project is built around an all-in-one standalone architecture designed for rapid deployment:
* **`app_ui.py`**: The main application file containing the Streamlit UI layout, custom CSS styles, sidebar controls, session state handlers, and OpenAI client integration[cite: 1].
* **`requirements.txt`**: Lists all project dependencies including `streamlit`, `openai`, `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `python-dotenv`, and `requests`.
* **`.env`**: Local environment configuration file used to securely store API keys (excluded from GitHub).

---

## ⚙️ Local Setup & Installation Instructions

Follow these steps to run CodePilot AI locally on your machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/codepilot-ai.git](https://github.com/your-username/codepilot-ai.git)
cd codepilot-ai

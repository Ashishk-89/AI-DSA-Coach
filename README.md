<div align="center">
  <h1>🧠 AI DSA Coach</h1>
  <p><em>Your intelligent companion for mastering Data Structures & Algorithms.</em></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
  [![Gemini](https://img.shields.io/badge/AI-Google_Gemini-8E75B2?style=for-the-badge)](https://deepmind.google/technologies/gemini/)
</div>

<br/>

## 📋 Overview

**AI DSA Coach** is a next-generation learning platform that combines a LeetCode-like coding environment with a multi-agent AI mentor system. It dynamically adapts to your skill level (Beginner to Advanced), gently guides you through your thought process, and evaluates your code!

## 🚀 Key Features

*   **🗣️ Mentor Agent:** Fosters critical thinking by evaluating your approach *before* you write code. Provides hints based on your skill level without giving away the answer.
*   **💻 Code Agent:** Runs and evaluates your code for correctness, edge cases, and time/space complexity optimality.
*   **📈 Evaluation Agent:** Generates a comprehensive summary of your performance, tracks hint usage, and updates your progression.

---

## 🛠️ Quick Start

### 📦 Installation

```bash
git clone https://github.com/suyash242004/AI-DSA-Coach.git
cd AI-DSA-Coach

# Install Backend / Streamlit dependencies
pip install -r requirements.txt

# Install Frontend dependencies (Next.js)
cd frontend
npm install
```

### 🚀 Running the App (Two Options)

#### Option 1: Classic Streamlit Interface
This runs the original monolithic interface.
```bash
cd AI-DSA-Coach
streamlit run app.py
# Or run demo.py for an alternative interface:
streamlit run demo.py
```
*Available at `http://localhost:8501`*

#### Option 2: Modern Next.js Interface (Recommended)
This runs the new high-performance, split-pane IDE interface. **Requires 2 Terminals.**

**Terminal 1 (Backend):**
```bash
cd AI-DSA-Coach
.\run_backend.bat
# Or manually: uvicorn backend.api:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd AI-DSA-Coach/frontend
npm run dev
```
*Available at `http://localhost:3000`*

---

## 🎮 How to Use

1. **Pick a Challenge:** Select a DSA problem from the dropdown.
2. **Discuss Approach:** Explain your strategy to the Mentor Agent.
3. **Write Code:** Implement your approved logic in the built-in editor.
4. **Get Feedback:** Analyze your performance and learn from detailed feedback!

<div align="center">
  <i>Built with ❤️</i>
</div>

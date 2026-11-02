# 🎓 EduMind AI — University Student Assistant

A responsive, AI-powered web application designed to help university students organize their academic activities, master difficult concepts, synthesize lecture notes, generate self-assessment quizzes, and review code.

---

## 🌟 Project Overview & Features

### 1. Modern Responsive Frontend (Task 1)
- **Homepage & Dashboard:** Clean introduction banner with academic course tags and quick starter cards.
- **Multimodal Student Input:** Select from 5 assistance capabilities:
  - 🧠 **Explain Concept:** Theoretical breakdown, analogies, call-stack traces, and exam tips.
  - 📝 **Summarize Notes:** High-yield executive summary, core bullet points, and flashcards.
  - 🎯 **Practice Quiz:** Self-assessment questions with multiple choice options and answer keys.
  - 💻 **Code Review & Debug:** Time/space complexity ($O(N)$) analysis, edge-case guards, and refactored code.
  - 📅 **Study Planner:** 5-day study sprints and Pomodoro revision intervals.
- **Dynamic AI Response Display:** Formatted Markdown rendering with code syntax styling, copy-to-clipboard, and loading skeletons.
- **Responsive & Themed:** Responsive desktop and mobile layouts with a toggleable Dark/Light mode.

### 2. Dual-Engine AI Integration (Task 2)
- **Live LLM API Integration:** Seamlessly supports Google Gemini or OpenAI API via environment variables.
- **Intelligent Local Simulated AI Service:** Built-in offline academic engine producing structured pedagogical guidance without requiring API keys.
- **Dynamic Asynchronous Updates:** Client-side `fetch()` communicates with the backend without page reloads.
- **Input Validation & Feedback:** Real-time character count, empty input prevention with shake animation, and error alerts.

### 3. Backend & Relational Database (Task 3)
- **Zero-Dependency Python REST Server:** Built natively with Python's standard library `http.server` — no external pip packages required.
- **SQLite Relational Persistence (`student_assistant.db`):** Automatically saves student queries, AI answers, selected mode, and timestamps.
- **History Drawer:** Browse, review, and delete previous study sessions directly from the UI.
- **Defensive API Design:** Parameterized SQL queries to eliminate SQL injection and clean HTTP status codes (200, 201, 400, 404).

### 4. AI-Assisted Development & Testing (Task 4)
- Documented in detail inside [`SUBMISSION_REPORT.md`](SUBMISSION_REPORT.md).
- Automated test suite in [`test_app.py`](test_app.py) verifying AI generation and SQLite CRUD.

---

## 📂 Simplified File Structure

```
student_assistant/
├── app.py                # Complete Backend: HTTP Server, SQLite Database & AI Engine
├── index.html            # Complete Frontend: HTML5, CSS Styling & JavaScript Logic
├── test_app.py           # Automated Test Suite (Task 4)
├── SUBMISSION_REPORT.md  # Comprehensive Task 4 Submission Evidence & Report
├── student_assistant.db  # SQLite Relational Database (Auto-created)
└── README.md             # Project Documentation & Setup Guide
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher installed on your computer.
- No external packages or `pip install` commands needed!

### Running the Web Application
1. Open your terminal in this project folder:
   ```bash
   python3 app.py
   ```
2. Your browser will automatically open to:
   ```
   http://127.0.0.1:8000
   ```
   *(If it does not open automatically, simply click or paste the link above into your browser).*

3. Press `Ctrl + C` in your terminal to stop the server when done.

---

## 🧪 Running Automated Tests (Task 4)

To run the automated test suite verifying both the AI engine and SQLite database persistence:

```bash
python3 test_app.py
```

**Expected Test Output:**
```
test_1_ai_generation (__main__.TestStudentAssistant.test_1_ai_generation)
Verify AI produces structured output across modes. ... 
✅ Test 1 Passed: AI generated explanation successfully.
ok
test_2_database_persistence (__main__.TestStudentAssistant.test_2_database_persistence)
Verify database saves, retrieves, and deletes records. ... 
✅ Test 2 Passed: SQLite database successfully saved and retrieved record.
ok

----------------------------------------------------------------------
Ran 2 tests in 0.30s

OK
```

---

## 👤 Author
- **Name:** Umama Manzoor
- **GitHub:** [@umama-24](https://github.com/umama-24)

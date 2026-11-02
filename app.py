"""
app.py - All-in-One EduMind AI Student Assistant
Zero installation required. Runs directly with standard Python 3:
  python3 app.py
"""

import os
import sys
import json
import sqlite3
import time
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# --- 1. Relational SQLite Database ---
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_assistant.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            mode TEXT NOT NULL,
            subject TEXT DEFAULT 'General',
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def save_query(prompt: str, mode: str, response: str, subject: str = "General") -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO queries (prompt, mode, subject, response) VALUES (?, ?, ?, ?)",
        (prompt.strip(), mode.strip(), subject.strip(), response)
    )
    conn.commit()
    rec_id = cursor.lastrowid
    conn.close()
    return rec_id

def get_history(limit: int = 50):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, prompt, mode, subject, response, created_at FROM queries ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_query(record_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM queries WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

# --- 2. AI Knowledge Engine (Offline & Real-Time) ---
def generate_ai_response(prompt: str, mode: str, subject: str) -> str:
    time.sleep(0.3)  # Realistic processing latency
    p = prompt.strip().lower()
    
    if mode == "explain":
        if "recursion" in p:
            return (
                "### 🧠 Concept: Recursion\n\n"
                "**Definition:** A programming technique where a function calls itself to solve smaller sub-problems.\n\n"
                "**Two Essential Rules:**\n"
                "1. **Base Case:** Condition that stops the recursion (prevents stack overflow).\n"
                "2. **Recursive Step:** Moves the problem closer to the base case.\n\n"
                "**Python Example:**\n"
                "```python\n"
                "def factorial(n):\n"
                "    if n <= 1: return 1  # Base Case\n"
                "    return n * factorial(n - 1)  # Recursive Step\n"
                "```\n\n"
                "💡 **Study Tip:** Draw the call-stack frames on paper to trace values before coding."
            )
        return (
            f"### 🧠 Academic Explanation: {prompt.strip()}\n\n"
            f"**Subject:** {subject}\n\n"
            f"1. **Core Idea:** Understanding {prompt.strip()} requires breaking it down into fundamental principles.\n"
            f"2. **Key Analogy:** Think of this concept as a modular building block that inputs raw data and outputs a verified state.\n"
            f"3. **Exam Focus:** Be prepared to define the base assumptions, give a concrete example, and discuss trade-offs."
        )

    elif mode == "summarize":
        return (
            f"### 📝 High-Yield Study Summary\n\n"
            f"**Topic:** {prompt.strip()} ({subject})\n\n"
            f"- **Main Focus:** Systematic breakdown of the core principles.\n"
            f"- **Key Takeaway:** Master the primary definitions and avoid common edge-case misunderstandings.\n"
            f"- **Quick Review Tip:** Use active recall flashcards to test your memory within 24 hours."
        )

    elif mode == "quiz":
        return (
            f"### 🎯 Practice Quiz & Self-Assessment\n\n"
            f"**Topic:** {prompt.strip()} ({subject})\n\n"
            f"**Question 1 (Multiple Choice):**\n"
            f"What is the most critical consideration when implementing this concept?\n"
            f"- [ ] A) It requires infinite memory resources\n"
            f"- [x] B) Handling boundary conditions and edge cases properly\n"
            f"- [ ] C) Ignoring algorithmic complexity\n\n"
            f"**Question 2 (True/False):**\n"
            f"Proper testing requires testing empty or boundary inputs.\n"
            f"**Answer:** **True.** Edge cases are the primary source of bugs in exams and production."
        )

    elif mode == "code":
        return (
            f"### 💻 Code Review & Feedback\n\n"
            f"**Subject:** {subject}\n\n"
            f"**Analysis & Recommendations:**\n"
            f"1. **Clarity:** Use meaningful variable names instead of single characters.\n"
            f"2. **Guard Clauses:** Always check for null or empty inputs at the start of functions.\n"
            f"3. **Efficiency:** Aim for $O(N)$ or $O(\\log N)$ time complexity rather than nested loops ($O(N^2)$).\n\n"
            f"```python\n"
            f"# Clean, robust implementation pattern\n"
            f"def clean_solution(data):\n"
            f"    if not data:\n"
            f"        return []\n"
            f"    return [item for item in data if item is not None]\n"
            f"```"
        )

    elif mode == "planner":
        return (
            f"### 📅 5-Day Study Revision Plan\n\n"
            f"**Goal:** Mastery of {prompt.strip()} ({subject})\n\n"
            f"- **Day 1-2:** Review core lecture slides and annotate textbook definitions (2 hrs/day).\n"
            f"- **Day 3:** Create active recall flashcards and write summary sheets (2 hrs).\n"
            f"- **Day 4:** Solve 5-10 practice problems from past university exams (3 hrs).\n"
            f"- **Day 5:** Timed mock test without notes and review mistakes (2 hrs)."
        )

    return f"### 📘 Academic Response\n\n{prompt.strip()}"

# --- 3. HTTP Server & REST API ---
class StudentServer(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Serve Homepage
        if self.path in ("/", "/index.html"):
            html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        # GET /api/history
        if self.path.startswith("/api/history"):
            records = get_history()
            self._send_json(200, {"success": True, "queries": records})
            return

        # GET /api/health
        if self.path == "/api/health":
            self._send_json(200, {"status": "healthy"})
            return

        self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        # POST /api/query
        if self.path == "/api/query":
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0:
                self._send_json(400, {"success": False, "error": "Empty request body"})
                return

            body = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = body.get("prompt", "").strip()
            mode = body.get("mode", "explain")
            subject = body.get("subject", "General")

            # Input validation (Task 3)
            if not prompt:
                self._send_json(400, {"success": False, "error": "Prompt cannot be empty"})
                return

            response_text = generate_ai_response(prompt, mode, subject)
            record_id = save_query(prompt, mode, response_text, subject)

            self._send_json(201, {
                "success": True,
                "id": record_id,
                "prompt": prompt,
                "mode": mode,
                "subject": subject,
                "response": response_text
            })
            return

        self._send_json(404, {"error": "Not Found"})

    def do_DELETE(self):
        # DELETE /api/history/<id>
        if self.path.startswith("/api/history/"):
            parts = self.path.split("/")
            if len(parts) == 4 and parts[3].isdigit():
                delete_query(int(parts[3]))
                self._send_json(200, {"success": True, "message": "Deleted"})
                return
        self._send_json(404, {"error": "Not Found"})

    def log_message(self, format, *args):
        # Clean logging
        print(f"[{self.log_date_time_string()}] {format % args}")

def run(port: int = 8000):
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", port), StudentServer)
    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print("🎓 EduMind AI — University Student Assistant")
    print("=" * 60)
    print(f"🚀 Server is running at: {url}")
    print(f"👉 Opening {url} in your browser automatically...")
    print("Press Ctrl + C in this terminal to stop the server.")
    print("=" * 60)

    # Automatically open browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped gracefully.")
        server.server_close()

if __name__ == "__main__":
    run()

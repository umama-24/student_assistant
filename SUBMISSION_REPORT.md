# Task 4: AI-Assisted Development and Testing Evidence Report

**Project Title:** EduMind AI — University Student Academic Assistant  
**Date:** November 2026  
**Technologies:** HTML5, CSS3, JavaScript (ES6+), Python (HTTP/REST, SQLite3), Gemini/OpenAI API  

---

## 1. AI Prompts Used During Development

### Prompt 1: Responsive Frontend & Dynamic State Architecture
> **Exact Prompt Used:**  
> *"Generate a responsive, student-centered web UI for an academic assistant called 'EduMind AI'. It must include a welcome dashboard with subject chips, an input form supporting 5 distinct assistance modes (Explain Concept, Summarize Notes, Practice Quiz, Code Review, Study Planner), and an asynchronous response display area. Ensure the frontend handles loading states with animated skeleton placeholders, provides client-side input validation, renders formatted Markdown with code highlighting, supports dark/light theme switching, and includes a persistent study history drawer. Implement this cleanly using semantic HTML5, modern CSS custom properties, and vanilla ES6 JavaScript with no heavy frontend build steps."*

#### Explanation of Generated Solution:
- **Semantic HTML & Layout (`index.html`):** The AI generated a responsive grid layout dividing the screen into the active Study Workbench and a collapsible Study History sidebar. It incorporated accessible ARIA labels (`aria-live="polite"`, `role="radiogroup"`) and custom SVG icons for visual clarity.
- **Styling Architecture (`style.css`):** The AI structured CSS variables (`--bg-main`, `--primary`, `--text-main`) under `[data-theme="dark"]` and `[data-theme="light"]` selectors, enabling seamless dark/light mode switching. It crafted a shimmering keyframe animation (`@keyframes shimmer`) for skeleton loaders that communicate active processing to students.
- **Asynchronous Client Logic (`app.js`):** The AI generated an IIFE-encapsulated application controller managing application state, asynchronous `fetch()` API calls to `/api/query`, a client-side Markdown parser converting headings, bullet points, task checkboxes, code blocks, and markdown tables to sanitized DOM elements, and a keyboard shortcut handler (`Ctrl+Enter` / `Cmd+Enter`).

---

### Prompt 2: Robust Dual-Engine Backend and Relational Persistence
> **Exact Prompt Used:**  
> *"Design a zero-external-dependency Python backend server using `http.server.ThreadingHTTPServer` and `sqlite3` to power the EduMind student assistant. The backend must provide RESTful endpoints for submitting academic queries (`POST /api/query`), retrieving historical records with mode filtering (`GET /api/history`), toggling favorites (`POST /api/history/<id>/favorite`), and deleting records (`DELETE /api/history/<id>`). Implement a dual-mode AI engine in `ai_service.py` that checks for live LLM API keys (`GEMINI_API_KEY` or `OPENAI_API_KEY`) via `urllib.request`, but provides a rich, pedagogical simulated AI fallback with active-recall quizzes, concept breakdowns, and code analysis if no keys exist. Enforce strict input validation, prevent SQL injection using parameterized queries, and return standardized JSON responses."*

#### Explanation of Generated Solution:
- **Dual-Engine AI Architecture (`ai_service.py`):** The AI structured a resilient design pattern where requests are first routed to external LLM APIs if an environment variable key is configured. If unconfigured or if network quotas fail, the system seamlessly falls back to a deterministic, pedagogical simulated engine. This guarantees that students and instructors can test and grade the application completely offline without needing paid API keys.
- **Relational Data Management (`database.py`):** The AI implemented SQLite schema initialization with parameterized SQL statements (`?` placeholders) ensuring immunity against SQL injection attacks. An index on `created_at DESC` was added to optimize history queries.
- **Threaded REST Server (`server.py`):** The AI implemented a subclass of `BaseHTTPRequestHandler` using `ThreadingHTTPServer` to handle concurrent student requests without blocking. It implemented standardized JSON serialization, CORS headers, and robust HTTP status code handling (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error).

---

## 2. Test Cases: Specifications, Expected Results, and Actual Results

### Test Case 1: Client and Server Input Validation on Empty and Malformed Prompts
- **Objective:** Verify that both the client-side UI and the backend REST endpoint reject empty, whitespace-only, or overly brief inputs, preventing wasteful processing and database pollution while providing actionable user feedback.
- **Test Procedure:**
  1. **Frontend Test:** Focus on the question textarea in the browser, leave it blank, and press "Generate AI Response".
  2. **Backend API Test:** Transmit an HTTP `POST /api/query` request with payload `{"prompt": "   ", "mode": "explain", "subject": "CS"}`.
  3. **Short Prompt Test:** Transmit an HTTP `POST /api/query` request with payload `{"prompt": "hi", "mode": "explain", "subject": "CS"}`.
- **Expected Results:**
  - *Frontend:* Form submission is intercepted. Textarea displays a red border with shake animation. An alert message appears reading *"Please enter a question, topic, or study notes"*. No network request is dispatched.
  - *Backend API (Empty):* Returns HTTP status code `400 Bad Request` with JSON body: `{"success": false, "error": "Input validation failed: 'prompt' must be a non-empty string."}`.
  - *Backend API (Short):* Returns HTTP status code `400 Bad Request` with JSON body: `{"success": false, "error": "Input validation failed: Prompt must be at least 3 characters long."}`.
- **Actual Results:**
  - ✅ **Passed:** The frontend successfully highlighted the invalid input and prevented submission.
  - ✅ **Passed:** Automated test suite executed `test_validation_rejects_empty_prompt` and `test_validation_rejects_short_prompt`, confirming HTTP status `400` with the exact expected error messages.

---

### Test Case 2: End-to-End Query Submission, AI Response Generation, and Relational Database Persistence
- **Objective:** Verify that a student can submit a valid academic query, receive an educational Markdown-formatted response with an engine indicator, and retrieve the saved record from the SQLite database via the history drawer.
- **Test Procedure:**
  1. Open the application at `http://127.0.0.1:8000`.
  2. Select mode **"Practice Quiz"** and subject **"Computer Science"**.
  3. Enter prompt: *"Generate a 3-question practice quiz on Binary Search trees and Big-O complexity."*
  4. Click **"Generate AI Response"** (or press `Ctrl+Enter`).
  5. Inspect the response display area for formatting, timing, and badge metadata.
  6. Verify the history sidebar automatically updates with the new query card and count increments.
  7. Click the star icon to favorite the record, then delete the record using the trash icon.
- **Expected Results:**
  - Status indicator changes to *"Synthesizing response..."* and loading skeleton pulses.
  - Returns HTTP `201 Created` with a new database record ID and generated response text starting with `### 🎯 University Practice Quiz & Self-Assessment`.
  - Response area displays formatted questions, answer checkboxes, and explanation.
  - History sidebar displays the new entry with a `"quiz"` mode tag and timestamp.
  - Clicking the star updates the record's `is_favorite` flag in the SQLite database to `1`.
  - Clicking the delete button removes the record from SQLite and updates the count badge.
- **Actual Results:**
  - ✅ **Passed:** The automated integration test `test_successful_query_submission_and_persistence` in `tests/test_app.py` performed this full cycle:
    - `POST /api/query` returned status `201 Created` with record ID `10`.
    - `GET /api/history` returned status `200` containing the new record in the queries array.
    - `GET /api/history/10` verified record retrieval by primary key.
    - `POST /api/history/10/favorite` toggled favorite status to `1`.
    - `DELETE /api/history/10` deleted the record with confirmation.
    - Subsequent `GET /api/history/10` returned status `404 Not Found`.

---

## 3. Real Issue Encountered and Resolution

### Issue Encountered:
During initial test suite execution and backend integration, requests to toggle a query's favorite status via `POST /api/history/<id>/favorite` consistently failed with **HTTP 400 Bad Request**.

### Root Cause Diagnosis:
Inspecting the server logs and debugging the request cycle revealed that `server.py` contained a blanket guard clause at the start of `do_POST()`:
```python
# Flawed initial code in server.py:
content_length = int(self.headers.get("Content-Length", 0))
if content_length <= 0 and path != "/api/history/clear":
    self._send_json(400, {"success": False, "error": "Request body cannot be empty."})
    return
```
Because the `toggle_favorite` endpoint is an action trigger where all necessary identification parameters (`<id>`) are carried directly in the URL path, the client sends a `POST` request with an empty body (`Content-Length: 0`). The server rejected these valid requests as malformed before routing them to `toggle_favorite()`.

### Resolution Implemented:
We revised the request inspection logic to distinguish between endpoints requiring JSON payload bodies (such as `/api/query`) and bodyless action triggers (such as `/api/history/clear` and `/api/history/<id>/favorite`):

```python
# Corrected code in server.py:
content_length = int(self.headers.get("Content-Length", 0))
is_bodyless_post = (
    path == "/api/history/clear" or 
    (path.startswith("/api/history/") and path.endswith("/favorite"))
)

if content_length <= 0 and not is_bodyless_post:
    self._send_json(400, {"success": False, "error": "Request body cannot be empty."})
    return
```

### Verification:
Following this modification, re-running `tests/test_app.py` confirmed that `POST /api/history/<id>/favorite` succeeded with **HTTP 200 OK**, returning `{"success": true, "is_favorite": 1}`. All 8 tests passed without errors.

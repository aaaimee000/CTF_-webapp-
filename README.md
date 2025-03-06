# CTF_-webapp-


# CTF Web App (SQLi & XSS Challenges)

A vulnerable web application designed for Capture The Flag (CTF) practice, featuring SQL Injection and Cross-Site Scripting (XSS) challenges.

## Overview
- **SQL Injection Challenge**: Bypass login to retrieve a hidden flag.
- **XSS Challenge**: Steal a cookie containing the flag via stored XSS.
- **Intentionally Vulnerable**: Do NOT deploy this in a production environment.

## Prerequisites
- Python 3.x
- pip3 (Python package manager)
- SQLite3 (preinstalled on macOS/Linux)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ctf-webapp.git
   cd ctf-webapp
   ```

2. **Install dependencies** (Flask):
   ```bash
   pip3 install flask
   ```

## Usage
1. **Run the app**:
   ```bash
   python3 app.py
   ```
   - The app will start at `http://localhost:5000`.

2. **Access challenges**:
   - **Homepage**: `http://localhost:5000`
   - **SQL Injection**: `http://localhost:5000/sqli-login`
   - **XSS Challenge**: `http://localhost:5000/xss-comment`

## Challenges & Flags
### 1. SQL Injection
- **Objective**: Bypass the login to retrieve the flag.
- **Exploit**: 
  - Username: `' OR 1=1 --` (leave password empty)
  - **Flag**: `FLAG_SQLI_123` (stored in the `users` table).

### 2. XSS (Cross-Site Scripting)
- **Objective**: Steal the cookie containing the flag.
- **Exploit**: 
  - Submit `<script>alert(document.cookie)</script>` as a comment.
  - **Flag**: `FLAG_XSS_COOKIE_456` (set in the browser cookie).

## Security Notes
- 🔒 **Isolation**: Run this app in a VM/Docker container or disposable environment.
- ♻️ **Reset Database**: Delete `ctf.db` and restart the app to clear data:
  ```bash
  rm ctf.db && python3 app.py
  ```
- 🚫 **Never expose this app to the public internet**.

## File Structure
```
.
├── app.py             # Flask backend
├── README.md          # This file
├── templates/         # HTML pages
│   ├── index.html
│   ├── sqli_login.html
│   └── xss_comment.html
└── ctf.db             # Database (auto-created)
```

## Troubleshooting
- **Blank Page**:
  - Ensure the `templates` folder exists and contains the HTML files.
  - Hard-refresh the page (`Ctrl + Shift + R` or `Cmd + Shift + R`).
- **"Template Not Found" Error**:
  - The `templates` folder must be in the same directory as `app.py`.
- **Port Conflict**:
  - Kill existing processes on port 5000:
    ```bash
    lsof -ti:5000 | xargs kill -9
    ```

---

## Disclaimer
This app contains intentional vulnerabilities for educational purposes. Do not use insecure code patterns in real-world applications.
```

---

### How to Use the README:
1. Create the file:
   ```bash
   touch README.md
   ```
2. Paste the content above into it.
3. Update the "Clone the repository" URL with your actual Git repo (if applicable).

###CTF Walkthrough

1. Perform SQL Injection

- Extract the encryption key from keys_table.
- Extract the video ID (42) from videos table.
2. Retrieve the Encrypted Video

- Access /get_video?id=42 and download secret_video.enc.
3. Decrypt the Video Using OpenSSL

- openssl aes-256-cbc -d -in secret_video.enc -out secret_video.mp4 -k "mysecretkey123"

4. Watch the Decrypted Video

5. Open secret_video.mp4 and find the next hint.


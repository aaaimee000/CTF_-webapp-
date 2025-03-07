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
- Extract the video ID (1) from videos table.
2. Retrieve the Encrypted Video

- Access /get_video?id=1 and download secret_video.enc.
3. Decrypt the Video Using OpenSSL

- openssl aes-256-cbc -d -in secret_video.enc -out secret_video.mp4 -k "OMNI_AI_VIDEO_KEY_619"

4. Watch the Decrypted Video

5. Open secret_video.mp4 and find the next hint.


# WHAT DO WE NEED TO GIVE THEM HINT -- can be included in the brief
1. tell them in the previous flag or on the website, username is admin, password is password123, and there are four tables in the web app, their names are users, keys_table, videos, and comments. 
2. tell them what encryption it is -- aes-256-cbc



# SQL injection 
### BEST TO INJECT TO GET A LIST OF TABLES FIRST -- this does not work anymore because i hardcode it to return from users[0] so it works to return the decryption key, but if you need below to work, users[3] with the following sql injection command would work. 

1. ' UNION SELECT NULL, NULL, NULL, group_concat(name, char(124)) FROM sqlite_master WHERE type='table' --
2. return "Flag: users|comments|videos|keys_table | Access /get_video?id=1"


## when doing it properly as a hacker
1. enter username as admin
2. enter password as ' UNION SELECT (SELECT decryption_key FROM keys_table LIMIT 1), NULL, NULL, NULL -- 
3. it will return you with the flag as key, and the location of the video 
### how do they know the number of fields? BY TRYING, because the prompt will tell them. 
1. If they did less than the fields, e.g.,
' UNION SELECT (SELECT decryption_key FROM keys_table LIMIT 1), NULL, NULL --

It will return " Error: SELECTs to the left and right of UNION do not have the same number of result columns", prompting them to reduce or increase the number of fields. 



## if you did it without sql injection or incorrectly-- still as admin
1. enter username as admin, or ' OR '1'='1
2. enter password as password123, ' OR '1'='1
3. it will return you a wrong flag, it will display: Flag: admin | Access /get_video?id=1 (location is still correct)

## if you did it without admin 
1. enter wrong username or wrong password, it will tell you "ACCESS DENIED: Insufficient clearance."



Download and decrypt video 

openssl aes-256-cbc -d -in secret_video.enc -out decrypted_video.mp4 -k "OMNI_AI_VIDEO_KEY_619"


3. File Setup Instructions
* Encrypt the Video:

openssl aes-256-cbc -e -in secret_video.mp4 -out secret_video.enc -k "OMNI_AI_VIDEO_KEY_619"

* Place secret_video.enc in your project folder.

* Update init_db() to insert the encrypted video (code provided above).


progress
1. frontend with a countdown 
2. simple sql injection --> changed to advance one where you need to get an encryption key from database _key, then use this encryptionkey to decrypt our video file, by downloading it form our website, then watch it -- Siam 's flag 
3. 

TODO Update:
### experimentwith video encrypt, then serve it on webapp
#### next flag--   XSS
#### need to see what exactly is the decryption key
#### frontend of sql 




--------------
Final CTF Flow
SQLi Challenge:

Extract decryption key from keys_table.

Use key to decrypt video for the final flag.

XSS Challenge:

Bypass <script> filtering to steal the cookie.

Both challenges are independent (no dependency between them).
# CTF_-webapp-


# CTF Web App (SQLi & XSS Challenges)

A vulnerable web application designed for Capture The Flag (CTF) practice, featuring SQL Injection and Cross-Site Scripting (XSS) challenges.

The website is hosted on Render at this link: https://ctf-webapp.onrender.com/

## Overview
- **SQL Injection Challenge**: Bypass login to retrieve a hidden flag.
- **XSS Challenge**: Steal a cookie containing the flag via stored XSS.


## Challenges & Flags
### 1. SQL Injection
#### when doing it properly as a hacker
1. enter username as admin
2. enter password as ' UNION SELECT (SELECT decryption_key FROM keys_table LIMIT 1), NULL, NULL, NULL -- 
3. it will return you with the flag as key, and the location of the video 

#### how do they know the number of fields? BY TRYING, because the prompt will tell them. 
1. If they did less than the fields, e.g.,
' UNION SELECT (SELECT decryption_key FROM keys_table LIMIT 1), NULL, NULL --

It will return " Error: SELECTs to the left and right of UNION do not have the same number of result columns", prompting them to reduce or increase the number of fields. 

#### if you did it without knowing username/pwd
1. enter wrong username or wrong password, it will tell you "ACCESS DENIED: Insufficient clearance."

#### if you did it with knowing username/pwd, incorrectly or with the most basic sql injection 
1. enter username as admin, or ' OR '1'='1
2. enter password as password123, ' OR '1'='1
3. it will return you a wrong flag, it will display: Flag: admin | Access /get_video?id=1 
(!!You get the place of the video, but clearly the flag is still incorrect since you cannot use it to decrypt the video.)



#### File Setup Instructions
* Encrypt the Video:

openssl aes-256-cbc -e -in secret_video.mp4 -out secret_video.enc -k "OMNI_AI_VIDEO_KEY_619"

* Place secret_video.enc in your project folder.

* Update init_db() to insert the encrypted video (code provided above).



### 2. XSS (Cross-Site Scripting) HONEYPOT-LIKE FUNCTION
- **Objective**: Steal the cookie containing the flag.
- **Exploit**: 
  - Submit `<script>alert(document.cookie)</script>` as a comment.
  - **MESSAGE**: `Gotchu - message that guide them to look into database` (set in the browser cookie).

## Security Notes
- 🔒 **Isolation**: Run this app in a VM/Docker container or disposable environment.
- ♻️ **Reset Database**: Delete `ctf.db` and restart the app to clear data:
  ```bash
  rm ctf.db && python3 app.py
  ```
- 🚫 **Never expose this app to the public internet**.
```


----------------------------------------------------------------------------------------------------------------

# CTF Walkthrough

1. Perform SQL Injection

- Extract the encryption key from keys_table.
- Extract the video ID (1) from videos table.
2. Retrieve the Encrypted Video

- Access /get_video?id=1 and download secret_video.enc.
3. Decrypt the Video Using OpenSSL

- openssl aes-256-cbc -d -in secret_video.enc -out secret_video.mp4 -k "OMNI_AI_VIDEO_KEY_619" 

[NOTE: this key "OMNI_AI_VIDEO_KEY_619" can be replaced with hash]

4. Watch the Decrypted Video (secret_video.mp4, ie, flag 4)

5. Open secret_video.mp4 and find the next hint.


# WHAT DO WE NEED TO GIVE THEM HINT -- can be included in the brief
1. tell them in the previous flag or on the website, username is admin, password is password123, and there are four tables in the web app, their names are users, keys_table, videos, and comments. 
2. tell them what encryption it is -- aes-256-cbc

# Things for ourselves in submission
1. See the CTF Walkthrough above. Both key and hash are included. 
2. XSS is only a bonus/ confusion to the whole CTF.



# SQL injection 


progress
1. frontend with a countdown 
2. simple sql injection --> changed to advance one where you need to get an encryption key from database _key, then use this encryptionkey to decrypt our video file, by downloading it form our website, then watch it -- Siam 's flag 
3. 

TODO Update:
#### DONE experiment with video encrypt, then serve it on webapp
#### DONE Hosting on Render
#### DONE need to see what exactly is the decryption key
#### next flag--   XSS
#### DONE frontend of sql  (when i have time i can put in a little jif on sql space, update the time part)
#### DONE put the hash below the SQL return line.
#### DONE make the time longer 



--------------
Final CTF Flow
SQLi Challenge:

Extract decryption key from keys_table.

Use key to decrypt video for the final flag.

XSS Challenge:

Bypass <script> filtering to steal the cookie.

Both challenges are independent (no dependency between them).
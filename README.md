<p align="center">
  <img src="https://img.icons8.com/fluency/96/password.png" width="90" alt="Password Icon"/>
</p>

<h1 align="center">🔐 Secure Password Manager</h1>

<p align="center">
  A Python-based password vault that encrypts credentials with a master password and stores them securely on disk.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-in%20progress-yellow" alt="Status"/>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/Encryption-AES%20Vault-orange" alt="Encryption"/>
  <img src="https://img.shields.io/badge/Security-Encrypted%20Vault-red" alt="Security"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
  <img src="https://img.shields.io/badge/Build-Stable-brightgreen" alt="Build"/>
</p>

---

## 📌 Overview

**Secure Password Manager** is a Python application that stores credentials in a **locally saved encrypted vault**.  
All sensitive values are **encrypted before being written to storage**, and vault access requires **master password authentication**.

This project demonstrates secure design practices including:

- Authentication controls (master password gate)
- Confidentiality through encryption-at-rest
- Clear separation between GUI and security logic
- Safe storage handling (no plaintext persistence)

---

## ✅ Key Features

- 🔑 Master password protected vault access  
- 🔒 Encryption before storage (no plaintext credentials)  
- ➕ Add / View / Update / Delete credential entries  
- 🎲 Optional password generator (if enabled)  
- 🧩 Modular design (GUI separate from crypto + storage)  
- 💾 Local encrypted vault file (offline-first)  

---

## 🧠 Security Model

This project follows a layered security approach:

- **Master password authentication** before accessing vault operations  
- **Encryption at rest** for stored credentials  
- **No plaintext storage** of passwords or sensitive fields  
- **Validation** to reduce errors and prevent empty/invalid entries  
- **Controlled decrypt** only after successful unlock  

> Note: For real-world production usage, security can be strengthened further with salting + key derivation (Argon2/PBKDF2), secure clipboard handling, and tamper detection.

---

## 🧩 Architecture

```text
User
 │
 ▼
Tkinter GUI
 │
 ▼
Authentication Layer
(Master Password Verification)
 │
 ▼
Crypto Engine
(Encrypt / Decrypt)
 │
 ▼
Encrypted Vault Storage
(Local File)



📁 Project Structure
secure-password-manager/
│
├── Vault_GUI.py          # Main GUI application (entry point)
├── crypto.py             # Encryption / decryption operations
├── hsm.py                # Master password verification logic
├── keystore.py           # Vault storage read/write management
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

Requirements
Python 3.10+


Run the Application
python Vault_GUI.py


Secure Password Manager
-----------------------
Email:    [__________]
Password: [__________]

[ Add Entry ]  [ View Entries ]
[ Update ]     [ Delete Entry ]


🛠 Future Enhancements/Roadmap
☁️ Encrypted cloud sync (optional + user-controlled)
🔄 Multi-device vault import/export
🧾 Secure backup + recovery workflow
🌙 Dark mode UI
🧠 Stronger key derivation (Argon2id / PBKDF2) + per-vault salt
🛡 Tamper detection (HMAC / signature on vault records)


📄 License
Licensed under the MIT License.


👨‍💻 Author
Pranjal Panta




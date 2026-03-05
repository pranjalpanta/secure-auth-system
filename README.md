<p align="center">
  <img src="https://img.icons8.com/fluency/96/password.png" width="90"/>
</p>

<h1 align="center">🔐 Secure Password Manager</h1>

<p align="center">
A Python-based encrypted credential vault with master password protection.
</p>

<p align="center">
  
![Status](https://img.shields.io/badge/status-in%20progress-yellow) 
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Encryption](https://img.shields.io/badge/Encryption-AES%20Vault-orange)
![Security](https://img.shields.io/badge/Security-Password%20Vault-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Build-Stable-brightgreen)



</p>

---

# 📌 Project Overview

This project is a **secure password manager built with Python** that stores credentials inside an **encrypted vault protected by a master password**.

All sensitive data is encrypted **before storage** and can only be accessed after successful authentication.

The system demonstrates **secure software design principles including authentication, encryption, and data protection**.

---

# ✅ Project Highlights

- 🔑 Master password protected vault
- 🔐 Strong encryption for stored credentials
- ➕ Add / View / Update / Delete credential entries
- 🎲 Optional password generator
- 🧩 Clean separation of GUI and security logic
- 💾 Local encrypted vault file storage

---

# ⚙️ Features

## 🔑 Authentication

- Master password required to unlock the vault
- Input validation for empty fields (email/password)

## 🔒 Vault Security

- No plaintext password storage
- Encrypted vault stored locally
- Decryption only after successful authentication

## 🖥️ User Interface

- Simple **Tkinter GUI**
- Easy workflow for managing credentials

---

# 🧠 System Architecture
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
(Encryption / Decryption)
│
▼
Encrypted Vault Storage


The application follows a **layered security architecture** to separate user interface, authentication, cryptography, and storage.

---

# 🏗️ Architecture (Layer Description)

1️⃣ **GUI Layer**  
Tkinter interface used for interacting with the application.

2️⃣ **Authentication Layer**  
Verifies the master password before vault access.

3️⃣ **Crypto Layer**  
Handles encryption and decryption operations.

4️⃣ **Vault Layer**  
Stores encrypted credential entries securely.

---

# 🚀 Setup & Run

## Requirements

- Python **3.10+**

---

## Install Dependencies

```bash
pip install -r requirements.txt

python Vault_GUI.py



Secure Password Manager
-----------------------

Email: ________
Password: ________

[ Add Entry ]
[ View Entries ]
[ Delete Entry ]




📁 Project Structure
secure-password-manager/
│
├── Vault_GUI.py          # Main GUI application
├── crypto.py             # Encryption / Decryption logic
├── hsm.py               # Master password verification
├── keystore.py              # Vault storage management
├── requirements.txt
└── README.md


🔐 Security Model

This password manager follows a layered security model:

• Master password authentication
• Encryption before vault storage
• No plaintext password storage
• Encrypted credential vault
• Input validation and error handling


🛠 Future Improvements

Cloud vault synchronization

Multi-device password sync

Dark mode UI

Secure backup export

Advanced password generator



📄 License

This project is licensed under the MIT License.


👨‍💻 Author

Pranjal Panta




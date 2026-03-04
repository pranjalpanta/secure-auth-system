# 🔐 Secure Password Manager

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Security](https://img.shields.io/badge/Security-Encrypted%20Vault-orange)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

A Python-based **Password Manager** that securely stores credentials using **strong encryption and master-password protection**.

All sensitive vault data is **encrypted before storage** and only accessible after successful authentication.

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

- Master password required to unlock vault
- Input validation for empty fields (email / password)

## 🔒 Vault Security

- No plaintext password storage
- Encrypted vault stored locally
- Decryption only after successful authentication

## 🖥️ User Interface

- Simple **Tkinter GUI**
- Easy workflow for managing credentials

---

# 🏗️ Architecture (Simple)

The system follows a **layered security architecture**.

1. **GUI Layer**  
   Tkinter interface for user interaction.

2. **Authentication Layer**  
   Verifies the master password.

3. **Crypto Layer**  
   Handles encryption and decryption operations.

4. **Vault Layer**  
   Stores encrypted credential data.

---

# 🚀 Setup & Run

## Requirements

- Python **3.10+**

---

## Install Dependencies

```bash
pip install -r requirements.txt


python Vault_GUI.py


#📁 Project Structure
secure-password-manager/
│
├── Vault_GUI.py          # Main GUI application
├── crypto.py             # Encryption / Decryption logic
├── hsm.py               # Master password verification
├── vkeystore.py              # Vault storage management
├── requirements.txt
└── README.md


🔐 Security Notes

Passwords are never stored in plaintext

Vault data is encrypted before disk storage

Access is controlled by a master password

Separation of GUI and cryptographic logic


🛠 Future Improvements

Cloud vault sync

Auto password generator improvements

Multi-device support

Dark mode UI

Secure backup export


📄 License

This project is licensed under the MIT License.


📄 License

This project is licensed under the MIT License.


👨‍💻 Author
Pranjal Panta



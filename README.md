# 🔐 Secure Password Manager

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Security](https://img.shields.io/badge/Security-Encrypted%20Vault-critical)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

A Python-based **Password Manager** that securely stores credentials using **encryption** and **master-password protection**.  
All sensitive vault data is encrypted before storage and only accessible after successful authentication.

---

## ✅ Project Highlights

- Master password protected vault
- Strong encryption for stored credentials
- Add / View / Update / Delete credential entries
- Password generator (optional)
- Clean separation of GUI and security logic
- Local encrypted storage (vault file)

---

## 🧩 Features

### 🔑 Authentication
- Master password required to unlock vault
- Input validation for empty fields (email/password)

### 🔒 Vault Security
- No plaintext password storage
- Encrypted vault saved locally
- Decryption only after successful authentication

### 🖥️ User Interface
- Simple GUI (Tkinter)
- Easy workflow for managing credentials

---

## 🏗️ Architecture (Simple)

1. **GUI Layer** (Tkinter)  
2. **Auth Layer** (Master password verification)  
3. **Crypto Layer** (Encrypt / Decrypt operations)  
4. **Vault Layer** (Store encrypted credential data)

---
## ⚙️ Setup & Run

### Requirements
- Python 3.10+

### Install Dependencies
```bash
pip install -r requirements.txt

python Vault_GUI.py



## 📌 Requirements Fulfillment

| Requirement | Implementation |
|------------|----------------|
| Secure storage | Encrypted local vault |
| Authentication | Master password protection |
| Confidentiality | Encryption before saving |
| Usability | Tkinter GUI |
| Validation | Empty input checks |


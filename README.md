
# Secure Password Manager

A Python-based security application implementing strong user authentication, PKI integration, and encrypted vault storage using applied cryptographic principles.

---

## 🔐 Project Overview

This system is designed to demonstrate secure software development practices by integrating:

- Public Key Infrastructure (PKI)
- Certificate Authority (CA) services
- Secure vault storage
- Controlled user authentication
- Cryptographic encryption and decryption

The application follows a modular architecture separating GUI components from backend security logic to maintain clean design and security boundaries.

---

## ✨ Key Features

- Secure encryption and decryption of stored data  
- Certificate-based authentication model  
- Modular HSM, CA, and Vault components  
- Tkinter-based graphical user interface  
- Structured backend inside `src/` directory  
- Controlled vault access per authenticated user  

---

## 🏗️ System Architecture

The project follows a layered design:

1. GUI Layer – Tkinter-based frontend  
2. Authentication Layer – PKI & certificate validation  
3. Cryptographic Engine – Secure encryption/decryption  
4. Vault Storage Layer – Protected credential storage  
5. Security Modules – HSM, CA, and vault management  

---

## ⚙️ Installation & Execution

### Requirements
- Python 3.10+
- Required dependencies (install if needed)

### Run the Application

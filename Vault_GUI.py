import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys #Add required Tkinter, messagebox, OS, and system imports for GUI and runtime functionality

if __name__ == "__main__":
    # This is the application entry point
    app = VaultApp()
    app.mainloop()

# Import the core backend logic
try:
    from src.security.hsm import SoftHSM 
    from src.pki.ca import CertificateAuthority
    from src.core.vault import Vault
except ImportError as e:
    messagebox.showerror("Setup Error", f"Missing security module files. Please ensure you created the 'src' folders and files correctly.\nError: {e}") #Add safe backend module imports with ImportError handling and startup validation
    sys.exit(1) 


class VaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zyper PKI Vault GUI")
        self.geometry("600x500") 
        self.resizable(False, False) #Initialize main VaultApp window with title, fixed geometry configuration, and disabled resizing for consistent GUI layout control

        self.current_hsm = None
        self.current_vault = None
        self.ca_service = CertificateAuthority()
        self.current_user_email = "" 
        self.notification_label = None #Initialize core security state variables including HSM reference, vault context, certificate authority service, user session tracking, and notification handler

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True) # Implement VaultApp main window initialization with Tkinter root configuration, application state variables, CertificateAuthority integration, and primary container frame setup


        self.frames = {}
        # List ALL page classes
        page_classes = (AuthPage, VaultPage, SavePage, ListPage) #Initialize frame registry and define application page classes for dynamic multi-page navigation management
        
        for F in page_classes:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") #Implement dynamic frame registration and initialization for multi-page GUI navigation

        self.show_frame("AuthPage")

    def show_frame(self, page_name, email=None):
        frame = self.frames[page_name]
        frame.tkraise() #Add show_frame method to handle dynamic page switching by retrieving stored frames and raising the selected frame for GUI navigation control
        
        if page_name == "VaultPage" and email:
            self.current_user_email = email
            frame.update_vault_data()
        elif page_name == "VaultPage":
            frame.update_vault_data() #Enhance VaultPage navigation logic to assign user context and trigger vault data refresh during frame transitions
        
        if page_name == "ListPage":
            frame._refresh_list_tab() #If navigating to VaultPage with an email → store the email and update vault data  #If class name changes → navigation breaks silently.
            
        # --- FIX: Trigger reset on the AuthPage when navigating to it ---
        if page_name == "AuthPage":
            self.frames["AuthPage"].clear_fields()

    def show_notification(self, message, duration=5000):
        if not self.notification_label:
            self.notification_label = ttk.Label(self, text="", relief='sunken', foreground='white', background='blue', font=('Arial', 10, 'bold'))
            self.notification_label.pack(side='bottom', fill='x', ipady=5) #Add show_notification method to create and display a styled bottom notification label for user feedback within the GUI

        self.notification_label.config(text=message)
        if hasattr(self, '_notification_after_id'):
            self.after_cancel(self._notification_after_id) #Update notification label text and cancel existing scheduled timer to prevent overlapping GUI notification events
            
        self._notification_after_id = self.after(duration, lambda: self.notification_label.config(text="")) #Improve notification handling by cancelling previous timers and implementing auto-clear functionality to prevent overlapping GUI messages


class AuthPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller #Implement AuthPage frame class with parent initialization and controller binding for structured GUI navigation control

        main_label = ttk.Label(self, text="PKI Vault: Login / Register", font=('Arial', 16, 'bold'))
        main_label.pack(pady=20) #Add authentication page title label with styling and layout spacing for improved user interface clarity

        self.switch_frame = ttk.Frame(self)
        self.switch_frame.pack(padx=10, pady=5) #Add container frame for authentication widgets with padding to organize login/register UI layout

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar() #Initialize Tkinter StringVar variables for email, password, and confirm password input state management in authentication form
        
        self.is_register_mode = False
        self._create_widgets()
        self._toggle_mode() #Initialize default authentication mode and trigger widget creation with initial UI state toggle configuration

    def _create_widgets(self):
        ttk.Label(self.switch_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.switch_frame, textvariable=self.email_var, width=30).grid(row=0, column=1, padx=5, pady=5) #Implement email input label and entry field in authentication form layout within widget creation method

        ttk.Label(self.switch_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.switch_frame, textvariable=self.password_var, show='*', width=30).grid(row=1, column=1, padx=5, pady=5) #Add password label and masked entry field to authentication form for secure credential input handling

        self.confirm_label = ttk.Label(self.switch_frame, text="Confirm Pass:")
        self.confirm_entry = ttk.Entry(self.switch_frame, textvariable=self.confirm_password_var, show='*', width=30) #Add confirm password label and masked entry field to support registration validation in authentication interface
        
        self.action_button = ttk.Button(self.switch_frame, text="Login", command=self._handle_action)
        self.action_button.grid(row=3, column=0, columnspan=2, pady=10) #Add authentication action button with event handler binding and layout configuration for login and registration operations

        self.mode_switch_button = ttk.Button(self.switch_frame, text="Switch to Register", command=self._toggle_mode)
        self.mode_switch_button.grid(row=4, column=0, columnspan=2, pady=5) #Add mode switch button to toggle between login and registration views within the authentication interface

    def _toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.password_var.set("")
        self.confirm_password_var.set("")
        self.email_var.set("")  #Implement authentication mode toggle logic and reset input fields to ensure clean state transition between login and registration views

        if self.is_register_mode:
            self.confirm_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
            self.confirm_entry.grid(row=2, column=1, padx=5, pady=5)
            self.action_button.config(text="Register")
            self.mode_switch_button.config(text="Switch to Login") #Update registration mode UI to display confirm password fields and adjust button labels for registration workflow 
        else:
            self.confirm_label.grid_forget()
            self.confirm_entry.grid_forget()
            self.action_button.config(text="Login")
            self.mode_switch_button.config(text="Switch to Register") #Restore login mode UI by hiding confirm password fields and updating button labels for authentication workflow

    def clear_fields(self):
        """Clears the Email, Password, and Confirm Password fields."""
        self.email_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("") #Implement clear_fields method to reset email, password, and confirm password input variables in the authentication form


    def _handle_action(self):
        email = self.email_var.get().strip()
        password = self.password_var.get() #Add authentication handler to capture and sanitize user email and password input from the login form
        
        if not email or not password:
            messagebox.showerror("Error", "Email and Password cannot be empty.") #Add input validation to prevent empty email or password submissions with user error notification
            return

        if self.is_register_mode:
            confirm_password = self.confirm_password_var.get()
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.") #add password confirmation validation during registration
                return
            self._register_user(email, password)
        else:
            self._login_user(email, password) # implement conditional login and registration handling

    def _register_user(self, email, password):
        try:
            hsm = SoftHSM(email)
            vault = Vault(email) #initialize HSM and Vault during user registration

            if os.path.exists(hsm.keystore.filename):
                messagebox.showerror("Error", "User already registered. Please Login.") #prevent duplicate user registration
                return

            hsm.initialize_new_token(password, self.controller.ca_service)
            vault.setup(hsm) #initialize HSM token and configure vault
            
            messagebox.showinfo("Success", "Registration successful! Please log in now.")
            self._toggle_mode() #Show a success message after registration and switch back to login mode

        except FileExistsError:
            messagebox.showerror("Error", "User files already exist. Cannot register.")
        except Exception as e:
            messagebox.showerror("Registration Error", f"An unexpected error occurred: {e}") #Improved the registration error handling logic.

    def _login_user(self, email, password):
        try:
            hsm = SoftHSM(email)
            vault = Vault(email) #Update login initialization in Vault_GUI.py
            
            if not os.path.exists(hsm.keystore.filename):
                messagebox.showerror("Login Error", "User not found. Please register first.") #Added a check to stop login and show an error if the user account does not exist.
                return

            if hsm.login(password):
                if vault.unlock(hsm):
                    self.controller.current_hsm = hsm
                    self.controller.current_vault = vault
                    messagebox.showinfo("Success", "Login successful! Vault unlocked.")
                    self.controller.show_frame("VaultPage", email) 
                else:
                    messagebox.showerror("Login Error", "Vault data corrupted or access denied.")
            else:
                messagebox.showerror("Login Error", "Invalid Keystore Password.")

        except FileNotFoundError:
            messagebox.showerror("Login Error", "User files not found. Please register.")
        except Exception as e:
            messagebox.showerror("Login Error", f"An unexpected error occurred: {e}") #Added the full login workflow by verifying the keystore password attempting to unlock the vault storing the active HSM and Vault session after successful authentication redirecting the user to the VaultPage and handling invalid credentials missing user files corrupted vault data and unexpected exceptions with clear error messages.


class VaultPage(ttk.Frame):
    """Main Hub Page with Button Navigation"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.selected_credential = {}

        self.welcome_label = ttk.Label(self, text="", font=('Arial', 14, 'bold'))
        self.welcome_label.pack(pady=10) #Add VaultPage main hub with controller, credential state, and welcome label
        
        # --- NAVIGATION BUTTONS ---
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=20)
        
        ttk.Button(nav_frame, text="Save New Password", 
                   command=lambda: self.controller.show_frame("SavePage")).pack(side='left', padx=10, ipady=5)
        
        ttk.Button(nav_frame, text="List Your Passwords", 
                   command=lambda: self.controller.show_frame("ListPage")).pack(side='left', padx=10, ipady=5) #Add navigation frame with buttons for save and list password pages

        # Logout Button is at the bottom of the main frame
        ttk.Button(self, text="Logout", command=self._logout).pack(pady=10)

    def update_vault_data(self):
        # Fix for Welcome None: always use the stored email
        email = self.controller.current_user_email
        if email:
            self.welcome_label.config(text=f"Welcome {email}!")
        else:
            self.welcome_label.config(text="Welcome!") #Update welcome label using stored user email with fallback text

    def _logout(self):
        self.welcome_label.config(text="")
        
        self.controller.current_hsm._private_key = None
        self.controller.current_hsm = None
        self.controller.current_vault = None
        self.controller.current_user_email = "" 
        
        messagebox.showinfo("Logout", "Successfully logged out of the Vault system.") #Add logout flow to reset user, HSM, vault, and private key state
        
        # Navigate to AuthPage, which triggers the clearing of fields
        self.controller.show_frame("AuthPage")


class SavePage(ttk.Frame):
    """Dedicated frame for saving credentials"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller #Create SavePage frame for credential saving with controller binding
        
        ttk.Label(self, text="Save New Credential", font=('Arial', 14)).pack(pady=10)
        
        self.site_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20) #Initialize save form variables and create input frame layout
 
        # Site Name
        ttk.Label(input_frame, text="Site Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(input_frame, textvariable=self.site_var, width=30).grid(row=0, column=1, padx=5, pady=5) #Add Site Name label and input field to GUI form

        # Username
        ttk.Label(input_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(input_frame, textvariable=self.username_var, width=30).grid(row=1, column=1, padx=5, pady=5) #Add Username label and input field to GUI form

        # Password
        ttk.Label(input_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(input_frame, textvariable=self.password_var, show='*', width=30).grid(row=2, column=1, padx=5, pady=5) #Add password label and masked entry field
        
        ttk.Button(self, text="Save Credential", command=self._save_credential).pack(pady=10)
        ttk.Button(self, text="<< Back to Menu", command=lambda: self.controller.show_frame("VaultPage")).pack(pady=5) #Add Save Credential and Back to Menu buttons

    def _save_credential(self):
        site = self.site_var.get().strip()
        user = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not site or not user or not password:
            messagebox.showerror("Error", "All three fields are required.") #Add input validation for saving credentials
            return

        try:
            self.controller.current_vault.add_entry(site, user, password)
            messagebox.showinfo("Success", f"Credential for '{site}' saved successfully.")
            self.site_var.set("")
            self.username_var.set("")
            self.password_var.set("")
            self.controller.show_frame("VaultPage")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save credential: {e}") #Implement credential save logic with success and error handling


class ListPage(ttk.Frame):
    """Dedicated frame for listing, editing, and deleting credentials"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.selected_credential = {} #Add ListPage frame initialization for credential listing, editing, and deletion
        
        ttk.Label(self, text="Your Saved Passwords", font=('Arial', 14)).pack(pady=10)
        
        # --- Treeview Widget for Hierarchical List ---
        self.tree = ttk.Treeview(self, columns=("Username", "Password"), show="tree headings")
        self.tree.heading("#0", text="Site Name", anchor='w')
        self.tree.heading("Username", text="Username", anchor='w')
        self.tree.heading("Password", text="Password", anchor='w') #dd Treeview widget with Username and Password columns for credential display
        
        self.tree.column("#0", width=150)
        self.tree.column("Username", width=150)
        self.tree.column("Password", width=150)
        
        self.tree.pack(padx=10, pady=5, fill='both', expand=True) #Set Treeview column widths and pack widget with padding and expandable layout

        # Context Menu Binding (Right-click)
        self.tree.bind("<Button-3>", self._show_context_menu) #Bind right-click (Button-3) event to display the context menu on the tree widget.
        
        # Action Frame
        action_frame = ttk.Frame(self)
        action_frame.pack(fill='x', pady=5) #Create and pack an action frame to organize action-related widgets horizontally with vertical padding.
        
        ttk.Button(action_frame, text="Refresh List", command=self._refresh_list_tab).pack(side='left', padx=10)
        ttk.Button(action_frame, text="<< Back to Menu", command=lambda: self.controller.show_frame("VaultPage")).pack(side='right', padx=10)


    def _refresh_list_tab(self):
        self.tree.delete(*self.tree.get_children())
        if not self.controller.current_vault: return

        all_entries = self.controller.current_vault.get_all_site_entries()
        
        for site, credentials_list in all_entries.items():
            site_id = self.tree.insert('', tk.END, text=site, open=False)
            
            for cred in credentials_list:
                tags = (site, cred['username']) 
                self.tree.insert(site_id, tk.END, text="", values=(cred['username'], cred['password']), tags=tags)

    def _show_context_menu(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return

        self.tree.selection_set(item_id)
        
        is_credential_row = self.tree.parent(item_id)
        if not is_credential_row: return

        values = self.tree.item(item_id, 'values')
        site_name = self.tree.item(self.tree.parent(item_id), 'text')
        
        self.selected_credential = {
            'site': site_name,
            'user': values[0],
            'pass': values[1]
        }
        
        menu = tk.Menu(self.controller, tearoff=0)
        
        menu.add_command(label=f"Copy Username", command=lambda: self._copy_to_clipboard(values[0]))
        menu.add_command(label=f"Copy Password", command=lambda: self._copy_to_clipboard(values[1]))
        menu.add_separator()
        
        menu.add_command(label="Edit Credential", command=self._open_edit_dialog)
        menu.add_command(label="Delete Credential", command=self._delete_credential_prompt)

        menu.tk_popup(event.x_root, event.y_root)

    def _copy_to_clipboard(self, value):
        self.controller.clipboard_clear()
        self.controller.clipboard_append(value)
        self.controller.show_notification(f"Copied to clipboard!", 2000)

    def _delete_credential_prompt(self):
        cred = self.selected_credential
        
        # SAFE STRING DEFINITION
        prompt = "Do you really want to delete credential:\nUsername: " + cred['user'] + "\nPassword: " + cred['pass']
        
        if messagebox.askyesno("Confirm Deletion", prompt):
            try:
                if self.controller.current_vault.delete_credential(cred['site'], cred['user']):
                    
                    success_msg = "Successfully deleted " + cred['user'] + " on " + cred['site']
                    self.controller.show_notification(success_msg, 5000)
                    
                    self._refresh_list_tab()
                else:
                    messagebox.showerror("Error", "Deletion failed. Credential not found in vault.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during deletion: {e}")

    def _open_edit_dialog(self):
        cred = self.selected_credential
        if not cred: return

        dialog = tk.Toplevel(self.controller)
        dialog.title(f"Edit Credential for {cred['site']}")
        dialog.geometry("400x200")
        dialog.transient(self.controller) 
        dialog.grab_set()

        site_var = tk.StringVar(value=cred['site'])
        old_user = cred['user'] 
        new_user_var = tk.StringVar(value=cred['user'])
        new_pass_var = tk.StringVar(value=cred['pass']) 
        
        # Fields
        ttk.Label(dialog, text="Site Name (Read Only):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(dialog, textvariable=site_var, state='readonly', width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="New Username:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(dialog, textvariable=new_user_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="New Password:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(dialog, textvariable=new_pass_var, width=30).grid(row=2, column=1, padx=5, pady=5) #Added input fields for the edit credential dialog including a read only site name field and editable username and password fields for updating saved credentials.

        def save_edits():
            new_user = new_user_var.get().strip() 
            new_pass = new_pass_var.get() #Retrieve updated username and password values in save_edits()
            
            if not new_user or not new_pass:
                messagebox.showerror("Error", "Username and Password cannot be empty.") #Add validation to prevent empty username and password submission
                return

            try:
                if self.controller.current_vault.update_credential(cred['site'], old_user, new_user, new_pass):
                    messagebox.showinfo("Success", f"Credential for {cred['site']} updated.")
                    dialog.destroy()
                    self._refresh_list_tab()
                else:
                    messagebox.showerror("Error", "Update failed. Credential not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {e}")

        ttk.Button(dialog, text="Save Changes", command=save_edits).grid(row=3, column=0, columnspan=2, pady=10)
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        self.controller.wait_window(dialog) #Implemented the save changes flow for credential editing by updating stored values handling success and failure cases refreshing the credential list closing the dialog after a successful update and showing an error message when an exception occurs.


if __name__ == "__main__":
    # This is the application entry point
    app = VaultApp()
    app.mainloop()
  

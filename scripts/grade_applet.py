import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import threading
import os
import platform
import subprocess
import time
from config_manager import ConfigManager

import smtplib
from email.message import EmailMessage
import socket

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MailManager:
    @staticmethod
    def test_connection():
        try:
            with smtplib.SMTP("smtpserver.sfu.ca", 25, timeout=5) as server:
                return True, "Connected to SFU Relay"
        except Exception as e:
            return False, f"VPN Connection Error: {e}"

class GradeApplet(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SFU Grade Distribution Applet")
        self.geometry("1100x650")
        self.config = ConfigManager.load_config()
        self.df = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # Left Panel
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.left_panel, text="Step 1: Compose Template", font=("Inter", 18, "bold")).pack(pady=10)
        
        ctk.CTkLabel(self.left_panel, text="Send From:", font=("Inter", 12)).pack(anchor="w", padx=25)
        self.sender_entry = ctk.CTkEntry(self.left_panel, placeholder_text="yourname@sfu.ca", width=400)
        sender_val = self.config.get("sender_email", "")
        if sender_val: self.sender_entry.insert(0, sender_val)
        self.sender_entry.pack(pady=(0, 5))

        ctk.CTkLabel(self.left_panel, text="Subject:", font=("Inter", 12)).pack(anchor="w", padx=25)
        self.subject_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Email Subject", width=400)
        subj_val = self.config.get("subject", "")
        if subj_val: self.subject_entry.insert(0, subj_val)
        self.subject_entry.pack(pady=(0, 5))
        
        self.body_text = ctk.CTkTextbox(self.left_panel, width=400, height=180)
        self.body_text.insert("1.0", self.config.get("body", ""))
        self.body_text.pack(pady=5)
        self.body_text.bind("<KeyRelease>", self.update_preview)
        
        ctk.CTkLabel(self.left_panel, text="Step 2: Grade Data", font=("Inter", 18, "bold")).pack(pady=(20, 10))
        self.file_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.file_frame.pack(pady=5)
        self.file_button = ctk.CTkButton(self.file_frame, text="Import Spreadsheet", width=190, command=self.import_file)
        self.file_button.pack(side="left", padx=5)
        self.template_button = ctk.CTkButton(self.file_frame, text="Get Template CSV", fg_color="gray", width=190, command=self.save_template)
        self.template_button.pack(side="left", padx=5)
        self.file_label = ctk.CTkLabel(self.left_panel, text="No file selected", text_color="gray")
        self.file_label.pack()
        
        ctk.CTkLabel(self.left_panel, text="Step 3: VPN Relay Status", font=("Inter", 18, "bold")).pack(pady=(20, 10))
        self.status_label_info = ctk.CTkLabel(self.left_panel, text="Checking SFU Relay...", text_color="gray")
        self.status_label_info.pack()
        
        # Status loop
        threading.Thread(target=self.background_status_check, daemon=True).start()

        # Right Panel
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        ctk.CTkLabel(self.right_panel, text="Email Preview", font=("Inter", 18, "bold")).pack(pady=10)
        self.student_selector = ctk.CTkComboBox(self.right_panel, values=["Import data first..."], command=self.update_preview, width=300)
        self.student_selector.pack(pady=10)
        self.preview_box = ctk.CTkTextbox(self.right_panel, width=400, height=300, state="disabled")
        self.preview_box.pack(pady=10, fill="both", expand=True)

        # Control Panel (Bottom of Right Column)
        self.control_panel = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.control_panel.pack(pady=10, fill="x")
        
        self.status_label = ctk.CTkLabel(self.control_panel, text="Ready")
        self.status_label.pack(side="top", pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.control_panel, width=380)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="top", pady=5)
        
        self.send_button = ctk.CTkButton(self.control_panel, text="SEND VIA SFU RELAY", font=("Inter", 14, "bold"), fg_color="#D8232A", hover_color="#A51B1F", width=380, height=45, command=self.send_all)
        self.send_button.pack(side="top", pady=10)
        
        # Set initial focus to help UI render placeholders
        self.sender_entry.focus_set()

    def background_status_check(self):
        while True:
            success, msg = MailManager.test_connection()
            if success: self.after(0, lambda m=msg: self.status_label_info.configure(text=m, text_color="green"))
            else: self.after(0, lambda m=msg: self.status_label_info.configure(text=m, text_color="red"))
            time.sleep(10)

    def save_template(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")], initialfile="grade_template.csv")
        if path:
            try:
                pd.DataFrame(columns=["Name", "Email", "Grade"]).to_csv(path, index=False)
                messagebox.showinfo("Success", "Template saved with columns: Name, Email, Grade.")
            except Exception as e: messagebox.showerror("Error", str(e))

    def import_file(self):
        path = filedialog.askopenfilename(filetypes=[("Spreadsheet files", "*.csv *.xlsx")])
        if not path: return
        try:
            self.df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
            
            # Normalize column names for detection
            cols = {c.lower().strip(): c for c in self.df.columns}
            self.col_map = {
                "name": cols.get("name"),
                "email": cols.get("email"),
                "grade": cols.get("grade")
            }

            # Validation
            missing = [k.capitalize() for k, v in self.col_map.items() if v is None]
            if missing:
                messagebox.showwarning("Warning", f"Missing columns: {', '.join(missing)}\nPlease ensure your file has headers: Name, Email, Grade")

            # Create display list: Name (Email)
            display_list = []
            name_col = self.col_map["name"] or self.df.columns[0]
            email_col = self.col_map["email"] or (self.df.columns[1] if len(self.df.columns) > 1 else name_col)
            
            for _, row in self.df.iterrows():
                val_name = str(row[name_col])
                val_email = str(row[email_col])
                display_list.append(f"{val_name} ({val_email})")
            
            self.student_selector.configure(values=display_list)
            self.student_selector.set(display_list[0])
            self.file_label.configure(text=os.path.basename(path), text_color="white")
            self.update_preview()
        except Exception as e: messagebox.showerror("Error", str(e))

    def update_preview(self, event=None):
        if self.df is None: return
        selected_text = self.student_selector.get()
        display_list = self.student_selector.cget("values")
        try:
            idx = display_list.index(selected_text)
            row = self.df.iloc[idx]
        except: return
        
        name_col = self.col_map["name"] or self.df.columns[0]
        email_col = self.col_map["email"] or (self.df.columns[1] if len(self.df.columns) > 1 else name_col)
        grade_col = self.col_map["grade"] or (self.df.columns[2] if len(self.df.columns) > 2 else name_col)

        name = str(row[name_col])
        email = str(row[email_col])
        grade = str(row[grade_col])
        preview_content = self.body_text.get("1.0", "end-1c").replace("$NAME$", name).replace("$GRADE$", grade)
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.insert("1.0", f"To: {email}\nSubject: {self.subject_entry.get()}\n---\n\n{preview_content}")
        self.preview_box.configure(state="disabled")

    def send_all(self):
        if self.df is None or len(self.df) == 0:
            messagebox.showwarning("Warning", "Please import a spreadsheet with data first.")
            return
        
        success, msg = MailManager.test_connection()
        if not success:
            messagebox.showerror("Error", f"Could not connect to relay. Please ensure you are on the SFU VPN.\n\n{msg}")
            return
        
        # Save current config
        ConfigManager.save_config(
            self.config.get("username", ""),
            self.sender_entry.get(),
            self.subject_entry.get(),
            self.body_text.get("1.0", "end-1c")
        )
        
        if not messagebox.askyesno("Confirm", f"Send {len(self.df)} emails via SFU SMTP Relay?"): return
        
        self.send_button.configure(state="disabled")
        self.status_label.configure(text="Initializing SMTP...")
        threading.Thread(target=self.batch_send_worker, daemon=True).start()

    def batch_send_worker(self):
        sender = self.sender_entry.get()
        subject = self.subject_entry.get()
        template = self.body_text.get("1.0", "end-1c")
        success_count = 0; fail_count = 0; total = len(self.df)
        
        try:
            name_col = self.col_map["name"] or self.df.columns[0]
            email_col = self.col_map["email"] or (self.df.columns[1] if len(self.df.columns) > 1 else name_col)
            grade_col = self.col_map["grade"] or (self.df.columns[2] if len(self.df.columns) > 2 else name_col)

            with smtplib.SMTP("smtpserver.sfu.ca", 25, timeout=10) as server:
                for i, row in self.df.iterrows():
                    name = str(row[name_col])
                    recipient = str(row[email_col])
                    grade = str(row[grade_col])
                    body = template.replace("$NAME$", name).replace("$GRADE$", grade)
                    
                    try:
                        msg = EmailMessage()
                        msg.set_content(body)
                        msg['Subject'] = subject
                        msg['From'] = sender
                        msg['To'] = recipient
                        
                        server.send_message(msg)
                        success_count += 1
                    except Exception as e:
                        print(f"Error sending to {recipient}: {e}")
                        fail_count += 1
                    
                    progress = (i + 1) / total
                    self.after(0, lambda p=progress, s=success_count, f=fail_count: self.update_progress(p, s, f))
                    time.sleep(0.1) # Small safety delay
                
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Critical Error", f"SMTP connection lost: {e}"))
        
        self.after(0, lambda: self.finalize_send(success_count, fail_count))

    def update_progress(self, progress, success, fail):
        self.progress_bar.set(progress)
        self.status_label.configure(text=f"Sent: {success} | Failed: {fail}")

    def finalize_send(self, success, fail):
        self.send_button.configure(state="normal")
        messagebox.showinfo("Complete", f"Batch complete.\nSent: {success}\nFailed: {fail}")
        self.status_label.configure(text="Ready")

if __name__ == "__main__":
    app = GradeApplet()
    app.mainloop()

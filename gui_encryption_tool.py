import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Encryption Tool (AES-256)")
        self.root.geometry("500x300")
        self.root.config(bg="#f4f4f4")

        self.key = get_random_bytes(32)  # 256-bit AES key

        # Label
        self.label = tk.Label(root, text="Select a file to encrypt/decrypt:", bg="#f4f4f4", font=("Arial", 12))
        self.label.pack(pady=10)

        # Select File Button
        self.select_file_btn = tk.Button(root, text="Choose File", command=self.select_file, bg="#3498db", fg="white", font=("Arial", 10))
        self.select_file_btn.pack(pady=5)

        # Encrypt Button
        self.encrypt_btn = tk.Button(root, text="Encrypt File", command=self.encrypt_file, bg="#2ecc71", fg="white", font=("Arial", 10))
        self.encrypt_btn.pack(pady=5)

        # Decrypt Button
        self.decrypt_btn = tk.Button(root, text="Decrypt File", command=self.decrypt_file, bg="#e74c3c", fg="white", font=("Arial", 10))
        self.decrypt_btn.pack(pady=5)

        self.selected_file = None  # Stores selected file path

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo("File Selected", f"Selected File: {file_path}")

    def pad(self, data):
        return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

    def encrypt_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        with open(self.selected_file, 'rb') as file:
            plaintext = file.read()
        plaintext = self.pad(plaintext)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_data = iv + cipher.encrypt(plaintext)

        enc_file_path = self.selected_file + ".enc"
        with open(enc_file_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)

        messagebox.showinfo("Success", f"File Encrypted Successfully!\nSaved as: {enc_file_path}")

    def decrypt_file(self):
        if not self.selected_file or not self.selected_file.endswith(".enc"):
            messagebox.showerror("Error", "Select a valid encrypted (.enc) file!")
            return

        with open(self.selected_file, 'rb') as enc_file:
            encrypted_data = enc_file.read()
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:]).rstrip(b"\0")

        dec_file_path = self.selected_file.replace(".enc", "_decrypted")
        with open(dec_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        messagebox.showinfo("Success", f"File Decrypted Successfully!\nSaved as: {dec_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()

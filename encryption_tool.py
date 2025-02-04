from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


class FileEncryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, data):
        return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            plaintext = file.read()
        plaintext = self.pad(plaintext)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_data = iv + cipher.encrypt(plaintext)

        enc_file_path = file_path + ".enc"
        with open(enc_file_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)

        print(f"File Encrypted: {enc_file_path}")

    def decrypt_file(self, enc_file_path):
        with open(enc_file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:]).rstrip(b"\0")

        dec_file_path = enc_file_path.replace(".enc", "_decrypted")
        with open(dec_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        print(f"File Decrypted: {dec_file_path}")


if __name__ == "__main__":
    key = get_random_bytes(32)  # 256-bit key
    encryptor = FileEncryptor(key)

    choice = input("Enter 'E' to Encrypt or 'D' to Decrypt: ").upper()

    if choice == 'E':
        file_path = input("Enter file path to encrypt: ")
        encryptor.encrypt_file(file_path)
    elif choice == 'D':
        file_path = input("Enter encrypted file path to decrypt: ")
        encryptor.decrypt_file(file_path)
    else:
        print("Invalid Choice!")

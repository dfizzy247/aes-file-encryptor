import os
import datetime
import ctypes
import base64
from argon2 import PasswordHasher, low_level
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

CHUNK_SIZE = 64 * 1024  # 64KB
ph = PasswordHasher()  # Argon2 Password Hasher

def secure_erase(password: str):
    """Overwrites password in memory to prevent leakage."""
    length = len(password)
    buf = ctypes.create_string_buffer(length)
    ctypes.memset(buf, 0, length)  # Zero out memory

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a key using Argon2 with a fixed output length."""
    try:
        key = low_level.hash_secret_raw(
            secret=password.encode(),
            salt=salt,
            time_cost=4,  # Increased cost for better security
            memory_cost=2**16,
            parallelism=1,
            hash_len=32,  # Ensure 32-byte output for AES-256
            type=low_level.Type.ID
        )

        print(f"[DEBUG] Derived Key: {key.hex()} | Salt: {salt.hex()}")  # Print key for verification
        return key
    except Exception as e:
        raise ValueError(f"Key derivation failed: {str(e)}")
    finally:
        secure_erase(password)  # Ensure password is erased from memory

def encrypt_file(input_path: str, password: str, output_path: str):
    """Encrypts a file using AES-256-GCM and stores the original extension."""
    salt = os.urandom(16)
    iv = os.urandom(12)  # AES-GCM IV should be 12 bytes
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    print(f"[DEBUG] Derived Key: {key.hex()} | Salt: {salt.hex()}")  # Print key for verification

    original_extension = os.path.splitext(input_path)[1].encode()
    ext_len = len(original_extension)

    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        outfile.write(salt + iv + bytes([ext_len]) + original_extension)  # Store metadata

        while chunk := infile.read(CHUNK_SIZE):
            ciphertext = aesgcm.encrypt(iv, chunk, None)
            outfile.write(ciphertext) # Write encrypted data

    print(f"[DEBUG] Encryption Complete - File saved at: {output_path}")  

def decrypt_file(input_path: str, password: str, output_path: str) -> str:
    """Decrypts a file using AES-256-GCM and restores the original extension."""
    try:
        with open(input_path, 'rb') as infile:
            salt = infile.read(16)  # Read stored salt
            iv = infile.read(12)  # Read stored IV
            ext_len = int.from_bytes(infile.read(1), 'big')  # Read extension length
            original_extension = infile.read(ext_len).decode()  # Read original extension

            print(f"[DEBUG] Decryption - Extracted Salt: {salt.hex()} | IV: {iv.hex()} | Original Extension: {original_extension}")

            key = derive_key(password, salt)  # Derive key from extracted salt
            print(f"[DEBUG] Decryption - Derived Key: {key.hex()}")

            aesgcm = AESGCM(key)

            decrypted_output_path = output_path + original_extension  # Restore extension

            with open(decrypted_output_path, 'wb') as outfile:
                while chunk := infile.read(CHUNK_SIZE + 16):  # GCM adds 16-byte tag
                    try:
                        decrypted_chunk = aesgcm.decrypt(iv, chunk, None)
                        outfile.write(decrypted_chunk)
                    except InvalidTag:
                        print("Decryption failed: Incorrect password or corrupted file.")
                        return None  # Decryption failed

        print(f"[DEBUG] Decryption Successful - File saved at: {decrypted_output_path}")
        return decrypted_output_path  # Return correct filename
    except Exception as e:
        print(f"[DEBUG] Decryption Error: {str(e)}")
        return None

# Ensure LOG_FILE is defined (it should already be in crypto_utils.py)
LOG_FILE = "encryption_history.log"  # If not already present, add this line

def log_event(event_type, filename, status, output_path=None):
    """Logs encryption & decryption events to a file, including output path."""
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Include output_path in the log
        log.write(f"[{timestamp}] {event_type} - {filename} - {status} - {output_path or ''}\n")
    print(f"Logged event: {event_type} - {filename} - {status} - {output_path or ''}")

def get_full_history():
    """Fetches the complete encryption history."""
    try:
        with open(LOG_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "No history available."

def clear_history():
    """Clears the history log without deleting the file."""
    open(LOG_FILE, "w").close()

def get_recent_events(lines=20):
    """Fetches the most recent encryption/decryption events."""
    try:
        with open(LOG_FILE, "r") as f:
            content = f.readlines()
            return "".join(content[-lines:]) if content else "No recent history."
    except FileNotFoundError:
        return "No history available."

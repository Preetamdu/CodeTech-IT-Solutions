import os
import hashlib
import argparse
import json


def compute_hash(file_path, hash_algo='sha256'):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def generate_hashes(directory, hash_algo, hash_file):
    """Generate hashes for all files in the directory and save them to a JSON file."""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            hashes[file_path] = compute_hash(file_path, hash_algo)

    with open(hash_file, 'w') as f:
        json.dump(hashes, f, indent=4)
    print(f"Hashes generated and saved to {hash_file}.")


def check_hashes(directory, hash_file):
    """Check file integrity by comparing current hashes with stored hashes."""
    if not os.path.exists(hash_file):
        print(f"Hash file {hash_file} not found.")
        return

    with open(hash_file, 'r') as f:
        saved_hashes = json.load(f)

    current_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            current_hashes[file_path] = compute_hash(file_path)

    for file, saved_hash in saved_hashes.items():
        current_hash = current_hashes.get(file)
        if current_hash is None:
            print(f"File missing: {file}")
        elif current_hash != saved_hash:
            print(f"File modified: {file}")
        else:
            print(f"File intact: {file}")

    for file in current_hashes:
        if file not in saved_hashes:
            print(f"New file detected: {file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("action", choices=["generate", "check"], help="Action to perform")
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("--hash-algo", default="sha256", help="Hash algorithm to use (default: sha256)")
    parser.add_argument("--hash-file", default="hashes.json", help="File to save/load hash values (default: hashes.json)")

    args = parser.parse_args()

    if args.action == "generate":
        generate_hashes(args.directory, args.hash_algo, args.hash_file)
    elif args.action == "check":
        check_hashes(args.directory, args.hash_file)

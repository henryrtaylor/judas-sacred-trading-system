import os

def clean_env_file(path=".env"):
    if not os.path.exists(path):
        print(f"❌ No .env file found at {path}")
        return

    with open(path, "rb") as f:
        content = f.read()

    # Remove BOM if present
    if content.startswith(b'\xef\xbb\xbf'):
        print("⚠️ BOM detected and removed.")
        content = content[3:]

    # Decode and clean up
    decoded = content.decode("utf-8", errors="ignore").strip()
    lines = decoded.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

    # Overwrite with clean version
    with open(path, "w", encoding="utf-8") as f:
        for line in cleaned_lines:
            f.write(line + "\n")

    print(f"✅ .env cleaned and saved: {path}")
    print("📜 Final contents:")
    for line in cleaned_lines:
        print("   ", line)

if __name__ == "__main__":
    clean_env_file()
import argparse
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

DEFAULT_IGNORE_PATTERNS = ["__pycache__", ".git", "venv", ".idea", ".vscode", "*.pyc", "*.pyo", "*.pyd", "*.zip", "*.venv"]


def should_ignore(path_name, ignore_list):
    for pattern in ignore_list:
        if pattern.startswith("*") and path_name.endswith(pattern[1:]):
            return True
        elif path_name == pattern:
            return True
    return False

def make_zip_backup(source_dir, output_dir, ignore_list):
    source_path = Path(source_dir).resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(output_dir, f"{source_path.name}_backup_{timestamp}.zip")

    print(f" Starting ZIP backup for: {source_path.name}")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            dirs[:] = [d for d in dirs if not should_ignore(d, ignore_list)]


            for file in files:
                if not should_ignore(file, ignore_list):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_path)
                    zipf.write(file_path, arcname)
                    print(f" Adding: {arcname}")

    print(f"\n✓ ZIP Backup created successfully at: {zip_filename}")

def main():
    parser = argparse.ArgumentParser(description="CLI Project Backup Wizard with Auto-Ignore")
    parser.add_argument("-s", "--source", required=True, help= "Source project directory to backup")
    parser.add_argument("-o", "--output", default="./my_backups", help="Output directory for backup archiives")

    args = parser.parse_args()

    source_dir = args.source
    output_dir = args.output

    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok= True)
    make_zip_backup(source_dir, output_dir, DEFAULT_IGNORE_PATTERNS)

if __name__ == "__main__":
    main()


                
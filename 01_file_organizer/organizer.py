import os
import shutil
from datetime import datetime
from pathlib import Path

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".avi", ".mkv", ".mov"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".c", ".cpp", ".java", ".cs", ".rb", ".php", ".go", ".rs", ".swift", ".ts", ".kt", ".m", ".pl", ".lua", ".r", ".sql", ".vb", ".asm", ".h", ".hpp", ".d", ".erl", ".ex", ".exs", ".fs", ".groovy", ".hs", ".jl", ".lisp", ".nim", ".pas", ".racket", ".scala", ".vhdl",".py", ".ipynb", ".md", ".json", ".xml", ".yaml", ".yml"],
    "Others": []
}

def organize_folder(target_dir):
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"Error: Path '{target_dir}' does not exist.")
        return

    for item in target_path.iterdir():
        if item.is_file():
            file_extension = item.suffix.lower()
            moved = False
           
            for category, extensions in FILE_CATEGORIES.items():
                if file_extension in extensions:
                    dest_dir = target_path / category
                    dest_dir.mkdir(exist_ok=True)
                    shutil.move(str(item), str(dest_dir / item.name))
                    print(f"Moved '{item.name}' to '{category}'")
                    moved = True
                    break

            if not moved and file_extension != "":
                others_dir = target_path / "Others"
                others_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(others_dir / item.name))
                print(f"Moved '{item.name}' to 'Others'")

def create_backup(target_dir, backup_location):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archieve_name = os.path.join(backup_location, f"backup_{timestamp}")
    shutil.make_archive(archieve_name, 'zip', target_dir)
    print(f"Backup successfuly created at '{archieve_name}.zip'")

if __name__ == "__main__":
    DIRECTORY_TO_ORGANIZE = "./test_folder"  # Change this to the directory you want to organize
    BACKUP_DESTINATION = "./backups"  # Change this to the desired backup location

    os.makedirs(BACKUP_DESTINATION, exist_ok=True)

    print("---Starting Folder Organization---")
    organize_folder(DIRECTORY_TO_ORGANIZE)

    print("\n---Creating Archieve Backup---")
    create_backup(DIRECTORY_TO_ORGANIZE, BACKUP_DESTINATION)
import argparse
from pathlib import Path


def bulk_rename(directory, prefix="", extension="", start_num=1):
    dir_path = Path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: Directory '{directory}' does not exist.")
        return

    # এক্সটেনশন ফিল্টার কেস-ইনসেনসিটিভ করা হলো
    files = [f for f in dir_path.iterdir() if f.is_file()]
    if extension:
        clean_ext = extension.lstrip('.').lower()
        files = [f for f in files if clean_ext in f.name.lower()]

    if not files:
        print("No matching files found to rename.")
        return

    print(f"🔄 Renaming {len(files)} files in '{dir_path.resolve()}'...\n")

    count = start_num
    for file_path in files:
        ext = file_path.suffix if file_path.suffix else f".{extension}"
        new_name = f"{prefix}_{count:03d}{ext}" if prefix else f"file_{count:03d}{ext}"
        new_file_path = dir_path / new_name

        file_path.rename(new_file_path)
        print(f"✓ Renamed: {file_path.name} -> {new_name}")
        count += 1

    print("\n✓ Bulk renaming completed successfully!")

def main():
    parser = argparse.ArgumentParser(description="Python CLI Bulk File Renamer")
    parser.add_argument("-d", "--dir", required= True, help= "Path to the target directory")
    parser.add_argument("-p", "--prefix", default="", help="Prefix for renamed files")
    parser.add_argument("-e", "--ext", default="", help="Filter files by extension (e.g., txt, pdf)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Starting sequencenumber (default: 1)")

    args = parser.parse_args()
    bulk_rename(args.dir, args.prefix, args.ext, args.start)

if __name__ == "__main__":
    main()
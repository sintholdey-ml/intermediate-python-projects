import os
import sys
from pathlib import Path

def scan_portfolio(root_dir):
    root_path = Path(root_dir).resolve()
    projects = []

    if not root_path.exists():
        print(f"Error: Path '{root_path}' does not exist.")
        return projects

    for item in sorted(root_path.iterdir()):
        if item.is_dir() and not item.name.startswith(".") and item.name != "venv":
            py_files = list(item.glob("*.py"))
            json_files = list(item.glob("*.json"))
            csv_files = list(item.glob("*.csv"))
            
            file_names = [f.name for f in item.iterdir() if f.is_file()]
            
            projects.append({
                "name": item.name,
                "py_count": len(py_files),
                "data_files": len(json_files) + len(csv_files),
                "files": file_names
            })

    return projects

def display_dashboard(projects):
    print("=" * 60)
    print(" PYTHON 30-DAYS PORTFOLIO DASHBOARD (WEEK 1)")
    print("=" * 60)

    if not projects:
        print("No project folders found.")
        return

    total_projects = len(projects)
    total_scripts = sum(p["py_count"] for p in projects)

    for idx, p in enumerate(projects, start=1):
        print(f"\n📂 [{idx}] Project Folder: {p['name']}")
        print(f"   └── Python Scripts   : {p['py_count']}")
        print(f"   └── Output/Data Files: {p['data_files']}")
        key_files = ", ".join(p['files'][:4]) if p['files'] else "None"
        print(f"   └── Key Files        : {key_files}")

    print("\n" + "=" * 60)
    print(f" SUMMARY: {total_projects} Projects Completed | {total_scripts} Total Python Scripts")
    print("=" * 60)

def main():
    # বর্তমান ফাইলের অভিভাবক ডিরেক্টরি (মূল python-30-days ফোল্ডার) পাথ হিসেবে ব্যবহার করা হয়েছে
    root_dir = Path(__file__).resolve().parent.parent
    projects = scan_portfolio(root_dir)
    display_dashboard(projects)

if __name__ == "__main__":
    main()
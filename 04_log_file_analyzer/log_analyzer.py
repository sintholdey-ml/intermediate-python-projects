import argparse
import json
import re
from collections import Counter
from pathlib import Path

def parse_log_line(line):
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \s+\[(\w+)\] \s+(\w+) \s+(.*)"
    match = re.match(pattern, line)
    if match:
        timestamp, level, message = match.groups()
        return level.upper(),message
    return None, None

def analyze_log_file(log_path):
    level_counter = Counter()
    error_messages = Counter()

    with open(log_path,"r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            level, message = parse_log_line(line)
            if level:
                level_counter[level] += 1 
                if level in ["ERROR", "CRITICAL"]:
                    error_messages[message] += 1
                else:
                    level_counter["unknown"] += 1

    return level_counter, error_messages

def save_report(output_path, report_data):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
    print(f"✓ Report saved successfully to: {output_path}:")

def main():
    parser = argparse.ArgumentParser(description="Python CLI Log File Analyzer")
    parser.add_argument("-i", "--input", required=True, help="Path to input .log file")
    parser.add_argument("-o", "--output", required=True, help="Optional JSON file path to save report")

    args = parser.parse_args()

    log_path = Path(args.input)
    if not log_path.exists():
        print(f"Error: Log file '{args.input}' not found.")
        return

    levels, top_errors = analyze_log_file(log_path)

    print("\n---Log Analysis summary---")
    for level, count in levels.items():
        print(f"{level:<10}: {count}")

    if top_errors:
        print("\n---Most Common Errors ---")
        for msg, count in top_errors.most_common(5):
            print(f"[{count}x]: {msg}")

    if args.output:
        report_data = {
            "summary": dict(levels),
            "top_errors": dict(top_errors.most_common(5))
        }
        save_report(args.output, report_data)

if __name__ == "__main__":
    main()
# Import standard libraries
import re
import json
from pathlib import Path
from datetime import datetime

# Define current directory
CURRENT_DIR = Path(__file__).parent


# Function to extract summary JSON blocks from log file
def extract_summaries_from_log(log_path):
    """
    Extracts all JSON summary blocks from a given log file.

    Args:
        log_path (Path): Path to the log_*.txt file.

    Returns:
        list: A list of extracted dictionaries.
    """
    with open(log_path, "r") as f:
        content = f.read()

    # Regex pattern to extract JSON blocks after 📊 Summary JSON:
    pattern = r"📊 Summary JSON:\s*\[\s*{.*?}\s*\]"
    matches = re.findall(pattern, content, flags=re.DOTALL)

    summaries = []
    for block in matches:
        json_text = block.split("📊 Summary JSON:")[-1].strip()
        try:
            summaries.extend(json.loads(json_text))
        except json.JSONDecodeError as e:
            print(f"\n❌ Failed to parse block:\n{json_text}\nError: {e}")

    return summaries


# Function to append extracted summaries to result_*.json
def append_to_result_json(result_path, new_entries):
    """
    Appends summary entries to the result JSON file.

    Args:
        result_path (Path): Path to result_*.json file.
        new_entries (list): List of result dictionaries to append.
    """

    if result_path.exists() and result_path.stat().st_size > 0:
        try:
            with open(result_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"\n⚠️ Corrupted JSON: {result_path.name} — starting fresh")
            data = []
    else:
        data = []


    data.extend(new_entries)

    with open(result_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n📄 Appended {len(new_entries)} entries → {result_path.name}")


# Command center
def process_log_to_result():
    """
    Parse log file and update/create corresponding result JSON.
    """

    # Step 1: Look for a single log_*.txt file in current directory
    log_files = list(CURRENT_DIR.glob("log_*.txt"))
    if not log_files:
        print("\n❌ No log_*.txt file found")
        return

    # Step 2: Use the first log file
    log_file = log_files[0]
    print(f"\n📂 Parsing log file: {log_file.name}")

    # Step 3: Derive result file name from log file name
    timestamp = log_file.stem.replace("log_", "")
    result_path = CURRENT_DIR / f"result_{timestamp}.json"

    # Step 4: Extract all summary JSON blocks
    summaries = extract_summary_blocks(log_file)
    if not summaries:
        print("\n⚠️ No summary blocks found.")
        return

    # Step 5: Append extracted blocks to JSON
    append_to_result_json(result_path, summaries)

    print(f"\n✅ {len(summaries)} entries added to {result_path.name}")


# Execute
process_log_to_result()
print("\n✅ extract_log_summaries.py successfully executed")

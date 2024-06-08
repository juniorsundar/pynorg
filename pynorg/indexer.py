import os
import subprocess
import shutil
import json

def find_norg_files(index_dir: str):
    norg_files = []
    for root, _, files in os.walk(index_dir):
        if "journal" in root:
            continue
        for file in files:
            if file.endswith(".norg"):
                relative_path = os.path.relpath(os.path.join(root, file), index_dir)
                relative_path = f":$/{relative_path[:-5]}:"
                norg_files.append(relative_path)
    return norg_files

def run_ripgrep(text_list, search_dir):
    results = []

    for text in text_list:
        text_result = {"text": text, "matches": []}
        try:
            command = ["rg", "--json", "--fixed-strings", text, search_dir]
            result = subprocess.run(command, text=True, capture_output=True)
            if result.returncode == 0:
                json_lines = result.stdout.splitlines()
                for json_line in json_lines:
                    try:
                        match_data = json.loads(json_line)
                        if match_data.get("type") == "match":
                            for submatch in match_data["data"]["submatches"]:
                                line_number = match_data["data"]["line_number"]
                                start = submatch["start"] + 1
                                end = submatch["end"]
                                text_result["matches"].append(
                                    {
                                        "match": match_data["data"]["path"]["text"],
                                        "line": line_number,
                                        "start_column": start,
                                        "end_column": end,
                                    }
                                )
                    except json.JSONDecodeError:
                        continue
            else:
                text_result["matches"].append(
                    {
                        "match": None,
                        "line": None,
                        "start_column": None,
                        "end_column": None,
                        "error": (
                            result.stderr.strip()
                            if result.stderr
                            else f"No matches for: {text}"
                        ),
                    }
                )
        except Exception as e:
            text_result["matches"].append(
                {
                    "match": None,
                    "line": None,
                    "start_column": None,
                    "end_column": None,
                    "error": str(e),
                }
            )

        results.append(text_result)

    return results


def check(index_dir: str):
    contents = os.listdir(index_dir)
    if "cache.json" not in contents:
        print("No cache found.")
        return False
    else:
        return True


def reindex(index_dir: str):
    check_result = check(index_dir)

    if not check_result:
        norg_files = find_norg_files(index_dir) 
        rg_results = run_ripgrep(norg_files, index_dir)
        
        print(rg_results[0])
    return
import os
import subprocess
import json
import multiprocessing

from .helpers.norg_parser import extract_metadata

def find_norg_files(index_dir: str):
    norg_files = []
    for root, _, files in os.walk(index_dir):
        for file in files:
            if file.endswith(".norg"):
                relative_path = os.path.relpath(os.path.join(root, file), index_dir)
                relative_path = f":$/{relative_path.split('.')[0]}:"
                norg_files.append(relative_path)
    return norg_files


def strip_rel_addr(addr: str):
    addr_tuple = addr.split("/")
    addr_tuple[-1] = addr_tuple[-1].split(".")[0]
    return "/".join(addr_tuple)


def run_ripgrep_for_text(text, search_dir, return_dict):
    text_key = text.split(":")[1][2:]
    text_result = {f"{text_key}": {"backlinks": [], "metadata": {}}}
    text_result[f"{text_key}"]["metadata"] = extract_metadata(f"{search_dir}/{text_key}.norg")

    command = ["rg", "--json", "--fixed-strings", f":$/{text_key}:", search_dir]
    result = subprocess.run(command, text=True, capture_output=True)
    try:
        if result.returncode == 0:
            json_lines = result.stdout.splitlines()
            for json_line in json_lines:
                try:
                    match_data = json.loads(json_line)
                    if match_data.get("type") == "match":
                        for submatch in match_data["data"]["submatches"]:
                            match_addr = strip_rel_addr(
                                os.path.relpath(
                                    match_data["data"]["path"]["text"], search_dir
                                )
                            )
                            text_result[f"{text_key}"]["backlinks"].append(
                                {
                                    "match": match_addr,
                                    "line": match_data["data"]["line_number"],
                                    "col": submatch["start"] + 1,
                                }
                            )
                except json.JSONDecodeError:
                    continue
        else:
            text_result[f"{text_key}"]["backlinks"].append(
                {
                    "match": None,
                    "line": None,
                    "col": None,
                }
            )
    except Exception as e:
        text_result[f"{text_key}"]["backlinks"].append(
            {
                "match": None,
                "line": None,
                "col": str(e),
            }
        )

    return_dict[text_key] = text_result[f"{text_key}"]


def run_ripgrep(text_list, search_dir):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    processes = []

    for text in text_list:
        p = multiprocessing.Process(
            target=run_ripgrep_for_text, args=(text, search_dir, return_dict)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return return_dict.copy()


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
        with open(f"{index_dir}/cache.json", "w") as cache_file:
            json.dump(rg_results, cache_file)
    return

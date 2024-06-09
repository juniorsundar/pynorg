def extract_metadata(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    metadata = {}
    capture = False
    categories_capture = False
    categories_lines = []

    for line in lines:
        line = line.strip()
        if line == "@document.meta":
            capture = True
            continue
        elif line == "@end":
            if categories_capture:
                categories_capture = False
                if categories_lines:
                    # Manually parse categories
                    categories_str = "".join(categories_lines).strip("[]").strip()
                    metadata['categories'] = [cat.strip() for cat in categories_str.split(",") if cat.strip()]
            break
        elif capture:
            if ": " in line:
                key, value = line.split(": ", 1)
                if key in ["created", "updated"]:
                    # Convert ISO format string to datetime object if needed
                    # value = datetime.fromisoformat(value)
                    pass
                elif key == "categories":
                    categories_capture = True
                    categories_lines = [value]
                else:
                    metadata[key] = value
            elif categories_capture:
                if line:
                    categories_lines.append(line)
                else:
                    categories_capture = False
                    if categories_lines:
                        # Manually parse categories
                        categories_str = "".join(categories_lines).strip("[]").strip()
                        metadata['categories'] = [cat.strip() for cat in categories_str.split(",") if cat.strip()]
            else:
                categories_capture = False
                if categories_lines:
                    # Manually parse categories
                    categories_str = "".join(categories_lines).strip("[]").strip()
                    metadata['categories'] = [cat.strip() for cat in categories_str.split(",") if cat.strip()]

    if 'categories' not in metadata:
        metadata['categories'] = []

    return metadata


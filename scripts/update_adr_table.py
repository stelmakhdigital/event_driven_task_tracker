import glob
import os
import re

ADR_DIR = "docs/ADRs/"
README_PATH = "docs/readme.md"
MAX_DESC_LENGTH = 200
COUNTS_ADR_FOR_TABLE = 6

def extract_adr_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(file_path)
    match = re.match(r'^(\d{4})_', filename)
    if match:
        adr_number = match.group(1)
    else:
        adr_number = "0000"
    
    data = {
        "number": adr_number,
        "date": "Unknown",
        "status": "Unknown",
        "author": "Unknown",
        "description": "No description"
    }
    
    date_match = re.search(r"\* \*\*Data:\*\* (\d{4}-\d{2}-\d{2})", content)
    if date_match:
        data["date"] = date_match.group(1)
    
    status_match = re.search(r"\* \*\*Status:\*\* (.+)", content)
    if status_match:
        data["status"] = status_match.group(1).split('/')[0].strip()
    
    author_match = re.search(r"\* \*\*Author:\*\* (.+)", content)
    if author_match:
        data["author"] = author_match.group(1)
    
    desc_match = re.search(r"## Description\n(.+?)(\n## |$)", content, re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()
        if len(description) > MAX_DESC_LENGTH:
            description = description[:MAX_DESC_LENGTH] + "..."
        data["description"] = description
    
    return data

def main():
    # забираем указанное кол-во ADR файлов
    adr_files = glob.glob(os.path.join(ADR_DIR, "[0-9]*_*.md"))
    adr_files.sort(key=lambda x: int(re.search(r'(\d{4})_', os.path.basename(x)).group(1)), reverse=True)
    adr_files = adr_files[:COUNTS_ADR_FOR_TABLE]
    
    table = "| Number ADR | Data | Author | Status | Description |\n"
    table += "|------------|------|--------|--------|-------------|\n"
    
    for file in adr_files:
        data = extract_adr_data(file)
        table += f"| {data['number']} | {data['date']} | {data['author']} | {data['status']} | {data['description']} |\n"
    
    # вставляем в  README
    with open(README_PATH, 'r+', encoding='utf-8') as f:
        content = f.read()
        new_content = re.sub(
            r'(<!-- ADR_TABLE_START -->).*?(<!-- ADR_TABLE_END -->)',
            r'\1\n' + table + r'\2',
            content,
            flags=re.DOTALL
        )
        f.seek(0)
        f.write(new_content)
        f.truncate()

if __name__ == "__main__":
    main()
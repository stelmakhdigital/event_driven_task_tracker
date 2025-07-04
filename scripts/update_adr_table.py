import glob
import os
import re
from datetime import datetime

ADR_DIR = "docs/ADRs/"
README_PATH = "docs/readme.md"
MAX_DESC_LENGTH = 200
COUNTS_ADR_FOR_TABLE = 6

def extract_adr_data(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    data = {
        "number": os.path.basename(file_path).split('-')[0],
        "date": re.search(r"\* \*\*Data:\*\* (\d{4}-\d{2}-\d{2})", content).group(1),
        "status": re.search(r"\* \*\*Status:\*\* (\w+)", content).group(1),
        "author": re.search(r"\* \*\*Author:\*\* (.+)", content).group(1),
        "description": re.search(r"## Description\n(.+?)(\n## |$)", content, re.DOTALL).group(1).strip()
    }
    
    # описание не больше указанного кол-во символов чтобы влезло в таблицу
    if len(data["description"]) > MAX_DESC_LENGTH:
        data["description"] = data["description"][:MAX_DESC_LENGTH] + "..."
    
    return data

def main():
    # Получаем последние 6 ADR-файлов
    adr_files = sorted(glob.glob(os.path.join(ADR_DIR, "*.md")), key=os.path.getmtime, reverse=True)[:COUNTS_ADR_FOR_TABLE]
    
    # Формируем таблицу
    table = "| Number ADR | Data | Author | Status | Description |\n"
    table += "|------------|------|--------|--------|-------------|\n"
    
    for file in adr_files:
        data = extract_adr_data(file)
        table += f"| {data['number']} | {data['date']} | {data['author']} | {data['status']} | {data['description']} |\n"
    
    # Обновляем README
    with open(README_PATH, 'r+') as f:
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
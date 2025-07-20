import os
import json
from heading_extractor import extract_headings

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_pdf(input_path, output_path):
    outline_json = extract_headings(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(outline_json, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            json_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            print(f"Processing: {filename}")
            process_pdf(pdf_path, json_path)

if __name__ == "__main__":
    main()

import os
import json
import time
import re
from tqdm import tqdm
import sys
from dotenv import load_dotenv
from llama_cpp import Llama
load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../llama.cpp/tinyllama-1.1b-chat-v1.0.Q5_K_S.gguf"))

print("Resolved MODEL_PATH:", MODEL_PATH)

INPUT_FILE = "data/dfoeufs_with_predictions_with_ground_truth.jsonl"
OUTPUT_FILE = "data/dfoeufs_with_predictions_with_ground_truth_with_llama.jsonl"

# Initialize Llama model once globally
llm = Llama(model_path=MODEL_PATH,
            n_ctx=2048)

def parse_groq_response(text):
    # Regex to capture the value after each key
    breeding_pattern = r'"breeding_type_related"\s*:\s*"([^"]*)"'
    weight_pattern = r'"weight_related"\s*:\s*((?:"[^"]*"(?:,\s*)?)+)'

    breeding_match = re.search(breeding_pattern, text, re.IGNORECASE)
    weight_match = re.search(weight_pattern, text, re.IGNORECASE)

    breeding_value = breeding_match.group(1).strip() if breeding_match else ""
    weight_value = ""

    if weight_match:
        # The weight_related part may contain multiple quoted strings separated by commas
        all_weights = re.findall(r'"([^"]*)"', weight_match.group(1))
        weight_value = ", ".join(w.strip() for w in all_weights)

    return {
        "breeding_type_related": breeding_value,
        "weight_related": weight_value
    }

def extract_spans_from_ocr(ocr_text):
    prompt = f"""
You are a text extraction assistant. Given the following OCR text from packaging, extract two fields:

breeding_type_related: Any text span(s) related to breeding type (e.g. free range, cage, barn, organic hens, etc.)
weight_related: Any text span(s) related to weight, quantity, or number of eggs (e.g. 12 large, 53 g, dozen, weight 200g, etc.)

The information can be in languages other than English, make sure to extract the relevant spans regardless of the language.

Return ONLY a JSON object with keys "breeding_type_related" and "weight_related" and the corresponding text snippets (or empty string if none found).

Don't make any other comments.

OCR text:
\"\"\"
{ocr_text}
\"\"\"
"""
    output = llm(prompt, max_tokens=256, temperature=0, top_p=1)
    text_response = output['choices'][0]['text'].strip()

    try:
        spans = parse_groq_response(text_response)
    except json.JSONDecodeError:
        print("[DEBUG] JSON decode error in response:", text_response)
        spans = {
            "breeding_type_related": "",
            "weight_related": ""
        }

    return spans

def main():
    # Track already processed codes to avoid duplicates
    processed_codes = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f_out:
            for line in f_out:
                try:
                    existing_entry = json.loads(line)
                    code = existing_entry.get("code")
                    if code:
                        processed_codes.add(code)
                except json.JSONDecodeError:
                    continue

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "a", encoding="utf-8") as fout:  # append mode

        for line in tqdm(fin):
            entry = json.loads(line)
            code = entry.get("code")

            if code in processed_codes:
                continue  # skip already processed

            ocr_text = entry.get("ocr_text", "")

            if not ocr_text:
                entry["groq_spans"] = {
                    "breeding_type_related": "",
                    "weight_related": ""
                }
            else:
                try:
                    spans = extract_spans_from_ocr(ocr_text)
                    entry["groq_spans"] = spans
                except Exception as e:
                    print(f"Error processing entry with code {code}: {e}")
                    entry["groq_spans"] = {
                        "breeding_type_related": "",
                        "weight_related": ""
                    }

            fout.write(json.dumps(entry, ensure_ascii=False) + "\n")
            fout.flush()  # ensure written immediately
            processed_codes.add(code)
            time.sleep(0.2)  # adjust delay as needed

if __name__ == "__main__":
    main()

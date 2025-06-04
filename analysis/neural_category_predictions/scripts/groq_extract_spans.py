import os
import json
import time
import re
from tqdm import tqdm 
import sys
from dotenv import load_dotenv
from openai import OpenAI  # assuming you have installed Groq's OpenAI-compatible client

load_dotenv()

INPUT_FILE = "data/dfoeufs_with_predictions_with_ground_truth.jsonl"
OUTPUT_FILE = "data/dfoeufs_with_predictions_with_ground_truth_with_groq.jsonl"
MODEL = "llama3-70b-8192"



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


def extract_spans_from_ocr(client, ocr_text):
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

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0,
        top_p=1,
        n=1
    )

    text_response = response.choices[0].message.content.strip()
    #print(text_response)

    try:
        spans = parse_groq_response(text_response)
    except json.JSONDecodeError:
        print("[DEBUG] JSON falsely decoded")
        spans = {
            "breeding_type_related": "",
            "weight_related": ""
        }

    return spans


def main():
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

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
                    spans = extract_spans_from_ocr(client, ocr_text)
                    entry["groq_spans"] = spans
                except Exception as e:
                    error_msg = str(e)
                    if "rate_limit_exceeded" in error_msg or "Error code: 429" in error_msg or "Error code: 503" in error_msg:
                        print(f"\n[!] Rate limit exceeded. Exiting script. Full error:\n{error_msg}")
                        sys.exit(1)
                    
                    print(f"Error processing entry with code {code}: {e}")
                    entry["groq_spans"] = {
                        "breeding_type_related": "",
                        "weight_related": ""
                    }


            fout.write(json.dumps(entry, ensure_ascii=False) + "\n")
            fout.flush()  # ensure written immediately
            processed_codes.add(code)
            time.sleep(0.2)  # adjust for rate limiting


if __name__ == "__main__":
    main()
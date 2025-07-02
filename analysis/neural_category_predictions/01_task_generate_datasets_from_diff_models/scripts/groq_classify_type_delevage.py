import os
import json
from openai import OpenAI  # <-- synchronous client
from dotenv import load_dotenv
from tqdm import tqdm
import os

load_dotenv()

INPUT_FILE = "data/dfoeufs_with_predictions_with_ground_truth_with_groq_fixed.jsonl"
OUTPUT_FILE = "data/dfoeufs_groq_predictions_with_breeding_type.jsonl"
MODEL = "llama3-8b-8192"

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

system_prompt = """
You are an expert in classifying egg packaging based on OCR text. The text may contain multiple languages, such as English, French, German, Spanish, Dutch, or Italian. Your task is to analyze the text and determine the most likely chicken breeding type.

Possible breeding types (output only one of these):
- barn
- cage
- free_range

Rules:

1️⃣ cage
- Codes: 3
- Keywords: cage, caged hens, cages, battery cage, cage farming, élevage en cage, Hühnerkäfig, enjaulado, en batterie, in gabbia, in kooien.

2️⃣ barn
- Codes: 2
- Keywords: barn, indoor housing, raised indoors, aviary, au sol, Bodenhaltung, sin jaula, a terra, scharrel.

3️⃣ free_range
- Codes: 0 or 1
- Keywords: free range, free roaming, open air, organic, pasture, plein air, bio, biologique, ökologisch, ecological, ecologico, ecologiche, pasture raised, plein air, Freilandhaltung, campero.

OCR text may also contain noisy or partial text (e.g. "ALLAVENS ROAM FREELY IN HARNE" could mean "All hens roam freely in barn").

👉 Normalize to the most likely breeding type based on keywords.

👉 If text contains no clues, return an empty string, don't make anything up! If a human would not be able to deduce, don't deduce anything.

👉 Output only one of:
- barn
- cage
- free_range

👉 Output NOTHING else. Only "barn" OR "cage" OR "free_range". Don't leave any extra comments or reasoning.

If you can't determine the type, return an empty string
"""

def classify_breeding(ocr_text):
    try:
        #print(f"[DEBUG] Sending OCR text to API: {ocr_text[:30]}...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"OCR text:\n{ocr_text}\n\nWhat is the breeding type?"}
            ],
            max_tokens=20,
            temperature=0,
            top_p=1,
            n=1
        )
        result = response.choices[0].message.content.strip()
        #print(f"[DEBUG] Received response: {result}")
        return result
    except Exception as e:
        #print(f"[ERROR] classify_breeding failed: {e}")
        return None


def main():
    processed_codes = set()

    # If output file exists, load processed codes first
    if os.path.exists(OUTPUT_FILE):
        #print("[DEBUG] Loading already processed codes from output file")
        with open(OUTPUT_FILE, "r") as outfile:
            for line in outfile:
                record = json.loads(line)
                code = record.get("code")  # replace "code" with your unique key
                if code:
                    processed_codes.add(code)

    #print("[DEBUG] Starting to process input and write output")

    with open(INPUT_FILE, "r") as infile, open(OUTPUT_FILE, "a") as outfile:
        for line in tqdm(infile):
            record = json.loads(line)
            code = record.get("code")  # same unique key here

            if code in processed_codes:
                # Already processed, skip
                continue

            ocr_text = record.get("ocr_text")
            if ocr_text:
                breeding_type = classify_breeding(ocr_text)
            else:
                breeding_type = None

            record["groq_breeding_type_prediction"] = breeding_type
            outfile.write(json.dumps(record) + "\n")
            processed_codes.add(code)  # Add to set to avoid duplicates in this run

    #print("[DEBUG] Finished processing")

if __name__ == "__main__":
    main()

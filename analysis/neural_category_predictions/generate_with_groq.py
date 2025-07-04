import pandas as pd
import json

# File paths
csv_path = "data/ocr_elevage.csv"  # has code, ocr_text, elevage
jsonl_path = "data/dfoeufs_with_predictions_with_ground_truth_with_groq_spans.jsonl"  # has code and groq_spans

# Load CSV
df_csv = pd.read_csv(csv_path)

# Load JSONL into dict keyed by 'code'
json_data = {}
with open(jsonl_path, 'r') as f:
    for line in f:
        obj = json.loads(line)
        code = str(obj['code'])
        json_data[code] = obj.get("groq_spans", {}).get("breeding_type_related", None)

# Add groq_spans["breeding_type_related"] to the CSV
df_csv["breeding_type_related"] = df_csv["code"].astype(str).map(json_data)

print(df_csv["breeding_type_related"].tolist())

# Reorder columns if needed
df_csv = df_csv[["code", "ocr_text", "breeding_type_related", "elevage"]]

# Save new CSV
#df_csv.to_csv("merged_breeding_data.csv", index=False)

print("✅ Saved to merged_breeding_data.csv")

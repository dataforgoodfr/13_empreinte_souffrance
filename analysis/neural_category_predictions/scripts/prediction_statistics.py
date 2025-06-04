import json
import pandas as pd
import numpy as np
import math
from collections import defaultdict
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
from collections import Counter


KERAS_TO_GT_LABELS = {
    "en:free-range-chicken-eggs": ["free_range"],
    "en:barn-chicken-eggs": ["barn"],
    "en:cage-chicken-eggs": ["conventional_cage", "furnished_cage"],
}

GT_TO_KERAS_LABELS = {
    gt: keras for keras, gts in KERAS_TO_GT_LABELS.items() for gt in gts
}


def safe_parse_json(line):
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        # Try to parse only the first JSON object on the line
        try:
            first_brace = line.index('{')
            last_brace = line.rindex('}') + 1
            cleaned_line = line[first_brace:last_brace]
            return json.loads(cleaned_line)
        except Exception as e:
            print(f"[ERROR] Could not parse line: {e}")
            return None
        
        
def is_valid_gt(gt):
    return (
        gt
        and isinstance(gt, str)
        and gt.lower() not in ["none", "nan"]
    )


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def dataset_statistics(entries):
    stats = {
        "total": len(entries),
        "gt": 0,
        "ocr": 0,
        "keras": 0,
        "ocr_no_gt": 0,
        "keras_no_gt": 0,
    }
    for e in entries:
        gt = e.get("ground_truth")
        ocr = e.get("ocr_text")
        keras = e.get("keras_category_classifier_v3_prediction")

        has_gt = is_valid_gt(gt)
        has_ocr = bool(ocr and str(ocr).strip())
        has_keras = keras is not None

        stats["gt"] += has_gt
        stats["ocr"] += has_ocr
        stats["keras"] += has_keras
        stats["ocr_no_gt"] += has_ocr and not has_gt
        stats["keras_no_gt"] += has_keras and not has_gt

    print("🧾 Dataset Stats")
    for k, v in stats.items():
        print(f"{k.replace('_', ' ').capitalize()}: {v}")


def extract_label_sets(entries):
    gt_labels = set()
    keras_labels = set()
    both_present = 0

    for e in entries:
        gt = e.get("ground_truth")
        keras_preds = e.get("keras_category_classifier_v3_prediction")

        if is_valid_gt(gt):
            gt_labels.add(gt)
        if is_valid_gt(gt) and keras_preds:
            both_present += 1
        if keras_preds:
            for label, _ in keras_preds:
                keras_labels.add(label)

    print(f"\n📌 Both GT and Keras predictions present: {both_present}")
    print(f"\n📌 Unique ground truth labels: {gt_labels}")
    print(f"\n📌 Unique Keras labels ({len(keras_labels)}):")
    for label in sorted(keras_labels):
        print("  ", label)


def compute_topk_metrics(entries, top_k=2):
    y_true = []
    y_pred_top1 = []
    matched_at_topk = 0
    wrong_labels = set()

    for e in entries:
        gt = e.get("ground_truth")
        preds = e.get("keras_category_classifier_v3_prediction")

        if not is_valid_gt(gt) or not preds:
            continue

        mapped_gt = GT_TO_KERAS_LABELS.get(gt, "wrong")
        if mapped_gt == "wrong":
            wrong_labels.add(gt)
            continue

        top_preds = [p[0] for p in preds[:top_k]]

        y_true.append(mapped_gt)
        y_pred_top1.append(top_preds[0])

        if mapped_gt in top_preds:
            matched_at_topk += 1

    top1_acc = sum(yt == yp for yt, yp in zip(y_true, y_pred_top1)) / len(y_true)
    topk_acc = matched_at_topk / len(y_true)

    print("\n📈 Evaluation (Top-1 / Top-2)")
    print(f"Evaluated examples: {len(y_true)}")
    print("Top-1 Accuracy:", round(top1_acc, 4))
    print("Top-2 Accuracy:", round(topk_acc, 4))
    print("Precision (macro):", round(precision_score(y_true, y_pred_top1, average='macro', zero_division=0), 4))
    print("Recall (macro):", round(recall_score(y_true, y_pred_top1, average='macro', zero_division=0), 4))
    print("F1-score (macro):", round(f1_score(y_true, y_pred_top1, average='macro', zero_division=0), 4))
    print("\nClassification report (top-1 prediction):\n")
    print(classification_report(y_true, y_pred_top1, digits=4, zero_division=0))
    print("\nUnknown/wrong GT labels found:", wrong_labels)


def compute_topk_accuracy_per_class(entries, top_k=2):
    class_counts = defaultdict(int)
    class_hits = defaultdict(int)
    wrong_labels = set()

    for e in entries:
        gt = e.get("ground_truth")
        preds = e.get("keras_category_classifier_v3_prediction")

        if not is_valid_gt(gt) or not preds:
            continue

        mapped_gt = GT_TO_KERAS_LABELS.get(gt)
        if not mapped_gt:
            wrong_labels.add(gt)
            continue

        class_counts[mapped_gt] += 1
        top_preds = [p[0] for p in preds[:top_k]]
        if mapped_gt in top_preds:
            class_hits[mapped_gt] += 1

    print("\n🎯 Top-2 Accuracy per class:")
    for label in class_counts:
        acc = class_hits[label] / class_counts[label]
        print(f"{label:30s}: {acc:.4f} ({class_hits[label]}/{class_counts[label]})")

    if wrong_labels:
        print("\nUnknown GT labels found:", wrong_labels)


def ground_truth_none_breeding_type_present(input_file):
    counter = Counter()

    count = 0

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = safe_parse_json(line)
            if entry is None:
                continue
            ground_truth = entry.get("ground_truth")
            code = entry.get("code", "UNKNOWN_CODE")
            breeding_type = entry.get("groq_spans", {}).get("breeding_type_related", "")

            # Normalize ground_truth for counting
            if ground_truth is None:
                normalized = "None (Python None)"
            elif isinstance(ground_truth, str) and ground_truth.strip().lower() in {"", "none", "nan"}:
                normalized = f"String: '{ground_truth.strip()}'"
            else:
                normalized = str(ground_truth).strip()

            counter[normalized] += 1

            # Print only if ground_truth is null-like
            if normalized.startswith("None") or normalized.startswith("String:") and breeding_type:
                print(f"Code: {code} → Breeding Type: {breeding_type!r}")
                count += 1

    print(f"Number of products with OCR-deciphered breeding type and no ground truth: {count}")

    print("\nSummary of ground_truth values:")
    for val, count in counter.items():
        print(f"{val:30} → {count}")



def ground_truth_free_range_breeding_type_present(input_file):
    count = 0
    count_bio = 0

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = safe_parse_json(line)
            if entry is None:
                continue
            ground_truth = entry.get("ground_truth", "") #.strip().lower()
            code = entry.get("code", "UNKNOWN_CODE")
            breeding_type = entry.get("groq_spans", {}).get("breeding_type_related", "")

            if ground_truth == "free_range" and breeding_type:
                #print(f"Code: {code} → Breeding Type: {breeding_type!r}")
                count += 1
                if "bio" in breeding_type.lower():
                    count_bio += 1
                    #print(f"Code: {code} == free_range → Breeding Type: {breeding_type!r}")
            

    print(f"\nTotal entries with ground_truth == 'free_range': {count}")
    print(f"\nTotal entries with ground_truth == 'free_range' and bio on packaging: {count_bio}")



def main():
    jsonl_path = "data/dfoeufs_with_predictions_with_ground_truth.jsonl"
    jsonl_path_groq = "data/dfoeufs_with_predictions_with_ground_truth_with_groq.jsonl"

    entries = load_jsonl(jsonl_path)

    dataset_statistics(entries)
    extract_label_sets(entries)
    compute_topk_metrics(entries, top_k=2)
    compute_topk_accuracy_per_class(entries, top_k=2)
    ground_truth_none_breeding_type_present(jsonl_path_groq)
    ground_truth_free_range_breeding_type_present(jsonl_path_groq)


if __name__ == "__main__":
    main()

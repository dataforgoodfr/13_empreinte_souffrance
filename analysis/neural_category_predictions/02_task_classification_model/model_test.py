from model2vec.train import StaticModelForClassification
from huggingface_hub import hf_hub_download
import json

# Load the model — no need to explicitly pass tokenizer
model = StaticModelForClassification.from_pretrained(model_name="adeliaKH/breeding_type_classificator", out_dim=3)

with open("saved_model/classes.json", "r") as f:
    classes = json.load(f)

print(model.classes_)
print(model.out_dim)

# Assign it back to the model
model.classes_ = classes


# Run prediction
texts = ["barn chicken", "free range chicken", "furnished cage chicken"]
print(texts)
preds = model.predict(texts)
print(preds)

import pandas as pd
import os
from pathlib import Path
from openai import OpenAI
from time import sleep
from tqdm import tqdm

class SynthGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model_name = "mistral-saba-24b"
        self.df_path = Path(__file__).resolve().parent.parent.parent / "data/ocr_elevage.csv"
        self.df = pd.read_csv(self.df_path)
        self._prepare_barn_texts()

        self.output_path = Path(__file__).resolve().parent.parent.parent / "data/synthetic_barn_ocr.csv"

    def _prepare_barn_texts(self):
        self.barn_texts = (
            self.df[self.df["elevage"] == "barn"]["ocr_text"]
            .dropna()
            .apply(lambda x: " ".join(str(x).split()))
            .tolist()
        )

    def _load_prompt(self, example: str):
        return f"""
Tu es un générateur de textes OCR sur des emballages d'œufs.
Voici un exemple d’étiquette OCR pour des œufs issus d’élevages au sol :

- {example}

Génère une seule nouvelle ligne OCR crédible, différente mais similaire à celle-ci.
Assure-toi que le texte généré ait une **longueur comparable** et un **niveau de détail équivalent**.
Il doit s'agir des poules élevés AU SOL, pas d'autre type! Pas de plen air, pas de cage!
        """.strip()

    def generate_data(self):
        all_generated = []

        for i, example in enumerate(tqdm(self.barn_texts)):
            prompt = self._load_prompt(example)

            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                content = response.choices[0].message.content.strip()
                # Extract the line and clean it
                line = content.lstrip("-•* ").strip()

                all_generated.append({
                    "code": f"synthetic_{i}",
                    "ocr_text": line,
                    "elevage": "barn"
                })

                print(f"✅ {i + 1}/{len(self.barn_texts)}: Generated")

            except Exception as e:
                print(f"❌ Error at index {i}: {e}")
                sleep(5)

        return all_generated

    def save_to_csv(self):
        all_generated = self.generate_data()
        pd.DataFrame(all_generated).to_csv(self.output_path, index=False)
        print(f"✅ All synthetic OCRs saved to {self.output_path}")


if __name__ == "__main__":
    synthgenerator = SynthGenerator()
    synthgenerator.save_to_csv()

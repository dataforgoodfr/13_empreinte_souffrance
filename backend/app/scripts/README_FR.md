# Extraction et Mise à Jour des Données Produits OpenFoodFacts

Ce dépôt contient trois scripts Python pour travailler avec les données OpenFoodFacts :

1. **extract_egg_products.py** : Extraction et filtrage des produits de catégorie "eggs" depuis la base de données OpenFoodFacts exportée au format Parquet
2. **update_off_product_data.py** : Upload vers OpenFoodFacts des données produit de quantité, et mode d'élevage via l'API d'écriture
3. **process_product_data.py** : Analyse et traitement des données produits œufs avec prédictions OCR et calcul des types d'élevage

## Dépendances

Installez les dépendances avec :

```bash
uv pip install --group dev
```

---

## 1. extract_egg_products.py

### Description

Ce script télécharge un fichier Parquet volumineux (~4 Go) contenant la base de données produit OpenFoodFacts, filtre les produits correspondant aux œufs de poule (catégorie **en:eggs**), et exporte ces données sous format CSV.
Les données parquet, csv et txt sont stockées dans le fichier data/

### Fonctionnalités principales

- Téléchargement optionnel du fichier **food.parquet** depuis Hugging Face **https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet**.
- Filtrage avec DuckDB des produits contenant la catégorie `en:eggs`, excluant certaines catégories non conernées par les œufs de poules (ex : **en:duck-eggs**, **en:meals**).
- Export dans un fichier **eggs_from_parquet.csv** avec sérialisation JSON des colonnes complexes.
- Export des colonnes au format json dans un fichier **cols_to_json.txt** pour faciliter l'import ultérieur du csv
- Suppression optionnelle du fichier Parquet local.

### Utilisation

```bash
python extract_egg_products.py [--download] [--remove] [--csv-export]
```

Options :

- `--download` : télécharge le fichier Parquet avant traitement.
- `--remove` : supprime le fichier Parquet après export.
- `--csv-export` : exporte directement le CSV filtré sans demander.
Si les options ne sont pas fournies, il sera demandé ses choix à l'utilisateur dans l'interface CLI

### Exemples

- Télécharger le fichier Parquet et exporter le CSV, conserver le fichier Parquet pour réutilisation :

```bash
python extract_egg_products.py --download --csv-export
```

- Exporter le CSV à partir d'un fichier Parquet existant à partir d'un fichier parquet déjà stocké et conservé :

```bash
python extract_egg_products.py --csv-export
```

- Pour récupérer les dernière données produit sans encombrer l'espace disque : télécharger le fichier Parquet, exporter le csv et supprimer le fichier Parquet :

```bash
python extract_egg_products.py --download --csv-export --remove
```
---

## 2. Script de mise à jour de données produit OpenFoodFacts : update_off_product_data.py


Automatise les mises à jour de données produit sur [OpenFoodFacts](https://world.openfoodfacts.org/) via l’API d’écriture.

### Vue d’ensemble

Le script permet :

- L’ajout de tags de catégorie (élevage et calibre)
- La mise à jour du champ quantité (remplacement)
- Le traitement par lot depuis des fichiers CSV
- Le test sur un seul produit
- La vérification par défaut de l'existence des codes-barres pour éviter de créer des produits


### Lancer le script

```bash
python update_product_data.py [options]
```

#### Mise à jour par lot

```bash
python update_product_data.py --breeding --file breeding.csv
python update_product_data.py --caliber --file caliber.csv
python update_product_data.py --quantity --file quantity.csv
```

#### Test sur un seul produit

```bash
python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:organic-eggs"
python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
```

### Format CSV

- Les fichiers doivent être placés dans le dossier `./data/`
- Colonnes obligatoires : `barcode` et `tag`
- Séparateurs acceptés : `,` ou `;`

Exemple :

```csv
barcode,tag
0061719011930,en:free-range-chicken-eggs
```

### Comportement des opérations

- `--breeding` et `--caliber` : les tags sont **ajoutés** en tant que catégories.
- `--quantity` : la valeur est **remplacée**.

#### Tags valides

##### Élevage :

- `en:eggs`
- `en:chicken-eggs`
- `en:cage-chicken-eggs`
- `en:barn-chicken-eggs`
- `en:free-range-chicken-eggs`
- `en:organic-eggs`

##### Calibre :

- `en:small-eggs`
- `en:medium-eggs`
- `en:large-eggs`
- `en:extra-large-eggs`

##### Quantité :

- Format : `"{nombre} pcs"` (ex. `12 pcs`)

### API utilisée

- **GET** (vérification de code-barres) :
  `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`

- **POST** (mise à jour) :
  `https://world.openfoodfacts.org/cgi/product_jqm2.pl`

### Vérification des codes-barres

- Activée par défaut
- Vérification API pour chaque code-barres
- Limite : ~100 requêtes/minute (0.6s entre appels)
- Pour désactiver : `--no-verify-barcodes`

> ⚠️ Si la vérification est désactivée, un produit sera **créé** si le code-barres n'existe pas.

### Authentification requise

Le script nécessite des **identifiants OpenFoodFacts**.

Méthodes :

- Arguments CLI : `--username`, `--password`
- Saisie interactive si non fournis

---

## 3. Script d'analyse et traitement des données produits : process_product_data.py

### Description

Ce script traite et analyse les données produits œufs en combinant les données OpenFoodFacts avec les prédictions OCR et les calculs de types d'élevage. Il génère des visualisations sous forme de graphiques sunburst pour analyser la couverture des données.

### Fonctionnalités principales

- Chargement et parsing des données CSV avec colonnes JSON
- Intégration des prédictions OCR depuis un fichier JSONL
- Calcul automatique des types d'élevage et quantités d'œufs via le `PainReportCalculator`
- Génération de graphiques sunburst interactifs pour visualiser la répartition des données
- Export des données enrichies au format CSV
- Filtrage des produits français vs internationaux

### Structure des données

Le script traite plusieurs sources de données :

- **Données produits** : fichier CSV `eggs_from_parquet.csv` avec colonnes JSON
- **Prédictions OCR** : fichier JSONL contenant les extractions de texte et prédictions
- **Métadonnées** : fichier `cols_to_json.txt` listant les colonnes à parser en JSON

### Fonctions principales

#### Chargement et parsing des données

```python
def load_eggs_df() -> pd.DataFrame
def safe_json_loads(s) -> object
def create_dataframe_from_jsonl(file_path: Path) -> pd.DataFrame
```

#### Enrichissement des données

```python
def enrich_eggs_with_ocr(eggs_df: pd.DataFrame, ocr_df: pd.DataFrame) -> pd.DataFrame
def row_to_product_data(row) -> ProductData
def row_to_breeding_type_and_quantity(row) -> tuple
```

#### Visualisation

```python
def plot_egg_sunburst(dataset: str, include_caliber: bool, eggs_df: pd.DataFrame) -> None
def prepare_egg_display_columns(df: pd.DataFrame) -> pd.DataFrame
```

### Calcul des métriques d'élevage

Le script utilise le `PainReportCalculator` pour extraire :

- **Nombre d'œufs** : comptage automatique depuis les données produit
- **Calibre** : taille des œufs (small, medium, large, extra-large)
- **Type d'élevage** : mode d'élevage (cage, barn, free-range, organic)

### Codes de retour

- `egg_count = -1` : quantité non trouvée
- `egg_count = -2` : produit non géré par le calculateur
- `caliber = "no caliber"` : calibre non déterminé
- `breeding = "no breeding"` : type d'élevage non déterminé

### Visualisations générées

Le script génère des graphiques sunburst avec deux modes :

- **Données mondiales** : tous les produits œufs avec distinction français/non-français
- **Données françaises** : focus sur les produits français uniquement

Options d'affichage :

- Avec ou sans inclusion du calibre dans la hiérarchie
- Pourcentages et valeurs absolues affichés sur chaque segment

### Fichiers de sortie

- `processed_products.csv` : données complètes avec calculs d'élevage
- `processed_products_fr.csv` : sous-ensemble des produits français

### Structure des chemins

```
ROOT_PATH/
├── analysis/neural_category_predictions/data/
│   └── dfoeufs_with_predictions_with_ground_truth_with_groq.jsonl
└── data/
    ├── eggs_from_parquet.csv
    ├── cols_to_json.txt
    ├── processed_products.csv
    └── processed_products_fr.csv
```

### Utilisation

```bash
python process_product_data.py [--dataset {world,france}] [--include-caliber] [--no-plot] [--no-process]
```

#### Options

- `--dataset {world,france}` : choix du jeu de données à visualiser (défaut: france)
- `--include-caliber` : inclure les calibres dans le graphique sunburst
- `--no-plot` : désactiver l'affichage du graphique
- `--no-process` : ignorer le traitement et charger les données déjà traitées

#### Exemples

```bash
# Traitement avec graphique par défaut (France, sans calibres)
python process_product_data.py

# Graphique mondial sans calibres
python process_product_data.py --dataset world

# Graphique français avec calibres
python process_product_data.py --dataset france --include-caliber

# Traitement uniquement, sans affichage
python process_product_data.py --no-plot

# Affichage uniquement, sans retraitement (charge les données déjà traitées)
python process_product_data.py --no-process --dataset world --include-caliber
```

Le script s'exécute et :

1. Charge les données œufs depuis le CSV
2. Intègre les prédictions OCR depuis le JSONL
3. Calcule les types d'élevage et quantités
4. Sauvegarde les données enrichies
5. Génère un graphique sunburst selon les options choisies (par défaut : France sans calibres)

### Dépendances spécifiques

- `plotly.express` pour les visualisations sunburst
- Module métier `app.business.open_food_facts.pain_report_calculator`
- Schémas de validation `app.schemas.open_food_facts.external.ProductData`

# Extraction et Mise à Jour des Données Produits OpenFoodFacts

Ce dépôt contient trois scripts Python pour travailler avec les données OpenFoodFacts :

1. **extract_egg_products.py** : Extraction et filtrage des produits de catégorie "eggs" depuis la base de données OpenFoodFacts exportée au format Parquet
2. **update_off_product_data.py** : Upload vers OpenFoodFacts des données produit de quantité, et mode d'élevage via l'API d'écriture
3. **process_product_data.py** : Analyse et traitement des données produits œufs avec prédictions OCR et calcul des types d'élevage
4. **export_computed_data_to_excel.py** : Export des données traitées vers des fichiers Excel formatés avec images et colonnes d’analyse

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
- Le remplacement complet de la liste des catégories
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
python update_product_data.py --categories --file categories.csv
```

#### Test sur un seul produit

```bash
python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:organic-eggs"
python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
python update_product_data.py --test-categories --barcode 0061719011930 --tag "en:eggs,en:chicken-eggs,en:free-range-chicken-eggs"
```

### Format CSV

- Les fichiers doivent être placés dans le dossier `./data/`
- Colonnes obligatoires : `barcode` et `tag`
- Séparateurs acceptés : `,` ou `;`
- Séparateur pour le script de mise à jour des catégories : `;`

Exemple :

```csv
barcode,tag
0061719011930,en:free-range-chicken-eggs
```

```csv
barcode;tag
0061719011930;"en:free-range-chicken-eggs,en:chicken-eggs,en:eggs"
```

```csv
barcode;tag
0061719011930;"en:free-range-chicken-eggs,en:chicken-eggs,\nen:eggs"
```

### Comportement des opérations

- `--breeding` et `--caliber` : les tags sont **ajoutés** en tant que catégories.
- `--quantity` : la valeur est **remplacée**.
- `--categories` : remplace la liste complète des catégories par les tags fournis.

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

##### Catégories :

Toutes les chaînes commençant par `en:` ou `fr:` correspondant aux tags de catégorie OpenFoodFacts.

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

Ce script traite et analyse les données produits œufs en combinant les données OpenFoodFacts avec les prédictions OCR et les résultats du calculateurr (PainReportCalculator). Il génère des visualisations sous forme de graphiques sunburst pour visualiser la couverture des données.

### Fonctionnalités principales

- Chargement et parsing des données des produits au format CSV avec colonnes JSON
- Calcul automatique des types d'élevage et quantités d'œufs via le `PainReportCalculator`
- Intégration des prédictions OCR depuis un fichier JSONL
- Export des données enrichies au format CSV
- Filtrage des produits français
- Génération de graphiques sunburst interactifs pour visualiser la répartition des données

### Structure des données

Le script traite plusieurs sources de données :

- **Données produits** : fichier CSV `eggs_from_parquet.csv` avec colonnes JSON
- **Prédictions OCR** : fichier JSONL contenant les extractions de texte et prédictions
- **Métadonnées** : fichier `cols_to_json.txt` listant les colonnes à parser en JSON

Fichiers de sortie :

- `processed_products.csv` : données complètes avec calculs d'élevage
- `processed_products_fr.csv` : sous-ensemble des produits français

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

### Calcul de quantité et mode d'élevage

Le script utilise le `PainReportCalculator` pour extraire :

- **Nombre d'œufs** : comptage automatique depuis les données produit
- **Calibre** : taille des œufs (small, medium, large, extra-large)
- **Type d'élevage** : mode d'élevage (cage, barn, free-range, organic)

Codes de retour :

- `egg_count = -1` : quantité non trouvée
- `egg_count = -2` : produit non géré par le calculateur
- `caliber = "no caliber"` : calibre non déterminé
- `breeding = "no breeding"` : type d'élevage non déterminé
- `caliber/breeding = "not managed"` : produit non géré par le calculateur

### Visualisations générées

Le script génère des graphiques sunburst présentant la part et le nombre de produits pour lesquel
le mode d'élevage et la quantité ont été trouvés par le calculateur

Options d'affichage :
- Avec ou sans inclusion du calibre dans la hiérarchie
- Dataset **France** ou **Monde**


### Utilisation

```bash
python process_product_data.py [--dataset {world,france}] [--include-caliber] [--no-plot] [--no-process]
```

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
python process_product_data.py --include-caliber

# Traitement uniquement, sans affichage
python process_product_data.py --no-plot

# Affichage uniquement, sans retraitement (charge les données déjà traitées)
python process_product_data.py --no-process --dataset world --include-caliber
```

### Dépendances spécifiques

- `plotly.express` pour les visualisations sunburst
- Module métier `app.business.open_food_facts.pain_report_calculator`
- Schémas de validation `app.schemas.open_food_facts.external.ProductData`


## 4. export_computed_data_to_excel.py

### Description

Ce script exporte les données produits traitées par le calcualteur (`processed_products(_fr).csv`) vers des fichiers Excel formatés pour vérifier les données.
Il ajoute automatiquement les données produit, les images, les colonnes d’analyse (OCR, prédictions, types d’élevage…), les hyperliens vers OpenFoodFacts.

### Fonctionnalités principales

- Chargement du fichier CSV des oeufs Openfoodfacts après ajout des informations générées par le calculateur + l'OCR
- Génération de fichiers Excel :
  - **Test** : échantillon aléatoire de `n` produits (`test_products.xlsx`)
  - **Tous les produits** : l’ensemble du CSV (`all_products.xlsx`)
  - **Produits avec informations manquantes** : produits sans mode d'élevage ni quantité détectés (`missing_data_products.xlsx`)
- Hyperliens vers les pages produit OpenFoodFacts
- Insertion d’images via formules Excel (ouvrir sous Google sheets pour les afficher automatiquement)

Adapter le script pour une liste donnée de codes produits

### Utilisation

```bash
# Mode test (échantillon aléatoire)
python backend/app/scripts/export_computed_data_to_excel.py --test

# Tous les produits
python backend/app/scripts/export_computed_data_to_excel.py --all-products

# Mode production (catégories filtrées)
python backend/app/scripts/export_computed_data_to_excel.py --missing-data

# Pour ne traiter que les produits français
python backend/app/scripts/export_computed_data_to_excel.py --all-products --fr
```

Si aucun argument n’est fourni, le script propose un mode interactif.

### Fichiers d’entrée et de sortie

- Entrée : `backend/app/scripts/data/processed_products(_fr).csv`
- Sorties :
  - `test_products(_fr).xlsx` (test)
  - `all_productss(_fr).xlsx` (tous produits)
  - `missing_data_productss(_fr).xlsx` (production avec plusieurs feuilles)

### Dépendances spécifiques

- `pandas`, `numpy`
- `openpyxl` pour l’écriture et le formatage Excel
- `tqdm` pour les barres de progression

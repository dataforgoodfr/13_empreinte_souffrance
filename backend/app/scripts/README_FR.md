# Script de mise à jour de données produit OpenFoodFacts : update_off_product_data.py

Automatise les mises à jour de données produit sur [OpenFoodFacts](https://world.openfoodfacts.org/) via l’API d’écriture.

## Vue d’ensemble

Le script permet :

- L’**ajout de tags de catégorie** (élevage et calibre)
- La **mise à jour du champ quantité** (remplacement)
- Le traitement par lot depuis des fichiers CSV
- Le test sur un seul produit
- La **vérification optionnelle** de l'existence des codes-barres

## Installation

Installez les dépendances avec :

```bash
uv pip install --group dev
```

## Lancer le script

```bash
python update_product_data.py [options]
```

### Mise à jour par lot

```bash
python update_product_data.py --breeding --file breeding.csv
python update_product_data.py --caliber --file caliber.csv
python update_product_data.py --quantity --file quantity.csv
```

### Test sur un seul produit

```bash
python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:organic-eggs"
python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
```

## Format CSV

- Les fichiers doivent être placés dans le dossier `./data/`
- Colonnes obligatoires : `barcode` et `tag`
- Séparateurs acceptés : `,` ou `;`

Exemple :

```csv
barcode,tag
0061719011930,en:free-range-chicken-eggs
```

## Comportement des opérations

- `--breeding` et `--caliber` : les tags sont **ajoutés** en tant que catégories.
- `--quantity` : la valeur est **remplacée**.

### Tags valides

#### Élevage :

- `en:eggs`
- `en:chicken-eggs`
- `en:cage-chicken-eggs`
- `en:barn-chicken-eggs`
- `en:free-range-chicken-eggs`
- `en:organic-eggs`

#### Calibre :

- `en:small-eggs`
- `en:medium-eggs`
- `en:large-eggs`
- `en:extra-large-eggs`

#### Quantité :

- Format : `"nombre pcs"` (ex. `12 pcs`)

## API utilisée

- **GET** (vérification de code-barres) :
  `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`

- **POST** (mise à jour) :
  `https://world.openfoodfacts.org/cgi/product_jqm2.pl`

## Vérification des codes-barres

- Activée par défaut
- Vérification API pour chaque code-barres
- Limite : ~100 requêtes/minute (0.6s entre appels)
- Pour désactiver : `--no-verify-barcodes`

> ⚠️ Si la vérification est désactivée, un produit sera **créé** si le code-barres n’existe pas.

## Authentification requise

Le script nécessite des **identifiants OpenFoodFacts**.

Méthodes :

- Arguments CLI : `--username`, `--password`
- Saisie interactive si non fournis

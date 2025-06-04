
## 📈 Data analysis


### Description:
Open Food Facts is a food products database "made by everyone, for everyone".
This organisation uses an OCR (Optical Caracter Recognition) system to extract from a photograph the text of a package's list of ingredients.
The aim of this project was to automatically associate to each ingredient list (retrieved by OCR) a product category.


### Data Source:
Open Food Facts CSV of 1.634 734 products.
Open Food Facts json of 795 609 list of ingredients extracted from photos via OCR (Google Cloud Vision API).

### Type of analysis:
- Data Analysis to identify 38 categories of products and their occurrences.
- Search for the best Machine Learning model to classify products automatically
- Test for Deep Learning scores

This project focuses on French products. The model had been trained on French texts from OCR.

## ⚒ Startup the project

### The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

### Unittest test:
```bash
make clean install test
```

Check for OpenFoodFacts in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/OpenFoodFacts`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "OpenFoodFacts"
git remote add origin git@github.com:{group}/OpenFoodFacts.git
git push -u origin master
git push -u origin --tags
```

### Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
OpenFoodFacts-run
```

## 👩🏻‍💻 Install

Go to `https://github.com/ramsyy0/OpenFoodFacts` to see the project, manage issues,
setup you ssh public key, ...

### Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

### Clone the project and install it:

```bash
git clone git@github.com:ramsyy0/OpenFoodFacts.git
cd OpenFoodFacts
pip install -r requirements.txt
make clean install test                # install and test
```
### Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
OpenFoodFacts-run
````

## 🔍 Analyse the dataset

Open food facts uses an OCR system to extract text from photos of products taken by their contributors (OCR).
The organisation provided us with a dataset of 795,609 OCRs of ingredients in French.
We matched these OCRs to the corresponding products in their database (thanks to the codebar) to to find their categories (our y for machine learning).
We choosed to work on the "PNNS 2" column which contains 38 distinct categories of products. PNNS stands for "Programme national nutrition santé", categories have been established by the French Ministry of Health.
The names of the categories were also cleaned to eliminate duplicates due to different spellings or the use of capital letters.


## 🚿 Clean the data

We have applied the following preprocessing:
- remove punctuation
- remove non alphabetical characters (numbers, special characters)
- remove accentuated characters
- remove extra spaces
- basic spellcheck with Levenshtein distance of 1 (optional)


## 🏋🏻 Train the model

Several models have been tried to predict as accurately as possible the category of a products from an OCR of ingredients.
The most efficient is a Ridge Classifier, associated with a TF_IDF, with the n_grams 2 and the French NLTK stop_words as parameters.

Various preprocessing treatments on the text have been tested, for example:
- Stopwords and French Lemmatizer from Spacy
- Spellcheck to correct the spelling of the OCR

However, the above-mentioned Pipeline obtains the best results (84% accuracy, with a good balance over categories) on text that is simply cleaned up (accents, special characters, spaces, numbers, etc. as detailed in the clean data section)
You can see three of these training tests and their results in the notebooks.

We also found that when the model is wrong, it's not so wrong. Is classifying a soup as a one dish meal really a mistake? Some categories are very broad, others more precise and narrow, and this can lead to ambiguity, as some products can belong to several categories.
This is why we have configured the result of the model so that in case of hesitation (below a threshold of certainty) the model returns the two categories between which it hesitates to allow the human to decide. This can be seen in predictor.py file of the package.

## 📷 OCR test

To test our categorizer with new data we have implemented an OCR system.
Please, find the setup in the notebooks folder (OCR_setup.ipynb).

Two OCR system were tested: tesseract and easyocr.

### To understand how to custom parameters of tesseract see:
https://pypi.org/project/pytesseract/
https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc#config-files-and-augmenting-with-user-data

### Easy OCR doesn't need custom config:
https://pypi.org/project/easyocr/


### If you wish to use those OCR in production:
- easyocr is very easy to use as its name suggests, but it's also very heavy and may be to big for plateforms like Heroku (It may exceed
  the slug size).

- To use tesseract in production you will have to change the path.
  For example, our path was pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' for a local usage and pytesseract.pytesseract.tesseract_cmd = ‘/app/.apt/usr/bin/tesseract’ in production
  To know more see: https://towardsdatascience.com/deploy-python-tesseract-ocr-on-heroku-bbcc39391a8d

- We ended up using tesseract in a docker image


for new Docker files:

to build

docker build -t lewagon-ocr-model .

docker run -it --rm lewagon-ocr-model bash



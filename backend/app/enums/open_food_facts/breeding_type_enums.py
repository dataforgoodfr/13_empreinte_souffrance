# Breeding types and labels found in OpenFoodFacts products that imply that hens are free-range raised
FREE_RANGE_BREEDINGS = {"organic", "label-rouge", "biodynamic", "free-range", "pastured", "usda", "certified-humane"}

# All breeding types and labels found in OpenFoodFacts products
BREEDINGS = FREE_RANGE_BREEDINGS.union({"cage", "barn", "cage-free", "rspca", "kat"})

# Countries where conventional cages are prohibited for laying hens
COUNTRIES_WHERE_CAGES_ARE_FURNISHED = {
    "en:switzerland",  # conventional cages banned since 1992, phasing out of furnished cages
    "en:luxembourg",  # no more conventional cages since 2007, furnished cages to be phased out by 2025
    "en:sweden",  # cage systems banned
    "en:united-kingdom",  # conventional cages banned since 2012, transition to non-cage systems
    "en:france",  # EU regulations, ban on new conventional cage installations (2022)
    "en:germany",  # full exit from conventional cages by 2025, transition to furnished or cage-free systems
    "en:austria",  # total cage ban by 2025
    "en:netherlands",  # EU regulations
    "en:new-zealand",  # total cage ban in 2023
    "en:belgium",  # EU regulations
    "en:denmark",  # EU regulations
    "en:finland",  # EU regulations
    "en:ireland",  # EU regulations
    "en:italy",  # EU regulations
    "en:portugal",  # EU regulations
    "en:spain",  # EU regulations
    "en:poland",  # EU regulations
    "en:czech-republic",  # EU regulations
    "en:slovenia",  # EU regulations
    "en:croatia",  # EU regulations
    "en:bulgaria",  # EU regulations
    "en:hungary",  # EU regulations
    "en:latvia",  # EU regulations
    "en:lithuania",  # EU regulations
    "en:romania",  # EU regulations
    "en:estonia",  # EU regulations
    "en:greece",  # EU regulations
    "en:reunion",  # same as France
    "en:guadeloupe",  # same as France
    "en:martinique",  # same as France
    "en:mayotte",  # same as France
    "en:french-guiana",  # same as France
    "en:new-caledonia",  # same as France
}


BREEDING_PATTERNS_ALL_LANGUAGES: dict[str, set] = {}
"""
A dictionary storing breeding-related keywords in multiple languages for different animal breeding types.
Main languages that can be used on OpenFoodFacts are given
"""

for breeding in BREEDINGS:
    BREEDING_PATTERNS_ALL_LANGUAGES[breeding] = {breeding}
# Initializes the dictionnary with the basic name of each breeding

BREEDING_PATTERNS_ALL_LANGUAGES.update(
    {
        "cage": {
            "cage",  # Anglais, Français
            "caged",  # Anglais
            "батарейна клетка",  # Bulgare
            "klecovy chov",  # Tchèque
            "burhons",  # Suédois
            "hakkikanala",  # Finnois
            "kavezni uzgoj",  # Croate
            "chow klatkowy",  # Polonais
            "in custi",  # Roumain
            "laikymas narvuose",  # Lituanien
            "baterijska reja",  # Slovène
            "trobbija fil gageg",  # Maltais
            "i gcas",  # Irlandais
            "sprostu turesana",  # Letton
            "en jaula",  # Espagnol
            "en jaulas",  # Espagnol
            "puurikana",  # Finnois
            "buræg",  # Danois
            "kafig",  # Allemand
            "kafighaltung",  # Allemand
            "klietkovy chov",  # Slovaque
            "em gaiola",  # Portugais
            "κλωβοστοιχια",  # Grec
            "kooi",  # Néerlandais
            "gabbia",  # Italien
            "gabbi",  # Italien
            "ketreces tartas",  # Hongrois
        },
        "barn": {
            "sprotos",  # Letton
            "podnog",  # Croate
            "podestylkoveho",  # Tchèque
            "barn",  # Anglais
            "gridas turesana",  # Letton
            "frigaende inomhus",  # Suédois
            "podstielkovy chov",  # Slovaque
            "laikymas ant kraiko",  # Lituanien
            "suelo",  # Espagnol
            "suel",  # Espagnol
            "подово отглеждане",  # Bulgare
            "podni uzgoj",  # Croate
            "no solo",  # Espagnol
            "chow sciołkowy",  # Polonais
            "lattiakanala",  # Finnois
            "sol",  # Français
            "alternativ tartas",  # Hongrois
            "δαπεδο",  # Grec
            "talna reja",  # Slovène
            "podestylkovy chov",  # Tchèque
            "skrabeæg",  # Danois
            "scharrel",  # Néerlandais
            "trobbija fl art",  # Maltais
            "orrekanalad",  # Estonien
            "ar an urlar",  # Irlandais
            "terra",  # Portugais / Italien
            "bodenhaltung",  # Allemand
            "boden",  # Allemand
            "free run",  # Canada (Anglais)
        },
        "free-range": {
            "freilandeier",  # Allemand
            "freiland",  # Allemand
            "plein air",  # Français
            "ppa",  # Français (abréviation plein air)
            "camperas",  # Espagnol
            "campera",  # Espagnol
            "aire? libre",  # Français / Espagnol
            "volneho",  # Tchèque
            "laikymas laisveje",  # Lituanien
            "slobodni uzgoj",  # Croate
            "trobbija ħielsa",  # Maltais
            "свободно отглеждане",  # Bulgare
            "aer liber",  # Roumain
            "free range",  # Anglais
            "briva turesana",  # Letton
            "al aire libre",  # Espagnol
            "vabapidamine",  # Estonien
            "prosta reja",  # Slovène
            "ελευθερας βοσκης",  # Grec
            "szabadtartas",  # Hongrois
            "frigaende utomhus",  # Suédois
            "chow wolnowybiegowy",  # Polonais
            "frilandsæg",  # Danois
            "freilandhaltung",  # Allemand
            "ulkokanala",  # Finnois
            "all aperto",  # Italien
            "ar livre",  # Portugais
            "vrije uitloop",  # Néerlandais
            "saorshreabhadh",  # Irlandais
            "volny vybeh",  # Slovaque
        },
        "organic": {
            "ออร์แกนิค",  # Thaï
            "ecologica",  # Espagnol / Italien
            "bioeier",  # Allemand
            "bios?",  # Français
            "biologic",  # Anglais
            "biologico"  # Italien
            "biologique",  # Français
            "biologiques"  # Français
            "ekologiku",  # Maltais
            "luomu",  # Finnois
            "ecologico",  # Espagnol / Italien
            "ekoloski",  # Croate
            "organic",  # Anglais
            "ekologisk",
            "ekologiska"  # Suédois
            "ekologiskais",  # Letton
            "ecologic",  # Roumain
            "ekologichen",  # Bulgare
            "okologiai",  # Hongrois
            "viologiko",  # Grec
            "ekologiczny",  # Polonais
            "organach",  # Irlandais
            "biologi",  # Danois / Norvégien
            "ekologiskas",  # Lituanien
            "oekologisk",  # Danois
            "oekoloogiline",  # Estonien
            "ekologicky",  # Tchèque
            "okologische",
            "okologischen",
            "okologisches",  # Allemand
            "biologische",
            "biologischen",
            "biologisches",  # Allemand
        },
        "cage-free": {
            "libre de jaula",  # Espagnol
            "cage free",  # Anglais
            "vapaan",  # Finnois
            "libertad",  # Espagnol
            "libre",  # Espagnol / Français
        },
        "label-rouge": {
            "label rouge",  # Français
        },
        "certified-humane": {
            "certified humane",  # Anglais
        },
        "pastured": {
            "pasture",  # Anglais
            "pastured",  # Anglais
            "pastoreo",  # Espagnol
        },
        "biodynamic": {
            "biodynamic",  # Anglais
            "biodynamique",  # Français
        },
    }
)


EXCLUDED_PATTERNS: dict[str, set] = {}
# A dictionary that holds sets of regular expressions used
# to exclude specific patterns for each breeding_type

for breeding in BREEDINGS:
    EXCLUDED_PATTERNS[breeding] = set()
# Initializes each breeding with an empty set

EXCLUDED_PATTERNS.update(
    {
        "cage": {
            r"\b(cage free)\b",  # English
            r"\b(hors|pas|non|sans)\b.*\b(cage)\b",  # French
        },
        "free-range": {
            r"\b(no[tn]?|could|can)\b.*\b(free range)\b",  # English
            r"\b(sans|pas|non?|peuvent)\b.*\b(plein air)\b",  # French
        },
        "organic": {
            r"\b(no[tn]?)\b.*\b(organic)\b",  # English
            r"\b(sans|pas|no[tn]?)\b.*\b(bios?)\b",  # English/French
            r"\b(sans|pas|non?)\b.*\b(biologiques?)\b",  # French
        },
    }
)


def get_free_range_regex() -> str:
    """
    Constructs a regex pattern that matches 'free range' breeding types, based on a list of included and excluded
    breeding patterns for each specific 'free range' breeding type.

    Returns:
        str: A regex pattern that matches any of the 'free range' breeding types, ensuring that excluded patterns
        are not matched.
    """
    regex_by_breeding = []

    # Loop through each free-range breeding type
    for breeding in FREE_RANGE_BREEDINGS:
        # Get the set of included and excluded patterns for the current breeding type
        included = BREEDING_PATTERNS_ALL_LANGUAGES.get(breeding, set())
        excluded = EXCLUDED_PATTERNS.get(breeding, set())
        included_regex = "|".join(included)

        if not excluded:
            regex = rf".*\b({included_regex})\b"
        else:
            excluded_regex = "|".join(excluded)
            regex = rf"^(?!.*\b({excluded_regex})\b).*?\b({included_regex})\b"

        regex_by_breeding.append(regex)

    # Combine all individual regex patterns with an OR operator to match any of the free-range breeding types
    return r"^(" + r")|(".join(regex_by_breeding) + r")"


def get_barn_regex() -> str:
    """
    Constructs a regex pattern that matches 'barn' breeding types.
    Here no need for exclusions
    Returns:
        str: A regex pattern that matches any of the 'barn' breeding types.
    """
    return r"^.*\b(" + r"|".join(BREEDING_PATTERNS_ALL_LANGUAGES["barn"]) + r")\b"


def get_cage_regex() -> str:
    """
    Constructs a regex pattern that matches 'cage' breeding types, while excluding certain patterns
    like "cage free" or "not [...] cage"
    Returns:
        str: A regex pattern that matches 'cage' breeding types, ensuring excluded patterns are not matched.
    """
    # Join the list of excluded patterns for 'cage' breeding into a single regex pattern
    excluded_regex = "|".join(EXCLUDED_PATTERNS["cage"])

    # Join the list of included patterns for 'cage' breeding into a single regex pattern
    included_regex = "|".join(BREEDING_PATTERNS_ALL_LANGUAGES["cage"])

    # Create a regex pattern that uses a negative lookahead to exclude unwanted patterns
    regex = rf"^(?!.*\b({excluded_regex})\b).*?\b({included_regex})\b"

    return regex

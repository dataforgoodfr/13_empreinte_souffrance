export default {
  suffering_footprint: 'Empreinte souffrance',
  GoFurther: {
    title: 'Aller plus loin',
    downloadMediaKit: 'Télécharger le kit presse',
    share: 'Partager la page',
    methodology: 'Découvrir la méthodologie',
    aboutThisWebsite: 'À propos de ce site',
  },
  Home: {
    badge: "Adopter l'élevage en plein air pour chaque poulet en Europe !",
    animal_welfare: 'Bien-être animal',
    science: 'La science',
    explained: 'expliquée',
    paragraph:
      'Découvrez tout ce que vous devez savoir sur ce qu’un poulet vit en élevage et faites des choix éclairés.',
    link: 'Comprendre la méthode',
    how_much: 'Combien',
    does_this_hen_suffer_to_produce_eggs: 'souffre cette poule pour produire des oeufs ?',
    returnHome: "Retournez à l'accueil",
  },
  Results: {
    title: 'Les Résultats ?',
    agony: {
      title: "2 heures d'agonie",
      content:
        "...et 13 heures de souffrance intense : c'est ce que subit en moyenne chaque poule qui meurt de péritonite de l'oeuf avec septicémie, soit 1.5% des poules",
      image_description: "Poule se tenant sur un perchoir au dessus du cadavre d'une autre poule",
    },
    discomfort: {
      title: "3,5X plus d'inconfort",
      content:
        "Une poule élevée en cage connaîtra en moyenne 3,5 fois plus d'inconfort et deux fois plus de douleur au cours de sa vie qu'une poule élevée au sol",
      image_description: "Poule passant la tête à travers les barreaux d'une cage pour pouvoir manger",
    },
    suffering_reduction: {
      title: '93% de réduction des souffrances',
      content:
        "Le passage en élevage hors cage permet de diminuer de 93% les souffrances dues à l'impossibilité pour les poules d'adopter des comportements naturels",
      image_description: "Poule vu du dessous, à travers les barreaux d'une cage",
    },
    cage_figure: {
      title: '12 millions',
      content: 'Encore 12 millions de poules sont élevées en cage en France, soit 1 poule sur 4',
      image_description: 'Poules entassées dans des cages superposées les unes sur les autres',
    },
  },

  PainEquationSection: {
    title: "L'ÉQUATION DE LA DOULEUR",
    painStagesLabel: "Étapes de la douleur",
    formula: {
      duration: "DURÉE",
      intensity: "X INTENSITÉ",
      burden: "= FARDEAU DE DOULEUR"
    },
    description:
      "Comment ça marche ? Pour chaque source de douleur (fracture, infection, etc.), les chercheurs estiment combien de temps les poules passent dans un état d’inconfort, de douleur, de souffrance et d’agonie.",
    stages: {
      discomfort: {
        title: "Inconfort",
        text: "Inconfort léger, sans impact sur le comportement. Comparable à une démangeaison ou des chaussures qui frottent légèrement."
      },
      pain: {
        title: "Douleur",
        text: "Douleur persistante, altérant les comportements sans les empêcher. Semblable à un mal de tête ou un mal de dos chronique."
      },
      suffering: {
        title: "Souffrance",
        text: "Douleur constante, prioritaire sur tout. Réduit l’activité, le bien-être, l’attention. Semblable à une migraine ou une fracture."
      },
      agony: {
        title: "Agonie",
        text: "Douleur extrême, insupportable même brièvement. Provoque cris, tremblements. Comparable à une souffrance que l’on ne peut endurer."
      }
    },
    cta: "DÉCOUVRIR LA MÉTHODOLOGIE EN DÉTAIL"
  },

  SufferingCausesSection: {
    title: "De quoi souffrent les poules en cage ?",
    othersSources: "+ 24 autres sources de douleur",
    box1: {
      title: "Blessures dues au picage",
      text: "Stressées, les poules s’arrachent les plumes entre elles, causant blessures, infections... et parfois la mort par cannibalisme."
    },
    box2: {
      title: "Fracture du bréchet",
      text: "L’os de la poitrine se fracture souvent à cause de l’ostéoporose liée à la ponte intensive : c’est leur plus grande source de douleur."
    },
    box3: {
      title: "Restriction de mouvement",
      text: "En cage, les poules ne peuvent ni étendre leurs ailes, ni se retourner : un inconfort permanent, loin de tout comportement naturel."
    },
    box4: {
      title: "Peur et stress",
      text: "Avant l’abattoir, les poules sont capturées, entassées sans eau ni nourriture, et soumises à une peur extrême."
    },
    box5: {
      title: "Privation de comportements naturels",
      text: "Privées de nidification et d’exploration, les poules vivent une frustration intense, incapables de répondre à leurs besoins naturels."
    },
    box6: {
      title: "Péritonite de l’œuf",
      text: "Cette inflammation, due à des débris d’œuf dans l’abdomen, est la maladie la plus fréquente et mortelle chez les poules pondeuses."
    }
  },

  welfare_footprint_institute: 'Welfare Footprint Institute',
  KnowledgePanel: {
    title: 'Knowledge Panel',
    selectBarcode: 'Sélectionner un code-barres',
    otherBarcode: 'Autre code-barres...',
    enterBarcode: 'Entrez un code-barres',
    numericBarcodeError: 'Veuillez saisir un code-barres numérique',
    search: 'Rechercher',
    loading: 'Chargement des données...',
    productNotFound: 'Ce produit ne contient pas de produits animaux pris en charge',
  },
  footer: {
    legal_terms: 'Mentions légales',
    privacy_policy: 'Politique de confidentialité',
    contact_us: 'Contactez-nous',
    all_rights_reserved: 'Tous droits réservés',
    graphics: 'Graphisme :',
    rights: ' © 2024 Empreinte Souffrance et Data for Good',
  },
  science: {},
} as const;

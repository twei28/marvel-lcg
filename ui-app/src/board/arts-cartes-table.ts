// GENERE par tools/generer_arts_cartes.py depuis data/arts_alternatifs.json : ne pas modifier a la main.

/** Officielle -> codes d'art alternatif (image `<id>_<code>`). */
export const ARTS_CARTES: Record<string, string[]> = {
  "01057": [
    "tmnt"
  ],
  "01060": [
    "tmnt"
  ],
  "01065": [
    "tmnt"
  ],
  "01071": [
    "tmnt"
  ],
  "01074": [
    "tmnt"
  ],
  "01081": [
    "tmnt"
  ],
  "04047": [
    "tmnt"
  ],
  "04049": [
    "tmnt"
  ],
  "05023": [
    "tmnt"
  ],
  "05033": [
    "tmnt"
  ],
  "06031": [
    "tmnt"
  ],
  "09020": [
    "tmnt"
  ],
  "10014": [
    "tmnt"
  ],
  "10018": [
    "tmnt"
  ],
  "15019": [
    "tmnt"
  ],
  "16043": [
    "tmnt"
  ],
  "18012": [
    "tmnt"
  ],
  "19030": [
    "tmnt"
  ],
  "20026": [
    "tmnt"
  ],
  "21043": [
    "tmnt"
  ],
  "21050": [
    "tmnt"
  ],
  "21055": [
    "tmnt"
  ],
  "21061": [
    "tmnt"
  ],
  "28013": [
    "tmnt"
  ],
  "28017": [
    "tmnt"
  ],
  "30019": [
    "tmnt"
  ],
  "31023": [
    "tmnt"
  ],
  "31029": [
    "tmnt"
  ],
  "32014": [
    "tmnt"
  ],
  "35018": [
    "tmnt"
  ],
  "40060": [
    "tmnt"
  ],
  "41017": [
    "tmnt"
  ],
  "43019": [
    "tmnt"
  ],
  "45016": [
    "tmnt"
  ],
  "45043": [
    "tmnt"
  ],
  "45051": [
    "tmnt"
  ],
  "46014": [
    "tmnt"
  ],
  "47013": [
    "tmnt"
  ],
  "47015": [
    "tmnt"
  ],
  "48014": [
    "tmnt"
  ],
  "48016": [
    "tmnt"
  ],
  "49018": [
    "tmnt"
  ],
  "49022": [
    "tmnt"
  ],
  "50058": [
    "tmnt"
  ],
  "52019": [
    "tmnt"
  ],
  "54016": [
    "tmnt"
  ],
  "56013": [
    "tmnt"
  ],
  "56046": [
    "tmnt"
  ],
  "56047": [
    "tmnt"
  ],
  "56048": [
    "tmnt"
  ],
  "58016": [
    "tmnt"
  ],
  "58020": [
    "tmnt"
  ],
  "58021": [
    "tmnt"
  ],
  "58031": [
    "tmnt"
  ],
  "60028": [
    "tmnt"
  ],
  "60038": [
    "tmnt"
  ],
  "60048": [
    "tmnt"
  ],
  "60049": [
    "tmnt"
  ],
  "60050": [
    "tmnt"
  ],
  "60052": [
    "tmnt"
  ],
  "60053": [
    "tmnt"
  ],
  "60054": [
    "tmnt"
  ],
  "61034": [
    "tmnt"
  ],
  "61036": [
    "tmnt"
  ],
  "61037": [
    "tmnt"
  ],
  "62015": [
    "tmnt"
  ],
  "62019": [
    "tmnt"
  ]
}

/** Reimpression identique -> officielle (meme image, meme choix). */
export const ORIGINES_CARTES: Record<string, string> = {
  "03016": "01071",
  "04041": "01057",
  "04046": "01065",
  "14016": "01081",
  "15017": "01065",
  "18017": "01057",
  "21045": "01057",
  "21049": "01060",
  "21051": "01065",
  "21056": "01071",
  "21057": "01074",
  "21063": "01081",
  "22019": "01065",
  "23020": "01071",
  "25017": "01057",
  "34024": "05033",
  "36026": "05023",
  "38013": "09020",
  "40055": "30019",
  "43027": "05023",
  "45046": "18012",
  "48017": "32014",
  "50053": "06031",
  "56014": "46014",
  "56015": "19030",
  "59027": "31023",
  "60051": "32014"
}

export type SerieArt = {
  nom: string
  nom_en: string
  heros_cartes: string[]
  heros_ids: string[]
  sets_exclusifs: string[]
}

/** Series d'art : heros qui l'ont par defaut, sets exclusifs. */
export const SERIES_ARTS: Record<string, SerieArt> = {
  "tmnt": {
    "nom": "TMNT",
    "nom_en": "TMNT",
    "heros_cartes": [
      "tl001",
      "td001",
      "tm001",
      "tr001",
      "tv001",
      "tc001",
      "ta001",
      "tj001"
    ],
    "heros_ids": [
      "leonardo",
      "donatello",
      "michelangelo",
      "raphael",
      "venus",
      "casey_jones",
      "alopex",
      "jennika"
    ],
    "sets_exclusifs": [
      "TMNT Aggression",
      "TMNT Basic",
      "TMNT Justice",
      "TMNT Leadership",
      "TMNT Protection",
      "TMNT Dual-Aspect"
    ]
  }
}

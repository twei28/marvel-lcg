// GENERE par tools/generer_arts_cartes.py depuis data/arts_alternatifs.json : ne pas modifier a la main.

/** Officielle -> codes d'art alternatif (image `<id>_<code>`). */
export const ARTS_CARTES: Record<string, string[]> = {}

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

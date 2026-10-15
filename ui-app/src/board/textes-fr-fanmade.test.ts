// Les textes FR des cartes fan-made emploient le vocabulaire OFFICIEL des
// cartes francaises (releve le 7 septembre 2026 sur les cartes traduites de
// fr.marvelcdb.com : « Interruption forcee », « Action d'alter ego », « sous
// forme de heros », « Une fois dejouee », « 1 max par deck », « Percant »,
// « Renfort » pour Surge, « Deferlement » pour Overkill, « En Equipe (A et B) »).
// Constate par l'utilisateur : « Interruption obligatoire » et « identite
// civile » n'existent sur aucune carte francaise. Ce test interdit leur retour.
import { describe, expect, it } from 'vitest'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'

const INTERDITS: Array<[RegExp, string]> = [
  [/Obligatoire/i, 'forcée (Interruption forcée, Réponse forcée)'],
  [/identité civile/i, "alter ego (Action d'alter ego, sous forme d'alter ego)"],
  [/alter-ego/i, 'alter ego, sans trait d’union'],
  [/\ben forme (de héros|d'alter)/i, 'sous forme de héros / sous forme d’alter ego'],
  [/Quand (déjouée|vaincue?|elle est révélée|il est révélé)/, 'Une fois déjouée / vaincu / révélée'],
  [/Perforation/, 'Perçant'],
  [/\bSurge\b/, 'Renfort'],
  [/Team-Up \(/, 'En Équipe (A et B)'],
  [/Max(imum)? \d par/, '1 max par deck / par joueur'],
]

// Coffret Skrull Menace seulement (cartes `sk…`) : les autres packs fan-made ont
// le même écart (« devrait » dans 112 textes au 15/10/2026), à reprendre à part.
const INTERDITS_SKRULL_MENACE: Array<[RegExp, string]> = [
  // Relevé le 15/10/2026 sur les 4 393 textes officiels (textes-fr-complets.ts) :
  // « est censé » 209 fois contre « devrait » 3 ; « n'importe quelle quantité de
  // dégâts » et jamais « quels qu'ils soient » ; « stade achevé », pas « étape
  // complétée » ; « jeton » 804 fois contre « compteur » 8 (réservé au compteur
  // de points de vie) ; une carte qui perd son texte « perd le texte imprimé
  // dans sa boîte de texte », jamais « comme vierge ».
  [/\bdevr(ait|aient|iez)\b/, 'est censé(e) / sont censés / êtes censé'],
  [/quels qu'(ils|elles) soient/, "n'importe quelle quantité de"],
  [/\bcomplétée?\b/, 'achevé(e)'],
  [/comme vierge/, 'perd le texte imprimé dans sa boîte de texte'],
  // Guide de référence FR (mc01_guide_de_reference_fr.pdf) : « pion Accélération »,
  // « champ de boost » (zone imprimée de la carte), et « Une fois déjouée » pour
  // une manigance (« Une fois vaincu » est réservé aux personnages).
  [/jeton d'accélération/i, 'pion Accélération'],
  [/zone de boost/, 'champ de boost'],
]

describe('vocabulaire officiel des textes FR fan-made', () => {
  for (const [motif, attendu] of INTERDITS) {
    it(`n'emploie jamais ${motif} (attendu : ${attendu})`, () => {
      const fautifs = Object.entries(TEXTES_FR_FANMADE)
        .filter(([, texte]) => texte !== undefined && motif.test(texte))
        .map(([code]) => code)
      expect(fautifs).toEqual([])
    })
  }

  for (const [motif, attendu] of INTERDITS_SKRULL_MENACE) {
    it(`Skrull Menace : n'emploie jamais ${motif} (attendu : ${attendu})`, () => {
      const fautifs = Object.entries(TEXTES_FR_FANMADE)
        .filter(([code, texte]) => /^sk\d{3}/.test(code) && texte !== undefined && motif.test(texte))
        .map(([code]) => code)
      expect(fautifs).toEqual([])
    })
  }
})

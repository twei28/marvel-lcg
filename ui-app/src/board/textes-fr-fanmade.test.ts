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

describe('vocabulaire officiel des textes FR fan-made', () => {
  for (const [motif, attendu] of INTERDITS) {
    it(`n'emploie jamais ${motif} (attendu : ${attendu})`, () => {
      const fautifs = Object.entries(TEXTES_FR_FANMADE)
        .filter(([, texte]) => texte !== undefined && motif.test(texte))
        .map(([code]) => code)
      expect(fautifs).toEqual([])
    })
  }
})

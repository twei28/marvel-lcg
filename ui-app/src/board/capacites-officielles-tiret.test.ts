import { describe, expect, it } from 'vitest'
import { nomDeCapacite } from './DemandeCentrale'
import { extraireCapacite } from './texte-capacite'
import { TEXTES_FR_COMPLETS } from './textes-fr-complets'

// Francais officiel de certains heros : « Nom - Type » avec un TIRET SIMPLE. Le bouton gardait le nom anglais du moteur.
const opt = (name: string) => ({ name, bind_id: 1, all_legal_targets: [], is_text_choice: false }) as never
const CAS: [string, string, string, string][] = [
  ['20001a', 'Symbiotic Bond', 'Hero Resource', 'Lien Symbiotique'],
  ['22001a', 'Combat Protocols', 'Forced Response', 'Protocoles de Combat'],
  ['26001a', 'Density Manipulation', 'Hero Action', 'Manipulation de la Densité'],
  ['49001a', 'Magnetic Pull', 'Hero Action', 'Attraction Magnétique'],
  ['53001a', 'Eagle-Eyed', 'Hero Response', 'Vue Perçante'],
  ['56001a', 'On the Hunt', 'Hero Response', 'En Chasse'],
  ['23001a', 'Locked and Loaded', 'Forced Response', 'Paré à Tirer'],
  ['54001a', 'Lethal Protector', 'Hero Response', 'Protecteur Mortel'],
]
describe('noms de capacité des héros officiels (tiret simple)', () => {
  it.each(CAS)('%s : %s -> nom français', (id, nom, type, attendu) => {
    const texte = extraireCapacite(TEXTES_FR_COMPLETS[id], nom, type)
    expect(nomDeCapacite(opt(nom), texte).toLowerCase()).toBe(attendu.toLowerCase())
  })
})

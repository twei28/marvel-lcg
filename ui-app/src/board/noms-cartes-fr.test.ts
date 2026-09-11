// Le nom francais des cartes. Defaut signale par l'utilisateur le 11/09/2026 :
// la carte affichait « L'Effraction ! » sur son illustration francaise et
// « THE BREAK-IN! » en titre a cote. Le desaccord se voit au premier coup
// d'oeil.
//
// La regle : le titre suit la LANGUE DES SCANS, pas celle de l'interface, et
// c'est le meme reglage qui commande les deux (scansFrActifs). Un joueur qui
// coupe les scans francais a la carte anglaise sous les yeux : lui ecrire un
// titre francais recreerait le meme desaccord, dans l'autre sens.
//
// Ce qui n'a PAS de nom francais retombe sur `carte.name` sans bruit : les
// cartes fan-made (marvelcdb ne les connait pas) et celles dont la VF est
// identique a la VO (« Rhino », « Baron Zemo »).

import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { CLE_SCANS_FR } from './scans-fr'
import { nomAffiche } from './noms-cartes-fr'

/** Le strict minimum que lit nomAffiche(), pour ne pas fabriquer un WorldCard
    entier a chaque cas. */
const carte = (card_id: string, name: string) => ({ card_id, name })

beforeEach(() => window.localStorage.removeItem(CLE_SCANS_FR))
afterEach(() => window.localStorage.removeItem(CLE_SCANS_FR))

describe('nomAffiche', () => {
  it('rend le nom francais officiel quand les scans francais sont actifs', () => {
    // 01097a : la manigance principale de la boite Rhino, celle de la capture.
    expect(nomAffiche(carte('01097a', 'The Break-In!'))).toBe("L'Effraction !")
  })

  it('rend le nom anglais quand le joueur a coupe les scans francais', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    expect(nomAffiche(carte('01097a', 'The Break-In!'))).toBe('The Break-In!')
  })

  it('retombe sur le nom du moteur pour une carte fan-made, inconnue de marvelcdb', () => {
    // Les codes fan-made ne sont pas numeriques (« wd002a » = Web of Deceit) :
    // marvelcdb ne les connait pas, leur scan est anglais, leur nom le reste.
    expect(nomAffiche(carte('wd002a', 'Shock Party'))).toBe('Shock Party')
  })

  it('retombe sur le nom du moteur quand la VF est identique a la VO', () => {
    // « Rhino » ne figure pas dans NOMS_FR, justement parce qu'il n'y a rien
    // a traduire : le dictionnaire ne garde que les noms qui DIFFERENT.
    expect(nomAffiche(carte('01096', 'Rhino'))).toBe('Rhino')
  })

  it('ne rend jamais une chaine vide quand le moteur n\'a pas de nom', () => {
    expect(nomAffiche(carte('99999', ''))).toBe('')
  })

  it('accepte une carte sans card_id sans lever', () => {
    expect(nomAffiche({ name: 'Minion' })).toBe('Minion')
  })
})

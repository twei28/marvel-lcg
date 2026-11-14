import { describe, expect, it } from 'vitest'
import { groupeDeLaPile, pileAOuvrirSeule, pilesToutesALaFois } from './pile-auto'

// Rapport du 26/10/2026 (Safe House #30, Winter Soldier, partie sur telephone) : la porte « Chercher dans le paquet
// rencontre » est posee sous le deck, et sur telephone ce deck n'est PAS a l'ecran (il est dans le tiroir « Piles ») :
// le joueur ne voit aucune porte, ne choisit aucun sbire, et rien ne se passe. Sur telephone, la pile seule s'ouvre donc
// toute seule ; sur la table du PC, la regle du 17/10/2026 (« c'est le clic sur la pile qui ouvre la fenetre ») reste.
describe('pileAOuvrirSeule', () => {
  const unePile = new Map([[42, 'Chercher dans le paquet rencontre']])

  it('ouvre la pile seule sur telephone, quand une recherche attend son choix', () => {
    expect(pileAOuvrirSeule({ telephone: true, rechercheEnCours: true, piles: unePile, pileOuverte: undefined })).toBe(42)
  })

  it('laisse la porte de la pile sur la table du PC', () => {
    expect(pileAOuvrirSeule({ telephone: false, rechercheEnCours: true, piles: unePile, pileOuverte: undefined })).toBeUndefined()
  })

  it('ne choisit pas a la place du joueur quand il y a plusieurs piles', () => {
    const deux = new Map([[42, 'deck'], [43, 'defausse']])
    expect(pileAOuvrirSeule({ telephone: true, rechercheEnCours: true, piles: deux, pileOuverte: undefined })).toBeUndefined()
  })

  it('ne rouvre pas une pile deja ouverte ni hors recherche', () => {
    expect(pileAOuvrirSeule({ telephone: true, rechercheEnCours: true, piles: unePile, pileOuverte: 42 })).toBeUndefined()
    expect(pileAOuvrirSeule({ telephone: true, rechercheEnCours: false, piles: unePile, pileOuverte: undefined })).toBeUndefined()
  })
})

// Rapport du 26/10/2026 (Suit Up de Laura Kinney, telephone) : « cherchez dans votre deck ET pile de defausse un allie et une
// amelioration ». Des qu'un allie est en defausse, DEUX piles portent des cartes cherchees : la porte de chaque pile est cachee
// dans le tiroir « Piles », rien ne s'ouvre, l'action est payee pour rien. Sur telephone, on montre alors TOUTES les cartes
// d'un coup, rangees par pile.
describe('pilesToutesALaFois', () => {
  const deuxPiles = new Map([[42, 'Chercher dans le deck'], [43, 'Prendre dans la défausse']])

  it('sur telephone, ouvre toutes les piles quand plusieurs portent des cartes cherchees', () => {
    expect(pilesToutesALaFois({ telephone: true, rechercheEnCours: true, piles: deuxPiles, pileOuverte: undefined })).toBe(true)
  })

  it('ne le fait pas sur la table du PC (la porte de la pile est a l’ecran)', () => {
    expect(pilesToutesALaFois({ telephone: false, rechercheEnCours: true, piles: deuxPiles, pileOuverte: undefined })).toBe(false)
  })

  it('laisse la pile seule a pileAOuvrirSeule, et ne rouvre rien si une pile est deja ouverte ou hors recherche', () => {
    const une = new Map([[42, 'deck']])
    expect(pilesToutesALaFois({ telephone: true, rechercheEnCours: true, piles: une, pileOuverte: undefined })).toBe(false)
    expect(pilesToutesALaFois({ telephone: true, rechercheEnCours: true, piles: deuxPiles, pileOuverte: 42 })).toBe(false)
    expect(pilesToutesALaFois({ telephone: true, rechercheEnCours: false, piles: deuxPiles, pileOuverte: undefined })).toBe(false)
  })
})

describe('groupeDeLaPile', () => {
  it('nomme la pile en un mot, d’apres sa nature (jamais d’apres un libelle deja traduit)', () => {
    expect(groupeDeLaPile('deck')).toBe('Deck')
    expect(groupeDeLaPile('defausse')).toBe('Défausse')
    expect(groupeDeLaPile('rencontre')).toBe('Paquet rencontre')
    expect(groupeDeLaPile('defausse-rencontre')).toBe('Défausse rencontre')
    expect(groupeDeLaPile('autre')).toBe('Pile de cartes')
  })
})

// 26/10/2026, demande de l'utilisateur : quand une action cherche dans plusieurs piles (deck + defausse), cliquer sur UNE pile
// ouvre la MEME fenetre, qui contient toutes les piles concernees ; avec une seule pile, c'est la pile cliquee.
import { choixEnAttente, ouvertureDePile, pilesChoisissables } from './pile-auto'

describe('ouvertureDePile', () => {
  it('avec plusieurs piles, un clic sur une seule ouvre toutes les piles ensemble', () => {
    const deuxPiles = new Map([[42, 'Chercher dans le deck'], [43, 'Prendre dans la défausse']])
    expect(ouvertureDePile(deuxPiles, 42)).toEqual({ pile: undefined, toutes: true })
    expect(ouvertureDePile(deuxPiles, 43)).toEqual({ pile: undefined, toutes: true })
  })

  it('avec une seule pile, ouvre cette pile', () => {
    expect(ouvertureDePile(new Map([[42, 'deck']]), 42)).toEqual({ pile: 42, toutes: false })
  })
})

// Fermeture accidentelle (telephone) : la fenetre se reduit SANS annuler l'action. Le choix reste « en attente » tant que la
// recherche court et que la fenetre est fermee : l'onglet « Piles » clignote, un bandeau propose de rouvrir.
describe('choixEnAttente', () => {
  it('est en attente quand la recherche court et que la fenetre est reduite', () => {
    expect(choixEnAttente({ rechercheEnCours: true, reduit: true })).toBe(true)
  })

  it('ne l’est ni sans recherche, ni fenetre ouverte', () => {
    expect(choixEnAttente({ rechercheEnCours: false, reduit: true })).toBe(false)
    expect(choixEnAttente({ rechercheEnCours: true, reduit: false })).toBe(false)
  })
})

describe('pilesChoisissables', () => {
  it('compte, pour chaque pile, les cartes qu’on peut y choisir (les piles sans carte choisissable sont omises)', () => {
    const piles = [
      { cle: 'joueur-deck', ids: [1, 2, 3] },
      { cle: 'joueur-defausse', ids: [4, 5] },
      { cle: 'rencontre-encounter-deck', ids: [6] },
    ]
    expect(pilesChoisissables(piles, new Set([2, 3, 5]))).toEqual(
      new Map([['joueur-deck', 2], ['joueur-defausse', 1]])
    )
  })
})

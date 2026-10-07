// Ce qui s'est passe entre deux mondes de la relecture, dit au joueur :
// « Joueur 2 (Captain America) joue Bouclier, paye avec Poing de fer
// (Physique) », « Spider-Man attaque Rhino : 3 degats ». Module PUR.
//
// Une carte JOUEE quitte la main pour une zone de jeu (ou la zone de
// resolution, pour un evenement) ; une carte qui PAIE quitte la main pour la
// defausse, dans les rendus qui entourent le coup. L'attaque et le contre
// viennent du moteur lui-meme : `event_name` et `active_card_ids` ([0] la
// cible, [1] l'agissante), comme pour la charge du plateau (CoucheCharge.tsx).
import type { World } from '../world'
import { nomAffiche } from '../noms-cartes-fr'
import type { Relecture } from './fichier'

export type CarteVue = { id: number; nom: string }
export type Paiement = CarteVue & { ressources: string[] }
export type Degat = CarteVue & { montant: number }

export type Action = {
  index: number
  genre: 'joue' | 'attaque' | 'contre' | 'manigance'
  siege?: number
  acteur?: CarteVue
  carte?: CarteVue
  cible?: CarteVue
  paiement: Paiement[]
  degats: Degat[]
}

const EVENEMENTS: Record<string, Action['genre']> = {
  WhenUnitWouldTakeDamage: 'attaque',
  WhenDamageIsZero_Text: 'attaque',
  WhenSchemeWouldRemoveThreat: 'contre',
  WhenSchemeWouldPlaceThreat: 'manigance',
}

/** Fenetre (en rendus) ou une defausse depuis la main compte comme paiement du coup joue. */
const FENETRE_PAIEMENT = 4
/** Fenetre (en rendus) ou des degats se rattachent a l'action qui precede. */
const FENETRE_DEGATS = 4

type Place = { nom: string; zone: string; siege?: number; pv?: number }

const nomLisible = (nom: string | undefined) => (nom ?? '').replace(/^\W*/, '')

function places(monde: World): Map<number, Place> {
  const resultat = new Map<number, Place>()
  const noter = (cartes: unknown, zone: string, siege?: number) => {
    if (!Array.isArray(cartes)) return
    for (const carte of cartes as { id?: number; name?: string; card_id?: string; info?: Record<string, number> }[]) {
      if (typeof carte?.id !== 'number') continue
      const pv = carte.info?.health
      resultat.set(carte.id, { nom: nomLisible(nomAffiche(carte)), zone, siege, pv: typeof pv === 'number' ? pv : undefined })
    }
  }
  for (const [cle, valeur] of Object.entries(monde)) if (cle !== 'players') noter(valeur, cle)
  ;(monde.players ?? []).forEach((joueur, siege) => {
    for (const [cle, valeur] of Object.entries(joueur)) noter(valeur, cle, siege)
  })
  return resultat
}

const ZONES_HORS_JEU = new Set(['hand_cards', 'player_discard_pile', 'player_deck'])

export function ressourcesLisibles(texte: string | undefined): string[] {
  if (!texte) return []
  const bas = texte.toLowerCase()
  const mots: [RegExp, string][] = [
    [/physical/g, 'Physique'],
    [/mental/g, 'Mental'],
    [/energy/g, 'Énergie'],
    [/wild/g, 'Joker'],
    [/lightning/g, 'Éclair'],
  ]
  const parMots = mots.flatMap(([motif, nom]) => Array.from(bas.matchAll(motif), () => nom))
  if (parMots.length > 0) return parMots
  const lettres: Record<string, string> = { r: 'Physique', b: 'Mental', y: 'Énergie', g: 'Joker', l: 'Éclair' }
  return Array.from(bas.replace(/[^rbygl]/g, '')).map((l) => lettres[l])
}

export function actionsDe(relecture: Relecture): Action[] {
  const actions: Action[] = []
  const derniereParSiege = new Map<number, Action>()
  const enAttente: { index: number; siege: number; paiement: Paiement }[] = []
  let precedent = places(relecture.trames[0].monde)
  let derniere: Action | undefined

  relecture.trames.forEach(({ monde }, index) => {
    if (index === 0) return
    const ici = places(monde)
    const avant = relecture.trames[index - 1].monde
    let nouvelle: Action | undefined

    for (const [id, place] of precedent) {
      if (place.zone !== 'hand_cards' || place.siege === undefined) continue
      const apres = ici.get(id)
      if (!apres || apres.zone === 'hand_cards') continue
      const carte = { id, nom: apres.nom || place.nom }
      if (apres.zone === 'player_discard_pile') {
        const paiement = { ...carte, ressources: ressourcesLisibles(relecture.ressources[id]) }
        const action = derniereParSiege.get(place.siege)
        if (action && action.genre === 'joue' && index - action.index <= FENETRE_PAIEMENT) action.paiement.push(paiement)
        else enAttente.push({ index, siege: place.siege, paiement })
      } else if (!ZONES_HORS_JEU.has(apres.zone)) {
        const action: Action = { index, genre: 'joue', siege: place.siege, carte, paiement: [], degats: [] }
        for (let n = enAttente.length - 1; n >= 0; n -= 1) {
          const attente = enAttente[n]
          if (attente.siege === place.siege && index - attente.index <= FENETRE_PAIEMENT) {
            action.paiement.unshift(attente.paiement)
            enAttente.splice(n, 1)
          }
        }
        actions.push(action)
        derniereParSiege.set(place.siege, action)
        nouvelle = action
      }
    }

    const genre = EVENEMENTS[monde.event_name ?? '']
    const actifs = monde.active_card_ids ?? []
    const memeEvenement =
      avant.event_name === monde.event_name && (avant.active_card_ids ?? []).join() === actifs.join()
    if (genre && actifs.length >= 2 && !memeEvenement) {
      const cible = ici.get(actifs[0])
      const acteur = ici.get(actifs[1])
      const action: Action = {
        index,
        genre,
        siege: acteur?.siege,
        acteur: acteur ? { id: actifs[1], nom: acteur.nom } : undefined,
        cible: cible ? { id: actifs[0], nom: cible.nom } : undefined,
        paiement: [],
        degats: [],
      }
      actions.push(action)
      nouvelle = action
    }

    if (nouvelle) derniere = nouvelle
    for (const [id, place] of ici) {
      const pvAvant = precedent.get(id)?.pv
      if (place.pv === undefined || pvAvant === undefined || place.pv >= pvAvant) continue
      const degat = { id, nom: place.nom, montant: pvAvant - place.pv }
      if (derniere && index - derniere.index <= FENETRE_DEGATS) derniere.degats.push(degat)
    }
    precedent = ici
  })
  return actions
}

/** Les degats subis a chaque rendu, pour le chiffre qui s'envole au-dessus de la cible. */
export function degatsParRendu(relecture: Relecture): Map<number, Degat[]> {
  const resultat = new Map<number, Degat[]>()
  let precedent = places(relecture.trames[0].monde)
  relecture.trames.forEach(({ monde }, index) => {
    if (index === 0) return
    const ici = places(monde)
    const degats: Degat[] = []
    for (const [id, place] of ici) {
      const pvAvant = precedent.get(id)?.pv
      if (place.pv !== undefined && pvAvant !== undefined && place.pv < pvAvant) {
        degats.push({ id, nom: place.nom, montant: pvAvant - place.pv })
      }
    }
    if (degats.length > 0) resultat.set(index, degats)
    precedent = ici
  })
  return resultat
}

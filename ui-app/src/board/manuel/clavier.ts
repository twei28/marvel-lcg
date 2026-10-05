// clavier.ts — ce que veut dire une touche, quand on survole quelque chose.
//
// Calqué sur le plugin OCTGN de Marvel Champions (definition.xml et
// scripts/actions.py du dépôt twistedsistem/OCTGN-Marvel-Champions) : mêmes
// touches, mêmes effets, y compris la façon dont une même touche change de
// sens selon le TYPE de la carte survolée (flèches haut et bas : points de
// vie sur un héros ou un méchant, dégâts sur un sbire ou un allié, menace sur
// une manigance, marqueur ailleurs).
//
// `interpreterTouche` est une fonction PURE : elle ne touche ni au DOM ni au
// réseau, elle dit seulement quel geste la touche demande. Le branchement
// (survol du pointeur, envoi au moteur) vit dans CoucheTriche.tsx.
//
// ⚠ ON NE DEVINE PAS : une touche qui ne s'applique pas à cette carte ne fait
// rien. Le clic droit, lui, nomme chaque jeton.

export type Touche = { cle: string; majuscule: boolean; ctrl?: boolean; alt?: boolean }

export type StatutsPortes = { stunned: boolean; confused: boolean; tough: boolean }

export type CarteVisee = {
  genre: 'carte'
  id: number
  /** `card_type` du moteur : « Hero », « Minion », « MainScheme »... */
  type: string
  /** Redressée (false = inclinée). */
  prete: boolean
  faceVisible: boolean
  statuts: StatutsPortes
}

export type CibleClavier = CarteVisee | { genre: 'pile'; zone: string }

export type GesteClavier =
  | { geste: 'retourner'; id: number }
  | { geste: 'incliner'; id: number }
  | { geste: 'redresser'; id: number }
  | { geste: 'melanger'; zone: string }
  | { geste: 'piocher'; zone: string; nombre: number }
  | { geste: 'piocherPlusieurs'; zone: string }
  | { geste: 'jetons'; id: number; nature: 'degats' | 'menace' | 'pv'; nombre: number }
  | { geste: 'compteur'; id: number; nombre: number }
  | { geste: 'acceleration'; id: number; nombre: number }
  | { geste: 'defausser'; id: number }
  | { geste: 'statut'; id: number; statut: 'stun' | 'confuse' | 'tough'; pose: boolean }
  | { geste: 'victoire'; id: number }
  | { geste: 'amplification' }
  | { geste: 'vaincreStade' }
  | { geste: 'maniganceTerminee' }
  | { geste: 'toutRedresser' }
  | { geste: 'finPhaseHeros' }

// --- Les types de cartes, comme `isScheme`, `isAttackable`... d'OCTGN --------

const IDENTITES = new Set(['Hero', 'AlterEgo'])
const VILAINS = new Set(['EncounterVillain', 'Villain'])
const MANIGANCES = new Set(['MainScheme', 'SideScheme', 'EncounterSideScheme', 'PlayerSideScheme', 'Scheme'])
const ATTAQUABLES = new Set(['Hero', 'AlterEgo', 'EncounterVillain', 'Villain', 'Minion', 'Ally'])
/** Ce qui s'incline : héros, alliés, améliorations, soutiens (`exhaustable`). */
const INCLINABLES = new Set(['Hero', 'AlterEgo', 'Ally', 'Upgrade', 'Support'])
/** Ce qui ne porte aucun état : un événement, une traîtrise... */
const SANS_ETAT = new Set(['Event', 'Treachery', 'Obligation', 'Resource'])

export const estIdentite = (type: string) => IDENTITES.has(type)
export const estVilain = (type: string) => VILAINS.has(type)
export const estManigance = (type: string) => MANIGANCES.has(type)
export const estAttaquable = (type: string) => ATTAQUABLES.has(type)
export const estInclinable = (type: string) => INCLINABLES.has(type)
export const estSansEtat = (type: string) => SANS_ETAT.has(type)

/**
 * Ce que mesure naturellement une carte (`addMarker` d'OCTGN) : les points de
 * vie d'un héros ou d'un méchant, les dégâts d'un sbire ou d'un allié, la
 * menace d'une manigance, un marqueur générique partout ailleurs.
 */
export function natureDe(type: string): 'pv' | 'degats' | 'menace' | 'marqueur' {
  if (MANIGANCES.has(type)) return 'menace'
  if (IDENTITES.has(type) || VILAINS.has(type)) return 'pv'
  if (ATTAQUABLES.has(type)) return 'degats'
  return 'marqueur'
}

function basculer(carte: CarteVisee): GesteClavier {
  return carte.prete ? { geste: 'incliner', id: carte.id } : { geste: 'redresser', id: carte.id }
}

/** Le double-clic d'OCTGN (`defaultCardAction`). */
export function interpreterDoubleClic(carte: CarteVisee): GesteClavier | undefined {
  if (MANIGANCES.has(carte.type)) return undefined
  if (!carte.faceVisible) return { geste: 'retourner', id: carte.id }
  if (VILAINS.has(carte.type)) return { geste: 'amplification' }
  if (INCLINABLES.has(carte.type)) return basculer(carte)
  return undefined
}

export function interpreterTouche(touche: Touche, cible: CibleClavier): GesteClavier | undefined {
  const cle = touche.cle.toLowerCase()
  const ctrl = touche.ctrl === true
  const alt = touche.alt === true
  const maj = touche.majuscule

  // La table entière : pas besoin de survoler quoi que ce soit.
  if (alt && !ctrl && cle === 'enter') return { geste: 'amplification' }
  if (ctrl && !alt && !maj && cle === 'q') return { geste: 'toutRedresser' }
  if (!ctrl && !alt && cle === 'f12') return { geste: 'finPhaseHeros' }

  if (cible.genre === 'pile') {
    if (ctrl && !alt) {
      if (cle === 's' && !maj) return { geste: 'melanger', zone: cible.zone }
      if (cle === 'd') {
        return maj
          ? { geste: 'piocherPlusieurs', zone: cible.zone }
          : { geste: 'piocher', zone: cible.zone, nombre: 1 }
      }
      return undefined
    }
    // Un chiffre pioche autant de cartes : notre raccourci, en plus d'OCTGN
    // (Ctrl+Maj+D y demande le nombre dans une fenêtre).
    if (!ctrl && !alt && /^[1-9]$/.test(cle)) return { geste: 'piocher', zone: cible.zone, nombre: Number(cle) }
    return undefined
  }

  const sens = maj ? -1 : 1
  const type = cible.type

  if (alt) {
    const statut = cle === 's' ? 'stun' : cle === 'c' ? 'confuse' : cle === 't' ? 'tough' : undefined
    if (!statut || !ATTAQUABLES.has(type)) return undefined
    const present =
      statut === 'stun' ? cible.statuts.stunned : statut === 'confuse' ? cible.statuts.confused : cible.statuts.tough
    // Le moteur BASCULE le statut : on ne l'appelle que si ça change quelque chose.
    return ctrl === present ? { geste: 'statut', id: cible.id, statut, pose: !ctrl } : undefined
  }
  if (ctrl) {
    if (maj) return undefined
    if (cle === 'f') return { geste: 'retourner', id: cible.id }
    if (cle === 'v') return { geste: 'victoire', id: cible.id }
    return undefined
  }

  switch (cle) {
    case 'f7':
      return SANS_ETAT.has(type) ? undefined : basculer(cible)
    case 'f3':
      return MANIGANCES.has(type) || SANS_ETAT.has(type)
        ? undefined
        : { geste: 'jetons', id: cible.id, nature: 'degats', nombre: sens }
    case 'f5':
      return MANIGANCES.has(type) ? { geste: 'jetons', id: cible.id, nature: 'menace', nombre: sens } : undefined
    case 'f4':
      return { geste: 'acceleration', id: cible.id, nombre: sens }
    case 'delete':
      if (IDENTITES.has(type)) return undefined
      if (VILAINS.has(type)) return { geste: 'vaincreStade' }
      if (type === 'MainScheme') return { geste: 'maniganceTerminee' }
      return { geste: 'defausser', id: cible.id }
    case 'arrowup':
    case 'arrowdown': {
      const nombre = cle === 'arrowup' ? 1 : -1
      const nature = natureDe(type)
      if (nature === 'marqueur') return { geste: 'compteur', id: cible.id, nombre }
      return { geste: 'jetons', id: cible.id, nature, nombre }
    }
    case 'arrowright':
      return { geste: 'compteur', id: cible.id, nombre: 1 }
    case 'arrowleft':
      return { geste: 'compteur', id: cible.id, nombre: -1 }
    default:
      return undefined
  }
}

// --- L'état des touches enfoncées, pour la tâche 5 --------------------------
//
// Contrat du plan (tâche 4) : IL N'Y AURA QU'UNE SEULE écoute clavier dans
// tout le mode manuel. La tâche 5 (glisser-déposer) a besoin de savoir si Maj
// est enfoncée au moment où on lâche une carte ; elle ne pose pas sa propre
// écoute, elle lit cet état, alimenté par la SEULE écoute réelle
// (CoucheTriche.tsx, `useTriche`). Deux écoutes concurrentes sur les mêmes
// événements sont une source de bugs d'ordonnancement.

export type EtatTouches = {
  /** À appeler depuis l'écoute unique, sur `keydown` ET `keyup`. */
  enregistrer(evenement: Pick<KeyboardEvent, 'key' | 'type'>): void
  /** Vrai si cette touche est actuellement enfoncée. Casse ignorée. */
  estEnfoncee(cle: string): boolean
}

export function creerEtatTouches(): EtatTouches {
  const enfoncees = new Set<string>()
  return {
    enregistrer(evenement) {
      const cle = evenement.key.toLowerCase()
      if (evenement.type === 'keydown') enfoncees.add(cle)
      else if (evenement.type === 'keyup') enfoncees.delete(cle)
    },
    estEnfoncee: (cle) => enfoncees.has(cle.toLowerCase()),
  }
}

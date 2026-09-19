// clavier.ts — ce que veut dire une touche, quand on survole quelque chose.
//
// Calqué sur Tabletop Simulator : F retourne, R mélange, Q incline, un chiffre
// agit sur ce qu'on survole. `interpreterTouche` est une fonction PURE : elle
// ne touche ni au DOM ni au réseau, elle dit seulement quel geste la touche
// demande. Le branchement (survol du pointeur, envoi au moteur) vit dans
// CoucheTriche.tsx, et se teste ailleurs.
//
// ⚠ ON NE DEVINE PAS le jeton d'une carte qui n'en a pas de naturel : mieux
// vaut ne rien poser que poser la mauvaise chose sur une carte qu'on ne
// relira pas. Le clic droit, lui, nomme chaque jeton.

export type Touche = { cle: string; majuscule: boolean }

export type CibleClavier =
  | { genre: 'carte'; id: number; jetonNaturel: 'degats' | 'menace' | 'aucun' }
  | { genre: 'pile'; zone: string }

export type GesteClavier =
  | { geste: 'retourner'; id: number }
  | { geste: 'incliner'; id: number }
  | { geste: 'melanger'; zone: string }
  | { geste: 'piocher'; zone: string; nombre: number }
  | { geste: 'jetons'; id: number; nature: 'degats' | 'menace'; nombre: number }

export function interpreterTouche(
  touche: Touche,
  cible: CibleClavier
): GesteClavier | undefined {
  const cle = touche.cle.toLowerCase()

  if (cle === 'f' && cible.genre === 'carte') return { geste: 'retourner', id: cible.id }
  if (cle === 'q' && cible.genre === 'carte') return { geste: 'incliner', id: cible.id }
  if (cle === 'r' && cible.genre === 'pile') return { geste: 'melanger', zone: cible.zone }

  const chiffre = /^[1-9]$/.test(cle) ? Number(cle) : undefined
  if (chiffre === undefined) return undefined

  if (cible.genre === 'pile') {
    return { geste: 'piocher', zone: cible.zone, nombre: chiffre }
  }
  if (cible.jetonNaturel === 'aucun') return undefined
  return {
    geste: 'jetons',
    id: cible.id,
    nature: cible.jetonNaturel,
    nombre: touche.majuscule ? -chiffre : chiffre,
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

// phases-manuel.ts — les phases d'un round, pour la piste affichée en mode manuel.
//
// Le moteur se tait en manuel : il ne sait plus où en est la table. La piste est donc
// PUREMENT visuelle et tenue à la main par le joueur (clic sur une étape, ou « Étape
// suivante »), comme le suivi de phase de DragnCards. Elle ne parle jamais au moteur.

export type EtapePhase = {
  id: string
  phase: 'heros' | 'mechant' | 'fin'
  libelle: string
  detail: string
}

export const ETAPES_MANUEL: EtapePhase[] = [
  {
    id: 'heros',
    phase: 'heros',
    libelle: 'Phase des héros',
    detail: 'Chaque héros joue son tour : cartes, actions, forme héros ou alter ego.',
  },
  {
    id: 'mechant-1',
    phase: 'mechant',
    libelle: '1. Menace',
    detail: 'Ajouter la menace sur la manigance principale (accélération comprise).',
  },
  {
    id: 'mechant-2',
    phase: 'mechant',
    libelle: '2. Activation du méchant',
    detail: 'Le méchant attaque ou manigance : une carte boost par activation.',
  },
  {
    id: 'mechant-3',
    phase: 'mechant',
    libelle: '3. Activation des sbires',
    detail: 'Chaque sbire attaque ou manigance : une carte boost par activation.',
  },
  {
    id: 'mechant-4',
    phase: 'mechant',
    libelle: '4. Carte de rencontre',
    detail: 'Distribuer une carte rencontre à chaque héros.',
  },
  {
    id: 'mechant-5',
    phase: 'mechant',
    libelle: '5. Révélation',
    detail: 'Chaque héros révèle sa carte rencontre ; une carte Surge en fait révéler une autre.',
  },
  {
    id: 'fin',
    phase: 'fin',
    libelle: 'Fin du round',
    detail: 'Tout redresser, piocher jusqu’à la taille de main, passer le jeton premier joueur.',
  },
]

export type PisteEtat = { round: number; index: number }

export function etatInitial(round: number | undefined): PisteEtat {
  return { round: Math.max(1, round ?? 1), index: 0 }
}

/** L'étape suivante ; après « Fin du round », on repart sur la phase des héros du round d'après. */
export function etapeSuivante(etat: PisteEtat): PisteEtat {
  if (etat.index >= ETAPES_MANUEL.length - 1) return { round: etat.round + 1, index: 0 }
  return { round: etat.round, index: etat.index + 1 }
}

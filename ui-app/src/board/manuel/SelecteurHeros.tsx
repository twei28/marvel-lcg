// SelecteurHeros.tsx — passer d'un héros à l'autre, en mode manuel.
//
// Pourquoi (tâche 7 bis, 19/09/2026) : la spec du mode manuel promettait
// « toutes les mains visibles, puisqu'il n'y a qu'un opérateur ». Structurel-
// lement impossible : `zones.ts` ne construit qu'UNE zone « main », celle du
// joueur regardé (`notre?.hand_cards`). Décision de l'utilisateur : une main
// à l'écran, et ce sélecteur pour passer de l'une à l'autre.
//
// Ce composant ne fait QUE poser `onRegarder` : il ne calcule rien de la vue
// lui-même. `board.tsx` le branche sur `vueForcee`, le même état qui entre
// déjà dans le calcul du joueur regardé en mode automatique (celui-là suit
// `etat.joueurDemande`) — pas de second chemin de vue.
//
// Repris de `board/mobile/OngletsJoueurs.tsx`, qui résout le même problème
// pour le multijoueur en portrait : un onglet par héros, celui qu'on regarde
// marqué, invisible en solo. Composant distinct plutôt que réutilisé tel
// quel : celui-ci vit dans `manuel/`, pas `mobile/`, et n'a pas vocation à
// suivre les évolutions propres au portrait.
//
// Apparence : les classes `bh-vue` / `bh-bouton` / `est-actif` sont celles du
// sélecteur de vue PC (board.tsx, board.css) — même style de chrome, sans
// réinventer une apparence pour la même idée (« regarde ce que le plateau
// sait déjà afficher d'un héros »). Ce sélecteur-ci n'a pas de bouton
// « Auto » : ce concept suit celui à qui le moteur pose une question, et le
// moteur ne demande plus rien en manuel.
import type { ReactElement } from 'react'
import { t } from '../langue'

export function SelecteurHeros({
  joueurs,
  regarde,
  onRegarder,
}: {
  joueurs: Array<{ id: number; nom: string }>
  regarde: number
  onRegarder: (id: number) => void
}): ReactElement | null {
  // À un seul héros, un sélecteur n'apprend rien et prend de la place sur un
  // plateau qu'on veut nu. C'EST LA SEULE GARDE : `board.tsx` ne filtre que
  // sur le mode manuel, pas sur le nombre de héros — même partage des
  // responsabilités qu'`OngletsJoueurs` (mobile/OngletsJoueurs.tsx), dont
  // l'appelant (PlateauPortrait) ne vérifie pas non plus la longueur.
  if (joueurs.length < 2) return null
  return (
    <span className="bh-vue" role="tablist" title={t('Quel héros est affiché (plateau et main)')}>
      {joueurs.map(({ id, nom }) => (
        <button
          type="button"
          role="tab"
          key={id}
          aria-selected={id === regarde}
          className={`bh-bouton${id === regarde ? ' est-actif' : ''}`}
          title={nom}
          onClick={() => onRegarder(id)}
        >
          {nom}
        </button>
      ))}
    </span>
  )
}

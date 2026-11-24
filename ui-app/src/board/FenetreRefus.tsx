// POURQUOI CETTE ACTION N'EST PAS OFFERTE : la petite fenetre du CLIC.
//
// Demande de l'utilisateur, 15/11/2026 (Casey's Bag, Mutant Fight Club, Nick Fury : des joueurs croyaient la carte cassee alors
// qu'il n'y avait « rien a faire », par exemple aucune arme dans la defausse). Le survol disait deja la raison (`raisons-refus.ts`) ;
// le CLIC sur une carte dont rien n'est offert ouvre maintenant cette fenetre, avec la raison et un acces direct a la defausse pour
// verifier soi-meme.
import { createContext, useContext } from 'react'
import { t } from './langue'

export interface OuvertureRefus {
  /** Nom de la carte cliquee. */
  carte: string
  /** Les raisons, deja en phrases (`phraseDuRefus`). */
  raisons: string[]
}

export interface PileConsultable {
  titre: string
  ouvrir: () => void
}

/** Ce que l'unite du plateau lit pour rendre une carte cliquable : ses raisons par carte, et comment ouvrir la fenetre. */
export const ContexteRefus = createContext<{
  raisons: Map<number, string[]>
  ouvrir: (ouverture: OuvertureRefus) => void
} | null>(null)

export function useContexteRefus() {
  return useContext(ContexteRefus)
}

export function FenetreRefus({
  ouverture,
  piles,
  fermer,
}: {
  ouverture: OuvertureRefus
  piles: PileConsultable[]
  fermer: () => void
}) {
  return (
    <div className="fenetre-refus-voile" role="presentation" onClick={fermer}>
      <div
        className="fenetre-refus"
        role="dialog"
        aria-modal="true"
        aria-label={ouverture.carte}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="fenetre-refus-titre">{ouverture.carte}</div>
        <div className="fenetre-refus-sous-titre">{t("Rien à faire avec cette carte pour l'instant")}</div>
        <ul className="fenetre-refus-raisons">
          {ouverture.raisons.map((raison) => (
            <li key={raison}>{raison}</li>
          ))}
        </ul>
        <div className="fenetre-refus-actions">
          {piles.map((pile) => (
            <button
              key={pile.titre}
              type="button"
              className="fenetre-refus-bouton"
              onClick={() => {
                fermer()
                pile.ouvrir()
              }}
            >
              {piles.length > 1 ? `${t('Voir')} ${pile.titre}` : t('Voir la défausse')}
            </button>
          ))}
          <button type="button" className="fenetre-refus-bouton fenetre-refus-fermer" onClick={fermer}>
            {t('Fermer')}
          </button>
        </div>
      </div>
    </div>
  )
}

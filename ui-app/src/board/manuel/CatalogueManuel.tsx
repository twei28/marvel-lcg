// CatalogueManuel.tsx — faire apparaître n'importe quelle carte du catalogue.
//
// Mode manuel uniquement : le moteur ne conduit plus rien, donc « ajouter une
// carte » ne peut venir que du joueur, qui la choisit ici PAR NOM (personne ne
// connaît le card_id d'une carte de tête) et la pose ensuite lui-même.
//
// La recherche ne part qu'à partir de deux caractères saisis
// (`Catalogue.chercherParNom`) : le catalogue dépasse les 6000 cartes, tout
// rendre à la première lettre serait à la fois illisible et coûteux.
//
// Chaque résultat montre son scan — mêmes classes que la pile ouverte du bac
// à sable (`CoucheTriche.tsx`, `.pile-triche*`) : une liste de noms nus est
// invérifiable à cette échelle, où plusieurs dizaines de cartes partagent
// souvent un mot.

import { useState } from 'react'
import { scanUrl } from '../card-model'
import { t } from '../langue'
import type { Catalogue } from '../catalogue'

export type CatalogueManuelProps = {
  catalogue: Catalogue
  onFermer: () => void
  /**
   * La carte choisie part en zone de résolution — voir `triche.creerCarte`.
   * Le NOM transite avec l'identifiant (ronde de correction 1, tâche 6) :
   * sans lui, le journal de partie n'aurait que le card_id à écrire, illisible
   * pour qui relit la partie plus tard.
   */
  onPoser: (cardId: string, nom: string) => void
}

export function CatalogueManuel({ catalogue, onFermer, onPoser }: CatalogueManuelProps) {
  const [recherche, setRecherche] = useState('')
  const resultats = catalogue.chercherParNom(recherche)

  return (
    <div className="pile-triche-voile" onPointerDown={onFermer}>
      <section
        className="pile-triche catalogue-manuel"
        role="dialog"
        aria-label={t('Faire apparaître une carte')}
        onPointerDown={(evenement) => evenement.stopPropagation()}
      >
        <header className="pile-triche-entete">
          <h2>{t('Faire apparaître une carte')}</h2>
          <span className="pile-triche-aide">{t('Cherche un nom, à partir de deux lettres')}</span>
          <button type="button" onClick={onFermer}>{t('Fermer')}</button>
        </header>

        <div className="catalogue-manuel-recherche">
          <input
            role="searchbox"
            type="text"
            autoFocus
            value={recherche}
            placeholder={t('Nom de la carte…')}
            onChange={(evenement) => setRecherche(evenement.target.value)}
          />
        </div>

        <div className="pile-triche-cartes">
          {resultats.map((resultat) => (
            <button
              type="button"
              key={resultat.card_id}
              className="pile-triche-carte catalogue-manuel-resultat"
              onClick={() => onPoser(resultat.card_id, resultat.name)}
            >
              <img src={scanUrl(resultat.pic_id ?? resultat.card_id)} alt={resultat.name} loading="lazy" />
              <span>{resultat.name}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  )
}

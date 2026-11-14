// La fenetre de choix PAR NOM (AskChooseOneText cote moteur : fouiller sa
// defausse/son deck pour une carte nommee, "Role: Brawler" exclu, voir
// `cartesDuLot`).
//
// AVANT (demande utilisateur du 07/11/2026, rapport de bug nicodede62) : ce
// choix passait par `DemandeCentrale`, le menu de boutons generique pour
// TOUT (cibler, Attaquer/Defendre, capacites). Deux defauts propres a ce cas
// precis :
//   - layout en bandes de texte empilees, pas une grille de vraies cartes ;
//   - quand la carte nommee n'etait pas retrouvee (bug de synchronisation),
//     le survol retombait sur bind_id = L'IDENTITE DU JOUEUR (le moteur ne
//     porte jamais la vraie carte pour ce type de choix, voir effect.py),
//     affichant Dazzler/Alison Blaire a la place d'une carte de sa defausse.
//
// Ce composant ne devine plus rien par survol : chaque case montre la vraie
// carte si `carteDeLOption` la retrouve, sinon une case NEUTRE (son nom
// seul, jamais l'identite) — `ScanCard` sait deja afficher ce repli (voir
// `scan-fallback`, declenche par une `imageUrl` vide).
//
// DEUX TEMPS (07/11/2026, retour utilisateur : « un bouton a valider, qu'on
// choisisse la carte et puis qu'on valide, et qu'on voit quelle carte on a
// choisi ») : un premier clic SELECTIONNE seulement (halo blanc, meme
// convention que `SelecteurCibles`/`state: 'selected'`), un second clic sur
// une autre carte change la selection, et seul « Valider » envoie le choix
// au moteur. Un clic malheureux ne valide donc plus rien tout seul.

import { useState } from 'react'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import type { Option } from './ask'
import { t } from './langue'
import './selecteur-fenetre.css'

/** Case neutre (nom seul, jamais l'identite du joueur) quand la carte n'a pas ete retrouvee. */
function carteInconnueDepuisOption(option: Option): ScanCardProps {
  return { id: `choix-${option.id}`, name: option.name, kind: 'unknown', imageUrl: '' }
}

export type SelecteurChoixTexteProps = {
  titre: string
  options: Option[]
  carteDeLOption: (option: Option) => ScanCardProps | undefined
  choisir: (option: Option) => void
  annuler?: () => void
}

export function SelecteurChoixTexte({ titre, options, carteDeLOption, choisir, annuler }: SelecteurChoixTexteProps) {
  const [selectionneeId, setSelectionneeId] = useState<number | undefined>(undefined)
  if (options.length === 0) return null
  const selectionnee = options.find((option) => option.id === selectionneeId)
  return (
    <div className="plateau-selecteur-voile">
      <div className="plateau-selecteur est-fenetre">
        <div className="plateau-selecteur-entete">
          <strong>{titre}</strong>
          <span className="plateau-selecteur-compte">
            {selectionnee ? t('Carte choisie : clique « Valider », ou une autre carte pour changer') : t('Clique une carte, puis « Valider »')}
          </span>
        </div>
        <div className="plateau-selecteur-cartes">
          {options.map((option) => {
            const props = carteDeLOption(option) ?? carteInconnueDepuisOption(option)
            const choisie = option.id === selectionneeId
            return (
              <ScanCard
                key={option.id}
                {...props}
                state={choisie ? 'selected' : 'targetable'}
                onSelect={() => setSelectionneeId(option.id)}
              />
            )
          })}
        </div>
        <div className="plateau-selecteur-boutons">
          {annuler ? (
            <button type="button" className="plateau-selecteur-annuler" onClick={annuler}>
              {t('Annuler')}
            </button>
          ) : null}
          <button
            type="button"
            className="plateau-selecteur-valider"
            disabled={!selectionnee}
            onClick={() => {
              if (selectionnee) choisir(selectionnee)
            }}
          >
            {t('Valider')}
          </button>
        </div>
      </div>
    </div>
  )
}

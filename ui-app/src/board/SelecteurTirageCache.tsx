// La fenêtre du TIRAGE MANUEL (14/11/2026, rapport 131). Les cartes cachées d'un tirage « au hasard » (captifs de
// côté, main) se présentent FACE CACHÉE : elles se mélangent pendant une seconde, puis le joueur en désigne une.
// Même voile et même geste que `SelecteurChoixTexte` (un clic sélectionne, « Valider » envoie), mais jamais de nom
// ni d'image : les options du moteur ne sont que des rangs (« [tirage-cache] 3 »).
import { useEffect, useState } from 'react'
import { ScanCard } from '../components/ScanCard'
import type { Option } from './ask'
import { scanUrl } from './card-model'
import { t } from './langue'
import { DUREE_MELANGE_MS } from './tirage-cache'
import './selecteur-fenetre.css'
import './tirage-cache.css'

export type SelecteurTirageCacheProps = {
  titre: string
  options: Option[]
  choisir: (option: Option) => void
  annuler?: () => void
  /** Pour les tests : durée du mélange (0 = aucun). */
  dureeMelangeMs?: number
}

export function SelecteurTirageCache({ titre, options, choisir, annuler, dureeMelangeMs = DUREE_MELANGE_MS }: SelecteurTirageCacheProps) {
  const [melange, setMelange] = useState(dureeMelangeMs > 0)
  const [selectionneeId, setSelectionneeId] = useState<number | undefined>(undefined)
  useEffect(() => {
    if (dureeMelangeMs <= 0) return
    const minuteur = window.setTimeout(() => setMelange(false), dureeMelangeMs)
    return () => window.clearTimeout(minuteur)
  }, [dureeMelangeMs])
  if (options.length === 0) return null
  const selectionnee = options.find((option) => option.id === selectionneeId)
  return (
    <div className="plateau-selecteur-voile">
      <div className="plateau-selecteur est-fenetre tirage-cache">
        <div className="plateau-selecteur-entete">
          <strong>{titre}</strong>
          <span className="plateau-selecteur-compte">
            {melange
              ? t('Les cartes se mélangent…')
              : selectionnee
                ? t('Carte choisie : clique « Valider », ou une autre carte pour changer')
                : t('Clique une carte, puis « Valider »')}
          </span>
        </div>
        <div className={`plateau-selecteur-cartes tirage-cache-cartes${melange ? ' est-melange' : ''}`} data-melange={melange ? 'oui' : 'non'}>
          {options.map((option, rang) => (
            <div key={option.id} className="tirage-cache-case" style={{ ['--rang' as string]: rang }}>
              <ScanCard
                id={`tirage-${option.id}`}
                name={t('Carte cachée')}
                kind="unknown"
                imageUrl={scanUrl('player')}
                facedown
                state={option.id === selectionneeId ? 'selected' : melange ? 'ready' : 'targetable'}
                onSelect={melange ? undefined : () => setSelectionneeId(option.id)}
              />
            </div>
          ))}
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
            disabled={melange || !selectionnee}
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

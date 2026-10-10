// LE BANDEAU « ANNULER » (zone 3 de la refonte du 09/10/2026) : cinq secondes
// apres chaque action du joueur, un bandeau au bas de l'ecran propose de la
// defaire. Sur telephone, « Annuler » vivait au fond du menu « … » : deux
// touchers pour rattraper un doigt qui a glisse.
//
// Il ne connait PAS l'annulation : il appelle celle du menu (`annulerCoup`,
// board.tsx), la meme que le bouton « ↶ Annuler » du plateau PC. Il s'allume
// sur le signal de `envoyerReponse` (moteur.ts), seulement apres un geste du
// joueur : une reponse automatique n'est pas « son » action.
import { useEffect, useRef, useState, type ReactElement } from 'react'
import { langueActuelle, t } from '../langue'
import { EVENEMENT_REPONSE_ENVOYEE } from '../moteur'
import { gesteRecent, installerSuiviDuGeste } from './telephone'

export const DUREE_BANDEAU_ANNULER_MS = 5000

export function BandeauAnnuler({ annuler }: { annuler?: () => void }): ReactElement | null {
  const [visible, setVisible] = useState(false)
  // Change a chaque action : la barre de temps repart de zero.
  const [tour, setTour] = useState(0)
  const minuteur = useRef<number | undefined>(undefined)

  useEffect(() => {
    if (!annuler) return
    installerSuiviDuGeste()
    const surReponse = () => {
      if (!gesteRecent()) return
      setVisible(true)
      setTour((n) => n + 1)
      if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
      minuteur.current = window.setTimeout(() => {
        minuteur.current = undefined
        setVisible(false)
      }, DUREE_BANDEAU_ANNULER_MS)
    }
    window.addEventListener(EVENEMENT_REPONSE_ENVOYEE, surReponse)
    return () => {
      window.removeEventListener(EVENEMENT_REPONSE_ENVOYEE, surReponse)
      if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
      minuteur.current = undefined
    }
  }, [annuler])

  if (!annuler || !visible) return null
  return (
    <div className="bandeau-annuler" role="status" key={tour}>
      <span className="bandeau-annuler-texte">{t('Action faite')}</span>
      <button
        type="button"
        className="bandeau-annuler-bouton"
        data-tactile="annuler"
        onClick={() => {
          if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
          minuteur.current = undefined
          setVisible(false)
          annuler()
        }}
      >
        {/* « Annuler » se traduit « Undo » ici, comme le bouton du menu (board.tsx) :
            le dictionnaire reserve « Annuler » -> « Cancel » a l'assistant. */}
        <span aria-hidden="true">↶</span> {langueActuelle() === 'fr' ? 'Annuler' : 'Undo'}
      </button>
      <span className="bandeau-annuler-temps" aria-hidden="true" />
    </div>
  )
}

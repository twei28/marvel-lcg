// La fenêtre « tu es sûr ? », à la typo du jeu.
//
// Elle remplace `window.confirm`. Le dialogue natif de Chrome ne se style pas :
// il tombait en plein milieu d'un plateau habillé, avec la police du système et
// les boutons du navigateur — signalé en jeu comme « un truc de Chrome ».
//
// L'API garde la forme de celle qu'elle remplace : on `await` une réponse
// booléenne, donc les appelants ne changent pas de structure.
//
//   const confirmer = useConfirmation()
//   if (!(await confirmer({ titre: '…', texte: '…' }))) return
//
// Deux choix d'implémentation qui comptent :
//
//  • La promesse est résolue par le bouton, jamais par un démontage. Un
//    dialogue qui disparaîtrait sans répondre laisserait l'appelant suspendu
//    pour toujours ; ici Échap et le voile répondent « non ».
//  • Le rendu passe par un portail sur `document.body`, comme l'aperçu de
//    carte. Le plateau crée des contextes d'empilement (transform, filter) qui
//    piégeraient un `position: fixed` posé à l'intérieur.

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { createPortal } from 'react-dom'
import { t } from './langue'
import { transformDecalage, useGlisserPanneau } from './placement/useGlisserPanneau'

export type DemandeConfirmation = {
  titre: string
  texte?: string
  /** Libellé du bouton qui valide. Défaut : « Confirmer ». */
  confirmer?: string
  /** Libellé du bouton qui renonce. Défaut : « Annuler ». */
  annuler?: string
  /** `danger` colore le bouton de validation en rouge : l'action est perdante. */
  ton?: 'normal' | 'danger'
}

type Demander = (demande: DemandeConfirmation) => Promise<boolean>

/**
 * Hors fournisseur, on retombe sur `window.confirm` plutôt que de refuser :
 * un test qui monte un composant isolé ne doit pas échouer sur l'absence de
 * décor, et une réponse laide vaut mieux qu'une action muette.
 */
const ContexteConfirmation = createContext<Demander>(async (demande) =>
  window.confirm([demande.titre, demande.texte].filter(Boolean).join('\n\n'))
)

export function useConfirmation(): Demander {
  return useContext(ContexteConfirmation)
}

type EnAttente = DemandeConfirmation & { repondre: (accepte: boolean) => void }

export function FournisseurConfirmation({ children }: { children: ReactNode }) {
  const [enAttente, setEnAttente] = useState<EnAttente | undefined>(undefined)

  const demander = useCallback<Demander>(
    (demande) =>
      new Promise<boolean>((resoudre) => {
        setEnAttente({
          ...demande,
          repondre: (accepte) => {
            setEnAttente(undefined)
            resoudre(accepte)
          },
        })
      }),
    []
  )

  return (
    <ContexteConfirmation.Provider value={demander}>
      {children}
      {enAttente ? <Dialogue demande={enAttente} /> : null}
    </ContexteConfirmation.Provider>
  )
}

function Dialogue({ demande }: { demande: EnAttente }) {
  const { repondre } = demande
  const valider = useRef<HTMLButtonElement | null>(null)
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »).
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(demande.titre)

  // Le bouton qui valide prend le focus : la touche Entrée répond « oui », et
  // le lecteur d'écran annonce le dialogue au lieu de le laisser passer.
  useEffect(() => {
    valider.current?.focus()
  }, [])

  useEffect(() => {
    const surTouche = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') {
        evenement.stopPropagation()
        repondre(false)
      }
    }
    window.addEventListener('keydown', surTouche, true)
    return () => window.removeEventListener('keydown', surTouche, true)
  }, [repondre])

  return createPortal(
    <div
      className="confirm-voile"
      // Cliquer à côté renonce — comme fermer la fenêtre du navigateur le
      // faisait. On filtre sur la cible pour ne pas intercepter les clics des
      // boutons, qui remontent jusqu'ici.
      onClick={(evenement) => {
        if (evenement.target === evenement.currentTarget) repondre(false)
      }}
    >
      <section
        className={`confirm-modale${demande.ton === 'danger' ? ' est-danger' : ''}`}
        role="alertdialog"
        aria-modal="true"
        aria-label={demande.titre}
        style={transformDecalage(decalage)}
      >
        <div
          className="poignee-glisser"
          onPointerDown={gestesGlisser.onPointerDown}
          onPointerMove={gestesGlisser.onPointerMove}
          onPointerUp={gestesGlisser.onPointerUp}
          onPointerCancel={gestesGlisser.onPointerCancel}
        >
          <span className="plateau-eyebrow">{t('Confirmation')}</span>
          <strong className="confirm-titre">{demande.titre}</strong>
        </div>
        {demande.texte ? <p className="confirm-texte">{demande.texte}</p> : null}
        <div className="confirm-boutons">
          <button type="button" className="confirm-non" onClick={() => repondre(false)}>
            {demande.annuler ?? t('Annuler')}
          </button>
          <button
            type="button"
            ref={valider}
            className="confirm-oui"
            onClick={() => repondre(true)}
          >
            {demande.confirmer ?? t('Confirmer')}
          </button>
        </div>
      </section>
    </div>,
    document.body
  )
}

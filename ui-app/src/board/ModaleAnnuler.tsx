// ModaleAnnuler : « Annuler remet la partie comme avant ta dernière action ».
//
// Depuis le 29/10/2026, « Annuler » ne rejoue plus toute la partie pendant le
// tour du joueur : le moteur restaure un instantané (game/world/instantane.py).
// Hors de ce cas (phase du méchant, début de tour), il rejoue encore, et cela
// peut durer. Le joueur ne pouvait pas le deviner : cette fenêtre le dit avant
// d'agir, avec la case « ne plus me montrer ça ».
//
// Même famille que ModaleAmbiance (case = un TROISIÈME renseignement, pas une
// réponse), même portail sur `document.body` pour échapper aux contextes
// d'empilement du plateau. Les classes `ambiance-*` sont celles de cette
// fenêtre-là : une seule mise en page pour toutes les questions à case.
//
// Réglage PERSONNEL (localStorage) : le moteur et les autres joueurs ne le
// voient pas. Cocher la case puis « Garder mon coup » vaut aussi « ne plus
// demander », comme pour l'ambiance : la case parle de la fenêtre, pas du choix.

import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { t } from './langue'
import { ecrireAnnulerExplique } from './moteur'

export function ModaleAnnuler({
  onConfirmer,
  onFermer,
}: {
  /** Le joueur veut bien annuler : l'appelant envoie `/undo auto`. */
  onConfirmer: () => void
  /** La fenêtre se ferme sans rien annuler. */
  onFermer: () => void
}) {
  const [nePlusMontrer, setNePlusMontrer] = useState(false)
  const boutonOui = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    boutonOui.current?.focus()
    const surTouche = (evenement: KeyboardEvent) => {
      if (evenement.key !== 'Escape') return
      evenement.stopPropagation()
      onFermer()
    }
    window.addEventListener('keydown', surTouche, true)
    return () => window.removeEventListener('keydown', surTouche, true)
  }, [onFermer])

  function repondre(annuler: boolean) {
    if (nePlusMontrer) ecrireAnnulerExplique(true)
    if (annuler) onConfirmer()
    else onFermer()
  }

  return createPortal(
    <div className="ambiance-voile annuler-voile" onClick={() => repondre(false)}>
      <section
        className="ambiance-modale annuler-modale"
        role="alertdialog"
        aria-modal="true"
        aria-label={t('Annuler ta dernière action ?')}
        onClick={(evenement) => evenement.stopPropagation()}
      >
        <strong className="ambiance-carte">{t('Annuler ta dernière action ?')}</strong>
        <p className="ambiance-effet">
          {t('La partie revient exactement comme avant ta dernière action : cartes, jetons, pioche et hasard.')}
        </p>
        <p className="ambiance-texte">
          {t(
            'Pendant ton tour, c’est instantané. Ailleurs (phase du méchant, début de tour), la partie est rejouée depuis le début et peut prendre quelques secondes.'
          )}
        </p>
        <p className="ambiance-texte">{t('Tu peux annuler plusieurs actions de suite.')}</p>
        <label className="ambiance-case">
          <input
            type="checkbox"
            checked={nePlusMontrer}
            onChange={(evenement) => setNePlusMontrer(evenement.target.checked)}
          />
          {t('Ne plus me montrer ça')}
        </label>
        <div className="ambiance-boutons">
          <button type="button" className="ambiance-non" onClick={() => repondre(false)}>
            {t('Garder mon coup')}
          </button>
          <button ref={boutonOui} type="button" className="ambiance-oui" onClick={() => repondre(true)}>
            {t('Oui, annuler')}
          </button>
        </div>
      </section>
    </div>,
    document.body
  )
}

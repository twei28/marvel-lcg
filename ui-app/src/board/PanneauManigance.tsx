// LA FACE A DE LA MANIGANCE, EN GRAND, AVANT QU'ELLE SE RETOURNE.
//
// Demande de l'utilisateur, 15/09/2026 : « on doit voir la face A de la
// premiere manigance, puis on fait ok, puis elle se place sur la face B ».
// Le moteur ATTEND vraiment cette reponse (World.ConfirmMainSchemeReveal) :
// c'est le seul mouvement de toute l'ouverture, tout le reste a ete rendu
// silencieux expres (voir manigance-face-a.ts).
//
// Correction du 15/09/2026 (relecture) : `repondre` demonte ce panneau des
// que le moteur avance (board.tsx retire <PanneauManigance> quand la
// question disparait). Poster la reponse AU CLIC coupait donc la transition
// CSS en plein vol sur un aller-retour local de quelques dizaines de ms : le
// joueur ne voyait qu'un eclair, jamais un retournement. On anime D'ABORD, on
// repond ENSUITE : le moteur attend deja le joueur, il attendra bien
// DUREE_RETOURNEMENT de plus.

import { useEffect, useRef, useState } from 'react'
import { scanUrl } from './card-model'
import { t } from './langue'
import { nomAffiche } from './noms-cartes-fr'
import type { WorldCard } from './world'

/**
 * ⚠ DOIT VALOIR LA MEME CHOSE que la transition de `.panneau-manigance.est-
 * retournee .panneau-manigance-carte` dans board.css. Valeur dupliquee et
 * assumee : CSS et JS n'ont aucun moyen de partager une constante ici.
 */
export const DUREE_RETOURNEMENT = 400

export function PanneauManigance({
  carte,
  onValider,
}: {
  carte: WorldCard
  /**
   * Poste la reponse au moteur, et dit si elle EST PARTIE (voir
   * `Moteur.repondre`). Un `false` rouvre le bouton : sans ce fait, un envoi
   * rate laissait le panneau ferme pour toujours et la partie figee.
   */
  onValider: () => Promise<boolean>
}) {
  // ⚠ UN SEUL ENVOI. Le moteur n'attend qu'une reponse ; une seconde partirait
  // dans le vide, ou pire, repondrait a la question suivante. `envoye` porte
  // aussi bien la garde du double clic que le declenchement du retournement :
  // les deux se decident au meme instant, seul l'appel a `onValider` est
  // retarde.
  const [envoye, setEnvoye] = useState(false)
  const idMinuteur = useRef<number | undefined>(undefined)
  const monte = useRef(true)

  useEffect(
    () => () => {
      monte.current = false
      if (idMinuteur.current !== undefined) window.clearTimeout(idMinuteur.current)
    },
    []
  )

  // ⚠ UN ENVOI QUI ECHOUE NE FERME PAS LA PORTE. Defaut trouve en relecture le
  // 15/09/2026 : `moteur.repondre` attrape l'erreur reseau, garde la demande et
  // ne publie qu'une erreur. Le bouton, lui, restait `disabled` : plus aucun
  // moyen de renvoyer, partie figee sur la face A. `repondre` dit desormais si
  // la reponse est partie, et le panneau rouvre sur ce FAIT — pas sur une
  // minuterie. La carte revient alors sur sa face A, ce qui est la verite : le
  // moteur attend toujours la meme reponse.
  const envoyer = async () => {
    const partie = await onValider()
    if (!partie && monte.current) setEnvoye(false)
  }

  return (
    <div
      className={`panneau-manigance${envoye ? ' est-retournee' : ''}`}
      role="dialog"
      aria-modal="true"
    >
      <img className="panneau-manigance-carte" src={scanUrl(carte.pic_id)} alt={nomAffiche(carte)} />
      <button
        type="button"
        className="panneau-manigance-ok"
        disabled={envoye}
        onClick={() => {
          if (envoye) return
          setEnvoye(true)
          // ⚠ PAS DE onTransitionEnd. Sous prefers-reduced-motion la
          // transition CSS n'existe pas (voir board.css) : l'evenement ne
          // partirait jamais et la partie resterait bloquee pour toujours,
          // un defaut pire que celui qu'on corrige. La gate est explicite.
          const mouvementReduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches
          if (mouvementReduit) {
            void envoyer()
            return
          }
          idMinuteur.current = window.setTimeout(() => void envoyer(), DUREE_RETOURNEMENT)
        }}
      >
        {t('Retourner la manigance')}
      </button>
    </div>
  )
}

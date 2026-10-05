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
import { mouvementReduit } from './affichage'

/**
 * ⚠ DOIT VALOIR LA MEME CHOSE que la transition de `.panneau-manigance.est-
 * retournee .panneau-manigance-carte` dans board.css. Valeur dupliquee et
 * assumee : CSS et JS n'ont aucun moyen de partager une constante ici.
 */
export const DUREE_RETOURNEMENT = 400

/**
 * Le pivot de la carte quand on connait sa face B (05/10/2026, demande de
 * l'utilisateur : « quand on clique sur retourner, elle se retourne au meme
 * endroit, a la meme taille, puis on fait OK »). ⚠ DOIT VALOIR la transition de
 * `.panneau-manigance-pivot-tourne` dans board.css (meme valeur dupliquee).
 */
export const DUREE_PIVOT = 500

export function PanneauManigance({
  carte,
  onValider,
  retournement = true,
  versoUrl,
}: {
  carte: WorldCard
  /**
   * La carte se retourne-t-elle au OK ?
   *
   * ⚠ VRAI POUR LA PRINCIPALE, FAUX POUR UNE ANNEXE (avenant du 15/09/2026).
   * Une manigance principale a deux faces imprimees et le moteur la RETOURNE ;
   * une annexe n'en a qu'une, elle est simplement entree en jeu. Lui jouer une
   * animation de retournement raconterait quelque chose qui n'arrive pas.
   */
  retournement?: boolean
  /**
   * Le scan de la face B, quand le monde la connait. Present : le clic sur
   * « Retourner la manigance » fait PIVOTER la carte sur place, a la meme
   * taille, sur sa face B, et c'est un second bouton « OK » qui repond au
   * moteur. Absent : l'ancien comportement (la reponse part apres l'animation
   * de fondu), faute d'image a montrer.
   */
  versoUrl?: string
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
  // Face B montree (premier clic) et pivot termine : voir `versoUrl`.
  const [faceB, setFaceB] = useState(false)
  const [pivote, setPivote] = useState(false)
  const pivoter = versoUrl !== undefined && retournement
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
      className={`panneau-manigance${envoye && retournement && !pivoter ? ' est-retournee' : ''}${faceB ? ' est-face-b' : ''}`}
      role="dialog"
      aria-modal="true"
    >
      {/* ⚠ UN CADRE AU FORMAT PAYSAGE, ET L'IMAGE QUI TOURNE DEDANS.
          Le serveur redresse TOUS ses scans en portrait
          (`ImageCreator.TryRotateImage`), y compris les manigances, qui sont
          imprimees en paysage. Une <img> posee telle quelle presentait donc la
          carte DEBOUT, texte a la verticale : signale en jeu le 15/09/2026,
          « le main scheme n'est pas en paysage ». Meme montage que
          `CoucheRevelation`, qui avait deja paye ce defaut le 09/09. */}
      {pivoter ? (
        <div className="panneau-manigance-pivot">
          <div className="panneau-manigance-pivot-tourne">
            <div className="panneau-manigance-cadre">
              <img src={scanUrl(carte.pic_id)} alt={nomAffiche(carte)} />
            </div>
            <div className="panneau-manigance-cadre panneau-manigance-cadre-verso">
              <img src={versoUrl} alt="" />
            </div>
          </div>
        </div>
      ) : (
        <div className="panneau-manigance-cadre">
          <img src={scanUrl(carte.pic_id)} alt={nomAffiche(carte)} />
        </div>
      )}
      <button
        type="button"
        className="bh-bouton panneau-manigance-ok"
        disabled={envoye || (pivoter && faceB && !pivote)}
        onClick={() => {
          if (envoye) return
          if (pivoter && !faceB) {
            // Premier clic : la carte pivote sur sa face B, rien ne part. Le
            // bouton ne repond a nouveau qu'une fois le pivot fini, pour qu'un
            // double clic ne saute pas la face B.
            setFaceB(true)
            if (mouvementReduit()) {
              setPivote(true)
              return
            }
            idMinuteur.current = window.setTimeout(() => {
              if (monte.current) setPivote(true)
            }, DUREE_PIVOT)
            return
          }
          setEnvoye(true)
          if (pivoter) {
            void envoyer()
            return
          }
          // ⚠ PAS DE onTransitionEnd. Sous prefers-reduced-motion la
          // transition CSS n'existe pas (voir board.css) : l'evenement ne
          // partirait jamais et la partie resterait bloquee pour toujours,
          // un defaut pire que celui qu'on corrige. La gate est explicite.
          // Sans retournement, il n'y a aucune animation a laisser voir : la
          // reponse part tout de suite, comme en mouvement reduit.
          const sansAttente = !retournement || mouvementReduit()
          if (sansAttente) {
            void envoyer()
            return
          }
          idMinuteur.current = window.setTimeout(() => void envoyer(), DUREE_RETOURNEMENT)
        }}
      >
        {pivoter && faceB ? t('OK') : retournement ? t('Retourner la manigance') : t('Continuer')}
      </button>
    </div>
  )
}

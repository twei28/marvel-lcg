// ModaleAmbiance : « une ambiance s'allume, tu la gardes ? »
//
// Certaines cartes repeignent la table : Dial M for Mojo la passe en noir et
// blanc, The Savage Land l'habille en jungle, les égouts du Hood l'emplissent
// de brume. Jusqu'ici cela arrivait SANS UN MOT : le joueur voyait son plateau
// changer sans savoir ni pourquoi ni comment revenir en arrière.
//
// Pourquoi un composant dédié plutôt que `useConfirmation` (ConfirmationJeu) :
// la confirmation du jeu rend une promesse booléenne et ne porte que deux
// boutons. Il manque ici la case « ne plus me montrer ça », qui n'est pas une
// réponse mais un TROISIÈME renseignement, et lui ajouter une case
// facultative alourdirait une API que trente appels utilisent déjà. La
// confirmation reste ce qu'elle est ; celle-ci vit à côté.
//
// Elle ne retient RIEN : ni le moteur, ni les autres joueurs. C'est un réglage
// personnel, tenu en état React local et dans le localStorage du navigateur.
// La partie continue derrière, y compris en multijoueur.
//
// Comme la confirmation, le rendu passe par un portail sur `document.body` :
// le plateau crée des contextes d'empilement (transform, filter) qui
// piégeraient un `position: fixed` posé à l'intérieur.

import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { enModeDecouverte } from './CoucheCoach'
import {
  LIBELLE_EFFET,
  premiereCarteAmbiance,
  type ApercuMeteo,
  type CarteAmbiance,
} from './CoucheMeteo'
import { t } from './langue'
import { ecrireReponseAmbiance, lireReponseAmbiance, type ReponseAmbiance } from './moteur'
import { transformDecalage, useGlisserPanneau } from './placement/useGlisserPanneau'
import type { World } from './world'

export function ModaleAmbiance({
  monde,
  ambianceActive,
  apercu,
  reglerApercu,
  onReponseFigee,
}: {
  monde: World | undefined
  /** L'interrupteur général de l'ambiance (Options › Ambiance). */
  ambianceActive: boolean
  /** L'état courant de l'aperçu. Voir ApercuMeteo : ses trois états comptent. */
  apercu: ApercuMeteo
  reglerApercu: (valeur: ApercuMeteo) => void
  /** Prévenu quand la case « ne plus me montrer ça » gèle la réponse. Le
   *  panneau Options affiche ce réglage : sans ce signal il montrerait une
   *  valeur périmée jusqu'au rechargement de la page. */
  onReponseFigee?: (valeur: ReponseAmbiance) => void
}) {
  /** La carte sur laquelle porte la question ouverte, ou rien. */
  const [demande, setDemande] = useState<CarteAmbiance | undefined>(undefined)
  /** La question a déjà été traitée pour CETTE partie. Un scénario Mojoverse
   *  enchaîne les décors : une modale par carte serait insupportable. */
  const [traite, setTraite] = useState(false)
  const [nePlusDemander, setNePlusDemander] = useState(false)

  useEffect(() => {
    if (traite) return
    // L'interrupteur général coupé, c'est déjà une décision : lui demander
    // s'il veut une ambiance serait absurde.
    if (!ambianceActive) return
    // Auto SEULEMENT. `[]` (Aucun) et une liste choisie sont des décisions du
    // joueur ; on ne redemande pas ce qu'il a déjà tranché.
    if (apercu !== undefined) return
    const carte = premiereCarteAmbiance(monde)
    if (!carte) return

    const reponse = lireReponseAmbiance()
    if (reponse === 'toujours') {
      // Rien à forcer : le mode Auto allume déjà ce que les cartes dictent.
      setTraite(true)
      return
    }
    if (reponse === 'jamais') {
      // Le refus a été gelé : il vaut pour toutes les parties, pas seulement
      // pour celle où la case a été cochée.
      setTraite(true)
      reglerApercu([])
      return
    }
    // Une modale de plus par-dessus une leçon serait du bruit. On ne marque
    // pas la question traitée : elle reviendra pour une partie normale.
    if (enModeDecouverte()) return

    setTraite(true)
    setDemande(carte)
  }, [monde, ambianceActive, apercu, reglerApercu, traite])

  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »).
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(demande ? demande.nom : 'aucune')

  if (!demande) return null

  function repondre(garder: boolean) {
    if (nePlusDemander) {
      const figee: ReponseAmbiance = garder ? 'toujours' : 'jamais'
      ecrireReponseAmbiance(figee)
      onReponseFigee?.(figee)
    }
    // `[]` et non `undefined` : seul l'état « Aucun » impose le vide quand une
    // carte voudrait allumer quelque chose. Refuser vaut pour TOUTE la partie,
    // pas seulement pour la carte qui a posé la question.
    if (!garder) reglerApercu([])
    setDemande(undefined)
  }

  return createPortal(
    <div className="ambiance-voile">
      <section
        className="ambiance-modale"
        role="alertdialog"
        aria-modal="true"
        aria-label={t('Une ambiance s’allume')}
        style={transformDecalage(decalage)}
      >
        <div
          className="poignee-glisser"
          onPointerDown={gestesGlisser.onPointerDown}
          onPointerMove={gestesGlisser.onPointerMove}
          onPointerUp={gestesGlisser.onPointerUp}
          onPointerCancel={gestesGlisser.onPointerCancel}
        >
          <span className="plateau-eyebrow">{t('Une ambiance s’allume')}</span>
          <strong className="ambiance-carte">{demande.nom}</strong>
        </div>
        <p className="ambiance-effet">
          {t('change l’atmosphère du plateau')} :{' '}
          <em>{t(LIBELLE_EFFET[demande.effet])}</em>
        </p>
        <p className="ambiance-texte">
          {t(
            'Tu peux la garder, la couper, ou en choisir une autre à tout moment dans Options › Aperçu d’ambiance.'
          )}
        </p>
        <label className="ambiance-case">
          <input
            type="checkbox"
            checked={nePlusDemander}
            onChange={(evenement) => setNePlusDemander(evenement.target.checked)}
          />
          {t('Ne plus me montrer ça')}
        </label>
        <div className="ambiance-boutons">
          <button type="button" className="ambiance-non" onClick={() => repondre(false)}>
            {t('Non, couper')}
          </button>
          <button type="button" className="ambiance-oui" onClick={() => repondre(true)}>
            {t('Oui, garder')}
          </button>
        </div>
      </section>
    </div>,
    document.body
  )
}

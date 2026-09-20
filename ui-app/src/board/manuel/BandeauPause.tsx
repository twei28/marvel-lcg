// BandeauPause.tsx — la pause manuelle EN COURS DE PARTIE (tâche 3).
//
// Une table ordinaire (mode_manuel = faux) qui rencontre un bug se met en
// PAUSE (route `POST /manuel_pause`, `triche.basculerPause`) : le moteur se
// tait le temps qu'on corrige à la main, exactement comme le fait le mode
// manuel DÉCLARÉ (`leMoteurSeTait`), mais sans en avoir la nature — voir
// `mode.ts`, `estEnPause`, pour la distinction.
//
// ⚠ CE BANDEAU EST EXEMPTÉ DU MASQUAGE (ruling du plan, 20/09/2026) : il est
// le SEUL moyen de reprendre la partie. Le masquer avec le reste des couches
// du moteur (bandeau de phase, assistant, barre d'actions...) rendrait la
// pause définitive. `board.tsx` doit donc le monter INCONDITIONNELLEMENT,
// jamais derrière la même garde que `bh-fin-tour` ou consorts.
//
// Sur une table EN LIGNE, chaque joueur voit sa propre partie s'arrêter sans
// prévenir : sans dire QUI a posé la pause et DEPUIS QUAND, les autres
// croient à une panne. C'est le cœur de la tâche — voir `enPause.par` /
// `enPause.depuis`, posés côté moteur par `World.BasculerPauseManuelle`
// (`Scene.pause_par` / `Scene.pause_a`, effacés à la reprise).
import { useEffect, useState } from 'react'
import { t } from '../langue'
import type { ResultatPasser } from '../triche'

/** L'état de la pause EN COURS, tel que la trame le publie. */
export type InfoPause = {
  /** Faux hors pause : le bandeau ne s'affiche alors pas. */
  actif: boolean
  /** Pseudo de qui a posé la pause. Vide = aucun pseudo n'a voyagé. */
  par: string
  /** Horodatage tel que le moteur l'a formaté (`Scene.pause_a`). Vide = tu. */
  depuis: string
}

/**
 * La phrase à montrer pour un refus de `POST /manuel_passer`, par CODE
 * STABLE (jamais une phrase venue du serveur -- même convention que
 * `raisons-refus.ts`/`failure_reason`, `Controller.NormaliserLeMotif` côté
 * moteur : le moteur ne parle pas la langue du joueur, c'est le plateau qui
 * écrit la phrase et `t()` qui la rend en anglais).
 *
 * ⚠ Fonction, pas une table figée au niveau du module : `t()` ne doit
 * s'évaluer qu'à l'usage (au clic), jamais au chargement du fichier.
 */
function motifDuRefus(code: string): string {
  if (code === 'aucune_question') {
    return t('Le moteur n’attend aucune réponse en ce moment')
  }
  if (code === 'question_forcee') {
    return t('Cette question exige une réponse : le jeu n’offre aucune sortie')
  }
  if (code === 'reseau') {
    return t('La requête n’est pas partie : vérifie ta connexion')
  }
  return t('Le moteur a refusé de passer cette question')
}

export type BandeauPauseProps = {
  enPause: InfoPause
  /** Reprend la partie (`POST /manuel_pause` avec `actif: false`). */
  onReprendre: () => void
  /**
   * Tente de passer la question fautive du moteur (tâche 5, échappatoire de
   * dernier recours) : `POST /manuel_passer`. Rend `{ ok: true }` quand le
   * moteur a vraiment passé la question courante, ou `{ ok: false, code }`
   * quand il a refusé -- `code` est affiché via `motifDuRefus` ci-dessus,
   * jamais tel quel : c'est un identifiant stable, pas une phrase.
   */
  onPasser: () => Promise<ResultatPasser>
  /**
   * Ce plateau REGARDE la table sans y être assis (I2, revue finale du
   * 20/09/2026) : le bandeau s'affiche toujours — sinon la partie s'arrête
   * sous les yeux du spectateur sans un mot, et passe pour cassée — mais
   * SANS aucun de ses deux boutons.
   *
   * ⚠ CE N'EST PAS LA GARANTIE, ce n'en est que la politesse : le moteur
   * refuse les routes `POST /manuel_pause` et `/manuel_passer` à un
   * spectateur (`SpectateurPeutEcrire`, `web_server.py`, plus la garde de
   * siège de chaque route). Ce que la garde d'écran apporte, c'est de ne
   * plus PROMETTRE ce qu'elle ne peut pas tenir — et surtout de ne plus
   * proposer « Passer la question », qui répondrait à la place d'un joueur
   * assis. Ce bandeau est monté HORS de `.board-actions`, la seule chose
   * que la CSS du spectateur masque : il n'était couvert par rien.
   */
  lectureSeule?: boolean
}

export function BandeauPause({
  enPause,
  onReprendre,
  onPasser,
  lectureSeule = false,
}: BandeauPauseProps) {
  // ⚠ AVANT le retour anticipé ci-dessous : les Hooks ne peuvent jamais être
  // conditionnels (règle de React), même quand le bandeau ne s'affiche pas.
  const [motifRefus, setMotifRefus] = useState<string | undefined>(undefined)

  // Le motif meurt avec la pause qui l'a produit (revue finale, 20/09/2026).
  // Ce composant reste MONTÉ hors pause (il ne fait que rendre `null`), donc
  // son état survivait à la reprise : un refus affiché lors d'une pause
  // réapparaissait tel quel à la pause suivante, longtemps après, sur une
  // question qui n'avait rien à voir avec lui.
  useEffect(() => {
    if (!enPause.actif) setMotifRefus(undefined)
  }, [enPause.actif])

  if (!enPause.actif) return null

  const qui = enPause.par || t('Quelqu’un')

  async function passer(): Promise<void> {
    setMotifRefus(undefined)
    const resultat = await onPasser()
    if (!resultat.ok) setMotifRefus(motifDuRefus(resultat.code))
  }

  return (
    <div className="bandeau-pause" role="alert">
      <span className="bandeau-pause-titre">
        <span aria-hidden="true">⏸</span> {t('Partie en pause')}
      </span>
      <span className="bandeau-pause-texte">
        {qui} {t('a mis la partie en pause')}
        {enPause.depuis ? ` ${t('depuis')} ${enPause.depuis}` : ''}
      </span>
      {/* Aucun bouton pour qui ne fait que regarder : voir `lectureSeule`. */}
      {lectureSeule ? null : (
        <span className="bandeau-pause-boutons">
          <button type="button" className="bandeau-pause-passer" onClick={() => { void passer() }}>
            {t('Passer la question')}
          </button>
          <button type="button" className="bandeau-pause-reprendre" onClick={onReprendre}>
            {t('Reprendre')}
          </button>
        </span>
      )}
      {/* Le refus DOIT se voir : sans lui, un joueur qui clique « Passer »
          sur une question forcée croirait le bouton cassé, alors que c'est
          le moteur qui exige une vraie réponse (voir motifDuRefus). */}
      {motifRefus ? <span className="bandeau-pause-refus">{motifRefus}</span> : null}
    </div>
  )
}

// CoucheCoach — le mode Découverte : une mission à la fois, par-dessus la table.
//
// Ne bloque JAMAIS rien : `pointer-events: none` sauf sur ses propres boutons,
// même règle que SplashTour. Un panneau qui avale les clics coûte plus cher
// qu'il ne rapporte, et un tutoriel qui empêche de jouer est un tutoriel qui
// se coince. Le coach observe l'état du monde, il n'agit sur rien.
//
// Ne s'affiche QUE si localStorage `marvel-board-tutoriel` existe et vaut autre
// chose que 'fini'.
//
// Cette clé est un état GLOBAL : rien ici ne la rattache à la partie qui l'a
// posée, et le plateau n'a aucun moyen de savoir s'il est bien la partie du
// tutoriel. C'est donc au wizard de garantir l'exclusivité, et il le fait en
// DÉSARMANT à chaque retour à la préparation (public/js/prepare/tutoriel-etat.js,
// appelé par app.js au chargement et par launcher.js au lancement). Sans ce
// désarmement, un tutoriel abandonné en cours de route laissait la clé sur le
// nom d'une leçon et le coach revenait sur toutes les parties suivantes.
// Règle vérifiée par `node outils/verifier-tutoriel-etat.mjs`.

import { useEffect, useRef, useState } from 'react'
import { LECONS, prendreRepere, type Repere } from './lecons'
import { t } from './langue'
import type { World } from './world'

export const CLE_TUTORIEL = 'marvel-board-tutoriel'

/** Identifiant de la première leçon. Le wizard écrit cette valeur au lancement.
 *  À changer EN MÊME TEMPS que la valeur en dur de public/js/prepare/launcher.js. */
export const PREMIERE_LECON = 'mulligan'

export function lireLeconCourante(): string | null {
  try {
    return window.localStorage.getItem(CLE_TUTORIEL)
  } catch {
    return null
  }
}

function ecrireLeconCourante(valeur: string): void {
  try {
    window.localStorage.setItem(CLE_TUTORIEL, valeur)
  } catch {
    /* stockage indisponible : le tutoriel reste jouable, sans reprise */
  }
}

export function CoucheCoach({ monde }: { monde?: World }) {
  const [idLecon, setIdLecon] = useState<string | null>(() => lireLeconCourante())
  const [replie, setReplie] = useState(false)
  const [felicite, setFelicite] = useState(false)
  const repere = useRef<Repere | null>(null)
  const leconDuRepere = useRef<string | null>(null)

  const index = LECONS.findIndex((lecon) => lecon.id === idLecon)
  const lecon = index >= 0 ? LECONS[index] : undefined

  // Le repère est pris À L'ENTRÉE dans la leçon : c'est lui qui permet de
  // mesurer une VARIATION (« Rhino a encore perdu des PV »), impossible à voir
  // sur le seul état courant. On ne le reprend pas à chaque rendu, sans quoi
  // la variation serait toujours nulle.
  if (monde && lecon && leconDuRepere.current !== lecon.id) {
    repere.current = prendreRepere(monde)
    leconDuRepere.current = lecon.id
  }

  function avancer() {
    const suivante = LECONS[index + 1]
    setFelicite(true)
    const prochaine = suivante ? suivante.id : 'fini'
    setIdLecon(prochaine)
    ecrireLeconCourante(prochaine)
  }

  // La félicitation s'efface toute seule.
  useEffect(() => {
    if (!felicite) return
    const minuteur = window.setTimeout(() => setFelicite(false), 1800)
    return () => window.clearTimeout(minuteur)
  }, [felicite])

  // Détection à chaque rendu du monde : une leçon accomplie en avance est
  // validée dès qu'on y entre.
  useEffect(() => {
    if (!monde || !lecon || lecon.manuelle || !repere.current) return
    if (lecon.accomplie(monde, repere.current)) avancer()
  })

  if (!lecon) return null

  if (replie) {
    return (
      <aside className="coach coach-replie">
        <button type="button" onClick={() => setReplie(false)}>
          {t('Coach')} · {index + 1}/{LECONS.length}
        </button>
      </aside>
    )
  }

  return (
    <aside className="coach" aria-live="polite">
      <span className="coach-eyebrow">
        {t('Leçon')} {index + 1}/{LECONS.length}
      </span>
      <strong>{lecon.titre}</strong>
      <p>{lecon.texte}</p>
      {felicite ? <span className="coach-bravo">{t('Bien joué !')}</span> : null}
      <div className="coach-boutons">
        <button type="button" onClick={() => setReplie(true)}>{t('Replier')}</button>
        <button type="button" onClick={avancer}>
          {lecon.manuelle ? t('J’ai compris') : t('Passer cette leçon')}
        </button>
        <button
          type="button"
          className="coach-quitter"
          onClick={() => { setIdLecon('fini'); ecrireLeconCourante('fini') }}
        >
          {t('Quitter le tutoriel')}
        </button>
      </div>
    </aside>
  )
}

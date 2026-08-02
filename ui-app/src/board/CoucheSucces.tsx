// CoucheSucces — bannière des succès du moteur (« Achievement: ... »).
//
// Le moteur enregistre des exploits (game/rule/achievement.py) et les notifie
// dans la narration sous la forme « Achievement: FIRST_BLOOD ». Cette couche
// les repère dans les textes du monde et les présente en bannière quelques
// secondes. Activable au choix (localStorage marvel-board-succes, actif par
// défaut) ; les compteurs cumulés restent visibles dans l'écran Stats du wizard.
import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import type { World } from './world'
import type { Demande } from './ask'

export const CLE_SUCCES = 'marvel-board-succes'

export function lireSuccesActifs(): boolean {
  try {
    return window.localStorage.getItem(CLE_SUCCES) !== 'off'
  } catch {
    return true
  }
}

const NOMS: Record<string, string> = {
  FIRST_BLOOD: 'Premier sang',
  DOUBLE_KILL: 'Double K.O.',
  TRIPLE_KILL: 'Triple K.O.',
  ULTRA_KILL: 'Quadruple K.O.',
  RAMPAGE: 'Déchaînement',
}

const DUREE_BANNIERE = 4000

export function CoucheSucces({
  monde,
  demande,
  actif,
}: {
  monde: World | undefined
  demande: Demande | undefined
  actif: boolean
}) {
  const [banniere, setBanniere] = useState<string | undefined>(undefined)
  const vus = useRef(new Set<string>())
  const minuteur = useRef<number | undefined>(undefined)

  useEffect(() => {
    if (!actif || !monde) return
    const textes = [monde.prompt, monde.prompt_last_text, demande?.prompt_text]
    for (const texte of textes) {
      const trouve = typeof texte === 'string' ? texte.match(/Achievement:\s*([A-Z_]+)/) : null
      if (!trouve) continue
      const cle = `${monde.round_id}:${trouve[1]}`
      if (vus.current.has(cle)) continue
      vus.current.add(cle)
      const nom = NOMS[trouve[1]] ? t(NOMS[trouve[1]]) : trouve[1]
      setBanniere(nom)
      if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
      minuteur.current = window.setTimeout(() => setBanniere(undefined), DUREE_BANNIERE)
    }
  }, [actif, monde, monde?.render_id, demande?.prompt_text])

  useEffect(
    () => () => {
      if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
    },
    [],
  )

  if (!actif || !banniere) return null
  return (
    <div className="banniere-succes" role="status">
      <span aria-hidden="true">{'\u{1F3C6}'}</span>
      <span className="banniere-succes-eyebrow">{t('Succès')}</span>
      <strong>{banniere}</strong>
    </div>
  )
}

// VISITE GUIDEE en 5 etapes (decision Q57, 24/10/2026), a la premiere partie en ronds : chaque etape eclaire un morceau de
// l'ecran et dit ce qu'on peut y faire. « Passer » la ferme pour de bon ; elle ne revient plus (localStorage).
import { useEffect, useLayoutEffect, useMemo, useState, type ReactElement } from 'react'
import { t } from '../../langue'

export const CLE_VISITE_RONDS = 'marvel-tel-visite-ronds'

export type EtapeVisite = { cible: string; titre: string; texte: string }

/** Les 5 etapes : les ronds, la main, la phase, le glisser, le menu. */
export function etapesDeLaVisite(): EtapeVisite[] {
  return [
    { cible: '.table-ronds', titre: t('Les ronds'), texte: t('Chaque carte en jeu est un rond. Touche-le pour voir la carte en grand et agir. Maintiens le doigt pour un simple aperçu.') },
    { cible: '.main-dock', titre: t('Ta main'), texte: t('Tes cartes sont sous la table. Fais-les défiler de côté ; glisse une carte vers le haut, sur sa cible, pour la jouer.') },
    { cible: '.portrait-bandeau', titre: t('La phase'), texte: t('Le bandeau du haut dit où en est le tour. « Fin du tour » le termine ; la flèche ↶ annule ton dernier geste.') },
    { cible: '.rond[data-kind="hero"], .rond[data-kind="alter-ego"]', titre: t('Glisser'), texte: t('Glisse ton héros (en forme héros) sur un ennemi pour attaquer, sur une manigance pour la déjouer. Les cibles s’allument en jaune.') },
    { cible: '.portrait-menu-bouton', titre: t('Le menu'), texte: t('Le bouton « … » ouvre les outils, les réglages et l’aide.') },
  ]
}

export function visiteDejaVue(): boolean {
  try {
    return window.localStorage.getItem(CLE_VISITE_RONDS) === 'oui'
  } catch {
    return false
  }
}

function marquerVue(): void {
  try {
    window.localStorage.setItem(CLE_VISITE_RONDS, 'oui')
  } catch {
    // Navigation privee : la visite reviendra, sans gravite.
  }
}

export function VisiteGuidee({ actif, onFin }: { actif: boolean; onFin?: () => void }): ReactElement | null {
  const [ouverte, setOuverte] = useState(false)
  const [rang, setRang] = useState(0)
  const [cadre, setCadre] = useState<{ x: number; y: number; w: number; h: number } | undefined>()
  // Elle s'ouvre une seule fois, quand le jeu est pret (`actif`) et que le joueur ne l'a jamais vue.
  useEffect(() => {
    if (actif && !visiteDejaVue()) setOuverte(true)
  }, [actif])
  const etapes = useMemo(() => etapesDeLaVisite(), [])
  const etape = etapes[rang]
  useLayoutEffect(() => {
    if (!ouverte || !etape) return
    const el = document.querySelector(etape.cible)
    const r = el?.getBoundingClientRect()
    setCadre(r && r.width > 0 ? { x: r.left, y: r.top, w: r.width, h: Math.min(r.height, window.innerHeight - r.top) } : undefined)
  }, [ouverte, etape])  // `etapes` est memorisee : `etape` ne change qu'avec `rang`
  if (!ouverte || !etape) return null
  const fermer = () => {
    marquerVue()
    setOuverte(false)
    onFin?.()
  }
  const enHaut = cadre ? cadre.y + cadre.h / 2 > window.innerHeight / 2 : false
  return (
    <div className="visite" role="dialog" aria-label={t('Visite guidée')}>
      {cadre ? <span className="visite-halo" style={{ left: cadre.x, top: cadre.y, width: cadre.w, height: cadre.h }} /> : null}
      <section className={`visite-bulle${enHaut ? ' est-en-haut' : ''}`}>
        <p className="visite-compte">
          {rang + 1} / {etapes.length}
        </p>
        <h2>{etape.titre}</h2>
        <p>{etape.texte}</p>
        <div className="visite-boutons">
          <button type="button" className="visite-passer" onClick={fermer}>
            {t('Passer')}
          </button>
          <button type="button" className="visite-suivant" onClick={() => (rang + 1 < etapes.length ? setRang(rang + 1) : fermer())}>
            {rang + 1 < etapes.length ? t('Suivant') : t('Terminer')}
          </button>
        </div>
      </section>
    </div>
  )
}

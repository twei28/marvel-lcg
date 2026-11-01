// VISITE GUIDEE en 6 etapes (decision Q57, 24/10/2026 ; 6e etape ajoutee le 26/10/2026), a la premiere partie en ronds : chaque
// etape eclaire un morceau de l'ecran et dit ce qu'on peut y faire. UNE SEULE FOIS (decision du 24/10/2026) : « Passer » ou
// « Terminer » coupe le reglage `aideDebut` ; Reglages > « Aide au debut de la partie » la remet pour la partie suivante.
//
// NOUVEAUTE (26/10/2026) : la 6e etape explique les cartes empilees (contour pointille dore + pastille « Pile de cartes : N »).
// Un joueur qui a DEJA vu la visite (`aideDebut` coupe) ne la revoit pas en entier : il ne voit que cette etape, une seule fois
// (`visitePiles` : « Compris » la coupe). Un joueur qui fait la visite complete la voit au passage et la coupe aussi.
import { useEffect, useLayoutEffect, useMemo, useState, type ReactElement } from 'react'
import { t } from '../../langue'
import { libelleEmpilees } from '../../empilees'
import { ecrireReglageTelephone, lireReglagesTelephone } from '../reglages-telephone'

export type EtapeVisite = { cible: string; titre: string; texte: string; exemple?: 'pile' }

/** Les 6 etapes : les ronds, la main, la phase, le glisser, le menu, les cartes empilees. */
export function etapesDeLaVisite(): EtapeVisite[] {
  return [
    { cible: '.table-ronds', titre: t('Les ronds'), texte: t('Chaque carte en jeu est un rond. Touche-le pour voir la carte en grand et agir.') },
    { cible: '.main-dock', titre: t('Ta main'), texte: t('Tes cartes sont sous la table. Fais-les défiler de côté ; glisse une carte vers le haut, sur sa cible, pour la jouer.') },
    { cible: '.portrait-bandeau', titre: t('La phase'), texte: t('Le bandeau du haut dit où en est le tour. « Fin du tour » le termine ; la flèche ↶ annule ton dernier geste.') },
    { cible: '.rond[data-kind="hero"], .rond[data-kind="alter-ego"]', titre: t('Glisser'), texte: t('Glisse ton héros (en forme héros) sur un ennemi pour attaquer, sur une manigance pour la déjouer. Les cibles s’allument en jaune.') },
    { cible: '.portrait-menu-bouton', titre: t('Le menu'), texte: t('Le bouton « … » ouvre les outils, les réglages et l’aide.') },
    ETAPE_PILES(),
  ]
}

/** La nouveaute du 26/10/2026 : les cartes posees sous une autre (State of Flow, cartes glissees sous Corsair ou Havok). */
function ETAPE_PILES(): EtapeVisite {
  return {
    cible: '.rond-mini.est-empilee',
    titre: t('Cartes empilées'),
    texte: t('Une carte posée sous une autre forme une pile : contour en pointillés dorés et pastille « Pile de cartes : N ». Ce n’est pas une amélioration, et un événement empilé n’est pas resté en jeu par erreur. Touche-la pour la lire.'),
    exemple: 'pile',
  }
}

/** Mini-illustration de la 6e etape : un rond porteur, une carte empilee (contour pointille dore) et la pastille. */
function ExemplePile(): ReactElement {
  return (
    <div className="visite-pile-exemple" aria-hidden="true">
      <span className="visite-pile-porteur" />
      <span className="visite-pile-mini est-empilee" />
      <span className="pile-sous-carte">{libelleEmpilees(2)}</span>
    </div>
  )
}

export function VisiteGuidee({ actif, onFin }: { actif: boolean; onFin?: () => void }): ReactElement | null {
  const [ouverte, setOuverte] = useState(false)
  // « complete » : la visite en 6 etapes (premiere fois, ou relancee par les reglages) ; « nouveaute » : la seule 6e etape, pour
  // celui qui a deja fait la visite avant le 26/10/2026.
  const [mode, setMode] = useState<'complete' | 'nouveaute'>('complete')
  const [rang, setRang] = useState(0)
  const [cadre, setCadre] = useState<{ x: number; y: number; w: number; h: number } | undefined>()
  // Elle s'ouvre une seule fois, quand le jeu est pret (`actif`) et que le joueur ne l'a jamais vue.
  useEffect(() => {
    if (!actif) return
    const reglages = lireReglagesTelephone()
    if (reglages.aideDebut) {
      setMode('complete')
      setOuverte(true)
    } else if (reglages.visitePiles) {
      setMode('nouveaute')
      setOuverte(true)
    }
  }, [actif])
  const etapes = useMemo(() => (mode === 'nouveaute' ? [ETAPE_PILES()] : etapesDeLaVisite()), [mode])
  const etape = etapes[rang]
  useLayoutEffect(() => {
    if (!ouverte || !etape) return
    const el = document.querySelector(etape.cible)
    const r = el?.getBoundingClientRect()
    setCadre(r && r.width > 0 ? { x: r.left, y: r.top, w: r.width, h: Math.min(r.height, window.innerHeight - r.top) } : undefined)
  }, [ouverte, etape])  // `etapes` est memorisee : `etape` ne change qu'avec `rang`
  if (!ouverte || !etape) return null
  const fermer = () => {
    // La visite complete a montre la nouveaute au passage : les deux se coupent. La nouveaute seule ne touche pas `aideDebut`.
    if (mode === 'complete') ecrireReglageTelephone('aideDebut', false)
    ecrireReglageTelephone('visitePiles', false)
    setOuverte(false)
    onFin?.()
  }
  const enHaut = cadre ? cadre.y + cadre.h / 2 > window.innerHeight / 2 : false
  return (
    <div className="visite" role="dialog" aria-label={t('Visite guidée')}>
      {cadre ? <span className="visite-halo" style={{ left: cadre.x, top: cadre.y, width: cadre.w, height: cadre.h }} /> : null}
      <section className={`visite-bulle${enHaut ? ' est-en-haut' : ''}`}>
        <p className="visite-compte">{mode === 'nouveaute' ? t('Nouveauté') : `${rang + 1} / ${etapes.length}`}</p>
        <h2>{etape.titre}</h2>
        <p>{etape.texte}</p>
        {etape.exemple === 'pile' ? <ExemplePile /> : null}
        <div className="visite-boutons">
          {mode === 'nouveaute' ? null : (
            <button type="button" className="visite-passer" onClick={() => fermer()}>
              {t('Passer')}
            </button>
          )}
          <button
            type="button"
            className="visite-suivant"
            onClick={() => (rang + 1 < etapes.length ? setRang(rang + 1) : fermer())}
          >
            {mode === 'nouveaute' ? t('Compris') : rang + 1 < etapes.length ? t('Suivant') : t('Terminer')}
          </button>
        </div>
      </section>
    </div>
  )
}

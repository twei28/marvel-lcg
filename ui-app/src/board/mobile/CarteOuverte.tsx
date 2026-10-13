// La carte ouverte EN GRAND, au milieu de l'ecran : le geste de lecture du
// telephone (tap). Avec ses attachees et ses statuts en dessous (spec du
// 12/09/2026 : « lisible, avec ses attachements ») : un tap sur l'une d'elles
// l'ouvre a son tour.
//
// Trois sorties sans rien engager : tap sur le voile, Fermer, Retour Android
// (`.carte-ouverte-voile` est dans FERMABLES). L'action du moteur, quand il
// y en a une, vit dans le maintien et dans le bouton du dessous.
//
// Retours de Raven (iPhone, 12/10/2026) :
// - une carte de la MAIN ouverte en grand se change d'un glisser du doigt,
//   a gauche ou a droite, vers sa voisine de main (`voisines`) ;
// - une carte a plusieurs faces (heros / alter ego) montre son autre face
//   d'un bouton, sans changer de forme en jeu ;
// - elle passe AU-DESSUS de la fenetre du mulligan : elle est montee dans
//   <body>. Dans `.plateau-portrait` (position fixed, donc son propre
//   contexte d'empilement), son z-index de 650 ne valait qu'a l'interieur du
//   plateau, et l'assistant (541, dans <body>) la recouvrait.
import { useRef, useState, type PointerEvent as ReactPointerEvent } from 'react'
import { createPortal } from 'react-dom'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import { useAppuiLong } from './useAppuiLong'
import './portrait.css'

/** Distance horizontale d'un glisser qui change de carte. */
export const SEUIL_GLISSER_CARTE = 50

/** Au-dela, le doigt glisse : ce n'est plus un maintien. */
const SEUIL_MOUVEMENT = 10

export function CarteOuverte({
  carte,
  attachees = [],
  onOuvrirAttachee,
  onFermer,
  libelleAction,
  voisines,
}: {
  carte: ScanCardProps
  attachees?: ScanCardProps[]
  onOuvrirAttachee?: (carte: ScanCardProps) => void
  onFermer: () => void
  /** Le libelle du bouton d'action : « Jouer » pour une carte de la main. */
  libelleAction?: string
  /** Les cartes voisines (la main) : un glisser horizontal passe de l'une a l'autre. */
  voisines?: {
    position: number
    total: number
    precedente?: () => void
    suivante?: () => void
  }
}) {
  const appui = useAppuiLong(
    carte.onSelect
      ? () => {
          carte.onSelect?.()
          onFermer()
        }
      : undefined
  )
  // L'autre face : 0 = la face en jeu, 1.. = les autres (Ant-Man en a deux).
  const autresFaces = carte.autresFaces ?? []
  const [face, setFace] = useState(0)
  const faceMontree = face > 0 ? autresFaces[face - 1] : undefined
  // Statuts (Tough, Stunned...) d'abord, en petit, puis les ameliorations.
  const statuts = attachees.filter((a) => a.kind === 'status')
  const ameliorations = attachees.filter((a) => a.kind !== 'status')

  const depart = useRef<{ x: number; y: number } | undefined>(undefined)
  const surDebut = (evenement: ReactPointerEvent) => {
    evenement.stopPropagation()
    depart.current = { x: evenement.clientX, y: evenement.clientY }
  }
  const surMouvement = (evenement: ReactPointerEvent) => {
    if (!depart.current) return
    const dx = evenement.clientX - depart.current.x
    const dy = evenement.clientY - depart.current.y
    // Un doigt qui glisse ne MAINTIENT pas : sans cela, un glisser lent
    // jouait la carte au bout de 450 ms.
    if (Math.abs(dx) > SEUIL_MOUVEMENT || Math.abs(dy) > SEUIL_MOUVEMENT) appui.gestes.onPointerCancel()
  }
  const surFin = (evenement: ReactPointerEvent) => {
    const debut = depart.current
    depart.current = undefined
    if (!debut || !voisines) return
    const dx = evenement.clientX - debut.x
    const dy = evenement.clientY - debut.y
    if (!Number.isFinite(dx) || !Number.isFinite(dy)) return
    if (Math.abs(dx) < SEUIL_GLISSER_CARTE || Math.abs(dx) < Math.abs(dy) * 1.5) return
    // Le doigt part vers la GAUCHE : la carte suivante arrive de la droite.
    if (dx < 0) voisines.suivante?.()
    else voisines.precedente?.()
  }

  return createPortal(
    <div className="carte-ouverte-voile" onPointerDown={onFermer}>
      <section
        className="carte-ouverte"
        role="dialog"
        aria-label={carte.name}
        onPointerDown={surDebut}
        onPointerMove={surMouvement}
        onPointerUp={surFin}
        onPointerCancel={() => {
          depart.current = undefined
        }}
      >
        <div className={`carte-ouverte-scan${faceMontree ? ' est-autre-face' : ''}`} {...appui.gestes}>
          {/* Sans onSelect, ScanCard ne rend pas de bouton : la carte est ici
              une image à lire, l'action vit dans le maintien et dans le
              bandeau du dessous. */}
          {/* Le scan COMPLET, pas la vignette de la table : agrandie a
              320 px sur un ecran 3x, la vignette etait floue (zone 3). */}
          {faceMontree ? (
            <ScanCard
              {...carte}
              imageUrl={faceMontree.url}
              isLandscape={faceMontree.isLandscape ?? carte.isLandscape}
              stats={undefined}
              allyHp={undefined}
              schemeThreat={undefined}
              exhausted={false}
              onSelect={undefined}
              highlight={false}
              taille="grande"
            />
          ) : (
            <ScanCard {...carte} onSelect={undefined} taille="grande" />
          )}
        </div>

        {carte.onSelect && !faceMontree ? (
          <span className="carte-ouverte-aide">{t('Maintenir pour utiliser')}</span>
        ) : null}

        {voisines && voisines.total > 1 ? (
          <div className="carte-ouverte-voisines">
            <button
              type="button"
              className="carte-ouverte-voisine"
              aria-label={t('Carte précédente')}
              disabled={!voisines.precedente}
              onClick={() => voisines.precedente?.()}
            >
              ‹
            </button>
            <span className="carte-ouverte-position">
              {voisines.position} / {voisines.total}
            </span>
            <button
              type="button"
              className="carte-ouverte-voisine"
              aria-label={t('Carte suivante')}
              disabled={!voisines.suivante}
              onClick={() => voisines.suivante?.()}
            >
              ›
            </button>
          </div>
        ) : null}

        {attachees.length > 0 ? (
          <div className="carte-ouverte-attachees" aria-label={t('Attachées')}>
            {[...statuts, ...ameliorations].map((attachee) => (
              <button
                type="button"
                className={`carte-ouverte-attachee${attachee.kind === 'status' ? ' est-statut' : ''}`}
                key={attachee.id}
                data-tactile="attachee"
                aria-label={attachee.name}
                onClick={() => onOuvrirAttachee?.(attachee)}
              >
                <ScanCard {...attachee} onSelect={undefined} highlight={false} />
              </button>
            ))}
          </div>
        ) : null}

        <div className="carte-ouverte-actions">
          {autresFaces.length > 0 ? (
            <button
              type="button"
              className="carte-ouverte-face"
              onClick={() => setFace((avant) => (avant + 1) % (autresFaces.length + 1))}
            >
              {face === autresFaces.length ? t('Face en jeu') : t('Autre face')}
            </button>
          ) : null}
          {carte.onSelect ? (
            <button
              type="button"
              className="carte-ouverte-agir"
              onClick={() => {
                carte.onSelect?.()
                onFermer()
              }}
            >
              {libelleAction ?? t('Utiliser cette carte')}
            </button>
          ) : null}
          <button type="button" className="carte-ouverte-fermer" onClick={onFermer}>
            {t('Fermer')}
          </button>
        </div>
      </section>
    </div>,
    document.body
  )
}

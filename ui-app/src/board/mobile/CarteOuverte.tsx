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
import { useEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from 'react'
import { createPortal } from 'react-dom'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import { PastillesTraits } from '../PastillesTraits'
import { typeDeBoite, useSurcoucheTraduction } from '../traduction-carte'
import { useAppuiLong } from './useAppuiLong'
import { FeuilleDetail } from './ronds/FeuilleDetail'
import './portrait.css'

/** Distance horizontale d'un glisser qui change de carte. */
export const SEUIL_GLISSER_CARTE = 50

/** Au-dela, le doigt glisse : ce n'est plus un maintien. */
const SEUIL_MOUVEMENT = 10

/**
 * Un ScanCard qui porte, posés dessus, le voile (traduction ou ERRATA officiel) et la pastille « Errata » : les mêmes que sur
 * ordinateur (traduction-carte.tsx). `code` : la carte dont c'est la face (celle de CETTE face, pas de la carte ouverte).
 * Sans lui, le téléphone affichait le scan imprimé nu : aucun errata (retour d'un joueur, 09/11/2026).
 */
function ScanCardAvecVoile({ code, type, artAlternatif, ...props }: ScanCardProps & { code?: string; type?: string }) {
  const surcouche = useSurcoucheTraduction({
    codeCarte: code,
    artAlternatif,
    imageUrl: props.imageUrl,
    traits: props.traits,
    paysage: props.isLandscape,
    type: type ?? (props.kind === 'main-scheme' ? 'MainScheme' : props.kind === 'side-scheme' ? 'SideScheme' : undefined),
    facedown: props.facedown,
  })
  return <ScanCard {...props} artAlternatif={artAlternatif} surcouche={props.surcouche ?? surcouche} />
}

export function CarteOuverte({
  carte,
  attachees = [],
  onOuvrirAttachee,
  onFermer,
  libelleAction,
  voisines,
  detail = false,
  apercuSeul = false,
}: {
  carte: ScanCardProps
  attachees?: ScanCardProps[]
  onOuvrirAttachee?: (carte: ScanCardProps) => void
  onFermer: () => void
  /** Le libelle du bouton d'action : « Jouer » pour une carte de la main. */
  libelleAction?: string
  /** Plateau en ronds (Q71, Q72) : PV, valeurs ajustees, jetons sous la carte, et les deux faces COTE A COTE. */
  detail?: boolean
  /** Appui long sur un rond (Q51) : la carte en grand tant que le doigt reste, sans boutons ; elle part au relacher. */
  apercuSeul?: boolean
  /** Les cartes voisines (la main) : un glisser horizontal passe de l'une a l'autre. */
  voisines?: {
    position: number
    total: number
    precedente?: () => void
    suivante?: () => void
  }
}) {
  const [face, setFace] = useState(0)
  const appui = useAppuiLong(
    carte.onSelect
      ? () => {
          // Sur une AUTRE forme que celle en jeu, rien a jouer.
          if (face > 0) return
          carte.onSelect?.()
          onFermer()
        }
      : undefined
  )
  // Un apercu tenu au doigt se ferme des que le doigt se leve.
  useEffect(() => {
    if (!apercuSeul) return
    window.addEventListener('pointerup', onFermer)
    window.addEventListener('pointercancel', onFermer)
    return () => {
      window.removeEventListener('pointerup', onFermer)
      window.removeEventListener('pointercancel', onFermer)
    }
  }, [apercuSeul, onFermer])
  // L'autre face : 0 = la face en jeu, 1.. = les autres (Ant-Man en a deux).
  const autresFaces = carte.autresFaces ?? []
  const faceMontree = face > 0 ? autresFaces[face - 1] : undefined
  // Plusieurs faces en detail (ronds) : UNE carte a la fois, des fleches (et un glisser) pour voir les autres. Les petits
  // ecrans ne tenaient pas deux scans l'un sous l'autre, et certains heros ont plus de deux faces (15/11/2026).
  const nbFaces = 1 + autresFaces.length
  const enCarrousel = !!detail && nbFaces >= 2
  const allerFace = (delta: number) => setFace((avant) => Math.min(nbFaces - 1, Math.max(0, avant + delta)))
  // Les cartes de la main ont leurs voisines ; sinon, en carrousel, le glisser change de face.
  const navigation = voisines
    ? { precedente: voisines.precedente, suivante: voisines.suivante }
    : enCarrousel
      ? { precedente: face > 0 ? () => allerFace(-1) : undefined, suivante: face < nbFaces - 1 ? () => allerFace(1) : undefined }
      : undefined
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
    if (!debut || !navigation) return
    const dx = evenement.clientX - debut.x
    const dy = evenement.clientY - debut.y
    if (!Number.isFinite(dx) || !Number.isFinite(dy)) return
    if (Math.abs(dx) < SEUIL_GLISSER_CARTE || Math.abs(dx) < Math.abs(dy) * 1.5) return
    // Le doigt part vers la GAUCHE : la carte suivante arrive de la droite.
    if (dx < 0) navigation.suivante?.()
    else navigation.precedente?.()
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
        <div
          className={`carte-ouverte-scan${faceMontree ? ' est-autre-face' : ''}${enCarrousel ? ' en-carrousel' : ''}`}
          {...appui.gestes}
        >
          {/* Sans onSelect, ScanCard ne rend pas de bouton : la carte est ici
              une image à lire, l'action vit dans le maintien et dans le
              bandeau du dessous. */}
          {/* Le scan COMPLET, pas la vignette de la table : agrandie a
              320 px sur un ecran 3x, la vignette etait floue (zone 3). */}
          {faceMontree ? (
            <ScanCardAvecVoile
              {...carte}
              code={faceMontree.code}
              artAlternatif={faceMontree.artAlternatif}
              type={typeDeBoite(faceMontree.type)}
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
            <ScanCardAvecVoile
              {...carte}
              code={carte.codeCarte}
              onSelect={undefined}
              taille="grande"
              {...(detail ? { jetonMenace: undefined, jetonDegats: undefined, counters: undefined } : {})}
            />
          )}
          {/* Les traits du heros en ce moment (reglage « Traits du heros ») : le tap est le geste de lecture du telephone. */}
          {!detail && !faceMontree ? <PastillesTraits carte={carte} surGrande /> : null}
          {/* Les fleches POSEES sur la carte (pas en dessous) : une rangee de plus coutait 50 px de hauteur, donc une carte plus petite. */}
          {enCarrousel && !voisines && !apercuSeul ? (
            <>
              <button
                type="button"
                className="carte-ouverte-voisine carte-ouverte-fleche est-gauche"
                aria-label={t('Carte précédente')}
                disabled={face === 0}
                onPointerDown={(evenement) => evenement.stopPropagation()}
                onClick={() => allerFace(-1)}
              >
                ‹
              </button>
              <button
                type="button"
                className="carte-ouverte-voisine carte-ouverte-fleche est-droite"
                aria-label={t('Carte suivante')}
                disabled={face === nbFaces - 1}
                onPointerDown={(evenement) => evenement.stopPropagation()}
                onClick={() => allerFace(1)}
              >
                ›
              </button>
              <span className="carte-ouverte-position carte-ouverte-position-coin">
                {face + 1} / {nbFaces}
              </span>
            </>
          ) : null}
        </div>

        {/* Ronds : les pastilles se lisent SOUS la carte. Cartes : sur la carte (voir plus haut),
            sinon le bandeau d'action du dessous les recouvre. */}
        {detail && !faceMontree ? <PastillesTraits carte={carte} /> : null}

        {detail && !faceMontree ? <FeuilleDetail carte={carte} /> : null}

        {voisines && voisines.total > 1 && !apercuSeul ? (
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

        {apercuSeul ? null : <div className="carte-ouverte-actions">
          {autresFaces.length > 0 && !detail ? (
            <button
              type="button"
              className="carte-ouverte-face"
              onClick={() => setFace((avant) => (avant + 1) % (autresFaces.length + 1))}
            >
              {face === autresFaces.length ? t('Face en jeu') : t('Autre face')}
            </button>
          ) : null}
          {carte.onSelect && !faceMontree ? (
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
        </div>}
      </section>
    </div>,
    document.body
  )
}

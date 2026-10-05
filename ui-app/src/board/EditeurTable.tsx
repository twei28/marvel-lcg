// L'EDITEUR DE LA TABLE (table personnalisable, decisions du 04/10/2026).
//
// Une couche posee DANS la scene du plateau, avec la MEME grille que la table
// (12 x 8, memes ecarts) : une zone ne peut tomber que sur des cases, c'est ce
// qui la rend aimantee. Chaque zone est encadree et porte deux poignees :
//  - « la place » (coin bas-droit) : l'emprise de la zone sur la grille ;
//  - « la taille des cartes » (coin haut-droit) : glisser vers le haut grossit.
// La zone elle-meme se deplace en la faisant glisser. Un deplacement qui ferait
// chevaucher deux zones, sortir de la grille ou passer sous le minimum est
// montre en rouge et refuse (table-briques.ts : deplacer, redimensionner).
//
// La barre (Terminer, Disposition d'origine, Annuler) vit hors de la scene,
// qui est mise a l'echelle : sans cela ses boutons changeraient de taille.

import { useEffect, useRef, useState, type CSSProperties, type PointerEvent as PointerEventReact } from 'react'
import { createPortal } from 'react-dom'
import {
  NOMS,
  ancre,
  changerTaille,
  deplacer,
  deposerBrique,
  estEpinglee,
  minimumDeZone,
  redimensionner,
  titreDeZone,
  zoneDe,
  zoneSousLaCase,
  type CleBrique,
  type Disposition,
  type PlaceZone,
} from './table-briques'
import { t } from './langue'
import './EditeurTable.css'

/** La case (a partir de 1) sous le pointeur, bornee a la grille. */
export function caseSousLePointeur(
  boite: { left: number; top: number; width: number; height: number },
  x: number,
  y: number,
  colonnes: number,
  lignes: number
): { col: number; ligne: number } {
  const borne = (n: number, max: number) => Math.min(max, Math.max(1, n))
  return {
    col: borne(Math.floor(((x - boite.left) / Math.max(1, boite.width)) * colonnes) + 1, colonnes),
    ligne: borne(Math.floor(((y - boite.top) / Math.max(1, boite.height)) * lignes) + 1, lignes),
  }
}

type Geste =
  | { genre: 'deplacer'; zone: CleBrique; depart: { col: number; ligne: number }; origine: PlaceZone }
  | { genre: 'place'; zone: CleBrique }
  | { genre: 'taille'; zone: CleBrique; y: number; taille: number }
  | { genre: 'brique'; zone: CleBrique; brique: CleBrique }

const grille = (p: PlaceZone): CSSProperties => ({
  gridColumn: `${p.col} / span ${p.largeur}`,
  gridRow: `${p.ligne} / span ${p.hauteur}`,
})

export function EditeurTable({
  disposition,
  changer,
  terminer,
  origine,
  annuler,
}: {
  /** La disposition en cours d'edition (grille 12 x 8), dessinee en direct. */
  disposition: Disposition
  changer: (d: Disposition) => void
  terminer: () => void
  origine: () => void
  annuler: () => void
}) {
  const couche = useRef<HTMLDivElement>(null)
  const [geste, setGeste] = useState<Geste>()
  // Ce que le geste en cours donnerait : la nouvelle disposition, ou un refus.
  const [fantome, setFantome] = useState<{ place: PlaceZone; refuse: boolean }>()

  useEffect(() => {
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') annuler()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [annuler])

  const caseDe = (e: PointerEventReact) => {
    const boite = couche.current?.getBoundingClientRect() ?? { left: 0, top: 0, width: 1, height: 1 }
    return caseSousLePointeur(boite, e.clientX, e.clientY, disposition.colonnes, disposition.lignes)
  }

  /** Ce que donnerait le geste sous ce pointeur. */
  const resultat = (g: Geste, e: PointerEventReact): { d?: Disposition; place: PlaceZone } => {
    const p = zoneDe(disposition, g.zone)
    if (!p) return { place: { col: 1, ligne: 1, largeur: 1, hauteur: 1, taille: 1 } }
    if (g.genre === 'taille') {
      const d = changerTaille(disposition, g.zone, g.taille + (g.y - e.clientY) / 150)
      return { d, place: zoneDe(d, g.zone) ?? p }
    }
    const ici = caseDe(e)
    if (g.genre === 'brique') {
      const d = deposerBrique(disposition, g.brique, ici.col, ici.ligne)
      // Sur une autre zone : elle sera la place de la fusion ; ailleurs : une case de depart.
      const cible = zoneSousLaCase(disposition, ici.col, ici.ligne)
      const m = minimumDeZone([g.brique])
      const place = cible && cible !== p ? cible : { ...p, col: ici.col, ligne: ici.ligne, ...m }
      return { d, place }
    }
    if (g.genre === 'deplacer') {
      const col = g.origine.col + ici.col - g.depart.col
      const ligne = g.origine.ligne + ici.ligne - g.depart.ligne
      return { d: deplacer(disposition, g.zone, col, ligne), place: { ...p, col, ligne } }
    }
    const largeur = Math.max(1, ici.col - p.col + 1)
    const hauteur = Math.max(1, ici.ligne - p.ligne + 1)
    return { d: redimensionner(disposition, g.zone, largeur, hauteur), place: { ...p, largeur, hauteur } }
  }

  const commencer = (g: Geste) => (e: PointerEventReact<HTMLElement>) => {
    e.stopPropagation()
    e.preventDefault()
    e.currentTarget.setPointerCapture?.(e.pointerId)
    setGeste(g)
  }
  const bouger = (e: PointerEventReact) => {
    if (!geste) return
    const { d, place } = resultat(geste, e)
    // La taille des cartes se voit en direct, sur la vraie table.
    if (geste.genre === 'taille' && d) changer(d)
    else setFantome({ place, refuse: !d })
  }
  const lacher = (e: PointerEventReact) => {
    if (!geste) return
    const { d } = resultat(geste, e)
    if (d) changer(d)
    setGeste(undefined)
    setFantome(undefined)
  }

  const barre = (
    <div className="editeur-table-barre" role="toolbar" aria-label={t('Modifier la table')}>
      <span className="editeur-table-aide">
        {t('Glisse une zone pour la déplacer. Coin bas-droit : sa place. Coin haut-droit : la taille des cartes. Une pastille glissée sur une autre zone les réunit, dehors elle s’en sépare.')}
      </span>
      <button type="button" className="bh-bouton" onClick={origine}>
        {t('Disposition d’origine')}
      </button>
      <button type="button" className="bh-bouton" onClick={annuler}>
        {t('Annuler')}
      </button>
      <button type="button" className="bh-bouton editeur-table-terminer" onClick={terminer}>
        {t('Terminer')}
      </button>
    </div>
  )

  return (
    <>
      <div
        ref={couche}
        className="editeur-table"
        style={{
          gridTemplateColumns: `repeat(${disposition.colonnes}, minmax(0, 1fr))`,
          gridTemplateRows: `repeat(${disposition.lignes}, minmax(0, 1fr))`,
        }}
        onPointerMove={bouger}
        onPointerUp={lacher}
        onPointerCancel={() => {
          setGeste(undefined)
          setFantome(undefined)
        }}
      >
        {disposition.zones.map((p) => {
          const zone = ancre(p)
          const nom = titreDeZone(p.briques, (b) => t(NOMS[b]), t('et'))
          return (
            <div
              key={zone}
              className={`editeur-zone${geste?.zone === zone ? ' est-saisie' : ''}`}
              data-zone={zone}
              style={grille(p)}
              onPointerDown={(e) =>
                commencer({ genre: 'deplacer', zone, depart: caseDe(e), origine: p })(e)
              }
            >
              <span className="editeur-zone-nom">{nom}</span>
              <span className="editeur-briques">
                {p.briques.filter((b) => !estEpinglee(b)).map((b) => (
                  <button
                    type="button"
                    key={b}
                    className={`editeur-brique${geste?.genre === 'brique' && geste.brique === b ? ' est-saisie' : ''}`}
                    data-brique={b}
                    title={t('Glisse cette pastille sur une autre zone pour les réunir, ou dehors pour la séparer.')}
                    onPointerDown={(e) => commencer({ genre: 'brique', zone, brique: b })(e)}
                  >
                    {t(NOMS[b])}
                  </button>
                ))}
              </span>
              <button
                type="button"
                className="editeur-poignee-taille"
                aria-label={`${t('Taille des cartes')} : ${nom}`}
                title={t('Taille des cartes')}
                onPointerDown={(e) => commencer({ genre: 'taille', zone, y: e.clientY, taille: p.taille })(e)}
                onKeyDown={(e) => {
                  const pas = e.key === 'ArrowUp' ? 0.05 : e.key === 'ArrowDown' ? -0.05 : 0
                  if (!pas) return
                  e.preventDefault()
                  changer(changerTaille(disposition, zone, p.taille + pas))
                }}
              >
                A {Math.round(p.taille * 100)}%
              </button>
              <button
                type="button"
                className="editeur-poignee-place"
                aria-label={`${t('Place de la zone')} : ${nom}`}
                title={t('Place de la zone')}
                onPointerDown={commencer({ genre: 'place', zone })}
              >
                ⤡
              </button>
            </div>
          )
        })}
        {fantome ? (
          <div className={`editeur-fantome${fantome.refuse ? ' est-refuse' : ''}`} style={grille(fantome.place)} />
        ) : null}
      </div>
      {createPortal(barre, document.body)}
    </>
  )
}

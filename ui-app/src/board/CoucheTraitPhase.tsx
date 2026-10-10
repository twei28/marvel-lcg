// Le trait qui montre qui frappe qui, et combien.
//
// Demande de l'utilisateur, 14/09/2026, d'après la phase du méchant de
// play.marvelsimulator.com : « j'aime bien les traits qui montrent qui va être
// attaqué », puis « montrer sur le trait, si c'est les dégâts le nombre de
// dégâts, si c'est la manigance le nombre de manigances, si c'est le nombre de
// contre le nombre de contre ».
//
// ⚠ CE COMPOSANT NE DÉCIDE RIEN. Ce que le trait dit vient de
// `trait-phase.ts` (pur, testé), où il passe aussi, et les rectangles de
// `mesures-plateau.ts`. Ici on mesure, on écoute les changements, on dessine.
//
// ⚠ UNE CARTE PEUT AVOIR DISPARU. Un sbire tué par sa propre cible n'est plus
// dans l'index du monde au moment où l'étape s'affiche : `boiteDeCarte` rend
// alors `undefined`, et on ne dessine PAS de trait plutôt que d'en tirer un
// vers un point inventé. Le cartouche, lui, garde le nom en clair (le fait le
// porte) : l'information n'est pas perdue, seul le trait manque.

import { useEffect, useLayoutEffect, useState } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'
import { boiteDeCarte, cadreDuPlateau } from './mesures-plateau'
import { alerteMenace, contenuDuTrait, deltaSurTable, traitEntre, type Trait } from './trait-phase'

export function CoucheTraitPhase({
  etape,
  actif,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
}) {
  const [trait, setTrait] = useState<Trait | undefined>(undefined)
  const [cadre, setCadre] = useState<{ w: number; h: number } | undefined>(undefined)
  // Une seconde mesure au repos : les cartes de l'étape viennent parfois
  // d'arriver sur la table et volent encore au premier rendu.
  const [seconde, setSeconde] = useState(0)

  // UN SBIRE QUI S'ENGAGE (v3, Q22) : sans auteur ni cible d'activation, le
  // trait va du sbire entre en jeu vers le heros avec qui il s'engage.
  const engagement = etape?.effets?.find(
    (effet): effet is Extract<typeof effet, { genre: 'entree' }> =>
      effet.genre === 'entree' && effet.engage_avec_id !== undefined
  )
  const sansActivation = etape?.carteId === undefined || etape?.cibleId === undefined
  const auteurId = sansActivation && engagement ? engagement.carte_id : etape?.carteId
  const cibleId = sansActivation && engagement ? engagement.engage_avec_id : etape?.cibleId
  const cle = etape?.cle

  useLayoutEffect(() => {
    if (!actif || auteurId === undefined || cibleId === undefined) {
      setTrait(undefined)
      return
    }
    const mesurer = () => {
      const c = cadreDuPlateau()
      if (!c) return
      const auteur = boiteDeCarte(auteurId, c)
      const cible = boiteDeCarte(cibleId, c)
      if (!auteur || !cible) {
        setTrait(undefined)
        return
      }
      setCadre({ w: c.boite.w, h: c.boite.h })
      setTrait(traitEntre(auteur, cible))
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    return () => window.removeEventListener('resize', mesurer)
  }, [actif, auteurId, cibleId, cle, seconde])

  useEffect(() => {
    if (!actif) return
    setSeconde(0)
    const minuteur = window.setTimeout(() => setSeconde(1), 260)
    return () => window.clearTimeout(minuteur)
  }, [actif, cle])

  if (!trait || !cadre || !etape) return null
  const contenu = contenuDuTrait(etape)
  // Rien à annoncer et aucune unité : le trait montre la direction, sans
  // étiquette. Un cartouche vide ferait un point noir posé sur la table.
  const etiquette =
    contenu.montant !== undefined
      ? `${contenu.montant}${contenu.unite ? ' ' + t(contenu.unite) : ''}`
      : contenu.unite
        ? t(contenu.unite)
        : ''

  return (
    <svg
      className={`trait-phase est-${contenu.ton}`}
      viewBox={`0 0 ${cadre.w} ${cadre.h}`}
      width={cadre.w}
      height={cadre.h}
      aria-hidden="true"
    >
      <defs>
        {/* La pointe prend la couleur du trait : `context-stroke` évite d'avoir
            un marqueur par ton, et garde la flèche d'accord avec la ligne. */}
        <marker
          id="trait-phase-pointe"
          viewBox="0 0 10 10"
          refX="9"
          refY="5"
          markerWidth="5"
          markerHeight="5"
          orient="auto-start-reverse"
        >
          <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" />
        </marker>
      </defs>
      {/* Deux traits superposés : un large et sombre dessous, qui détache le
          trait des illustrations, et le trait coloré dessus. Sans lui, un trait
          rouge sur une carte rouge disparaît. */}
      <line className="trait-phase-ombre" x1={trait.x1} y1={trait.y1} x2={trait.x2} y2={trait.y2} />
      <line
        className="trait-phase-ligne"
        x1={trait.x1}
        y1={trait.y1}
        x2={trait.x2}
        y2={trait.y2}
        markerEnd="url(#trait-phase-pointe)"
      />
      {etiquette ? (
        <g className="trait-phase-etiquette" transform={`translate(${trait.mx} ${trait.my})`}>
          {/* La largeur suit le texte : une boîte fixe couperait « 3 menaces »
              et laisserait du vide autour de « 2 ». 8,4 px par caractère est
              mesuré sur la fonte du plateau à cette taille. */}
          <rect
            x={-(etiquette.length * 4.2 + 10)}
            y={-13}
            width={etiquette.length * 8.4 + 20}
            height={26}
            rx={13}
          />
          <text x={0} y={5} textAnchor="middle">
            {etiquette}
          </text>
        </g>
      ) : null}
    </svg>
  )
}

/**
 * L'ALLUMAGE ET LA CARTE TOUCHEE (v3, 10/10/2026, Q6 et Q7).
 *
 * Halo dore sur la carte qui agit et sur sa cible, le reste de la table
 * attenue ; sur la cible d'une etape resolue, la jauge agrandie, son ancien
 * niveau en fantome, et le nombre qui s'envole au-dessus d'elle.
 *
 * ⚠ UNE FEUILLE DE STYLE GENEREE, PAS DES CLASSES POSEES A LA MAIN : React
 * reecrit la classe des cartes a chaque rendu et effacerait une classe ajoutee
 * hors de lui. Les identifiants sont des nombres : rien a echapper.
 */
export function EffetsSurTable({
  etape,
  actif,
  pvMax,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
  pvMax?: number
}) {
  const [boite, setBoite] = useState<{ x: number; y: number; w: number } | undefined>(undefined)
  const delta = etape && actif ? deltaSurTable(etape, pvMax) : undefined
  const cibleId = etape?.cibleId
  const cle = etape?.cle

  useLayoutEffect(() => {
    if (!delta || cibleId === undefined) {
      setBoite(undefined)
      return
    }
    const c = cadreDuPlateau()
    const b = c ? boiteDeCarte(cibleId, c) : undefined
    setBoite(b ? { x: b.x, y: b.y, w: b.w } : undefined)
    // `delta` change d'objet a chaque rendu : la cle de l'etape suffit.
  }, [cle, cibleId, delta === undefined])

  if (!actif || !etape) return null
  const ids = [etape.carteId, etape.cibleId].filter((id): id is number => id !== undefined)
  if (ids.length === 0) return null
  const sauf = ids.map((id) => `:not([data-card-id="${id}"])`).join('')
  const vises = ids.map((id) => `.plateau-cadre .scan-card[data-card-id="${id}"]`).join(',\n')
  const regles = [
    `.plateau-cadre .scan-card${sauf}:not(.rencontre-sur-table *) { filter: brightness(0.5) saturate(0.6); }`,
    `${vises} { outline: 3px solid #f0b95f; outline-offset: 2px; filter: drop-shadow(0 0 10px rgba(240, 185, 95, 0.85)); }`,
  ]
  if (delta && cibleId !== undefined) {
    const jauge = `.plateau-cadre .scan-card[data-card-id="${cibleId}"] .jauge-carte`
    regles.push(`${jauge} { transform: scale(1.12, 1.8); transition: transform 200ms ease-out; }`)
    if (delta.avant !== undefined)
      regles.push(`${jauge}::before { width: ${Math.round(delta.avant * 1000) / 10}%; }`)
  }
  if (cibleId !== undefined && alerteMenace(etape)) {
    regles.push(
      `.plateau-cadre .scan-card[data-card-id="${cibleId}"] .jauge-carte { animation: jauge-alerte 900ms ease-in-out infinite; }`
    )
  }
  return (
    <>
      <style>{regles.join('\n')}</style>
      {delta && boite ? (
        <span
          key={cle}
          className={`delta-sur-table est-${delta.ton}`}
          style={{ left: `${boite.x + boite.w / 2}px`, top: `${boite.y}px` }}
          aria-hidden="true"
        >
          {delta.texte}
        </span>
      ) : null}
    </>
  )
}

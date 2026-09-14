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
import { contenuDuTrait, traitEntre, type Trait } from './trait-phase'

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

  const auteurId = etape?.carteId
  const cibleId = etape?.cibleId
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

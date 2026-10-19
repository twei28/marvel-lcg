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

import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'
import { boiteDeCarte, cadreDuPlateau } from './mesures-plateau'
import { alerteMenace, contenuDuTrait, deltaSurTable, deltasDesEffets, etiquetteDuTrait, traitEntre, type Trait } from './trait-phase'

export function CoucheTraitPhase({
  etape,
  actif,
  sansEtiquette = false,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
  /** Le jeton porte déjà le nombre (16/10/2026) : pas de pastille « 4 dégâts » au milieu du trait. */
  sansEtiquette?: boolean
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
  // Une annonce à 0 (l'ATQ de Klaw avant ses boosts) ne dit pas « 0 dégâts » : ce serait faux.
  // 19/10/2026 : un coup a 0 degat ne l'affiche pas non plus (le bandeau et le « −0 PV » le disent).
  const etiquette = etiquetteDuTrait(contenu, sansEtiquette)
  const arc = `M ${trait.x1} ${trait.y1} Q ${trait.cx} ${trait.cy} ${trait.x2} ${trait.y2}`
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
      {/* ARC QUADRATIQUE (19/10/2026) : l'ancien <line> droit pointillé est remplacé, pas supprimé en
          pensée : `COURBURE_TRAIT` à 0 redonne la droite. `pathLength` = 1 pour que le tracé se dessine
          de la source vers la cible (animation `trait-phase-trace`, éteinte en mouvement réduit). */}
      <path className="trait-phase-ombre" d={arc} pathLength={1} />
      <path className="trait-phase-ligne" d={arc} pathLength={1} markerEnd="url(#trait-phase-pointe)" />
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

/** Combien de temps reste un « −X PV » (meme duree que celui d'une attaque : `delta-s-impact`, 1,6 s). */
const DUREE_DELTA_EFFET_MS = 1700

type DeltaPose = { cle: string; texte: string; ton: 'degats'; x: number; y: number; w: number }

/**
 * « −X PV » DES CARTES BLESSEES PAR UNE CARTE REVELEE (19/10/2026).
 *
 * ⚠ LES EFFETS D'UNE CARTE REVELEE N'ARRIVENT QU'A LA FIN DE SON ECRAN (constate a l'ecran, 19/10/2026) :
 * le moteur ne les mesure qu'une fois la carte resolue, c'est-a-dire quand le joueur a fini de la lire.
 * L'etape affichee ne les porte donc jamais : on les lit dans la LISTE des etapes, des qu'ils paraissent,
 * quelle que soit l'etape alors a l'ecran. Chaque (etape, carte) ne se montre qu'une fois ; ce qui est
 * deja la au premier rendu (rechargement de la page, relecture) ne se rejoue pas.
 */
function useDegatsDesEffets(etapes: readonly EtapeDeroule[] | undefined): DeltaPose[] {
  const [poses, setPoses] = useState<DeltaPose[]>([])
  const vus = useRef<Set<string> | undefined>(undefined)
  const tous = (etapes ?? []).flatMap((e) => deltasDesEffets(e).map((d) => ({ ...d, cle: `${e.cle}#${d.cibleId}` })))
  const signature = tous.map((d) => `${d.cle}:${d.texte}`).join('|')
  useLayoutEffect(() => {
    if (vus.current === undefined) {
      vus.current = new Set(tous.map((d) => d.cle))
      return
    }
    const nouveaux = tous.filter((d) => !vus.current?.has(d.cle))
    if (nouveaux.length === 0) return
    for (const d of nouveaux) vus.current.add(d.cle)
    const c = cadreDuPlateau()
    const posees: DeltaPose[] = []
    for (const d of nouveaux) {
      const b = c ? boiteDeCarte(d.cibleId, c) : undefined
      if (b) posees.push({ cle: d.cle, texte: d.texte, ton: d.ton, x: b.x, y: b.y, w: b.w })
    }
    if (posees.length === 0) return
    setPoses((liste) => [...liste, ...posees])
    const minuteur = window.setTimeout(
      () => setPoses((liste) => liste.filter((p) => !posees.some((q) => q.cle === p.cle))),
      DUREE_DELTA_EFFET_MS
    )
    // Pas de nettoyage au demontage de l'effet : un nouveau rendu ne doit pas effacer un « −X PV » en cours.
    void minuteur
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [signature])
  return poses
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
  etapes,
}: {
  etape: EtapeDeroule | undefined
  actif: boolean
  pvMax?: number
  /** Toutes les etapes de la phase : les « −X PV » d'une carte revelee viennent de la leur, pas de l'etape affichee. */
  etapes?: readonly EtapeDeroule[]
}) {
  const [boite, setBoite] = useState<{ x: number; y: number; w: number } | undefined>(undefined)
  const boitesEffets = useDegatsDesEffets(etapes)
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

  // Une ligne par carte blessee par un effet revele (hors attaque, dont le « −X PV » est celui de `delta`).
  const spansEffets = boitesEffets.map((e) => (
    <span
      key={e.cle}
      className={`delta-sur-table est-${e.ton}`}
      style={{ left: `${e.x + e.w / 2}px`, top: `${e.y}px` }}
      aria-hidden="true"
    >
      {e.texte}
    </span>
  ))
  if (!actif || !etape) return spansEffets.length > 0 ? <>{spansEffets}</> : null
  const ids = [etape.carteId, etape.cibleId].filter((id): id is number => id !== undefined)
  if (ids.length === 0) return spansEffets.length > 0 ? <>{spansEffets}</> : null
  const sauf = ids.map((id) => `:not([data-card-id="${id}"])`).join('')
  // 16/10/2026 : plus de contour orange épais ni de lueur sur les cartes qui agissent et qui
  // subissent. Il se calait sur le BLOC entier de la carte (pastille de type et barre de PV
  // comprises) et faisait un cadre décentré autour de Spider-Man ; ce sont les halos de
  // `TableSansModale`, ajustés sur l'image, qui désignent ces cartes. Seul reste l'assombrissement
  // des autres.
  const regles = [
    `.plateau-cadre .scan-card${sauf}:not(.rencontre-sur-table *) { filter: brightness(0.5) saturate(0.6); }`,
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
      {spansEffets}
    </>
  )
}

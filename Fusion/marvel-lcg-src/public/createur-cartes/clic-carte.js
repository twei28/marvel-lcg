// Cliquer sur la carte pour editer : le clic ouvre (et met en evidence) le champ du formulaire qui correspond a l'element touche.
import { elementSousPoint } from './carte.js'
import { S } from './commun.js'

const CHAMP = {
  title: 'titre', header: 'titre', typestr: 'typeTexte', traits: 'traits', rules: 'regles', quote: 'citation', 'set-line': 'ligneEnsemble',
  'c-line': 'createur', 'paycost cost': 'cout', 'thw sch cost': 'thw', 'atk cost': 'atk', 'def cost': 'def', 'rec cost': 'rec', 'hp cost': 'pv',
  handsize: 'tailleMain', 'targetthreat cost': 'menaceCible', startingthreatwrap: 'menaceDepart', acceleration: 'acceleration', villainstagenew: 'etape',
  'attachmentatknums cost': 'atkAttache', 'attachmentschnums cost': 'schAttache', 'mainschemephase cost': 'phaseNumero',
}

/** Rend le nom du champ de contenu touche par un clic (pixels du canvas), ou null. */
export function champSousPoint(spec, x, y, infos) {
  const hit = elementSousPoint(spec, x, y)
  if (!hit) return null
  if (['cardtext', 'rules', 'quote', 'traits'].includes(hit.cls)) {
    // le panneau de texte : on regarde quel bloc (traits, regles, citation) occupe cette hauteur (les boites du gabarit se recouvrent)
    const yRel = hit.local[1] - (spec.elements.find((e) => e.cls === 'cardtext')?.boite[1] ?? hit.panneau[1])
    const blocs = infos?.blocs ?? []
    const pris = blocs.find((b) => yRel >= b.y0 - 10 && yRel <= b.y1 + 14) ?? blocs.filter((b) => b.c !== 'traits').pop()
    return { traits: 'traits', rules: 'regles', quote: 'citation' }[pris?.c] ?? 'regles'
  }
  return CHAMP[hit.cls] ?? null
}

/** Ouvre et met en evidence le champ du formulaire. */
export function montrerChamp(nom) {
  const cible = document.querySelector(`#champs [data-champ="${nom}"]`)
  if (!cible) return false
  for (let d = cible.closest('details'); d; d = d.parentElement?.closest('details')) d.open = true
  cible.scrollIntoView({ block: 'center', behavior: 'smooth' })
  cible.focus({ preventScroll: true })
  if (cible.isContentEditable) {
    const r = document.createRange()
    r.selectNodeContents(cible)
    r.collapse(false)
    const s = getSelection()
    s.removeAllRanges()
    s.addRange(r)
  } else if (cible.select) cible.select()
  const cadre = cible.closest('label, .champ-riche, .nombre') ?? cible
  cadre.classList.add('flash-champ')
  setTimeout(() => cadre.classList.remove('flash-champ'), 1200)
  return true
}

export function clicSurCarte(e, toile) {
  const c = S.carte()
  if (!c) return
  const r = toile.getBoundingClientRect()
  const x = ((e.clientX - r.left) / r.width) * toile.width
  const y = ((e.clientY - r.top) / r.height) * toile.height
  const nom = champSousPoint(S.types[c.type], x, y, S.infosRendu)
  if (nom) montrerChamp(nom)
}

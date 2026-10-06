// Les cartes NOMMEES dans une ligne du journal, pour les souligner et en
// montrer l'image au survol (idee de Yarro, decisions du 06/10/2026).
//
// ⚠ ON NE DEVINE PAS. Une carte n'est reconnue que par son identifiant
// d'objet : celui que le moteur ecrit dans sa narration (« [(50,01113) Klaw] »,
// conserve dans `brut`) ou la carte visee par un fait du jeu (`cibleId`). Un
// nom porte par deux cartes differentes reste du texte simple.
import type { EntreeHistorique } from './HistoriquePartie'
import { NOMS_FR } from './noms-fr'
import { scansFrActifs } from './scans-fr'

export type RefCarte = { id: number; nom: string }
export type Morceau = string | RefCarte

const IDENTIFIANT = /\[+\(\s*(\d+)\s*,\s*([0-9a-z_]*)[^)]*\)\s*([^[\]]+?)\]+/g

export function referencesDeBrut(brut: string | undefined): RefCarte[] {
  if (!brut) return []
  const refs: RefCarte[] = []
  const francais = scansFrActifs()
  for (const trouve of brut.matchAll(IDENTIFIANT)) {
    // Le nom tel que la ligne l'affiche : le texte est passe en francais.
    const nom = ((francais ? NOMS_FR[trouve[2]] : undefined) ?? trouve[3]).trim()
    if (nom) refs.push({ id: Number(trouve[1]), nom })
  }
  return refs
}

export function referencesDeEntree(entree: Pick<EntreeHistorique, 'brut' | 'cibleId' | 'nomCarte'>): RefCarte[] {
  const refs = referencesDeBrut(entree.brut)
  if (entree.cibleId !== undefined && entree.nomCarte) refs.push({ id: entree.cibleId, nom: entree.nomCarte })
  return refs
}

const LETTRE = /[\p{L}\p{N}]/u

function bordDeMot(texte: string, debut: number, fin: number): boolean {
  return !LETTRE.test(texte[debut - 1] ?? '') && !LETTRE.test(texte[fin] ?? '')
}

export function decouperNoms(texte: string, refs: readonly RefCarte[]): Morceau[] {
  const parNom = new Map<string, RefCarte | null>()
  for (const ref of refs) {
    const deja = parNom.get(ref.nom)
    if (deja === undefined) parNom.set(ref.nom, ref)
    else if (deja !== null && deja.id !== ref.id) parNom.set(ref.nom, null)
  }
  const sures = [...parNom.values()]
    .filter((ref): ref is RefCarte => ref !== null)
    .sort((a, b) => b.nom.length - a.nom.length)
  if (sures.length === 0) return [texte]

  const morceaux: Morceau[] = []
  let reste = 0
  let i = 0
  while (i < texte.length) {
    const ref = sures.find(
      (candidate) => texte.startsWith(candidate.nom, i) && bordDeMot(texte, i, i + candidate.nom.length)
    )
    if (!ref) {
      i += 1
      continue
    }
    if (i > reste) morceaux.push(texte.slice(reste, i))
    morceaux.push({ id: ref.id, nom: ref.nom })
    i += ref.nom.length
    reste = i
  }
  if (reste < texte.length) morceaux.push(texte.slice(reste))
  return morceaux
}

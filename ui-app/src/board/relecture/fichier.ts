// Lecture d'un fichier .marvelreplay (gzip de lignes JSON), produit par
// `engine/enregistrement.py`. Meme format de difference que lui : une
// difference ne copie que le chemin qui change, donc garder tous les mondes
// reconstruits ne coute que la taille des differences.
import type { Demande } from '../ask'
import { lireDemande } from '../ask'
import type { World } from '../world'

export const FORMAT_RELECTURE = 1

type Difference = { v?: unknown; i?: Record<string, Difference>; o?: Record<string, Difference>; x?: string[] }

export function appliquer(a: unknown, d: Difference | undefined): unknown {
  if (d === undefined) return a
  if ('v' in d) return d.v
  if (d.i) {
    const copie = [...(a as unknown[])]
    for (const [indice, sous] of Object.entries(d.i)) copie[Number(indice)] = appliquer(copie[Number(indice)], sous)
    return copie
  }
  const copie: Record<string, unknown> = { ...(a as Record<string, unknown>) }
  for (const cle of d.x ?? []) delete copie[cle]
  for (const [cle, sous] of Object.entries(d.o ?? {})) copie[cle] = appliquer(copie[cle], sous)
  return copie
}

export type EnteteRelecture = {
  format: number
  date?: string
  scenario?: string
  expert?: boolean
  version?: string
  rounds?: number
  resultat?: 'victoire' | 'defaite' | 'inachevee'
  joueurs: { heros: string; deck?: string }[]
}

export type TrameRelecture = {
  t: number
  monde: World
  /** La question posee a chaque siege juste apres ce rendu. */
  demandes: Record<number, Demande>
}

export type Curseur = { t: number; p: number; x: number; y: number; clic: number }
export type EtapeLue = { t: number; p: number; cle: string; mode?: string }
/** Ce que le joueur voyait (ligne « v », `server_get.set_vu`) : un genre, une valeur. */
export type VuEnregistre = { t: number; p: number; g: string; v: unknown }

export type Relecture = {
  entete: EnteteRelecture
  trames: TrameRelecture[]
  curseurs: Curseur[]
  etapes: EtapeLue[]
  /** Absent des parties enregistrees avant le 08/10/2026 : elles se relisent sans. */
  vus: VuEnregistre[]
  /** Ressources imprimees des cartes passees en main (le monde ne les porte pas). */
  ressources: Record<number, string>
}

export class FichierInvalide extends Error {}

async function decompresser(donnees: ArrayBuffer): Promise<string> {
  const flux = new Response(donnees).body!.pipeThrough(new DecompressionStream('gzip'))
  return new Response(flux).text()
}

export async function lireRelecture(donnees: ArrayBuffer): Promise<Relecture> {
  let texte: string
  try {
    texte = await decompresser(donnees)
  } catch {
    throw new FichierInvalide('Ce fichier n’est pas une partie enregistrée (.marvelreplay).')
  }
  return analyserRelecture(texte)
}

export function analyserRelecture(texte: string): Relecture {
  const lignes = texte.split('\n').filter((l) => l.trim() !== '')
  let entete: EnteteRelecture | undefined
  const trames: TrameRelecture[] = []
  const curseurs: Curseur[] = []
  const etapes: EtapeLue[] = []
  const vus: VuEnregistre[] = []
  const ressources: Record<number, string> = {}
  let monde: unknown
  try {
    for (const [n, ligne] of lignes.entries()) {
      const o = JSON.parse(ligne) as Record<string, unknown>
      if (n === 0) {
        if (o.k !== 'entete') throw new FichierInvalide('Ce fichier n’est pas une partie enregistrée (.marvelreplay).')
        if (typeof o.format !== 'number' || o.format > FORMAT_RELECTURE) {
          throw new FichierInvalide('Cette partie a été enregistrée par une version plus récente du jeu.')
        }
        entete = { ...(o as unknown as EnteteRelecture), joueurs: Array.isArray(o.joueurs) ? (o.joueurs as EnteteRelecture['joueurs']) : [] }
        continue
      }
      const t = Number(o.t) || 0
      if (o.k === 'cle' || o.k === 'd') {
        if (o.k === 'cle') monde = o.m
        else if (monde === undefined) throw new FichierInvalide('Ce fichier est abîmé : il commence par une différence.')
        else monde = appliquer(monde, o.d as Difference)
        trames.push({ t, monde: monde as World, demandes: {} })
      } else if (o.k === 'q') {
        const demande = lireDemande(o.q)
        const derniere = trames.at(-1)
        if (demande && derniere) derniere.demandes = { ...derniere.demandes, [Number(o.p)]: demande }
      } else if (o.k === 'c') {
        curseurs.push({ t, p: Number(o.p), x: Number(o.x), y: Number(o.y), clic: Number(o.clic) || 0 })
      } else if (o.k === 'res') {
        for (const [id, texte] of Object.entries((o.m ?? {}) as Record<string, unknown>)) ressources[Number(id)] = String(texte)
      } else if (o.k === 'v') {
        if (typeof o.g === 'string') vus.push({ t, p: Number(o.p), g: o.g, v: o.v })
      } else if (o.k === 'e') {
        etapes.push({ t, p: Number(o.p), cle: String(o.cle ?? ''), ...(o.mode ? { mode: String(o.mode) } : {}) })
      }
    }
  } catch (erreur) {
    if (erreur instanceof FichierInvalide) throw erreur
    throw new FichierInvalide('Ce fichier est abîmé ou a été modifié : il ne peut pas être relu.')
  }
  if (!entete) throw new FichierInvalide('Ce fichier est vide.')
  if (trames.length === 0) throw new FichierInvalide('Ce fichier ne contient aucune action.')
  return { entete, trames, curseurs, etapes, vus, ressources }
}

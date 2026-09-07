// Les icones de ressources du jeu dans les textes du plateau.
//
// Le moteur ecrit une ressource de trois facons : un jeton « [[physical]] »
// dans ses narrations, une lettre (R/B/Y/G) dans un cout type (« BY »), un mot
// anglais dans ses questions (« Pay 1 mental resource(s) »). Le joueur, lui,
// veut voir l'icone de la carte (demande de l'utilisateur, 7 septembre 2026).
//
// Le texte reste un texte partout (traductions, tests, journal) : les
// ressources y deviennent un MARQUEUR « ⟦P⟧ », et `avecIcones` le rend en
// icone au moment d'afficher, dans la police ChampionsIcons deja embarquee
// (P poing, M cerveau, E eclair, W etoile), coloree par ressource.

import type { ReactNode } from 'react'
import { t } from './langue'

export type Ressource = {
  /** Lettre du moteur (`desc.RES`, couts types). */
  lettre: 'R' | 'B' | 'Y' | 'G'
  /** Glyphe dans la police ChampionsIcons. */
  glyphe: 'P' | 'M' | 'E' | 'W'
  /** Cle des jetons de narration (« [[physical]] »). */
  cle: 'physical' | 'mental' | 'energy' | 'wild'
  nom: string
}

export const RESSOURCES: readonly Ressource[] = [
  { lettre: 'R', glyphe: 'P', cle: 'physical', nom: 'physique' },
  { lettre: 'B', glyphe: 'M', cle: 'mental', nom: 'mentale' },
  { lettre: 'Y', glyphe: 'E', cle: 'energy', nom: 'énergie' },
  { lettre: 'G', glyphe: 'W', cle: 'wild', nom: 'libre' },
]

const PAR_GLYPHE = new Map(RESSOURCES.map((r) => [r.glyphe, r]))
const PAR_CLE = new Map(RESSOURCES.map((r) => [r.cle, r]))
const PAR_LETTRE = new Map(RESSOURCES.map((r) => [r.lettre, r]))

/** Le marqueur d'une ressource dans un texte : « ⟦P⟧ ». */
export function marqueurRessource(cle: Ressource['cle']): string {
  return `⟦${PAR_CLE.get(cle)?.glyphe ?? 'W'}⟧`
}

const JETONS = /\[\[(physical|mental|energy|wild)\]\]/g
const MOTS = /\b(physical|mental|energy|wild)(?= resources?\b)/gi

/**
 * Remplace, dans un texte du moteur, les jetons « [[energy]] » et les mots
 * « energy resource(s) » par le marqueur de l'icone. Le mot « resource(s) »
 * qui suit est garde : « ⟦E⟧ resource » se lit encore.
 */
export function marquerRessources(texte: string): string {
  return texte
    .replace(JETONS, (_, cle: Ressource['cle']) => marqueurRessource(cle))
    .replace(MOTS, (mot: string) => marqueurRessource(mot.toLowerCase() as Ressource['cle']))
}

/**
 * Un cout type du moteur (« BY », « RRB ») devient une suite de marqueurs.
 * Un cout ordinaire (« 2 », « 1/3 ») ou vide est rendu tel quel.
 */
export function coutEnIcones(cout: string): string {
  if (!/^[RBYG]+$/i.test(cout)) return cout
  return cout
    .toUpperCase()
    .split('')
    .map((lettre) => `⟦${PAR_LETTRE.get(lettre as Ressource['lettre'])?.glyphe ?? 'W'}⟧`)
    .join('')
}

const MARQUEUR = /⟦([PMEW])⟧/g

/**
 * Rend un texte porteur de marqueurs : les morceaux de texte tels quels, les
 * marqueurs en icones. Sans marqueur, rend la chaine elle-meme : les appelants
 * peuvent l'employer partout sans changer leur structure.
 */
export function avecIcones(texte: string): ReactNode {
  if (!texte.includes('⟦')) return texte
  const morceaux: ReactNode[] = []
  let dernier = 0
  let rang = 0
  for (const trouve of texte.matchAll(MARQUEUR)) {
    const debut = trouve.index ?? 0
    if (debut > dernier) morceaux.push(texte.slice(dernier, debut))
    const ressource = PAR_GLYPHE.get(trouve[1] as Ressource['glyphe'])
    if (ressource) {
      morceaux.push(
        <i
          key={`icone-${rang}`}
          className={`icone-res res-${ressource.cle}`}
          role="img"
          aria-label={t(ressource.nom)}
          title={t(ressource.nom)}
        >
          {ressource.glyphe}
        </i>
      )
    }
    rang += 1
    dernier = debut + trouve[0].length
  }
  if (dernier < texte.length) morceaux.push(texte.slice(dernier))
  return morceaux
}

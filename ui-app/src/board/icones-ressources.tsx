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

import type { CSSProperties, ReactNode } from 'react'
import { t } from './langue'

export type Ressource = {
  /** Lettre du moteur (`desc.RES`, couts types). */
  lettre: 'R' | 'B' | 'Y' | 'G' | 'L'
  /** Glyphe dans la police ChampionsIcons ; `L` n'y existe pas et se rend en SVG. */
  glyphe: 'P' | 'M' | 'E' | 'W' | 'L'
  /** Cle des jetons de narration (« [[physical]] »). */
  cle: 'physical' | 'mental' | 'energy' | 'wild' | 'lightning'
  nom: string
}

export const RESSOURCES: readonly Ressource[] = [
  { lettre: 'R', glyphe: 'P', cle: 'physical', nom: 'physique' },
  { lettre: 'B', glyphe: 'M', cle: 'mental', nom: 'mentale' },
  { lettre: 'Y', glyphe: 'E', cle: 'energy', nom: 'énergie' },
  { lettre: 'G', glyphe: 'W', cle: 'wild', nom: 'libre' },
  // L'eclair : ressource MAISON du pack Zeus (11/09/2026), cinquieme couleur
  // du moteur. Distincte de l'energie : un eclair ne paie pas un cout energie.
  { lettre: 'L', glyphe: 'L', cle: 'lightning', nom: 'éclair' },
]

/**
 * Les DEUX TONS de chaque ressource, comme l'icone imprimee dans le coin des
 * cartes : un fond de la couleur de la ressource, le picto dessus dans une
 * teinte voisine (demande de l'utilisateur, 20/10/2026). SOURCE UNIQUE : ces
 * valeurs arrivent sur chaque icone en variables CSS (`--res-fond`,
 * `--res-picto`), et toute pastille de ressource de l'interface les lit.
 *
 * Fonds echantillonnes au pixel sur les icones imprimees. Pictos : echantillon
 * de l'impression, puis ajuste au besoin pour garder un contraste >= 3,5:1
 * (energie : olive plus fonce ; libre : vert vif plus clair ; physique et
 * mentale : plus clairs).
 */
export const TONS_RESSOURCES: Record<Ressource['cle'], { fond: string; picto: string }> = {
  physical: { fond: '#9f2115', picto: '#f0a590' }, // imprime : #9f2115 / #e2876d
  mental: { fond: '#5c63a5', picto: '#d0d5ec' }, // imprime : #5c63a5 / #b9c0de
  energy: { fond: '#e6bf4f', picto: '#6b5a14' }, // imprime : #e6bf4f / #85742f
  wild: { fond: '#296329', picto: '#78c872' }, // imprime : #296329 / #508f4c
  // Maison (Zeus) : bleu electrique, a part de l'energie.
  lightning: { fond: '#2a7fc0', picto: '#d6f0ff' },
}

/**
 * Drapeau : true = icones en deux tons (fond + picto) ; false = l'ancien rendu
 * monochrome (picto colore sans fond), conserve derriere ce drapeau.
 */
export const ICONES_DEUX_TONS = true

const PAR_GLYPHE = new Map(RESSOURCES.map((r) => [r.glyphe, r]))
const PAR_CLE = new Map(RESSOURCES.map((r) => [r.cle, r]))
const PAR_LETTRE = new Map(RESSOURCES.map((r) => [r.lettre, r]))

/** Le marqueur d'une ressource dans un texte : « ⟦P⟧ ». */
export function marqueurRessource(cle: Ressource['cle']): string {
  return `⟦${PAR_CLE.get(cle)?.glyphe ?? 'W'}⟧`
}

// Un ou deux crochets : le moteur ecrit « [[energy]] », les textes francais
// officiels « [energy] ».
const JETONS = /\[{1,2}(physical|mental|energy|wild|lightning)\]{1,2}/g
const MOTS = /\b(physical|mental|energy|wild|lightning)(?= resources?\b)/gi

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

/** Le meme texte SANS icones, pour une infobulle native (`title`) : « ⟦E⟧ » devient « énergie ». */
export function ressourcesEnMots(texte: string): string {
  return marquerRessources(texte).replace(/⟦([PMEWL])⟧/g, (_, glyphe: Ressource['glyphe']) =>
    t(PAR_GLYPHE.get(glyphe)?.nom ?? 'libre')
  )
}

/**
 * Un cout type du moteur (« BY », « RRB ») devient une suite de marqueurs.
 * Un cout ordinaire (« 2 », « 1/3 ») ou vide est rendu tel quel.
 */
export function coutEnIcones(cout: string): string {
  if (!/^[RBYGL]+$/i.test(cout)) return cout
  return cout
    .toUpperCase()
    .split('')
    .map((lettre) => `⟦${PAR_LETTRE.get(lettre as Ressource['lettre'])?.glyphe ?? 'W'}⟧`)
    .join('')
}

const MARQUEUR = /⟦([PMEWL])⟧/g

/** Un eclair droit, comme sur les cartes de Zeus. `currentColor` suit `--res`. */
function IconeEclair() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M13 2 4 14h6l-1 8 9-12h-6z" />
    </svg>
  )
}

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
          className={`icone-res res-${ressource.cle}${ICONES_DEUX_TONS ? ' deux-tons' : ''}`}
          style={
            ICONES_DEUX_TONS
              ? ({
                  '--res-fond': TONS_RESSOURCES[ressource.cle].fond,
                  '--res-picto': TONS_RESSOURCES[ressource.cle].picto,
                } as CSSProperties)
              : undefined
          }
          role="img"
          aria-label={t(ressource.nom)}
          title={t(ressource.nom)}
        >
          {ressource.cle === 'lightning' ? <IconeEclair /> : ressource.glyphe}
        </i>
      )
    }
    rang += 1
    dernier = debut + trouve[0].length
  }
  if (dernier < texte.length) morceaux.push(texte.slice(dernier))
  return morceaux
}

// teinte.ts — la TEINTE DU FOND choisie par le joueur (04/10/2026).
//
// Demande de l'utilisateur, apres le retour d'un joueur (« le fond noir peut
// fatiguer ») : une roue de couleurs, dans les Reglages et a la premiere
// visite, pour teinter le fond, les bandeaux et les panneaux, « toujours dans
// des couleurs tres ternes ». Choix pris une question a la fois :
//  - une vraie roue, qui n'affiche QUE des couleurs ternes (saturation 0-18 %) ;
//  - un curseur de luminosite, du tres fonce au gris clair (6-62 %) ;
//  - fond + bandeaux + panneaux, pour rester coherent ; le halo du heros reste
//    par-dessus en mode Normal ;
//  - rendu en direct, bouton « Couleur d'origine », le choix suit le compte.
//
// ⚠ JUMEAU de `public/js/prepare/teinte-choix.js` (page de preparation). Les
// deux calculent les MEMES couleurs ; leurs tests partagent les memes valeurs
// attendues. Les bornes sont aussi celles du serveur (`TEINTE_BORNES`,
// server_get.py) : changer l'une oblige a changer les trois.
//
// ⚠ LISIBILITE. Le fond de la table peut aller jusqu'au gris clair, pas les
// bandeaux ni les panneaux : leurs textes sont blancs, leur luminosite est donc
// plafonnee. Les titres de zones, eux, sont poses SUR la table : ils passent en
// fonce des que la table devient claire.

export const CLE_TEINTE = 'mc_teinte_v1'

export const BORNES = { h: [0, 359], s: [0, 18], l: [6, 62] } as const

export type Teinte = { h: number; s: number; l: number }

/** La teinte de depart de la roue quand rien n'est choisi : proche du fond actuel. */
export const TEINTE_DE_DEPART: Teinte = { h: 220, s: 8, l: 12 }

const borne = (v: number, [bas, haut]: readonly [number, number]) => Math.min(haut, Math.max(bas, Math.round(v)))

/** « 210,12,18 » -> teinte, ou `undefined` pour toute forme invalide. */
export function lireTeinte(brut: unknown): Teinte | undefined {
  if (typeof brut !== 'string') return undefined
  const morceaux = brut.split(',')
  if (morceaux.length !== 3 || !morceaux.every((m) => /^\d+$/.test(m))) return undefined
  const [h, s, l] = morceaux.map(Number) as [number, number, number]
  if (h > BORNES.h[1] || s > BORNES.s[1] || l < BORNES.l[0] || l > BORNES.l[1]) return undefined
  return { h, s, l }
}

export function ecrireTeinteEnTexte(teinte: Teinte): string {
  const t = bornerTeinte(teinte)
  return `${t.h},${t.s},${t.l}`
}

export function bornerTeinte(teinte: Teinte): Teinte {
  return { h: borne(((teinte.h % 360) + 360) % 360, BORNES.h), s: borne(teinte.s, BORNES.s), l: borne(teinte.l, BORNES.l) }
}

/** HSL (0-360, 0-100, 0-100) -> « r g b » entiers, pour `rgb(var(--x) / a)`. */
export function hslVersRgb(h: number, s: number, l: number): string {
  const sat = s / 100
  const lum = l / 100
  const k = (n: number) => (n + h / 30) % 12
  const a = sat * Math.min(lum, 1 - lum)
  const f = (n: number) => lum - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)))
  return [f(0), f(8), f(4)].map((x) => Math.round(x * 255)).join(' ')
}

/** Le seuil au-dela duquel la table est « claire » : ses titres passent en fonce. */
export const SEUIL_TABLE_CLAIRE = 44

/**
 * Les variables CSS de la teinte. Toutes les surfaces derivent de la meme
 * teinte et de la meme saturation ; seule la luminosite change :
 *  - la table : la luminosite choisie ;
 *  - le bandeau du haut : un peu plus sombre que la table, jamais au-dessus de
 *    26 % (texte blanc) ;
 *  - les panneaux : proches de la table, jamais au-dessus de 24 % ;
 *  - le cadre : un ton plus clair que les panneaux.
 */
export function variablesDeTeinte(teinte: Teinte): Record<string, string> {
  const { h, s, l } = bornerTeinte(teinte)
  const lBandeau = Math.min(26, Math.max(5, l - 4))
  const lPanneau = Math.min(24, Math.max(8, l + 2))
  const lCadre = Math.min(36, lPanneau + 10)
  return {
    '--teinte-table': `hsl(${h} ${s}% ${l}%)`,
    '--teinte-table-rgb': hslVersRgb(h, s, l),
    '--teinte-bandeau': `hsl(${h} ${s}% ${lBandeau}%)`,
    '--teinte-bandeau-rgb': hslVersRgb(h, s, lBandeau),
    '--teinte-panneau': `hsl(${h} ${s}% ${lPanneau}%)`,
    '--teinte-panneau-rgb': hslVersRgb(h, s, lPanneau),
    '--teinte-cadre': `hsl(${h} ${Math.min(30, s + 4)}% ${lCadre}%)`,
    '--teinte-texte-table': l >= SEUIL_TABLE_CLAIRE ? '#1b1d21' : 'rgba(226, 232, 240, 0.78)',
  }
}

/** Pose (ou retire, avec `undefined`) la teinte sur la page. */
export function appliquerTeinte(teinte: Teinte | undefined): void {
  const racine = document.documentElement
  for (const nom of Object.keys(variablesDeTeinte(TEINTE_DE_DEPART))) racine.style.removeProperty(nom)
  if (!teinte) {
    delete racine.dataset.teinte
    return
  }
  for (const [nom, valeur] of Object.entries(variablesDeTeinte(teinte))) racine.style.setProperty(nom, valeur)
  racine.dataset.teinte = bornerTeinte(teinte).l >= SEUIL_TABLE_CLAIRE ? 'claire' : 'sombre'
}

export function lireTeinteDuNavigateur(): Teinte | undefined {
  try {
    return lireTeinte(window.localStorage.getItem(CLE_TEINTE))
  } catch {
    return undefined
  }
}

function envoyer(valeur: string | null): void {
  try {
    void fetch('/save_preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ changements: { teinte: valeur } }),
    }).catch(() => {})
  } catch {
    /* hors ligne : le navigateur garde le choix */
  }
}

/** Range le choix (navigateur + compte) ; `undefined` remet la couleur d'origine. */
export function ecrireTeinte(teinte: Teinte | undefined, versLeCompte = true): void {
  try {
    if (teinte) window.localStorage.setItem(CLE_TEINTE, ecrireTeinteEnTexte(teinte))
    else window.localStorage.removeItem(CLE_TEINTE)
  } catch {
    /* stockage indisponible : le choix ne survivra pas au rechargement */
  }
  appliquerTeinte(teinte)
  if (versLeCompte) envoyer(teinte ? ecrireTeinteEnTexte(teinte) : null)
}

/** Envoie le choix au compte seul (le navigateur est deja a jour). */
export function envoyerTeinteAuCompte(teinte: Teinte | undefined): void {
  envoyer(teinte ? ecrireTeinteEnTexte(teinte) : null)
}

/** Interroge le compte au chargement du plateau (voir `teinteDuCompte`). */
export async function chercherTeinteDuCompte(): Promise<Teinte | null | undefined> {
  try {
    const reponse = await fetch('/get_preferences', { cache: 'no-store' })
    if (!reponse.ok) return undefined
    return teinteDuCompte(await reponse.json())
  } catch {
    return undefined
  }
}

/**
 * La teinte du compte, quand il fait foi (meme contrat que l'affichage) :
 * `null` = le compte n'en a pas (couleur d'origine), `undefined` = le
 * navigateur reste la reference (invite, moteur local, compte sans fichier).
 */
export function teinteDuCompte(reponse: {
  compte?: boolean
  existe?: boolean
  preferences?: { teinte?: unknown }
} | null | undefined): Teinte | null | undefined {
  if (!reponse || !reponse.compte || !reponse.existe) return undefined
  return lireTeinte(reponse.preferences?.teinte) ?? null
}

/** Position sur la roue (angle = teinte, rayon = saturation) -> teinte. */
export function teinteDuPoint(dx: number, dy: number, rayon: number, l: number): Teinte {
  const angle = (Math.atan2(dy, dx) * 180) / Math.PI
  const distance = Math.min(1, Math.hypot(dx, dy) / Math.max(1, rayon))
  return bornerTeinte({ h: (angle + 90 + 360) % 360, s: distance * BORNES.s[1], l })
}

/** Inverse : la position du repere sur la roue, en fraction du rayon. */
export function pointDeLaTeinte(teinte: Teinte): { x: number; y: number } {
  const t = bornerTeinte(teinte)
  const angle = ((t.h - 90) * Math.PI) / 180
  const distance = t.s / BORNES.s[1]
  return { x: Math.cos(angle) * distance, y: Math.sin(angle) * distance }
}

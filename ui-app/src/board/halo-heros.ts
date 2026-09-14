// La couleur du héros, pour teinter le fond du plateau.
//
// Demande de l'utilisateur, 14/09/2026 : « une pointe de couleur dégradée dans
// le fond, la couleur principale du héros », placée « en diagonale, la couleur
// en bas à droite ».
//
// ⚠ LES COULEURS NE SE CALCULENT PAS ICI. Elles sont mesurées une fois pour
// toutes sur le CONTOUR des cartes de chaque deck, par
// `outils/palettes-heros.py`, et rangées dans `data/palettes-heros.json`. Les
// cartes ne changent pas : analyser des images en pleine partie serait payer
// à chaque tour ce qui se calcule une seule fois.
//
// ⚠ LA COULEUR SUIT LE HÉROS AFFICHÉ, pas la partie. En multijoueur, changer de
// vue change la teinte : « quand on change de héros, la couleur doit changer ».
// C'est pour cela que la palette se demande par identité et non une fois au
// chargement.

/** Une couleur, telle que le générateur l'écrit : [rouge, vert, bleu]. */
export type Couleur = readonly [number, number, number]

let promesse: Promise<Record<string, Couleur[]>> | undefined

async function charger(): Promise<Record<string, Couleur[]>> {
  try {
    const reponse = await fetch('/get_palettes_heros', { cache: 'no-store' })
    if (!reponse.ok) return {}
    // ⚠ Le moteur sert une IMAGE pour tout chemin inconnu : un 200 ne prouve
    // pas que la route existe. Sur un serveur d'avant elle, `json()` échoue et
    // le `catch` rend un catalogue vide, donc aucun halo. C'est le bon repli.
    const donnees = (await reponse.json()) as { palettes?: Record<string, Couleur[]> }
    return donnees?.palettes ?? {}
  } catch {
    return {}
  }
}

/** Le catalogue complet, demandé UNE SEULE FOIS par page. */
export function palettes(): Promise<Record<string, Couleur[]>> {
  promesse ??= charger()
  return promesse
}

/** Pour les tests seulement : oublie le catalogue retenu. */
export function oublierPalettes(): void {
  promesse = undefined
}

/**
 * Le fond du plateau pour ces couleurs : un halo ancré au coin BAS DROIT.
 *
 * ⚠ UN HALO D'ANGLE, PAS UNE DIAGONALE TRAVERSANTE. Les deux ont été montrées
 * à l'utilisateur ; il a retenu celle-ci, dans sa version marquée. La couleur
 * monte du coin et se perd avant le centre : elle n'atteint jamais la zone du
 * méchant, en haut à gauche, qui n'appartient pas au héros.
 *
 * Les couleurs suivantes s'échelonnent le long de la diagonale, de moins en
 * moins denses : c'est ce qui fait lire « deux ou trois couleurs » plutôt qu'un
 * aplat.
 */
export function fondDe(couleurs: readonly Couleur[] | undefined, sombre: string): string {
  if (!couleurs || couleurs.length === 0) return sombre
  const rgba = (c: Couleur, a: number) => `rgba(${c[0]},${c[1]},${c[2]},${a})`
  // Ancrage, étendue et force de chaque couche, de la plus dense à la plus
  // diffuse. Trois au plus : au-delà, les teintes se mélangent en boue.
  const COUCHES: Array<{ at: string; force: number }> = [
    { at: '90% 90% at 100% 100%', force: 0.28 },
    { at: '70% 70% at 78% 82%', force: 0.22 },
    { at: '55% 55% at 58% 70%', force: 0.15 },
  ]
  const couches = couleurs.slice(0, COUCHES.length).map((c, i) => {
    const { at, force } = COUCHES[i]
    return `radial-gradient(${at}, ${rgba(c, force)} 0%, ${rgba(c, 0)} 66%)`
  })
  return `${couches.join(', ')}, ${sombre}`
}

/** La forme minimale dont le halo a besoin : qui est assis, et sa carte d'identité. */
export type MondeVuDuHalo = {
  players?: Array<{ area_hero?: Array<{ card_id?: string }> }>
} | null | undefined

/**
 * La carte d'identité du héros AFFICHÉ, celle qui donne la couleur du fond.
 *
 * ⚠ C'EST LE HÉROS REGARDÉ, PAS LE SIÈGE. En multijoueur, `joueurActif` suit la
 * vue (`vueForcee ?? joueurSuivi ?? joueurDemande ?? playerId`) : regarder la
 * table d'un autre héros doit reteindre le fond. Exigence de l'utilisateur,
 * 14/09/2026 : « quand on joue à plusieurs héros, quand on change de héros, la
 * couleur doit changer ».
 *
 * ⚠ ET LES DEUX FACES COMPTENT POUR UNE. Se transformer change le `card_id`
 * (`03001a` <-> `03001b`), or les deux portent la même palette : le fond ne
 * saute pas quand Steve Rogers enfile son costume.
 */
export function identiteAffichee(monde: MondeVuDuHalo, joueurActif: number): string {
  return monde?.players?.[joueurActif]?.area_hero?.[0]?.card_id ?? ''
}

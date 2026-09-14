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
 * Le fond du plateau pour ces couleurs : UNE BANDE DIAGONALE au coin bas droit.
 *
 * ⚠ UNE BANDE, PAS UNE LUEUR D'ANGLE. Une premiere version posait trois halos
 * ronds ancres dans le coin ; l'utilisateur l'a rejetee le 14/09/2026 (« je
 * voulais une marque diagonale avec un leger degrade »). Il a ensuite choisi
 * cette forme-ci parmi quatre montrees sur le vrai plateau : une seule bande
 * large, ou les couleurs se succedent et s'eteignent ensemble.
 *
 * ⚠ ELLE S'ETEINT AVANT LE CENTRE (50 %). La couleur appartient au heros : elle
 * ne doit jamais atteindre la zone du mechant, en haut a gauche.
 *
 * ⚠ LES FORCES ONT ETE MONTEES le 14/09/2026 (0,32 / 0,24 / 0,14 -> 0,46 / 0,34
 * / 0,20) a la demande de l'utilisateur : « pousse un peu la colorisation du
 * halo pour qu'on le voie mieux ». Les aplats colores des zones (rouge sur la
 * ligne de combat, jaune sur les manigances annexes) ont ete retires dans le
 * meme mouvement : ils se superposaient a la bande et brouillaient les deux.
 *
 * `315deg` progresse vers le HAUT GAUCHE : la position 0 % est donc le coin bas
 * droit, celui que l'utilisateur a designe (« en diagonale, la couleur en bas a
 * droite »).
 */
export function fondDe(couleurs: readonly Couleur[] | undefined, sombre: string): string {
  if (!couleurs || couleurs.length === 0) return sombre
  const rgba = (c: Couleur, a: number) => `rgba(${c[0]},${c[1]},${c[2]},${a})`
  // Position et force de chaque couleur le long de la bande, de la plus dense
  // (au coin) a la plus diffuse. Trois arrets : au-dela les teintes se
  // melangent en boue, en deca la bande n'a plus de degrade.
  const ARRETS: Array<{ a: number; force: number }> = [
    { a: 0, force: 0.46 },
    { a: 16, force: 0.34 },
    { a: 30, force: 0.2 },
  ]
  // ⚠ UN HEROS PEUT N'AVOIR QU'UNE OU DEUX COULEURS (onze cadres sont noirs ou
  // gris, deux sets fan-made n'ont qu'un blanc). On repete alors la derniere :
  // la bande garde sa longueur et son degrade, elle porte juste moins de
  // teintes. C'est la forme exacte qui a ete montree et validee.
  const derniere = couleurs[couleurs.length - 1]
  const etapes = ARRETS.map((arret, i) => {
    const couleur = couleurs[i] ?? derniere
    return `${rgba(couleur, arret.force)} ${arret.a}%`
  })
  const fin = couleurs[ARRETS.length - 1] ?? derniere
  return `linear-gradient(315deg, ${etapes.join(', ')}, ${rgba(fin, 0)} 50%), ${sombre}`
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

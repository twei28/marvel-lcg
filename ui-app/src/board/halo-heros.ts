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
 * ⚠ LES FORCES ONT ETE MONTEES QUATRE FOIS, a la demande de l'utilisateur :
 * 14/09/2026 (0,32 / 0,24 / 0,14 -> 0,46 / 0,34 / 0,20, « pousse un peu la
 * colorisation du halo pour qu'on le voie mieux »), 22/09/2026 (-> 0,60 /
 * 0,44 / 0,26, « j'aimerais que les couleurs ressortent un peu plus »), puis
 * 23/09/2026 en DEUX temps : d'abord (-> 0,74 / 0,54 / 0,32, « encore plus
 * flashy »), puis au maximum (-> 1,0 / 0,9 / 0,75, la primaire desormais a
 * PLEINE opacite -- au-dela, la bande cesse d'etre un degrade et devient un
 * aplat). Les aplats colores des zones (rouge sur la ligne de combat, jaune
 * sur les manigances annexes) ont ete retires au premier passage : ils se
 * superposaient a la bande et brouillaient les deux.
 *
 * ⚠ LES POSITIONS AUSSI, UNE FOIS (23/09/2026, « la couleur primaire peut
 * ressortir un peu plus », la primaire etant deja a 1,0 -- impossible de
 * pousser l'opacite plus haut) : 0/16/30 % -> 0/22/38 %. La primaire pure
 * occupe donc une plus grande part de la bande avant que la tertiaire puis
 * la secondaire n'entrent en jeu, plutot que de renforcer le contraste en
 * affaiblissant les deux autres (option ecartee par l'utilisateur, montree
 * a cote de celle-ci).
 *
 * `315deg` progresse vers le HAUT GAUCHE : la position 0 % est donc le coin bas
 * droit, celui que l'utilisateur a designe (« en diagonale, la couleur en bas a
 * droite »).
 *
 * ⚠⚠ L'ORDRE DES TEINTES NE SUIT PLUS L'ORDRE DU FICHIER (23/09/2026,
 * demande de l'utilisateur, capture de l'editeur de palettes a l'appui :
 * « la primaire je la veux a droite, la secondaire a gauche et le tertiaire
 * au milieu »). Voir `ORDRE` ci-dessous.
 */
export function fondDe(
  couleurs: readonly Couleur[] | undefined,
  sombre: string,
  mechant?: readonly Couleur[] | undefined
): string {
  // Le coin HAUT GAUCHE porte les couleurs du méchant (17/10/2026) : même bande diagonale que
  // celle du héros, en sens inverse. Elle s'éteint, elle aussi, avant le centre.
  const coinMechant = mechant && mechant.length > 0 ? `${bandeMechant(mechant)}, ` : ''
  if (!couleurs || couleurs.length === 0) return coinMechant ? `${coinMechant}${sombre}` : sombre
  const rgba = (c: Couleur, a: number) => `rgba(${c[0]},${c[1]},${c[2]},${a})`
  // Position et force de chaque couleur le long de la bande, de la plus dense
  // (au coin) a la plus diffuse. Trois arrets : au-dela les teintes se
  // melangent en boue, en deca la bande n'a plus de degrade.
  const ARRETS: Array<{ a: number; force: number }> = [
    { a: 0, force: 1.0 },
    { a: 22, force: 0.9 },
    { a: 38, force: 0.75 },
  ]
  // La primaire (index 0 du fichier) reste au coin, la plus dense (0 %,
  // « a droite »). La tertiaire (index 2) vient ensuite (22 %, « au
  // milieu »). La secondaire (index 1) tient le dernier arret visible
  // (38 %, le plus diffus -- le plus loin du coin, donc « a gauche »).
  const ORDRE = [0, 2, 1]
  // ⚠ UN HEROS PEUT N'AVOIR QU'UNE OU DEUX COULEURS (onze cadres sont noirs ou
  // gris, deux sets fan-made n'ont qu'un blanc). On repete alors la derniere :
  // la bande garde sa longueur et son degrade, elle porte juste moins de
  // teintes. C'est la forme exacte qui a ete montree et validee.
  const derniere = couleurs[couleurs.length - 1]
  const etapes = ARRETS.map((arret, i) => {
    const couleur = couleurs[ORDRE[i]] ?? derniere
    return `${rgba(couleur, arret.force)} ${arret.a}%`
  })
  const fin = couleurs[ORDRE[ARRETS.length - 1]] ?? derniere
  return `${coinMechant}linear-gradient(315deg, ${etapes.join(', ')}, ${rgba(fin, 0)} 50%), ${sombre}`
}

/**
 * La bande du MÉCHANT, au coin haut gauche : DEUX couleurs (précision de l'utilisateur,
 * 17/10/2026 : « les méchants, c'est deux couleurs »), la principale au coin, la secondaire
 * ensuite, puis le fondu. `135deg` progresse vers le BAS DROIT : la position 0 % est le coin
 * haut gauche. Mêmes forces que la bande du héros (pleine, puis 0,9), éteinte avant le centre.
 */
export function bandeMechant(couleurs: readonly Couleur[]): string {
  const rgba = (c: Couleur, a: number) => `rgba(${c[0]},${c[1]},${c[2]},${a})`
  const [principale, secondaire] = [couleurs[0], couleurs[1] ?? couleurs[0]]
  return `linear-gradient(135deg, ${rgba(principale, 1)} 0%, ${rgba(secondaire, 0.9)} 26%, ${rgba(secondaire, 0)} 50%)`
}

/**
 * La marque du héros en affichage ÉPURÉ : trois BANDES EN BIAIS, aplaties, au
 * coin bas droit (demande de l'utilisateur, 15/10/2026 : « trois couleurs
 * aplaties, pas en halo », forme choisie : trois bandes en biais).
 *
 * Même ordre que `fondDe` (primaire au coin, tertiaire au milieu, secondaire
 * au bord) et même règle des héros à une ou deux couleurs : on répète la
 * dernière. Arrêts NETS (deux positions par couleur), aucun dégradé ni flou. La bande du
 * milieu est trois fois plus fine que les deux autres. Largeur doublee le
 * 15/10/2026 (44 -> 96 px) : « qu'elles prennent plus de place ».
 * Rend une valeur de `background`, posée sur un pseudo-élément du coin.
 */
export function marqueDe(couleurs: readonly Couleur[] | undefined, largeurBande = 96): string | undefined {
  if (!couleurs || couleurs.length === 0) return undefined
  const rgb = (c: Couleur) => `rgb(${c[0]},${c[1]},${c[2]})`
  const derniere = couleurs[couleurs.length - 1]
  const bandes = [0, 2, 1].map((i) => couleurs[i] ?? derniere)
  // PROPORTIONS 70 / 5 / 25 du coin vers le bord (demande du 16/10/2026, apres un
  // premier essai a l'envers en 25 / 5 / 70 ; avant : la bande du milieu faisait un
  // tiers des deux autres). La longueur totale reste celle d'avant (7/3 de
  // `largeurBande`, soit 224 px par defaut).
  const total = (largeurBande * 7) / 3
  const largeurs = [0.7, 0.05, 0.25].map((part) => Math.round(total * part * 100) / 100)
  let debut = 0
  const arrets = bandes.map((c, i) => {
    const fin = Math.round((debut + largeurs[i]) * 100) / 100
    const arret = `${rgb(c)} ${debut}px ${fin}px`
    debut = fin
    return arret
  })
  return `linear-gradient(315deg, ${arrets.join(', ')}, transparent ${debut}px)`
}

/**
 * La marque du MÉCHANT en affichage ÉPURÉ : DEUX bandes en biais, aplaties, au coin HAUT GAUCHE
 * (17/10/2026), le pendant de `marqueDe`. PROPORTIONS 40 / 60 (demande du 17/10/2026) : la
 * principale tient le coin (40 %), la secondaire le bord (60 %). Arrêts nets, aucun dégradé.
 */
export function marqueMechantDe(couleurs: readonly Couleur[] | undefined, largeurBande = 96): string | undefined {
  if (!couleurs || couleurs.length === 0) return undefined
  const rgb = (c: Couleur) => `rgb(${c[0]},${c[1]},${c[2]})`
  const [principale, secondaire] = [couleurs[0], couleurs[1] ?? couleurs[0]]
  const total = (largeurBande * 7) / 3
  const premiere = Math.round(total * 0.4 * 100) / 100
  const seconde = Math.round(total * 100) / 100
  return `linear-gradient(135deg, ${rgb(principale)} 0px ${premiere}px, ${rgb(secondaire)} ${premiere}px ${seconde}px, transparent ${seconde}px)`
}

/** La forme minimale dont le halo a besoin : qui est assis, et sa carte d'identité. */
export type MondeVuDuHalo = {
  players?: Array<{ area_hero?: Array<{ card_id?: string }> }>
  area_villain?: Array<{ card_id?: string }>
} | null | undefined

/**
 * La carte du MÉCHANT en jeu, celle qui donne la couleur du coin haut gauche. La première carte
 * de la zone du méchant qui a une palette ; `a-t-elle-une-palette` est décidé par l'appelant.
 */
export function identitesMechants(monde: MondeVuDuHalo): string[] {
  return (monde?.area_villain ?? []).map((carte) => carte?.card_id ?? '').filter(Boolean)
}

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

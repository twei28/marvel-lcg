// Le TRAIT qui relie qui frappe qui, et ce qu'il porte.
//
// Demande de l'utilisateur, 14/09/2026 : « j'aime bien les traits qui montrent
// qui va être attaqué », puis, en précisant : « montrer sur le trait qui mène
// d'un endroit à l'autre, si c'est les dégâts le nombre de dégâts, si c'est la
// manigance le nombre de manigances, si c'est le nombre de contre le nombre de
// contre, etc. ».
//
// Deux choses séparées dans ce fichier, et aucune ne touche au DOM :
//   1. CE QUE LE TRAIT DIT  : le nombre, son unité, et le ton qui le colore ;
//   2. OÙ LE TRAIT PASSE    : la géométrie, des bords des deux cartes.
//
// ⚠ LE MONTANT VIENT DE L'ÉTAPE, JAMAIS D'UN CALCUL D'ICI. `FaitMechant` porte
// `subi` en clair, et `etapesDeroule` le pose dans `montant` : c'est ce que la
// cible a RÉELLEMENT encaissé, une fois la défense déduite. Recalculer quoi que
// ce soit ici ferait dire au trait autre chose qu'au cartouche.

import { t } from './langue'
import type { EtapeDeroule } from './deroule-phase'

/** De quoi le trait parle : ce qui décide de sa couleur. */
export type TonTrait = 'degats' | 'menaces' | 'statut' | 'neutre'

export type ContenuTrait = {
  /** Le nombre, quand l'étape en porte un. */
  montant?: number
  /**
   * L'unité, DÉJÀ ACCORDÉE au nombre, en clé de traduction (`t`) : « dégât »
   * ou « dégâts ». Le pluriel se décide ici et pas à l'affichage, parce que
   * c'est ici qu'on sait de quoi on parle.
   */
  unite: string
  ton: TonTrait
}

/**
 * ⚠ UNE SEULE TABLE, FAITE POUR ÊTRE ÉTENDUE. Chaque temps de la phase compte
 * dans sa propre unité, et l'utilisateur a demandé qu'on les distingue. Un
 * titre inconnu tombe sur `neutre` sans unité : mieux vaut un trait qui montre
 * seulement la direction qu'un trait qui annonce une mauvaise unité.
 *
 * `contre` n'est pas produit par la phase du méchant (contrer est une action de
 * héros) mais figure ici parce que l'utilisateur l'a nommé et qu'un effet de
 * carte rencontre peut retirer de la menace : le jour où un fait en émettra, le
 * trait le dira sans qu'on ait à y revenir.
 */
const UNITES: Record<string, { un: string; plusieurs: string; ton: TonTrait }> = {
  attaque: { un: 'dégât', plusieurs: 'dégâts', ton: 'degats' },
  manigance: { un: 'menace', plusieurs: 'menaces', ton: 'menaces' },
  menace: { un: 'menace', plusieurs: 'menaces', ton: 'menaces' },
  contre: { un: 'contre', plusieurs: 'contres', ton: 'menaces' },
  distribution: { un: 'carte', plusieurs: 'cartes', ton: 'neutre' },
}

/** Ce que le trait de cette étape doit dire. */
export function contenuDuTrait(etape: EtapeDeroule): ContenuTrait {
  // Un STATUT n'a pas de nombre : il a un nom. « Étourdi » sur le trait dit
  // tout, « 1 » ne dirait rien.
  if (etape.statut) return { unite: etape.statut, ton: 'statut' }

  const table = UNITES[etape.titre]
  // ⚠ SUR UNE ANNONCE, LE MONTANT PREVU. Le coup n'a pas eu lieu : l'etape ne
  // porte aucun `montant`, seulement `valeurAnnoncee` (l'attaque imprimee).
  // Choix de l'utilisateur parmi trois (14/09/2026) : « des l'annonce, avec le
  // montant prevu », en sachant que ce nombre CHANGERA apres les boosts et sa
  // defense. C'est le prix a payer pour decider si l'on defend.
  const montant = etape.montant ?? etape.valeurAnnoncee
  if (!table) return { montant, unite: '', ton: 'neutre' }
  // ⚠ `Math.abs` : un retrait de menace est un nombre négatif dans le fait ;
  // l'unité s'accorde sur la quantité, pas sur le sens.
  const unite = Math.abs(montant ?? 0) === 1 ? table.un : table.plusieurs
  return { montant, unite, ton: table.ton }
}

/** Un rectangle à l'écran, dans le repère du cadre du plateau. */
export type Boite = { x: number; y: number; w: number; h: number }

export type Trait = {
  x1: number
  y1: number
  x2: number
  y2: number
  /** Où poser l'étiquette : au milieu de la COURBE (t = 0,5), pas de la corde. */
  mx: number
  my: number
  /** Point de contrôle de l'arc quadratique (19/10/2026) : la corde, décalée de sa perpendiculaire. */
  cx: number
  cy: number
}

/** Le creux de l'arc, en part de la longueur de la corde (19/10/2026 : « style 2 en version courbée », ~20 %). */
export const COURBURE_TRAIT = 0.2

/**
 * Le point de contrôle d'un arc de `(x1,y1)` à `(x2,y2)` : au milieu de la corde, décalé
 * perpendiculairement de `COURBURE_TRAIT` x longueur, TOUJOURS DU MÊME CÔTÉ (vers le haut quand la flèche
 * est horizontale, vers la droite quand elle est verticale), quel que soit le sens du coup.
 */
export function pointDeControle(x1: number, y1: number, x2: number, y2: number): { x: number; y: number } {
  const dx = x2 - x1
  const dy = y2 - y1
  const longueur = Math.hypot(dx, dy)
  if (longueur === 0) return { x: x1, y: y1 }
  let nx = dy / longueur
  let ny = -dx / longueur
  if (ny > 1e-9 || (Math.abs(ny) <= 1e-9 && nx < 0)) {
    nx = -nx
    ny = -ny
  }
  return { x: (x1 + x2) / 2 + nx * longueur * COURBURE_TRAIT, y: (y1 + y2) / 2 + ny * longueur * COURBURE_TRAIT }
}

/**
 * Le segment qui va d'une carte à l'autre, DE BORD À BORD.
 *
 * ⚠ IL NE PART PAS DES CENTRES. Un trait tiré de centre à centre passe sous
 * les deux cartes : on n'en voit que la portion du milieu, et il a l'air de
 * sortir de nulle part. On tire donc du centre au centre, puis on coupe à
 * l'endroit où le segment franchit chaque rectangle.
 *
 * Rend `undefined` quand les deux cartes se confondent : il n'y a alors aucune
 * direction à montrer, et un trait de longueur nulle afficherait une étiquette
 * posée sur rien.
 */
export function traitEntre(auteur: Boite, cible: Boite): Trait | undefined {
  const a = { x: auteur.x + auteur.w / 2, y: auteur.y + auteur.h / 2 }
  const b = { x: cible.x + cible.w / 2, y: cible.y + cible.h / 2 }
  const dx = b.x - a.x
  const dy = b.y - a.y
  if (dx === 0 && dy === 0) return undefined
  const depart = surLeBord(auteur, a, dx, dy)
  const arrivee = surLeBord(cible, b, -dx, -dy)
  const c = pointDeControle(depart.x, depart.y, arrivee.x, arrivee.y)
  return {
    x1: depart.x,
    y1: depart.y,
    x2: arrivee.x,
    y2: arrivee.y,
    // Milieu de la courbe quadratique : 1/4 départ + 1/2 contrôle + 1/4 arrivée.
    mx: depart.x / 4 + c.x / 2 + arrivee.x / 4,
    my: depart.y / 4 + c.y / 2 + arrivee.y / 4,
    cx: c.x,
    cy: c.y,
  }
}

/**
 * Le point où le rayon parti du centre de `boite` dans la direction (dx, dy)
 * franchit son bord.
 *
 * On cherche le plus petit facteur `t` tel que le point sorte du rectangle : la
 * moitié de la largeur divisée par |dx|, la moitié de la hauteur par |dy|, et
 * on garde le plus petit. Une composante nulle ne borne rien (le rayon est
 * parallèle à ce côté), d'où l'infini.
 */
function surLeBord(
  boite: Boite,
  centre: { x: number; y: number },
  dx: number,
  dy: number
): { x: number; y: number } {
  const tx = dx === 0 ? Number.POSITIVE_INFINITY : boite.w / 2 / Math.abs(dx)
  const ty = dy === 0 ? Number.POSITIVE_INFINITY : boite.h / 2 / Math.abs(dy)
  const t = Math.min(tx, ty)
  return { x: centre.x + dx * t, y: centre.y + dy * t }
}

/**
 * CE QUE LA CARTE TOUCHEE MONTRE (v3, 10/10/2026, Q7) : le nombre qui s'envole
 * (« -3 », « +2 ») et, quand le seuil est connu, l'ancien niveau de sa jauge en
 * fantome (fraction de 0 a 1). Seulement sur une etape RESOLUE qui a touche une
 * carte : une annonce n'a encore rien fait.
 */
export type DeltaTable = { texte: string; ton: 'degats' | 'menace'; avant?: number }

const borne = (x: number) => Math.min(1, Math.max(0, x))

export function deltaSurTable(etape: EtapeDeroule, pvMax?: number): DeltaTable | undefined {
  if (etape.etat !== undefined && etape.etat !== 'resolu') return undefined
  const montant = etape.montant
  if (montant === undefined || etape.cibleId === undefined) return undefined
  const restant = etape.restant
  // 19/10/2026 : « −X PV » sur la carte touchee, a la place du jeton de degats qui volait.
  // Une attaque qui passe a 0 degat l'affiche aussi (« −0 PV ») ; la Riposte aussi.
  if (etape.titre === 'attaque' || etape.titre === 'riposte') {
    const avant = pvMax && restant !== undefined ? borne((restant + montant) / pvMax) : undefined
    return { texte: `−${montant} ${t('PV')}`, ton: 'degats', avant }
  }
  if (montant === 0) return undefined
  if (etape.titre === 'manigance' || etape.titre === 'menace') {
    const plafond = etape.plafond
    const depart = etape.menaceAvant ?? (restant !== undefined ? restant - montant : undefined)
    const avant = plafond && depart !== undefined ? borne(depart / plafond) : undefined
    return { texte: montant > 0 ? `+${montant}` : `−${Math.abs(montant)}`, ton: 'menace', avant }
  }
  return undefined
}

/**
 * Le texte posé sur le trait (« 3 dégâts », « 2 menaces »), ou rien. Vide quand le jeton ou le bandeau
 * porte déjà le nombre (`sansEtiquette`), et pour un coup à 0 (19/10/2026 : « 0 dégâts » posé sur la
 * flèche, alors que le bandeau et le « −0 PV » de la carte le disent déjà ; une annonce à 0 non plus).
 */
export function etiquetteDuTrait(contenu: { montant?: number; unite?: string }, sansEtiquette = false): string {
  if (sansEtiquette || contenu.montant === 0) return ''
  if (contenu.montant !== undefined) return `${contenu.montant}${contenu.unite ? ' ' + t(contenu.unite) : ''}`
  return contenu.unite ? t(contenu.unite) : ''
}

/**
 * « −X PV » DES EFFETS D'UNE CARTE REVELEE (19/10/2026) : une trahison qui blesse un heros ou un allie,
 * parfois plusieurs cibles a la fois. Une ligne par carte blessee (deux effets sur la meme carte
 * s'additionnent), meme texte que l'attaque. Rien pour une attaque ou une riposte : leur « −X PV » est
 * celui de `deltaSurTable` (pas de doublon), et une carte deja nommee par `cibleId` ne l'est pas deux fois.
 */
export type DeltaEffet = { cibleId: number; texte: string; ton: 'degats' }

export function deltasDesEffets(etape: EtapeDeroule): DeltaEffet[] {
  if (etape.etat !== undefined && etape.etat !== 'resolu') return []
  if (etape.titre === 'attaque' || etape.titre === 'riposte') return []
  if (!(etape.temps === 'revelation' || etape.titre === 'entree' || etape.titre === 'stade-revele')) return []
  const parCarte = new Map<number, number>()
  for (const effet of etape.effets ?? []) {
    if (effet.genre !== 'degats' || effet.montant <= 0) continue
    parCarte.set(effet.cible_id, (parCarte.get(effet.cible_id) ?? 0) + effet.montant)
  }
  const dejaMontre = deltaSurTable(etape) ? etape.cibleId : undefined
  return [...parCarte]
    .filter(([id]) => id !== dejaMontre)
    .map(([cibleId, montant]) => ({ cibleId, texte: `−${montant} ${t('PV')}`, ton: 'degats' as const }))
}

/**
 * L'ALERTE DE MENACE (v3, Q16) : une manigance a 80 % de son seuil ou plus
 * apres l'etape. Rend le restant et le seuil, l'appelant redige la phrase.
 */
export function alerteMenace(etape: EtapeDeroule): { restant: number; plafond: number } | undefined {
  if (etape.titre !== 'manigance' && etape.titre !== 'menace') return undefined
  if (etape.etat !== undefined && etape.etat !== 'resolu') return undefined
  const { restant, plafond } = etape
  if (restant === undefined || !plafond) return undefined
  return restant / plafond >= 0.8 ? { restant, plafond } : undefined
}

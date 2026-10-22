// La carte qu'une option DESIGNE PAR SON NOM.
//
// Le moteur a deux facons de faire choisir : par CIBLES (le joueur clique une
// carte de la table) et par TEXTE (`AskChooseOneText`, dans player_ask.py, qui
// ne transporte que des noms). La seconde sert des que les cartes ne sont pas
// sur la table — fouiller son deck, nommer une carte de sa defausse — et elle
// laissait le joueur choisir a l'aveugle : Alison Blaire propose deux chansons
// dont il n'a jamais lu le texte.
//
// Ce module rattache un de ces noms a la carte du descripteur, qui, lui,
// contient le deck en entier. Le plateau n'a plus qu'a en dessiner le scan.

import { toScanCard } from './card-model'
import type { Catalogue } from './catalogue'
import type { Option } from './ask'
import type { ScanCardProps } from '../components/ScanCard'
import type { WorldCard } from './world'

/**
 * Cle de rapprochement entre le NOM d'une option et le nom d'une carte.
 *
 * Le moteur ecrit les deux, mais pas au meme endroit : le nom de l'option vient
 * de `AskChooseOneText`, qui recopie `CardFace.name` tel quel (guillemets
 * compris : la carte s'appelle bel et bien « "Beautiful Dreamer" »). On
 * normalise malgre tout casse, guillemets et espaces, parce qu'un choix ecrit a
 * la main dans une carte fan-made n'a aucune raison de respecter la ponctuation
 * du scan au caractere pres.
 */
export function cleNomCarte(nom: string): string {
  return nom
    .replace(/[«»"“”'’]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase()
}

/**
 * Index nom -> carte, sur TOUT le descripteur (deck et defausse compris).
 *
 * C'est ce qui permet de montrer la carte derriere un choix purement textuel :
 * le moteur, quand il fait choisir « une chanson parmi celles-ci », n'envoie
 * que des noms (voir carteNommeeParOption).
 */
export function indexerCartesMondeParNom(cartesParId: Map<number, WorldCard>): Map<string, WorldCard> {
  const index = new Map<string, WorldCard>()
  for (const carte of cartesParId.values()) {
    const cle = cleNomCarte(carte.name ?? '')
    // La premiere gagne : les exemplaires d'une meme carte portent le meme
    // scan, seul l'identifiant d'objet les distingue.
    if (cle && !index.has(cle)) index.set(cle, carte)
  }
  return index
}

/**
 * La carte qu'une option DESIGNE PAR SON NOM, ou rien.
 *
 * `AskChooseOneText` (moteur, player_ask.py) ne sait proposer que du TEXTE :
 * quand Alison Blaire fouille son deck pour y prendre une chanson, le joueur
 * voit deux boutons « "Beauty and the Beast" » / « "Beautiful Dreamer" » et
 * doit deviner ce que font des cartes qu'il n'a jamais eues en main. Le
 * descripteur, lui, contient ces cartes (le deck y figure en entier) : il
 * suffit de les retrouver par leur nom pour montrer le scan.
 *
 * La carte est forcee VISIBLE : le moteur vient precisement de nous demander de
 * choisir entre elles, donc il nous les montre deja — en clair, mais en texte.
 * Rien n'est revele que la question ne revele.
 *
 * Deux gardes :
 *  - un nom trop court ne designe pas une carte (« R », « 2 » : types de
 *    ressource et nombres passent par le meme AskChooseOneText) ;
 *  - la carte PORTEUSE de l'option est exclue : elle est deja sur la table, et
 *    son nom est deja sous le bouton (voir nomSource dans DemandeCentrale).
 */
export function carteNommeeParOption(
  option: Option,
  cartesParNom: Map<string, WorldCard>,
  playerId: number,
  catalogue: Catalogue
): ScanCardProps | undefined {
  const cle = cleNomCarte(option.name)
  if (cle.length < 3) return undefined
  const carte = cartesParNom.get(cle)
  if (!carte || carte.id === option.bind_id) return undefined
  return toScanCard(
    { ...carte, visible_for_players: [playerId], is_face_up: true },
    { playerId, actives: new Set(), catalogue }
  )
}

/**
 * Les cartes que le moteur NE POSE PAS encore quand il fait choisir un lot.
 *
 * Mutant Genesis (campagne) : au scenario 1, chaque joueur choisit un ROLE —
 * un lot de cinq ameliorations dont UNE sera tiree au hasard. Le moteur propose
 * « Role: Brawler » (mut_gen/campaign.py, `ROLE_SETS`) sans aucune carte
 * derriere : le survol montrait la manigance qui porte la question, ce qui ne
 * dit rien du role (signale le 22/10/2026). Ces cartes ne sont dans aucune
 * zone du monde, on les construit donc depuis leur identifiant, et on les
 * montre TOUTES : tirer au hasard ne doit pas cacher ce qu'on choisit.
 *
 * ⚠ Copie de `ROLE_SETS` du moteur : a tenir ensemble.
 */
export const LOTS_DE_ROLE: Readonly<Record<string, readonly string[]>> = {
  Brawler: ['32176', '32177', '32178', '32179', '32180'],
  Commander: ['32181', '32182', '32183', '32184', '32185'],
  Defender: ['32186', '32187', '32188', '32189', '32190'],
  Peacekeeper: ['32191', '32192', '32193', '32194', '32195'],
}

/** Les cartes du lot que l'option designe (« Role: Brawler »), ou rien. */
export function cartesDuLotParOption(
  option: Option,
  playerId: number,
  catalogue: Catalogue
): ScanCardProps[] | undefined {
  const role = /^Role:\s*(.+)$/.exec(option.name.trim())?.[1]?.trim()
  const lot = role ? LOTS_DE_ROLE[role] : undefined
  if (!lot) return undefined
  return lot.map((cardId) =>
    toScanCard(
      {
        // Identifiant negatif : aucune carte du monde n'en porte.
        id: -Number(cardId),
        is_ready: true,
        is_face_up: true,
        visible_for_players: [playerId],
        bind_object_id: 0,
        name: cardId,
        info: {},
        traits: {},
        buffs: {},
        card_id: cardId,
        pic_id: cardId,
        down_card_ids: [],
        card_type: catalogue.type(cardId) ?? 'Upgrade',
        cost: 0,
        resources: [],
      },
      { playerId, actives: new Set(), catalogue }
    )
  )
}
